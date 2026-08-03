#!/usr/bin/env python3
"""Erzeugt ein begrenztes, reproduzierbares Review-Paket."""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import fnmatch
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Optional
from urllib.parse import urlsplit

from review_package import file_hash, package_hash


UNSAFE_SUFFIXES = {".pem", ".key", ".p12", ".pfx"}
UNSAFE_NAMES = {".env", "id_rsa", "id_ed25519"}
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|secret)\b\s*[:=]\s*['\"]?[A-Za-z0-9_./+-]{16,}"
    ),
]
EVIDENCE_FIELDS = {
    "id",
    "repositoryUrl",
    "commit",
    "path",
    "lineStart",
    "lineEnd",
    "description",
    "verificationMethod",
}
EVIDENCE_ID = re.compile(r"^EV-[0-9]{3,}$")
COMMIT_ID = re.compile(r"^[0-9a-fA-F]{7,40}$")


def find_repository(start: Optional[Path] = None) -> Path:
    candidates = [start or Path.cwd(), Path(__file__).resolve().parent]
    for candidate in candidates:
        for path in (candidate.resolve(), *candidate.resolve().parents):
            if (path / ".git").exists() and (path / ".ai" / "config.json").is_file():
                return path
    raise RuntimeError("Repository-Wurzel mit .git und .ai/config.json wurde nicht gefunden.")


def git(repo: Path, arguments: list[str], binary: bool = False) -> Any:
    result = subprocess.run(
        ["git", *arguments],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=not binary,
        encoding=None if binary else "utf-8",
        errors=None if binary else "replace",
        shell=False,
        check=False,
    )
    if result.returncode != 0:
        stderr = (
            result.stderr.decode("utf-8", "replace") if binary else result.stderr
        ).strip()
        raise RuntimeError(f"Git-Befehl fehlgeschlagen: {stderr}")
    return result.stdout


def load_config(repo: Path) -> dict[str, Any]:
    try:
        config = json.loads((repo / ".ai" / "config.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f".ai/config.json kann nicht gelesen werden: {exc}") from exc
    if not isinstance(config, dict):
        raise RuntimeError(".ai/config.json muss ein JSON-Objekt enthalten.")
    return config


def repository_relative(repo: Path, value: Path, description: str) -> tuple[Path, str]:
    candidate = value if value.is_absolute() else repo / value
    resolved = candidate.resolve()
    try:
        relative = resolved.relative_to(repo.resolve()).as_posix()
    except ValueError as exc:
        raise RuntimeError(f"{description} liegt außerhalb des Repositorys: {value}") from exc
    if not relative or relative == ".":
        raise RuntimeError(f"{description} darf nicht die Repository-Wurzel sein.")
    return resolved, relative


def ensure_safe_path(relative: str, description: str) -> None:
    parts = PurePosixPath(relative).parts
    lowered = [part.lower() for part in parts]
    name = lowered[-1]
    if ".git" in lowered or name in UNSAFE_NAMES or name.startswith(".env"):
        raise RuntimeError(f"{description} ist aus Sicherheitsgründen ausgeschlossen: {relative}")
    if PurePosixPath(name).suffix in UNSAFE_SUFFIXES:
        raise RuntimeError(f"{description} hat einen ausgeschlossenen Schlüsseltyp: {relative}")


def split_zero_terminated(raw: bytes) -> list[str]:
    return [part.decode("utf-8", "surrogateescape") for part in raw.split(b"\0") if part]


def matches(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def untracked_patch(path: Path, relative: str) -> str:
    data = path.read_bytes()
    if b"\0" in data:
        raise RuntimeError(f"Unversionierte Binärdatei kann nicht sicher gepackt werden: {relative}")
    text = data.decode("utf-8", "replace").splitlines(keepends=True)
    if text and not text[-1].endswith(("\n", "\r")):
        text[-1] += "\n"
    return "".join(
        difflib.unified_diff(
            [],
            text,
            fromfile="/dev/null",
            tofile=f"b/{relative}",
            n=80,
        )
    )


def slug(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9_-]+", "-", value).strip("-").lower()
    return normalized or "review"


def reject_probable_secrets(text: str, description: str) -> None:
    if any(pattern.search(text) for pattern in SECRET_PATTERNS):
        raise RuntimeError(
            f"{description} enthält ein mögliches Zugangsdaten- oder Schlüssel-Muster. "
            "Das Review-Paket wurde nicht erzeugt; Inhalt manuell prüfen."
        )


def validate_evidence_manifest(value: Any, source: Path) -> list[dict[str, Any]]:
    if not isinstance(value, dict):
        raise RuntimeError(f"Externes Evidenzmanifest {source.name} muss ein JSON-Objekt sein.")
    expected = {"schemaVersion", "language", "evidence"}
    if set(value) != expected:
        raise RuntimeError(
            f"Externes Evidenzmanifest {source.name} hat fehlende oder unerwartete Top-Level-Felder."
        )
    if value.get("schemaVersion") != "1.0" or value.get("language") != "de":
        raise RuntimeError(
            f"Externes Evidenzmanifest {source.name} benötigt schemaVersion '1.0' und language 'de'."
        )
    items = value.get("evidence")
    if not isinstance(items, list) or not items:
        raise RuntimeError(f"Externes Evidenzmanifest {source.name} benötigt mindestens einen Eintrag.")
    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(items):
        location = f"{source.name}.evidence[{index}]"
        if not isinstance(item, dict) or set(item) != EVIDENCE_FIELDS:
            raise RuntimeError(f"{location} hat fehlende oder unerwartete Felder.")
        evidence_id = item.get("id")
        if not isinstance(evidence_id, str) or not EVIDENCE_ID.fullmatch(evidence_id):
            raise RuntimeError(f"{location}.id muss dem Format EV-001 entsprechen.")
        repository_url = item.get("repositoryUrl")
        if not isinstance(repository_url, str) or any(char in repository_url for char in "<>"):
            raise RuntimeError(f"{location}.repositoryUrl muss eine HTTPS-URL sein.")
        parsed = urlsplit(repository_url)
        if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
            raise RuntimeError(
                f"{location}.repositoryUrl muss eine HTTPS-URL ohne eingebettete Zugangsdaten sein."
            )
        commit = item.get("commit")
        if (
            not isinstance(commit, str)
            or not COMMIT_ID.fullmatch(commit)
            or set(commit) == {"0"}
        ):
            raise RuntimeError(f"{location}.commit muss eine Git-Commit-ID enthalten.")
        path = item.get("path")
        if not isinstance(path, str) or not path or any(char in path for char in "<>"):
            raise RuntimeError(f"{location}.path muss ein repository-relativer Pfad sein.")
        ensure_safe_path(path, f"{location}.path")
        if "\\" in path or path.startswith("/") or any(
            part in {"", ".", ".."} for part in PurePosixPath(path).parts
        ):
            raise RuntimeError(f"{location}.path ist kein sicherer repository-relativer Pfad.")
        start = item.get("lineStart")
        end = item.get("lineEnd")
        if (start is None) != (end is None):
            raise RuntimeError(f"{location}: lineStart und lineEnd müssen gemeinsam gesetzt werden.")
        if start is not None and (
            type(start) is not int or type(end) is not int or start < 1 or end < start
        ):
            raise RuntimeError(f"{location}: ungültiger Zeilenbereich.")
        for field in ("description", "verificationMethod"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise RuntimeError(f"{location}.{field} muss eine nicht leere deutsche Beschreibung sein.")
        normalized.append(dict(item))
    return normalized


def load_external_evidence(paths: list[Path]) -> list[dict[str, Any]]:
    combined: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for path in paths:
        resolved = path.resolve()
        if not resolved.is_file():
            raise RuntimeError(f"Externes Evidenzmanifest fehlt: {path}")
        try:
            text = resolved.read_text(encoding="utf-8")
            reject_probable_secrets(text, f"Externes Evidenzmanifest {resolved.name}")
            value = json.loads(text)
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Externes Evidenzmanifest {resolved.name} ist ungültig: {exc}") from exc
        for item in validate_evidence_manifest(value, resolved):
            if item["id"] in seen_ids:
                raise RuntimeError(f"Doppelte externe Evidenz-ID: {item['id']}")
            seen_ids.add(item["id"])
            combined.append(item)
    return combined


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Erzeugt ein task-spezifisches Review-Paket.")
    parser.add_argument("--task", required=True, type=Path, help="Konkrete Aufgabendatei")
    parser.add_argument("--base", help="Git-Basisreferenz; Standard aus .ai/config.json")
    parser.add_argument("--claim-inventory", type=Path, help="Optionales Claim-Inventar")
    parser.add_argument(
        "--external-evidence",
        action="append",
        default=[],
        type=Path,
        help=(
            "Strukturiertes Evidenzmanifest für ein externes Repository; wiederholbar. "
            "Es werden nur validierte Metadaten, keine externen Dateien aufgenommen."
        ),
    )
    parser.add_argument(
        "--include",
        action="append",
        default=[],
        type=Path,
        help="Explizit aufgabenrelevanter repository-relativer Pfad; wiederholbar",
    )
    parser.add_argument(
        "--include-implementation",
        action="store_true",
        help="Konfigurierte Implementierungspfade in den Diff aufnehmen",
    )
    args = parser.parse_args(argv)

    try:
        repo = find_repository()
        if shutil.which("git") is None:
            raise RuntimeError("Git ist nicht verfügbar.")
        config = load_config(repo)
        review = config.get("review")
        if not isinstance(review, dict):
            raise RuntimeError("review in .ai/config.json muss ein Objekt sein.")
        base = args.base or config.get("defaultBaseRef")
        if not isinstance(base, str) or not base.strip():
            raise RuntimeError("Keine Git-Basisreferenz konfiguriert oder angegeben.")
        try:
            base_commit = git(repo, ["rev-parse", "--verify", f"{base}^{{commit}}"] ).strip()
        except RuntimeError as exc:
            raise RuntimeError(f"Unbekannte Git-Basisreferenz '{base}': {exc}") from exc
        current_commit = git(repo, ["rev-parse", "HEAD"]).strip()

        task_path, task_relative = repository_relative(repo, args.task, "Aufgabendatei")
        ensure_safe_path(task_relative, "Aufgabendatei")
        if not task_path.is_file():
            raise RuntimeError(f"Aufgabendatei fehlt: {task_relative}")
        task_text = task_path.read_text(encoding="utf-8")
        reject_probable_secrets(task_text, "Aufgabendatei")

        schema_value = review.get("schema")
        prompt_value = review.get("prompt")
        if not isinstance(schema_value, str) or not isinstance(prompt_value, str):
            raise RuntimeError("review.schema und review.prompt müssen Pfade sein.")
        schema_path, schema_relative = repository_relative(
            repo, Path(schema_value), "Review-Schema"
        )
        prompt_path, prompt_relative = repository_relative(
            repo, Path(prompt_value), "Review-Prompt"
        )
        if not schema_path.is_file() or not prompt_path.is_file():
            raise RuntimeError("Konfiguriertes Review-Schema oder Review-Prompt fehlt.")

        explicit_paths: list[str] = []
        for include in args.include:
            include_path, include_relative = repository_relative(repo, include, "Expliziter Pfad")
            ensure_safe_path(include_relative, "Expliziter Pfad")
            if not include_path.exists():
                raise RuntimeError(f"Explizit angegebener Pfad fehlt: {include_relative}")
            if not include_path.is_file():
                raise RuntimeError(f"Explizite Includes müssen Dateien sein: {include_relative}")
            explicit_paths.append(include_relative)

        thesis_patterns = review.get("thesisPathPatterns", [])
        implementation_patterns = review.get("implementationPathPatterns", [])
        if not isinstance(thesis_patterns, list) or not all(
            isinstance(item, str) for item in thesis_patterns
        ):
            raise RuntimeError("review.thesisPathPatterns muss ein String-Array sein.")
        if not isinstance(implementation_patterns, list) or not all(
            isinstance(item, str) for item in implementation_patterns
        ):
            raise RuntimeError("review.implementationPathPatterns muss ein String-Array sein.")
        active_patterns = list(thesis_patterns)
        if args.include_implementation:
            active_patterns.extend(implementation_patterns)

        changed_all = split_zero_terminated(
            git(repo, ["diff", "--name-only", "-z", base, "--"], binary=True)
        )
        untracked_all = split_zero_terminated(
            git(repo, ["ls-files", "--others", "--exclude-standard", "-z"], binary=True)
        )
        explicit = set(explicit_paths)
        selected_tracked = sorted(
            path for path in changed_all if matches(path, active_patterns) or path in explicit
        )
        # Unversionierte Dateien werden nie allein aufgrund ihrer Endung aufgenommen:
        # Sie könnten unabhängig von der Aufgabe sein und müssen explizit benannt werden.
        selected_untracked = sorted(path for path in untracked_all if path in explicit)
        selected = sorted(set(selected_tracked + selected_untracked))
        for path in selected:
            ensure_safe_path(path, "Review-Datei")
        if not selected:
            raise RuntimeError(
                "Keine thesis-relevanten Änderungen gegen die Basis gefunden. "
                "Für codebasierte Aussagen --include-implementation oder --include <pfad> verwenden."
            )

        diff_parts: list[str] = []
        if selected_tracked:
            diff_parts.append(
                git(
                    repo,
                    ["diff", "--no-ext-diff", "--unified=80", base, "--", *selected_tracked],
                )
            )
        for relative in selected_untracked:
            diff_parts.append(untracked_patch(repo / relative, relative))
        combined_diff = "\n".join(part.rstrip("\n") for part in diff_parts if part) + "\n"
        if not combined_diff.strip():
            raise RuntimeError("Der ausgewählte Diff ist leer.")
        reject_probable_secrets(combined_diff, "Review-Diff")

        claim_source: Optional[tuple[Path, str]] = None
        if args.claim_inventory:
            claim_path, claim_relative = repository_relative(
                repo, args.claim_inventory, "Claim-Inventar"
            )
            ensure_safe_path(claim_relative, "Claim-Inventar")
            if not claim_path.is_file():
                raise RuntimeError(f"Claim-Inventar fehlt: {claim_relative}")
            reject_probable_secrets(
                claim_path.read_text(encoding="utf-8"), "Claim-Inventar"
            )
            claim_source = (claim_path, claim_relative)

        external_evidence = load_external_evidence(args.external_evidence)

        output_relative = review.get("outputDirectory")
        if not isinstance(output_relative, str) or not output_relative:
            raise RuntimeError("review.outputDirectory ist nicht konfiguriert.")
        output_root = (repo / output_relative).resolve()
        try:
            output_root.relative_to(repo.resolve())
        except ValueError as exc:
            raise RuntimeError("Review-Ausgabeverzeichnis liegt außerhalb des Repositorys.") from exc
        timestamp = dt.datetime.now(dt.timezone.utc)
        package_name = f"{timestamp.strftime('%Y%m%dT%H%M%SZ')}-{slug(task_path.stem)}"
        package = output_root / package_name
        counter = 1
        while package.exists():
            package = output_root / f"{package_name}-{counter}"
            counter += 1
        package.mkdir(parents=True)

        working_changed = set(
            split_zero_terminated(
                git(repo, ["diff", "--name-only", "-z", "HEAD", "--"], binary=True)
            )
        )
        working_tree_included = bool(set(selected_tracked) & working_changed) or bool(
            selected_untracked
        )
        metadata = {
            "packageVersion": "1.2",
            "generatedAt": timestamp.isoformat().replace("+00:00", "Z"),
            "language": review.get("language"),
            "baseRef": base,
            "baseCommit": base_commit,
            "headCommit": current_commit,
            "workingTreeIncluded": working_tree_included,
            "taskFile": task_relative,
            "changedFiles": selected,
            "includesImplementation": args.include_implementation,
            "explicitIncludes": explicit_paths,
            "claimInventory": claim_source[1] if claim_source else None,
            "externalEvidenceCount": len(external_evidence),
            "maximumFindings": review.get("maximumDefaultFindings"),
            "schema": schema_relative,
            "prompt": prompt_relative,
            "buildCommand": config.get("build", {}).get("command")
            if isinstance(config.get("build"), dict)
            else None,
        }
        (package / "changed-files.json").write_text(
            json.dumps(selected, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (package / "changes.diff").write_text(combined_diff, encoding="utf-8")
        diff_hash = file_hash(package / "changes.diff")
        metadata["diffHash"] = diff_hash
        shutil.copyfile(task_path, package / "task.md")
        shutil.copyfile(schema_path, package / "review-schema.json")
        shutil.copyfile(prompt_path, package / "review-prompt.md")
        metadata["reviewSchemaHash"] = file_hash(package / "review-schema.json")
        metadata["reviewPromptHash"] = file_hash(package / "review-prompt.md")
        package_config = {
            "reviewLanguage": review.get("language"),
            "maximumFindings": review.get("maximumDefaultFindings"),
            "schema": review.get("schema"),
            "prompt": review.get("prompt"),
        }
        (package / "review-config.json").write_text(
            json.dumps(package_config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        if claim_source:
            suffix = claim_source[0].suffix or ".txt"
            shutil.copyfile(claim_source[0], package / f"claim-inventory{suffix}")
        if external_evidence:
            evidence_document = {
                "schemaVersion": "1.0",
                "language": "de",
                "evidence": external_evidence,
            }
            (package / "external-evidence.json").write_text(
                json.dumps(evidence_document, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        (package / "metadata.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        metadata["packageHash"] = package_hash(package)
        (package / "metadata.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

        relative_package = package.relative_to(repo).as_posix()
        print(f"Review-Paket erzeugt: {relative_package}")
        print(f"Basis: {base} ({base_commit})")
        print(f"HEAD-Commit: {current_commit}")
        print(f"Arbeitsbaum enthalten: {'ja' if working_tree_included else 'nein'}")
        print(f"Diff-Hash: {diff_hash}")
        print(f"Paket-Hash: {metadata['packageHash']}")
        print(f"Geänderte Dateien: {len(selected)}")
        return 0
    except RuntimeError as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"FEHLER beim Schreiben des Review-Pakets: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

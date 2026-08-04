#!/usr/bin/env python3
"""Prüft alle Voraussetzungen vor einer Codex–Claude-Schreibaufgabe."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional

from claude_cli import (
    REQUIRED_CLAUDE_FLAGS,
    configured_model_and_effort,
    review_arguments,
    structured_output,
)
from review_schema import compact_json, load_schema, schema_hash, to_claude_cli_schema
from validate_review import validate_document


VERSION_PATTERN = re.compile(r"(?<!\d)(\d+)\.(\d+)\.(\d+)(?!\d)")


def find_repository(start: Optional[Path] = None) -> Path:
    candidates = [start or Path.cwd(), Path(__file__).resolve().parent]
    for candidate in candidates:
        for path in (candidate.resolve(), *candidate.resolve().parents):
            if (path / ".git").exists() and (path / ".ai" / "config.json").is_file():
                return path
    raise RuntimeError("Repository-Wurzel mit .git und .ai/config.json wurde nicht gefunden.")


def load_config(repo: Path) -> dict[str, Any]:
    try:
        value = json.loads((repo / ".ai" / "config.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f".ai/config.json kann nicht gelesen werden: {exc}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(".ai/config.json muss ein JSON-Objekt sein.")
    return value


def run(command: list[str], repo: Path, input_text: Optional[str] = None, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            cwd=repo,
            input=input_text,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            shell=False,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"Befehl überschritt das Zeitlimit von {timeout} Sekunden: {command[0]}") from exc


def parse_version(text: str, description: str) -> tuple[int, int, int]:
    match = VERSION_PATTERN.search(text)
    if not match:
        raise RuntimeError(f"Versionsnummer von {description} konnte nicht bestimmt werden: {text.strip()}")
    return tuple(int(part) for part in match.groups())


def repository_fingerprints(repo: Path) -> dict[str, str]:
    fingerprints: dict[str, str] = {}
    for root, directories, files in os.walk(repo, followlinks=False):
        root_path = Path(root)
        directories[:] = [name for name in directories if name != ".git"]
        for name in files:
            path = root_path / name
            relative = path.relative_to(repo).as_posix()
            digest = hashlib.sha256()
            try:
                if path.is_symlink():
                    digest.update(("SYMLINK:" + os.readlink(path)).encode("utf-8", "surrogateescape"))
                else:
                    with path.open("rb") as handle:
                        for block in iter(lambda: handle.read(1024 * 1024), b""):
                            digest.update(block)
                fingerprints[relative] = digest.hexdigest()
            except OSError as exc:
                raise RuntimeError(f"Datei kann nicht geprüft werden: {relative}: {exc}") from exc
    return fingerprints


def git_status(repo: Path) -> bytes:
    result = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "Git-Status kann nicht ermittelt werden: "
            + result.stderr.decode("utf-8", "replace").strip()
        )
    return result.stdout


def smoke_review() -> dict[str, Any]:
    return {
        "schemaVersion": "1.1",
        "reviewer": "claude",
        "language": "de",
        "reviewedCommit": "0000000",
        "workingTreeIncluded": False,
        "diffHash": "0" * 64,
        "packageHash": "0" * 64,
        "baseRef": "preflight",
        "verdict": "approved",
        "summary": "Der strukturierte Preflight-Test war erfolgreich.",
        "findings": [],
    }


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Prüft Python, Git, LaTeX und Claude einschließlich Anmeldung, "
            "Read-only-Modus und strukturierter Ausgabe."
        )
    )
    parser.add_argument(
        "--timeout",
        type=int,
        help="Zeitlimit des Claude-Smoke-Tests in Sekunden; Standard aus .ai/config.json",
    )
    args = parser.parse_args(argv)
    if args.timeout is not None and args.timeout < 1:
        parser.error("--timeout muss positiv sein")

    try:
        repo = find_repository()
        config = load_config(repo)
        print(f"OK: Python {sys.version.split()[0]}")
        if sys.version_info < (3, 9):
            raise RuntimeError("Python 3.9 oder neuer ist erforderlich.")

        preflight = config.get("preflight")
        if not isinstance(preflight, dict):
            raise RuntimeError("preflight in .ai/config.json muss ein Objekt sein.")
        executables = preflight.get("requiredExecutables")
        if not isinstance(executables, list) or not all(
            isinstance(item, str) and item for item in executables
        ):
            raise RuntimeError("preflight.requiredExecutables muss ein nicht leeres String-Array sein.")
        for executable in executables:
            resolved = shutil.which(executable)
            if resolved is None:
                raise RuntimeError(f"Erforderliches Werkzeug fehlt: {executable}")
            print(f"OK: Werkzeug {executable}: {resolved}")

        git_result = run(["git", "rev-parse", "--show-toplevel"], repo)
        if git_result.returncode != 0:
            raise RuntimeError("Git-Repository kann nicht geprüft werden: " + git_result.stderr.strip())
        print("OK: Git-Repository erreichbar")

        review = config.get("review")
        claude_config = config.get("claude")
        if not isinstance(review, dict) or not isinstance(claude_config, dict):
            raise RuntimeError("review und claude in .ai/config.json müssen Objekte sein.")
        schema_relative = review.get("schema")
        if not isinstance(schema_relative, str):
            raise RuntimeError("review.schema ist nicht konfiguriert.")
        canonical_schema = load_schema(repo / schema_relative)
        cli_schema = to_claude_cli_schema(canonical_schema)
        print(
            "OK: Kanonisches Schema transformierbar "
            f"(kanonisch {schema_hash(canonical_schema)[:12]}, CLI {schema_hash(cli_schema)[:12]})"
        )

        executable_name = claude_config.get("executable")
        if not isinstance(executable_name, str) or not executable_name:
            raise RuntimeError("claude.executable ist nicht konfiguriert.")
        claude = shutil.which(executable_name)
        if claude is None:
            raise RuntimeError(f"Claude CLI fehlt im PATH: {executable_name}")
        model, effort = configured_model_and_effort(claude_config)

        version_result = run([claude, "--version"], repo)
        version_text = (version_result.stdout + version_result.stderr).strip()
        if version_result.returncode != 0:
            raise RuntimeError("Claude-Version kann nicht ermittelt werden: " + version_text)
        actual_version = parse_version(version_text, "Claude CLI")
        minimum_text = claude_config.get("minimumStructuredOutputVersion")
        if not isinstance(minimum_text, str):
            raise RuntimeError("claude.minimumStructuredOutputVersion ist nicht konfiguriert.")
        minimum_version = parse_version(minimum_text, "Mindestversion")
        if actual_version < minimum_version:
            raise RuntimeError(
                f"Claude CLI {version_text} ist zu alt; für strukturierte Ausgabe ist mindestens {minimum_text} erforderlich."
            )
        print(f"OK: Claude CLI {version_text}")

        help_result = run([claude, "--help"], repo)
        help_text = help_result.stdout + help_result.stderr
        if help_result.returncode != 0:
            raise RuntimeError("claude --help ist fehlgeschlagen.")
        missing_flags = [flag for flag in REQUIRED_CLAUDE_FLAGS if flag not in help_text]
        if missing_flags or "plan" not in help_text.lower():
            detail = ", ".join(missing_flags) if missing_flags else "Berechtigungsmodus plan"
            raise RuntimeError(f"Claude CLI unterstützt die erforderlichen Optionen nicht: {detail}")
        print(
            "OK: Claude unterstützt Modell- und Effort-Auswahl, plan, deaktivierte "
            "Werkzeuge, JSON-Ausgabe und --json-schema"
        )

        timeout = args.timeout
        if timeout is None:
            configured_timeout = claude_config.get("smokeTestTimeoutSeconds", 60)
            if type(configured_timeout) is not int or configured_timeout < 1:
                raise RuntimeError("claude.smokeTestTimeoutSeconds muss eine positive ganze Zahl sein.")
            timeout = configured_timeout

        expected = smoke_review()
        prompt = (
            "Dies ist ein technischer Preflight ohne Repository-Inhalt. Gib ein JSON-Objekt "
            "ohne Findings zurück. Verwende exakt diese maschinenlesbaren Werte: "
            + json.dumps(expected, ensure_ascii=False)
        )
        command = [claude, *review_arguments(model, effort, compact_json(cli_schema))]
        status_before = git_status(repo)
        before = repository_fingerprints(repo)
        smoke_result = run(command, repo, input_text=prompt, timeout=timeout)
        status_after = git_status(repo)
        after = repository_fingerprints(repo)
        changed = sorted(path for path in set(before) | set(after) if before.get(path) != after.get(path))
        if status_before != status_after and not changed:
            changed = ["<Git-Index oder Git-Status>"]
        if changed or status_before != status_after:
            raise RuntimeError(
                "Claude veränderte während des Preflight-Smoke-Tests Repository oder Git-Index: "
                + ", ".join(changed)
            )
        if smoke_result.returncode != 0:
            detail = smoke_result.stderr.strip() or smoke_result.stdout.strip() or "keine Diagnose"
            raise RuntimeError(
                "Claude-Anmeldung oder strukturierter Schema-Smoke-Test fehlgeschlagen: "
                + detail[:1000]
            )
        document = structured_output(smoke_result.stdout)
        validation_errors = validate_document(document, maximum_findings=0)
        if validation_errors:
            raise RuntimeError(
                "Claude-Smoke-Ausgabe verletzt das Review-Schema: " + "; ".join(validation_errors)
            )
        print(
            f"OK: Claude-Anmeldung und strukturierter Read-only-Smoke-Test "
            f"mit Modell {model} und Effort {effort}"
        )
        print("Preflight erfolgreich. Die Schreib- und Review-Aufgabe kann beginnen.")
        return 0
    except RuntimeError as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        print("Preflight fehlgeschlagen. Vor dem Schreiben keine Review-Aufgabe beginnen.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

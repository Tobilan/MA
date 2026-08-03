#!/usr/bin/env python3
"""Validiert Entscheidungen und ihre vollständige Zuordnung zu Review-Findings."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Optional

from validate_review import validate_document


TOP_FIELDS = {
    "schemaVersion",
    "language",
    "taskName",
    "reviewFile",
    "reviewPackageHash",
    "decisions",
}
DECISION_FIELDS = {
    "findingId",
    "status",
    "statusLabel",
    "reviewerStatement",
    "verification",
    "checkedEvidence",
    "rationale",
    "resultingAction",
    "files",
    "checkCommand",
    "residualRisk",
}
STATUS_LABELS = {
    "ACCEPTED": "angenommen",
    "REJECTED": "abgelehnt",
    "DEFERRED": "zurückgestellt",
}
FINDING_ID = re.compile(r"^CL-[0-9]{3,}$")
SHA256_ID = re.compile(r"^[0-9a-fA-F]{64}$")
WINDOWS_ABSOLUTE = re.compile(r"^[A-Za-z]:")


def find_repository(start: Optional[Path] = None) -> Path:
    candidates = [start or Path.cwd(), Path(__file__).resolve().parent]
    for candidate in candidates:
        for path in (candidate.resolve(), *candidate.resolve().parents):
            if (path / ".git").exists() and (path / ".ai" / "config.json").is_file():
                return path
    raise ValueError("Repository-Wurzel mit .git und .ai/config.json wurde nicht gefunden.")


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def relative_path(value: Any) -> bool:
    if not nonempty(value) or "\\" in value or "\x00" in value:
        return False
    if value.startswith("/") or WINDOWS_ABSOLUTE.match(value):
        return False
    return all(part not in {"", ".", ".."} for part in PurePosixPath(value).parts)


def read_json(path: Path, description: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"{description} fehlt: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Ungültiges JSON in {description}, Zeile {exc.lineno}, Spalte {exc.colno}: {exc.msg}"
        ) from exc


def validate_decision_document(decisions: Any, review: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(decisions, dict):
        return ["Entscheidungsakte: Erwartet wird ein JSON-Objekt."]
    missing = sorted(TOP_FIELDS - set(decisions))
    extra = sorted(set(decisions) - TOP_FIELDS)
    if missing:
        errors.append("Entscheidungsakte: Pflichtfelder fehlen: " + ", ".join(missing) + ".")
    if extra:
        errors.append("Entscheidungsakte: Unerwartete Felder: " + ", ".join(extra) + ".")
    if decisions.get("schemaVersion") != "1.0":
        errors.append("Entscheidungsakte.schemaVersion muss exakt '1.0' sein.")
    if decisions.get("language") != "de":
        errors.append("Entscheidungsakte.language muss exakt 'de' sein.")
    if not nonempty(decisions.get("taskName")):
        errors.append("Entscheidungsakte.taskName muss eine nicht leere Zeichenkette sein.")
    if not relative_path(decisions.get("reviewFile")):
        errors.append("Entscheidungsakte.reviewFile muss repository-relativ und sicher sein.")
    package_hash = decisions.get("reviewPackageHash")
    if not isinstance(package_hash, str) or not SHA256_ID.fullmatch(package_hash):
        errors.append("Entscheidungsakte.reviewPackageHash muss ein SHA-256-Hash sein.")
    elif package_hash != review.get("packageHash"):
        errors.append("Entscheidungsakte.reviewPackageHash stimmt nicht mit dem Review überein.")

    items = decisions.get("decisions")
    if not isinstance(items, list):
        errors.append("Entscheidungsakte.decisions muss ein Array sein.")
        return errors
    found_ids: list[str] = []
    for index, item in enumerate(items):
        location = f"Entscheidungsakte.decisions[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{location} muss ein JSON-Objekt sein.")
            continue
        missing_item = sorted(DECISION_FIELDS - set(item))
        extra_item = sorted(set(item) - DECISION_FIELDS)
        if missing_item:
            errors.append(f"{location}: Pflichtfelder fehlen: {', '.join(missing_item)}.")
        if extra_item:
            errors.append(f"{location}: Unerwartete Felder: {', '.join(extra_item)}.")
        finding_id = item.get("findingId")
        if not isinstance(finding_id, str) or not FINDING_ID.fullmatch(finding_id):
            errors.append(f"{location}.findingId muss dem Format CL-001 entsprechen.")
        else:
            found_ids.append(finding_id)
        status = item.get("status")
        if status not in STATUS_LABELS:
            errors.append(f"{location}.status ist ungültig.")
        elif item.get("statusLabel") != STATUS_LABELS[status]:
            errors.append(f"{location}.statusLabel passt nicht zu {status}.")
        for field in (
            "reviewerStatement",
            "verification",
            "rationale",
            "resultingAction",
            "checkCommand",
            "residualRisk",
        ):
            if not nonempty(item.get(field)):
                errors.append(f"{location}.{field} muss eine nicht leere deutsche Zeichenkette sein.")
        evidence = item.get("checkedEvidence")
        if (
            not isinstance(evidence, list)
            or not evidence
            or not all(nonempty(entry) for entry in evidence)
        ):
            errors.append(f"{location}.checkedEvidence muss ein Array nicht leerer Zeichenketten sein.")
        files = item.get("files")
        if not isinstance(files, list) or not all(relative_path(entry) for entry in files):
            errors.append(f"{location}.files muss sichere repository-relative Pfade enthalten.")

    if len(found_ids) != len(set(found_ids)):
        errors.append("Entscheidungsakte: Mindestens eine Finding-ID wurde mehrfach entschieden.")
    review_ids = {
        item.get("id")
        for item in review.get("findings", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    decision_ids = set(found_ids)
    missing_decisions = sorted(review_ids - decision_ids)
    unknown_decisions = sorted(decision_ids - review_ids)
    if missing_decisions:
        errors.append("Entscheidungsakte: Findings ohne Entscheidung: " + ", ".join(missing_decisions) + ".")
    if unknown_decisions:
        errors.append("Entscheidungsakte: Entscheidungen ohne Review-Finding: " + ", ".join(unknown_decisions) + ".")
    return errors


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prüft eine maschinenlesbare Entscheidungsakte gegen das zugehörige Review."
    )
    parser.add_argument("review", type=Path, help="Normalisierte review.json eines erfolgreichen Attempts")
    parser.add_argument("decisions", type=Path, help="Maschinenlesbare Entscheidungsakte")
    args = parser.parse_args(argv)
    try:
        review = read_json(args.review, "Review")
        if not isinstance(review, dict):
            raise ValueError("Review muss ein JSON-Objekt sein.")
        review_errors = validate_document(review)
        decisions = read_json(args.decisions, "Entscheidungsakte")
    except ValueError as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        return 2
    errors = review_errors + validate_decision_document(decisions, review)
    if isinstance(decisions, dict):
        try:
            repo = find_repository()
        except ValueError as exc:
            errors.append(str(exc))
            repo = None
        if repo is None:
            expected_review_file = None
        else:
            try:
                expected_review_file = args.review.resolve().relative_to(repo).as_posix()
            except ValueError:
                errors.append("Review-Datei liegt außerhalb des Repositorys.")
                expected_review_file = None
        if expected_review_file is not None and decisions.get("reviewFile") != expected_review_file:
            errors.append(
                "Entscheidungsakte.reviewFile stimmt nicht mit der geprüften Review-Datei überein."
            )

        review_path = args.review.resolve()
        try:
            package = review_path.parent.parent
            marker = read_json(package / "successful-attempt.json", "Erfolgsmarkierung")
        except ValueError as exc:
            errors.append(str(exc))
        else:
            marker_review = marker.get("review") if isinstance(marker, dict) else None
            try:
                marked_path = (package / str(marker_review)).resolve()
                marked_path.relative_to(package.resolve())
            except (ValueError, OSError):
                errors.append("Erfolgsmarkierung enthält keinen sicheren Review-Pfad.")
            else:
                if marker_review is None or marked_path != review_path:
                    errors.append(
                        "Review-Datei ist nicht der in successful-attempt.json markierte Lauf."
                    )
            if not isinstance(marker, dict) or marker.get("packageHash") != review.get("packageHash"):
                errors.append(
                    "Erfolgsmarkierung stimmt nicht mit dem Paket-Hash des Reviews überein."
                )
    if errors:
        for error in errors:
            print(f"FEHLER: {error}", file=sys.stderr)
        print(f"Entscheidungsvalidierung fehlgeschlagen: {len(errors)} Fehler.", file=sys.stderr)
        return 1
    print("Entscheidungsakte ist gültig; jedes Finding wurde genau einmal entschieden.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

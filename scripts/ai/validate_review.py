#!/usr/bin/env python3
"""Validiert strukturierte Claude-Reviews ohne externe Abhängigkeiten."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Optional


TOP_LEVEL_FIELDS = {
    "schemaVersion",
    "reviewer",
    "language",
    "reviewedCommit",
    "workingTreeIncluded",
    "diffHash",
    "packageHash",
    "baseRef",
    "verdict",
    "summary",
    "findings",
}
FINDING_FIELDS = {
    "id",
    "severity",
    "category",
    "file",
    "lineStart",
    "lineEnd",
    "statement",
    "problem",
    "evidence",
    "requiredAction",
    "confidence",
}
VERDICTS = {"approved", "approved_with_comments", "changes_requested"}
SEVERITIES = {"blocking", "major", "minor", "suggestion"}
CATEGORIES = {
    "implementation_mismatch",
    "unsupported_claim",
    "source_problem",
    "reasoning_gap",
    "missing_limitation",
    "terminology",
    "german_language",
    "latex_structure",
    "style",
    "other",
}
CONFIDENCES = {"high", "medium", "low"}
FINDING_ID = re.compile(r"^CL-[0-9]{3,}$")
COMMIT_ID = re.compile(r"^[0-9a-fA-F]{7,40}$")
SHA256_ID = re.compile(r"^[0-9a-fA-F]{64}$")
WINDOWS_ABSOLUTE = re.compile(r"^[A-Za-z]:")


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _exact_positive_integer_or_none(value: Any) -> bool:
    return value is None or (type(value) is int and value >= 1)


def _relative_repository_path(value: Any) -> bool:
    if not _nonempty_string(value) or "\\" in value or "\x00" in value:
        return False
    if value.startswith("/") or WINDOWS_ABSOLUTE.match(value):
        return False
    parts = PurePosixPath(value).parts
    return bool(parts) and all(part not in {"", ".", ".."} for part in parts)


def _field_set_errors(
    value: dict[str, Any], expected: set[str], location: str
) -> list[str]:
    errors: list[str] = []
    missing = sorted(expected - set(value))
    extra = sorted(set(value) - expected)
    if missing:
        errors.append(f"{location}: Pflichtfelder fehlen: {', '.join(missing)}.")
    if extra:
        errors.append(f"{location}: Unerwartete Felder: {', '.join(extra)}.")
    return errors


def validate_document(
    document: Any, maximum_findings: Optional[int] = None
) -> list[str]:
    """Gibt alle strukturellen Validierungsfehler zurück."""

    if not isinstance(document, dict):
        return ["Wurzel: Erwartet wird ein JSON-Objekt."]

    errors = _field_set_errors(document, TOP_LEVEL_FIELDS, "Wurzel")
    if errors:
        # Vorhandene Felder werden trotzdem geprüft, ohne fehlende Schlüssel auszulesen.
        pass

    scalar_rules = (
        ("schemaVersion", lambda v: v == "1.1", "muss exakt '1.1' sein"),
        ("reviewer", lambda v: v == "claude", "muss exakt 'claude' sein"),
        ("language", lambda v: v == "de", "muss exakt 'de' sein"),
        (
            "reviewedCommit",
            lambda v: isinstance(v, str) and bool(COMMIT_ID.fullmatch(v)),
            "muss eine Git-Commit-ID mit 7 bis 40 Hexadezimalzeichen sein",
        ),
        (
            "workingTreeIncluded",
            lambda v: type(v) is bool,
            "muss ein boolescher Wert sein",
        ),
        (
            "diffHash",
            lambda v: isinstance(v, str) and bool(SHA256_ID.fullmatch(v)),
            "muss ein SHA-256-Hash mit 64 Hexadezimalzeichen sein",
        ),
        (
            "packageHash",
            lambda v: isinstance(v, str) and bool(SHA256_ID.fullmatch(v)),
            "muss ein SHA-256-Hash mit 64 Hexadezimalzeichen sein",
        ),
        ("baseRef", _nonempty_string, "muss eine nicht leere Zeichenkette sein"),
        (
            "verdict",
            lambda v: isinstance(v, str) and v in VERDICTS,
            f"muss einer von {sorted(VERDICTS)} sein",
        ),
        ("summary", _nonempty_string, "muss eine nicht leere deutsche Zusammenfassung sein"),
    )
    for field, predicate, message in scalar_rules:
        if field in document and not predicate(document[field]):
            errors.append(f"Wurzel.{field}: {message}.")

    findings = document.get("findings")
    if findings is not None and not isinstance(findings, list):
        errors.append("Wurzel.findings: Erwartet wird ein Array.")
        return errors
    if not isinstance(findings, list):
        return errors
    if maximum_findings is not None and len(findings) > maximum_findings:
        errors.append(
            "Wurzel.findings: "
            f"Enthält {len(findings)} Findings; höchstens {maximum_findings} sind zulässig."
        )

    seen_ids: set[str] = set()
    for index, finding in enumerate(findings):
        location = f"Wurzel.findings[{index}]"
        if not isinstance(finding, dict):
            errors.append(f"{location}: Erwartet wird ein JSON-Objekt.")
            continue
        errors.extend(_field_set_errors(finding, FINDING_FIELDS, location))

        finding_id = finding.get("id")
        if not isinstance(finding_id, str) or not FINDING_ID.fullmatch(finding_id):
            errors.append(f"{location}.id: Erwartet wird das Format 'CL-001'.")
        elif finding_id in seen_ids:
            errors.append(f"{location}.id: Die Finding-ID {finding_id} ist doppelt.")
        else:
            seen_ids.add(finding_id)

        enum_rules = (
            ("severity", SEVERITIES),
            ("category", CATEGORIES),
            ("confidence", CONFIDENCES),
        )
        for field, allowed in enum_rules:
            if field in finding and (
                not isinstance(finding[field], str) or finding[field] not in allowed
            ):
                errors.append(
                    f"{location}.{field}: Ungültiger Wert; zulässig sind {sorted(allowed)}."
                )

        if "file" in finding and not _relative_repository_path(finding["file"]):
            errors.append(
                f"{location}.file: Erwartet wird ein repository-relativer Pfad ohne '..' oder Backslashes."
            )

        for field in ("lineStart", "lineEnd"):
            if field in finding and not _exact_positive_integer_or_none(finding[field]):
                errors.append(
                    f"{location}.{field}: Erwartet wird null oder eine positive ganze Zahl."
                )
        start = finding.get("lineStart")
        end = finding.get("lineEnd")
        if (start is None) != (end is None):
            errors.append(
                f"{location}: lineStart und lineEnd müssen entweder beide null oder beide Zahlen sein."
            )
        elif type(start) is int and type(end) is int and end < start:
            errors.append(f"{location}: lineEnd darf nicht vor lineStart liegen.")

        for field in ("statement", "problem", "evidence", "requiredAction"):
            if field in finding and not _nonempty_string(finding[field]):
                errors.append(
                    f"{location}.{field}: Erwartet wird eine nicht leere deutsche Zeichenkette."
                )

    return errors


def check_schema_document(schema: Any) -> list[str]:
    """Prüft die für diesen Workflow benötigten Schema-Eigenschaften."""

    errors: list[str] = []
    if not isinstance(schema, dict):
        return ["Schema: Erwartet wird ein JSON-Objekt."]
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append("Schema.$schema: Draft 2020-12 muss deklariert sein.")
    if schema.get("type") != "object" or schema.get("additionalProperties") is not False:
        errors.append("Schema: Wurzel muss ein geschlossenes Objekt sein.")
    required = schema.get("required")
    if (
        not isinstance(required, list)
        or not all(isinstance(item, str) for item in required)
        or set(required) != TOP_LEVEL_FIELDS
    ):
        errors.append("Schema.required: Die Top-Level-Pflichtfelder sind unvollständig.")
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        return errors + ["Schema.properties: Erwartet wird ein Objekt."]
    expected_constants = {"schemaVersion": "1.1", "reviewer": "claude", "language": "de"}
    for field, expected in expected_constants.items():
        if not isinstance(properties.get(field), dict) or properties[field].get("const") != expected:
            errors.append(f"Schema.properties.{field}: const muss '{expected}' sein.")
    definitions = schema.get("$defs")
    finding = definitions.get("finding") if isinstance(definitions, dict) else None
    if not isinstance(finding, dict):
        return errors + ["Schema.$defs.finding: Definition fehlt."]
    if finding.get("additionalProperties") is not False:
        errors.append("Schema.$defs.finding: Zusätzliche Eigenschaften müssen abgelehnt werden.")
    finding_required = finding.get("required")
    if (
        not isinstance(finding_required, list)
        or not all(isinstance(item, str) for item in finding_required)
        or set(finding_required) != FINDING_FIELDS
    ):
        errors.append("Schema.$defs.finding.required: Finding-Pflichtfelder sind unvollständig.")
    return errors


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"Datei nicht gefunden: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Ungültiges JSON in {path}, Zeile {exc.lineno}, Spalte {exc.colno}: {exc.msg}"
        ) from exc


def _print_errors(errors: Iterable[str]) -> None:
    for error in errors:
        print(f"FEHLER: {error}", file=sys.stderr)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Validiert ein strukturiertes Claude-Review.")
    parser.add_argument("review", nargs="?", type=Path, help="Pfad zur Review-JSON-Datei")
    parser.add_argument(
        "--check-schema",
        type=Path,
        metavar="SCHEMA",
        help="Prüft stattdessen die Workflow-Eigenschaften des JSON-Schemas.",
    )
    parser.add_argument(
        "--maximum-findings", type=int, help="Optional zulässige Höchstzahl an Findings"
    )
    args = parser.parse_args(argv)

    if args.maximum_findings is not None and args.maximum_findings < 0:
        parser.error("--maximum-findings darf nicht negativ sein")
    target = args.check_schema or args.review
    if target is None:
        parser.error("Review-Datei oder --check-schema angeben")

    try:
        document = _read_json(target)
    except ValueError as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        return 2

    errors = (
        check_schema_document(document)
        if args.check_schema
        else validate_document(document, args.maximum_findings)
    )
    if errors:
        _print_errors(errors)
        print(f"Validierung fehlgeschlagen: {len(errors)} Fehler.", file=sys.stderr)
        return 1

    kind = "Review-Schema" if args.check_schema else "Review"
    print(f"{kind} ist strukturell gültig.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

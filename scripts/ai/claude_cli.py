"""Gemeinsame Konfiguration und Ausgabeauswertung für die Claude-CLI."""

from __future__ import annotations

import json
from typing import Any


REQUIRED_CLAUDE_FLAGS = (
    "--print",
    "--safe-mode",
    "--model",
    "--effort",
    "--permission-mode",
    "--tools",
    "--no-session-persistence",
    "--output-format",
    "--json-schema",
)
ALLOWED_EFFORT_LEVELS = {"low", "medium", "high", "xhigh", "max"}


def configured_model_and_effort(claude_config: dict[str, Any]) -> tuple[str, str]:
    """Liest und validiert die verbindliche Modellkonfiguration."""
    model = claude_config.get("model")
    if not isinstance(model, str) or not model.strip():
        raise RuntimeError("claude.model ist nicht konfiguriert.")
    effort = claude_config.get("effort")
    if not isinstance(effort, str) or effort not in ALLOWED_EFFORT_LEVELS:
        allowed = ", ".join(sorted(ALLOWED_EFFORT_LEVELS))
        raise RuntimeError(f"claude.effort muss einen der folgenden Werte verwenden: {allowed}.")
    return model.strip(), effort


def review_arguments(model: str, effort: str, schema: str) -> list[str]:
    """Erzeugt die gemeinsamen Read-only-Argumente eines strukturierten Reviews."""
    return [
        "--print",
        "--safe-mode",
        "--model",
        model,
        "--effort",
        effort,
        "--permission-mode",
        "plan",
        "--tools",
        "",
        "--no-session-persistence",
        "--output-format",
        "json",
        "--json-schema",
        schema,
    ]


def structured_output(raw_output: str) -> dict[str, Any]:
    """Extrahiert die schema-validierte Nutzlast aus dem JSON-Ausgabeformat."""
    try:
        envelope = json.loads(raw_output)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Claude lieferte trotz --output-format json kein gültiges JSON "
            f"(Zeile {exc.lineno}, Spalte {exc.colno}: {exc.msg})."
        ) from exc
    if not isinstance(envelope, dict):
        raise RuntimeError("Die JSON-Ausgabe der Claude-CLI muss ein Objekt sein.")
    document = envelope.get("structured_output")
    if not isinstance(document, dict):
        raise RuntimeError(
            "Die Claude-CLI-Ausgabe enthält kein schema-validiertes structured_output-Objekt."
        )
    return document

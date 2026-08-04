#!/usr/bin/env python3
"""
Führt den lokalen Codex-Claude-Workflow aus, ohne dass Codex die einzelnen
Python-Skripte starten oder überwachen muss.

Vorgesehener Zielpfad im Repository:
    scripts/ai/run_ai_workflow.py

Beispiele:
    python scripts/ai/run_ai_workflow.py check
    python scripts/ai/run_ai_workflow.py prepare
    python scripts/ai/run_ai_workflow.py review
    python scripts/ai/run_ai_workflow.py validate
    python scripts/ai/run_ai_workflow.py pre-review

Argumente an ein einzelnes Skript weiterreichen:
    python scripts/ai/run_ai_workflow.py prepare -- --base main --task .ai/tasks/kapitel-04-01.md

Argumente für die Stufen eines vollständigen Laufs:
    python scripts/ai/run_ai_workflow.py pre-review \
        --prepare-args "--base main --task .ai/tasks/kapitel-04-01.md" \
        --review-args "--package .ai/reviews/kapitel-04-01" \
        --validate-args ".ai/reviews/kapitel-04-01/review.json"

Hinweis:
Die konkreten Argumente hängen von den im Repository implementierten
Einzelskripten ab. Ohne Zusatzargumente werden deren Standardwerte verwendet.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


SCRIPT_NAMES = {
    "check": "check_thesis.py",
    "prepare": "prepare_review.py",
    "review": "run_claude_review.py",
    "validate": "validate_review.py",
}


class WorkflowError(RuntimeError):
    """Kontrollierter Fehler mit verständlicher Ausgabe."""


@dataclass(frozen=True)
class Step:
    key: str
    label: str
    script: Path
    arguments: tuple[str, ...] = ()


def find_repository_root(start: Path) -> Path:
    """Sucht vom Startpfad aufwärts nach dem Repository-Wurzelverzeichnis."""
    candidates = [start.resolve(), *start.resolve().parents]
    for candidate in candidates:
        scripts_dir = candidate / "scripts" / "ai"
        if scripts_dir.is_dir() and (
            (candidate / ".git").exists()
            or (candidate / ".ai").exists()
            or (candidate / "AGENTS.md").exists()
        ):
            return candidate

    raise WorkflowError(
        "Repository-Wurzel nicht gefunden. Starte das Skript innerhalb des "
        "Repositories oder lege es unter scripts/ai/ ab."
    )


def split_arguments(value: str | None) -> tuple[str, ...]:
    """Zerlegt eine zitierte Argumentzeichenfolge plattformgerecht."""
    if not value:
        return ()
    return tuple(shlex.split(value, posix=os.name != "nt"))


def normalize_passthrough(arguments: Sequence[str]) -> tuple[str, ...]:
    """Entfernt den optionalen Trenner '--' vor durchgereichten Argumenten."""
    if arguments and arguments[0] == "--":
        return tuple(arguments[1:])
    return tuple(arguments)


def ensure_scripts_exist(repo_root: Path, keys: Iterable[str]) -> dict[str, Path]:
    """Prüft, ob alle benötigten Workflow-Skripte vorhanden sind."""
    result: dict[str, Path] = {}
    missing: list[str] = []

    for key in keys:
        path = repo_root / "scripts" / "ai" / SCRIPT_NAMES[key]
        if path.is_file():
            result[key] = path
        else:
            missing.append(str(path.relative_to(repo_root)))

    if missing:
        formatted = "\n  - ".join(missing)
        raise WorkflowError(
            "Folgende benötigte Skripte fehlen:\n"
            f"  - {formatted}\n"
            "Führe zuerst das Setup des Codex-Claude-Workflows aus."
        )

    return result


def git_status(repo_root: Path) -> str:
    """Erfasst den aktuellen Git-Status für das Ausführungsprotokoll."""
    try:
        completed = subprocess.run(
            ["git", "status", "--short"],
            cwd=repo_root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
    except OSError:
        return "Git konnte nicht ausgeführt werden."

    output = completed.stdout.strip()
    return output or "Arbeitsverzeichnis sauber."


def write_metadata(
    log_dir: Path,
    *,
    repo_root: Path,
    command: str,
    steps: Sequence[Step],
    dry_run: bool,
) -> None:
    """Schreibt nicht-sensitive Metadaten über den Workflow-Lauf."""
    metadata = {
        "startedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "repository": str(repo_root),
        "command": command,
        "python": sys.executable,
        "dryRun": dry_run,
        "steps": [
            {
                "key": step.key,
                "label": step.label,
                "script": str(step.script.relative_to(repo_root)),
                "arguments": list(step.arguments),
            }
            for step in steps
        ],
        "gitStatusBefore": git_status(repo_root),
    }
    (log_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def run_step(
    step: Step,
    *,
    repo_root: Path,
    log_dir: Path,
    dry_run: bool,
) -> str:
    """Führt einen Workflow-Schritt aus und protokolliert dessen Ausgabe."""
    command = [sys.executable, str(step.script), *step.arguments]
    printable = " ".join(shlex.quote(part) for part in command)

    print(f"\n=== {step.label} ===")
    print(f"$ {printable}")

    log_path = log_dir / f"{step.key}.log"

    if dry_run:
        log_path.write_text(
            f"DRY RUN\n{printable}\n",
            encoding="utf-8",
        )
        return ""

    try:
        process = subprocess.Popen(
            command,
            cwd=repo_root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
        )
    except OSError as error:
        raise WorkflowError(
            f"{step.label} konnte nicht gestartet werden: {error}"
        ) from error

    output_lines: list[str] = []
    assert process.stdout is not None

    for line in process.stdout:
        print(line, end="")
        output_lines.append(line)

    return_code = process.wait()
    log_path.write_text("".join(output_lines), encoding="utf-8")

    if return_code != 0:
        raise WorkflowError(
            f"{step.label} ist mit Exit-Code {return_code} fehlgeschlagen. "
            f"Protokoll: {log_path.relative_to(repo_root)}"
        )

    print(f"Erfolgreich: {step.label}")
    return "".join(output_lines)


def extract_reported_path(output: str, prefix: str, repo_root: Path) -> Path:
    """Liest einen von einem Workflow-Skript ausgegebenen Repository-Pfad."""
    match = re.search(rf"^{re.escape(prefix)}(?P<path>.+)$", output, re.MULTILINE)
    if match is None:
        raise WorkflowError(
            f"Der erwartete Pfad konnte nicht aus der Ausgabe gelesen werden: {prefix.strip()}"
        )
    reported = Path(match.group("path").strip())
    candidate = reported if reported.is_absolute() else repo_root / reported
    resolved = candidate.resolve()
    try:
        resolved.relative_to(repo_root.resolve())
    except ValueError as error:
        raise WorkflowError("Ein Workflow-Schritt hat einen Pfad außerhalb des Repositorys gemeldet.") from error
    return resolved


def infer_task_file(repo_root: Path) -> Path:
    """Ermittelt die einzige konkrete Aufgabendatei, wenn --task fehlt."""
    task_directory = repo_root / ".ai" / "tasks"
    candidates = sorted(
        path
        for path in task_directory.glob("*.md")
        if path.name != "TASK_TEMPLATE.md"
    )
    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        raise WorkflowError(
            "Keine Aufgabendatei gefunden. Übergib für pre-review --task .ai/tasks/<aufgabe>.md."
        )
    raise WorkflowError(
        "Mehrere Aufgabendateien gefunden. Übergib für pre-review ausdrücklich "
        "--task .ai/tasks/<aufgabe>.md."
    )


def build_steps(
    repo_root: Path,
    command: str,
    args: argparse.Namespace,
) -> list[Step]:
    """Erzeugt die auszuführenden Schritte für das gewählte Kommando."""
    if command in SCRIPT_NAMES:
        paths = ensure_scripts_exist(repo_root, [command])
        passthrough = normalize_passthrough(args.passthrough)
        labels = {
            "check": "Masterarbeit prüfen",
            "prepare": "Review-Paket erzeugen",
            "review": "Claude-Review ausführen",
            "validate": "Review validieren",
        }
        return [
            Step(
                key=command,
                label=labels[command],
                script=paths[command],
                arguments=passthrough,
            )
        ]

    if command == "pre-review":
        keys = ["check", "prepare", "review", "validate"]
        paths = ensure_scripts_exist(repo_root, keys)
        task = (args.task or infer_task_file(repo_root)).resolve()
        try:
            task_argument = str(task.relative_to(repo_root))
        except ValueError as error:
            raise WorkflowError("Die Aufgabendatei für pre-review liegt außerhalb des Repositorys.") from error
        prepare_arguments = ["--task", task_argument]
        prepare_arguments.extend(split_arguments(args.prepare_args))
        return [
            Step(
                "check",
                "Masterarbeit vor dem Review prüfen",
                paths["check"],
                split_arguments(args.check_args),
            ),
            Step(
                "prepare",
                "Review-Paket erzeugen",
                paths["prepare"],
                tuple(prepare_arguments),
            ),
        ]

    if command == "post-review":
        paths = ensure_scripts_exist(repo_root, ["check"])
        return [
            Step(
                "check",
                "Masterarbeit nach den Review-Änderungen prüfen",
                paths["check"],
                split_arguments(args.check_args),
            )
        ]

    raise WorkflowError(f"Unbekanntes Kommando: {command}")


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Orchestriert die vorhandenen Python-Skripte des "
            "Codex-Claude-Workflows."
        )
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Kommandos nur anzeigen, aber nicht ausführen.",
    )
    parser.add_argument(
        "--log-root",
        default=".ai/workflow-logs",
        help=(
            "Verzeichnis für Ausführungsprotokolle, relativ zur "
            "Repository-Wurzel. Standard: .ai/workflow-logs"
        ),
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    for name, help_text in (
        ("check", "Nur check_thesis.py ausführen."),
        ("prepare", "Nur prepare_review.py ausführen."),
        ("review", "Nur run_claude_review.py ausführen."),
        ("validate", "Nur validate_review.py ausführen."),
    ):
        child = subparsers.add_parser(name, help=help_text)
        child.add_argument(
            "passthrough",
            nargs=argparse.REMAINDER,
            help="Argumente nach '--' werden an das Einzelskript weitergereicht.",
        )

    pre = subparsers.add_parser(
        "pre-review",
        help="Check, Review-Paket, Claude-Review und Validierung nacheinander.",
    )
    pre.add_argument(
        "--task",
        type=Path,
        help=(
            "Konkrete Aufgabendatei. Fehlt sie, wird die einzige Datei unter "
            ".ai/tasks/ verwendet."
        ),
    )
    pre.add_argument(
        "--check-args",
        default=os.environ.get("AI_CHECK_ARGS", ""),
        help="Argumentzeichenfolge für check_thesis.py.",
    )
    pre.add_argument(
        "--prepare-args",
        default=os.environ.get("AI_PREPARE_ARGS", ""),
        help="Argumentzeichenfolge für prepare_review.py.",
    )
    pre.add_argument(
        "--review-args",
        default=os.environ.get("AI_REVIEW_ARGS", ""),
        help="Argumentzeichenfolge für run_claude_review.py.",
    )
    pre.add_argument(
        "--validate-args",
        default=os.environ.get("AI_VALIDATE_ARGS", ""),
        help="Argumentzeichenfolge für validate_review.py.",
    )

    post = subparsers.add_parser(
        "post-review",
        help="Nach übernommenen Review-Änderungen die Masterarbeit erneut prüfen.",
    )
    post.add_argument(
        "--check-args",
        default=os.environ.get("AI_CHECK_ARGS", ""),
        help="Argumentzeichenfolge für check_thesis.py.",
    )

    return parser


def main() -> int:
    parser = create_parser()
    args = parser.parse_args()

    try:
        script_location = Path(__file__).resolve()
        repo_root = find_repository_root(script_location.parent)
        steps = build_steps(repo_root, args.command, args)

        timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        log_root = Path(args.log_root)
        if not log_root.is_absolute():
            log_root = repo_root / log_root
        log_dir = log_root / f"{timestamp}-{args.command}"
        log_dir.mkdir(parents=True, exist_ok=False)

        write_metadata(
            log_dir,
            repo_root=repo_root,
            command=args.command,
            steps=steps,
            dry_run=args.dry_run,
        )

        print(f"Repository: {repo_root}")
        print(f"Protokolle: {log_dir.relative_to(repo_root)}")

        if args.command == "pre-review":
            check_step, prepare_step = steps
            run_step(
                check_step,
                repo_root=repo_root,
                log_dir=log_dir,
                dry_run=args.dry_run,
            )
            prepare_output = run_step(
                prepare_step,
                repo_root=repo_root,
                log_dir=log_dir,
                dry_run=args.dry_run,
            )
            if not args.dry_run:
                package = extract_reported_path(
                    prepare_output, "Review-Paket erzeugt: ", repo_root
                )
                review_step = Step(
                    "review",
                    "Claude-Review ausführen",
                    repo_root / "scripts" / "ai" / SCRIPT_NAMES["review"],
                    ("--package", str(package.relative_to(repo_root)), *split_arguments(args.review_args)),
                )
                review_output = run_step(
                    review_step,
                    repo_root=repo_root,
                    log_dir=log_dir,
                    dry_run=False,
                )
                review_file = extract_reported_path(
                    review_output,
                    "Claude-Review erfolgreich, strukturiert und read-only: ",
                    repo_root,
                )
                validate_step = Step(
                    "validate",
                    "Review validieren",
                    repo_root / "scripts" / "ai" / SCRIPT_NAMES["validate"],
                    (str(review_file.relative_to(repo_root)), *split_arguments(args.validate_args)),
                )
                run_step(
                    validate_step,
                    repo_root=repo_root,
                    log_dir=log_dir,
                    dry_run=False,
                )
        else:
            for step in steps:
                run_step(
                    step,
                    repo_root=repo_root,
                    log_dir=log_dir,
                    dry_run=args.dry_run,
                )

        summary = {
            "finishedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
            "status": "success",
            "gitStatusAfter": git_status(repo_root),
        }
        (log_dir / "result.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        print("\nWorkflow erfolgreich abgeschlossen.")
        return 0

    except WorkflowError as error:
        print(f"\nFEHLER: {error}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nAbbruch durch Benutzer.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())

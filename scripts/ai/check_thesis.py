#!/usr/bin/env python3
"""Baut und prüft die konfigurierte LaTeX-Arbeit."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional


def find_repository(start: Optional[Path] = None) -> Path:
    candidates = [start or Path.cwd(), Path(__file__).resolve().parent]
    for candidate in candidates:
        for path in (candidate.resolve(), *candidate.resolve().parents):
            if (path / ".git").exists() and (path / ".ai" / "config.json").is_file():
                return path
    raise RuntimeError("Repository-Wurzel mit .git und .ai/config.json wurde nicht gefunden.")


def load_config(repo: Path) -> dict[str, Any]:
    path = repo / ".ai" / "config.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Konfiguration {path} kann nicht gelesen werden: {exc}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(".ai/config.json muss ein JSON-Objekt enthalten.")
    return value


def validate_command(value: Any, location: str) -> list[str]:
    if not isinstance(value, list) or not value or not all(
        isinstance(item, str) and item for item in value
    ):
        raise RuntimeError(f"{location} muss eine nicht leere Argumentliste sein.")
    return value


def run_command(command: list[str], repo: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=repo,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=False,
        check=False,
    )


def strip_latex_comment(line: str) -> str:
    for index, char in enumerate(line):
        if char == "%":
            backslashes = 0
            cursor = index - 1
            while cursor >= 0 and line[cursor] == "\\":
                backslashes += 1
                cursor -= 1
            if backslashes % 2 == 0:
                return line[:index]
    return line


def duplicate_labels(repo: Path) -> dict[str, list[str]]:
    labels: dict[str, list[str]] = {}
    excluded = {".git", "build", ".ai"}
    for path in repo.rglob("*.tex"):
        if any(part in excluded for part in path.relative_to(repo).parts):
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for number, line in enumerate(lines, 1):
            for label in re.findall(r"\\label\{([^{}]+)\}", strip_latex_comment(line)):
                labels.setdefault(label, []).append(f"{path.relative_to(repo).as_posix()}:{number}")
    return {label: places for label, places in labels.items() if len(places) > 1}


def inspect_log(path: Path) -> list[str]:
    if not path.is_file():
        return [f"Build-Protokoll fehlt: {path}"]
    text = path.read_text(encoding="utf-8", errors="replace")
    checks = [
        (r"There were undefined references|Reference .+ undefined", "Nicht aufgelöste Referenzen"),
        (r"Citation .+ undefined|There were undefined citations", "Nicht aufgelöste Zitate"),
        (r"multiply defined", "Mehrfach definierte LaTeX-Ziele"),
        (r"Please \(re\)run Biber|Empty bibliography", "Nicht aufgelöste Bibliografie"),
        (r"Package (?:babel|polyglossia) Error", "Problem der Sprachkonfiguration"),
        (r"^! (?:LaTeX|Package).+Error", "Schwerer LaTeX-Fehler im Protokoll"),
    ]
    return [message for pattern, message in checks if re.search(pattern, text, re.MULTILINE)]


def main() -> int:
    try:
        repo = find_repository()
        config = load_config(repo)
        main_path = config.get("thesisMain")
        if not isinstance(main_path, str) or not main_path:
            raise RuntimeError(
                "Kein LaTeX-Einstiegspunkt konfiguriert. thesisMain in .ai/config.json setzen."
            )
        if not (repo / main_path).is_file():
            raise RuntimeError(
                f"Konfigurierter LaTeX-Einstiegspunkt fehlt: {main_path}. "
                "Den tatsächlichen Pfad in .ai/config.json eintragen; keine Scheindatei anlegen."
            )

        build = config.get("build")
        if not isinstance(build, dict):
            raise RuntimeError("build in .ai/config.json muss ein Objekt sein.")
        build_command = validate_command(build.get("command"), "build.command")
        if shutil.which(build_command[0]) is None:
            raise RuntimeError(f"Erforderliches Build-Werkzeug fehlt: {build_command[0]}")

        print(f"Repository: {repo}")
        print(f"Build: {' '.join(build_command)}")
        build_result = run_command(build_command, repo)
        if build_result.returncode != 0:
            print(build_result.stdout, file=sys.stderr)
            print(f"FEHLER: Thesis-Build fehlgeschlagen ({build_result.returncode}).", file=sys.stderr)
            return 1
        print("Build erfolgreich.")

        required_failures = 0
        lint_commands = config.get("lintCommands", [])
        if not isinstance(lint_commands, list):
            raise RuntimeError("lintCommands muss ein Array sein.")
        for index, lint in enumerate(lint_commands):
            if not isinstance(lint, dict):
                raise RuntimeError(f"lintCommands[{index}] muss ein Objekt sein.")
            command = validate_command(lint.get("command"), f"lintCommands[{index}].command")
            name = lint.get("name", command[0])
            required = lint.get("required") is True
            if shutil.which(command[0]) is None:
                label = "erforderlich" if required else "optional"
                print(f"Lint übersprungen ({label}, Werkzeug fehlt): {name} [{command[0]}]")
                required_failures += int(required)
                continue
            result = run_command(command, repo)
            if result.returncode == 0:
                if result.stdout.strip():
                    print(f"Lint abgeschlossen, {name} meldet Hinweise:")
                    lines = result.stdout.strip().splitlines()
                    preview = lines[:20]
                    print("\n".join(preview))
                    if len(lines) > len(preview):
                        print(f"… {len(lines) - len(preview)} weitere Zeilen")
                else:
                    print(f"Lint erfolgreich: {name}")
            else:
                label = "FEHLER" if required else "Hinweis"
                print(f"{label}: {name} meldet Befunde (Exit-Code {result.returncode}).")
                if result.stdout.strip():
                    lines = result.stdout.strip().splitlines()
                    preview = lines[:20]
                    print("\n".join(preview))
                    if len(lines) > len(preview):
                        print(f"… {len(lines) - len(preview)} weitere Zeilen")
                required_failures += int(required)

        log_file = build.get("logFile")
        log_findings = inspect_log(repo / log_file) if isinstance(log_file, str) else []
        duplicates = duplicate_labels(repo)
        if log_findings:
            print("LaTeX-Protokollhinweise: " + "; ".join(log_findings))
        else:
            print("Keine konfigurierten kritischen Referenz-, Zitat- oder Sprachwarnungen erkannt.")
        if duplicates:
            for label, locations in duplicates.items():
                print(f"Hinweis: Label '{label}' ist mehrfach definiert: {', '.join(locations)}")
        else:
            print("Keine doppelten Labels im kanonischen LaTeX-Quellbestand erkannt.")

        if required_failures:
            print(f"FEHLER: {required_failures} erforderliche Prüfung(en) fehlgeschlagen.", file=sys.stderr)
            return 1
        print("Qualitätsprüfung abgeschlossen; optionale Lint-Befunde sind nicht automatisch fatal.")
        return 0
    except RuntimeError as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

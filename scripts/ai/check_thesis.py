#!/usr/bin/env python3
"""Baut und prüft die konfigurierte LaTeX-Arbeit."""

from __future__ import annotations

import argparse
import collections
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional


CHKTEX_PATTERN = re.compile(r"^Warning ([0-9]+) in (.+) line ([0-9]+): (.+)$")
LACHECK_PATTERN = re.compile(r'^"(.+)", line ([0-9]+): (.+)$')
OVERFULL_PATTERN = re.compile(
    r"Overfull \\([hv])box \(([0-9]+(?:\.[0-9]+)?)pt too (?:wide|high)\)"
    r"(?: in paragraph at lines? ([0-9]+(?:--[0-9]+)?))?"
)


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


def git_paths(repo: Path, arguments: list[str]) -> list[str]:
    result = subprocess.run(
        ["git", *arguments],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "Git-Befehl fehlgeschlagen: " + result.stderr.decode("utf-8", "replace").strip()
        )
    return [part.decode("utf-8", "surrogateescape") for part in result.stdout.split(b"\0") if part]


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


def inspect_log(path: Path, overfull_threshold_pt: float) -> list[str]:
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
    findings = [message for pattern, message in checks if re.search(pattern, text, re.MULTILINE)]
    for match in OVERFULL_PATTERN.finditer(text):
        dimension = float(match.group(2))
        if dimension <= overfull_threshold_pt:
            continue
        box_type = "hbox" if match.group(1) == "h" else "vbox"
        location = f", Zeile(n) {match.group(3)}" if match.group(3) else ""
        findings.append(
            f"Overfull \\{box_type}: {dimension:.3f} pt über Schwellwert "
            f"{overfull_threshold_pt:.3f} pt{location}"
        )
    return findings


def parse_lint_findings(tool: str, output: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    lower = tool.lower()
    for line in output.splitlines():
        match = CHKTEX_PATTERN.match(line) if "chktex" in lower else None
        if match:
            findings.append(
                {
                    "tool": tool,
                    "path": match.group(2).replace("\\", "/"),
                    "line": int(match.group(3)),
                    "code": match.group(1),
                    "message": match.group(4).strip(),
                }
            )
            continue
        match = LACHECK_PATTERN.match(line) if "lacheck" in lower else None
        if match:
            findings.append(
                {
                    "tool": tool,
                    "path": match.group(1).replace("\\", "/"),
                    "line": int(match.group(2)),
                    "code": "lacheck",
                    "message": match.group(3).strip(),
                }
            )
    return findings


def lint_key(item: dict[str, Any]) -> tuple[str, str, int, str, str]:
    return (
        str(item.get("tool")),
        str(item.get("path")),
        int(item.get("line", 0)),
        str(item.get("code")),
        str(item.get("message")),
    )


def load_lint_baseline(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        print(f"Hinweis: Lint-Baseline fehlt: {path}")
        return []
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Lint-Baseline kann nicht gelesen werden: {exc}") from exc
    if not isinstance(value, dict) or value.get("version") != "1.0":
        raise RuntimeError("Lint-Baseline benötigt version '1.0'.")
    entries = value.get("entries")
    if not isinstance(entries, list) or not all(isinstance(item, dict) for item in entries):
        raise RuntimeError("Lint-Baseline.entries muss ein Array von Objekten sein.")
    return entries


def changed_latex_files(repo: Path, base: str) -> list[str]:
    changed = git_paths(repo, ["diff", "--name-only", "-z", base, "--", "*.tex"])
    untracked = git_paths(repo, ["ls-files", "--others", "--exclude-standard", "-z", "--", "*.tex"])
    return sorted(
        path
        for path in set(changed + untracked)
        if (repo / path).is_file() and not path.startswith(("build/", ".ai/reviews/"))
    )


def command_for_file(command: list[str], main_path: str, file_path: str) -> list[str]:
    if main_path in command:
        return [file_path if argument == main_path else argument for argument in command]
    return [*command, file_path]


def print_preview(output: str, limit: int, full: bool) -> None:
    lines = output.strip().splitlines()
    shown = lines if full else lines[:limit]
    if shown:
        print("\n".join(shown))
    if not full and len(lines) > len(shown):
        print(f"… {len(lines) - len(shown)} weitere Zeilen")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Baut die Masterarbeit und prüft LaTeX-Protokoll, Labels und Lint-Baseline."
    )
    parser.add_argument("--base", help="Git-Basis für die Ermittlung geänderter LaTeX-Dateien")
    parser.add_argument(
        "--full-lint-output",
        action="store_true",
        help="Gibt auch für den Gesamtlauf sämtliche Linterzeilen aus.",
    )
    parser.add_argument(
        "--overfull-threshold-pt",
        type=float,
        help="Meldet Overfull-Boxen oberhalb dieses Werts in pt.",
    )
    args = parser.parse_args(argv)
    if args.overfull_threshold_pt is not None and args.overfull_threshold_pt < 0:
        parser.error("--overfull-threshold-pt darf nicht negativ sein")

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

        quality = config.get("quality", {})
        if not isinstance(quality, dict):
            raise RuntimeError("quality in .ai/config.json muss ein Objekt sein.")
        threshold = args.overfull_threshold_pt
        if threshold is None:
            configured = quality.get("overfullThresholdPt", 0.0)
            if type(configured) not in {int, float} or configured < 0:
                raise RuntimeError("quality.overfullThresholdPt muss eine nicht negative Zahl sein.")
            threshold = float(configured)
        preview_lines = quality.get("lintPreviewLines", 20)
        if type(preview_lines) is not int or preview_lines < 1:
            raise RuntimeError("quality.lintPreviewLines muss eine positive ganze Zahl sein.")
        baseline_relative = quality.get("lintBaseline")
        if not isinstance(baseline_relative, str) or not baseline_relative:
            raise RuntimeError("quality.lintBaseline ist nicht konfiguriert.")
        baseline = load_lint_baseline(repo / baseline_relative)

        base = args.base or config.get("defaultBaseRef")
        if not isinstance(base, str) or not base:
            raise RuntimeError("Keine Git-Basis für die Lint-Differenzierung konfiguriert.")
        changed_files = changed_latex_files(repo, base)

        build = config.get("build")
        if not isinstance(build, dict):
            raise RuntimeError("build in .ai/config.json muss ein Objekt sein.")
        build_command = validate_command(build.get("command"), "build.command")
        if shutil.which(build_command[0]) is None:
            raise RuntimeError(f"Erforderliches Build-Werkzeug fehlt: {build_command[0]}")

        print(f"Repository: {repo}")
        print(f"Build: {' '.join(build_command)}")
        print(f"Geänderte LaTeX-Dateien gegen {base}: {len(changed_files)}")
        build_result = run_command(build_command, repo)
        if build_result.returncode != 0:
            print(build_result.stdout, file=sys.stderr)
            print(f"FEHLER: Thesis-Build fehlgeschlagen ({build_result.returncode}).", file=sys.stderr)
            return 1
        print("Build erfolgreich.")

        required_failures = 0
        current_findings: list[dict[str, Any]] = []
        lint_commands = config.get("lintCommands", [])
        if not isinstance(lint_commands, list):
            raise RuntimeError("lintCommands muss ein Array sein.")
        for index, lint in enumerate(lint_commands):
            if not isinstance(lint, dict):
                raise RuntimeError(f"lintCommands[{index}] muss ein Objekt sein.")
            command = validate_command(lint.get("command"), f"lintCommands[{index}].command")
            name = lint.get("name", command[0])
            if not isinstance(name, str):
                raise RuntimeError(f"lintCommands[{index}].name muss eine Zeichenkette sein.")
            required = lint.get("required") is True
            if shutil.which(command[0]) is None:
                label = "erforderlich" if required else "optional"
                print(f"Lint übersprungen ({label}, Werkzeug fehlt): {name} [{command[0]}]")
                required_failures += int(required)
                continue
            result = run_command(command, repo)
            current_findings.extend(parse_lint_findings(name, result.stdout))
            if result.returncode == 0 and not result.stdout.strip():
                print(f"Lint erfolgreich: {name}")
            else:
                label = "FEHLER" if required and result.returncode != 0 else "Hinweis"
                print(f"{label}: {name} meldet Befunde (Exit-Code {result.returncode}).")
                print_preview(result.stdout, preview_lines, args.full_lint_output)
                required_failures += int(required and result.returncode != 0)

            for file_path in changed_files:
                focused = run_command(command_for_file(command, main_path, file_path), repo)
                print(f"Geänderte Datei, vollständige {name}-Ausgabe: {file_path}")
                if focused.stdout.strip():
                    print(focused.stdout.rstrip())
                else:
                    print("Keine Befunde.")

        baseline_counter = collections.Counter(lint_key(item) for item in baseline)
        current_counter = collections.Counter(lint_key(item) for item in current_findings)
        new_counter = current_counter - baseline_counter
        resolved_counter = baseline_counter - current_counter
        print(
            f"Lint-Baseline: {sum(new_counter.values())} neue, "
            f"{sum(resolved_counter.values())} behobene Befunde."
        )
        for key, count in sorted(new_counter.items()):
            tool, path, line, code, message = key
            suffix = f" ({count}×)" if count > 1 else ""
            print(f"NEU: {tool} {path}:{line} [{code}] {message}{suffix}")

        log_file = build.get("logFile")
        log_findings = (
            inspect_log(repo / log_file, threshold) if isinstance(log_file, str) else []
        )
        duplicates = duplicate_labels(repo)
        if log_findings:
            print("LaTeX-Protokollbefunde:")
            for finding in log_findings:
                print(f"  - {finding}")
        else:
            print("Keine konfigurierten kritischen Referenz-, Zitat-, Sprach- oder Overfull-Befunde erkannt.")
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

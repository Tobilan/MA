# Plattformunabhängiger AI-Workflow

Das plattformunabhängige Python-Skript führt die vorhandenen Workflow-Skripte aus und beendet den Ablauf sofort, falls ein Schritt fehlschlägt.

## Skript

`run_ai_workflow.py`

Lege das Skript im Masterarbeits-Repository unter folgendem Pfad ab:

```text
scripts/ai/run_ai_workflow.py
```

## Kompletter Ablauf vor dem Review

```bash
python scripts/ai/run_ai_workflow.py pre-review
```

Dabei werden nacheinander folgende Skripte ausgeführt:

1. `check_thesis.py`
2. `prepare_review.py`
3. `run_claude_review.py`
4. `validate_review.py`

## Ablauf nach den durch Codex übernommenen Review-Änderungen

```bash
python scripts/ai/run_ai_workflow.py post-review
```

## Einzelne Schritte

```bash
python scripts/ai/run_ai_workflow.py check
python scripts/ai/run_ai_workflow.py prepare
python scripts/ai/run_ai_workflow.py review
python scripts/ai/run_ai_workflow.py validate
```

## Argumente an ein Einzelskript weiterreichen

Argumente können mit `--` an ein einzelnes Skript weitergereicht werden:

```bash
python scripts/ai/run_ai_workflow.py prepare -- \
  --base main \
  --task .ai/tasks/kapitel-04-01.md
```

## Argumente für den vollständigen Ablauf

```bash
python scripts/ai/run_ai_workflow.py pre-review \
  --prepare-args "--base main --task .ai/tasks/kapitel-04-01.md" \
  --review-args "--package .ai/reviews/kapitel-04-01" \
  --validate-args ".ai/reviews/kapitel-04-01/review.json"
```

## Protokolle

Das Skript erzeugt für jeden Lauf Protokolle unter:

```text
.ai/workflow-logs/
```

Diesen Pfad solltest du in `.gitignore` aufnehmen:

```gitignore
.ai/workflow-logs/
```

## Prüfung

Die Python-Syntax und die Kommandozeilenhilfe des Skripts wurden erfolgreich geprüft.

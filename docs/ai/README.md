# Codex–Claude-Workflow für die Masterarbeit

Dieses Verzeichnis bündelt die verbindlichen fachlichen, sprachlichen und technischen Regeln für KI-gestützte Änderungen. Codex ist alleiniger Autor und Integrator der kanonischen Thesis-Dateien. Claude prüft ein erzeugtes Paket unabhängig und read-only. Kein Finding wird automatisch angewendet; Codex verifiziert und dokumentiert jede Entscheidung, bevor angenommene Änderungen umgesetzt werden. Die abschließende Freigabe vor dem Merge bleibt beim Menschen.

## Schnellstart

1. Vor jeder Schreibarbeit den vollständigen Preflight einschließlich Claude-Anmeldung und strukturiertem Schema-Smoke-Test ausführen:

   ```powershell
   py -3 scripts/ai/preflight.py
   ```

2. `.ai/tasks/TASK_TEMPLATE.md` kopieren und konkret ausfüllen.
3. Codex eine zusammenhängende Änderung bearbeiten lassen.
4. Qualität prüfen:

   ```powershell
   python scripts/ai/check_thesis.py
   ```

5. Review-Paket erzeugen:

   ```powershell
   python scripts/ai/prepare_review.py --task .ai/tasks/<aufgabe>.md
   ```

   Neue, noch unversionierte Thesis- oder Implementierungsdateien müssen aus Sicherheitsgründen ausdrücklich mit `--include <repository-relativer-pfad>` benannt werden.

   Externe Implementierungsevidenz wird nicht als beliebiger Dateibaum kopiert, sondern über ein validiertes Manifest eingebunden:

   ```powershell
   py -3 scripts/ai/prepare_review.py --task .ai/tasks/<aufgabe>.md --external-evidence <manifest.json>
   ```

6. Claude read-only ausführen. Jeder Lauf erhält ein eigenes `attempt-NN/`-Verzeichnis:

   ```powershell
   python scripts/ai/run_claude_review.py --package .ai/reviews/<paket>
   ```

   Modell und Effort-Level werden verbindlich unter `claude.model` und
   `claude.effort` in `.ai/config.json` festgelegt und im Ausführungsprotokoll
   des Attempts dokumentiert.

7. Das im `successful-attempt.json` markierte Review validieren:

   ```powershell
   python scripts/ai/validate_review.py .ai/reviews/<paket>/attempt-<nn>/review.json
   ```

8. Entscheidungen vollständig validieren:

   ```powershell
   python scripts/ai/validate_decisions.py .ai/reviews/<paket>/attempt-<nn>/review.json .ai/decisions/<entscheidungen>.json
   ```

   Der Validator akzeptiert ausschließlich den in `successful-attempt.json` markierten Lauf des Pakets.

Auf Windows kann bei einer regulären Python-Installation statt `python` der Launcher `py -3` verwendet werden. Nach einer Installation oder `PATH`-Änderung müssen bereits laufende Terminals und Agentenprozesse gegebenenfalls neu gestartet werden.

Die vollständige Reihenfolge, erwartete Artefakte und Fehlerfälle stehen in `REVIEW_WORKFLOW.md`. Die Schema-Transformation erklärt `SCHEMA_COMPATIBILITY.md`. Die fachlichen Grenzen definiert `THESIS_CONTRACT.md`; Schreibstil, Terminologie und Nachweise werden in `GERMAN_WRITING_GUIDE.md`, `TERMINOLOGY.md` und `CLAIM_POLICY.md` geregelt.

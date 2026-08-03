# Codex–Claude-Workflow für die Masterarbeit

Dieses Verzeichnis bündelt die verbindlichen fachlichen, sprachlichen und technischen Regeln für KI-gestützte Änderungen. Codex ist alleiniger Autor und Integrator der kanonischen Thesis-Dateien. Claude prüft ein erzeugtes Paket unabhängig und read-only. Kein Finding wird automatisch angewendet; Codex verifiziert und dokumentiert jede Entscheidung, bevor angenommene Änderungen umgesetzt werden. Die abschließende Freigabe vor dem Merge bleibt beim Menschen.

## Schnellstart

1. `.ai/tasks/TASK_TEMPLATE.md` kopieren und konkret ausfüllen.
2. Codex eine zusammenhängende Änderung bearbeiten lassen.
3. Qualität prüfen:

   ```powershell
   python scripts/ai/check_thesis.py
   ```

4. Review-Paket erzeugen:

   ```powershell
   python scripts/ai/prepare_review.py --task .ai/tasks/<aufgabe>.md
   ```

   Neue, noch unversionierte Thesis- oder Implementierungsdateien müssen aus Sicherheitsgründen ausdrücklich mit `--include <repository-relativer-pfad>` benannt werden.

5. Claude read-only ausführen und das normalisierte Review erzeugen:

   ```powershell
   python scripts/ai/run_claude_review.py --package .ai/reviews/<paket>
   ```

6. Review bei Bedarf erneut validieren:

   ```powershell
   python scripts/ai/validate_review.py .ai/reviews/<paket>/review.json
   ```

Auf Windows kann bei einer regulären Python-Installation statt `python` der Launcher `py -3` verwendet werden. Nach einer Installation oder `PATH`-Änderung müssen bereits laufende Terminals und Agentenprozesse gegebenenfalls neu gestartet werden.

Die vollständige Reihenfolge, erwartete Artefakte und Fehlerfälle stehen in `REVIEW_WORKFLOW.md`. Die fachlichen Grenzen definiert `THESIS_CONTRACT.md`; Schreibstil, Terminologie und Nachweise werden in `GERMAN_WRITING_GUIDE.md`, `TERMINOLOGY.md` und `CLAIM_POLICY.md` geregelt.

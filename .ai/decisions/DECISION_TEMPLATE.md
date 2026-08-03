# Review-Entscheidungen: <Aufgabenname>

Dateiname: `.ai/decisions/YYYY-MM-DD-<task-name>-review-decisions.md`. Zusätzlich ist die gleichnamige maschinenlesbare `.json`-Akte aus `DECISION_TEMPLATE.json` anzulegen. Die JSON-Datei ist für die Vollständigkeitsprüfung maßgeblich; diese Markdown-Datei kann ergänzende Erläuterungen enthalten.

Für jedes Claude-Finding ist ein eigener Abschnitt anzulegen. Zulässige maschinenlesbare Statuswerte sind ausschließlich `ACCEPTED`, `REJECTED` und `DEFERRED`.

Prüfung der JSON-Akte:

```powershell
python scripts/ai/validate_decisions.py .ai/reviews/<paket>/attempt-<nn>/review.json .ai/decisions/<datei>.json
```

## <Finding-ID>

- **Status:** `<ACCEPTED | REJECTED | DEFERRED>`
- **Deutsche Bezeichnung:** `<angenommen | abgelehnt | zurückgestellt>`
- **Aussage des Reviewers:** <deutsche Wiedergabe des Findings>
- **Verifikation durch Codex:** <durchgeführte unabhängige Prüfung>
- **Geprüfte Nachweise:** <Quellen, Pfade, Commits, Tests oder ADRs>
- **Begründung:** <deutsche Begründung der Entscheidung>
- **Resultierende Maßnahme:** <konkrete Änderung oder keine Änderung>
- **Betroffene Dateien:** `<repository-relative Pfade>`
- **Prüfkommando:** `<reproduzierbarer Befehl>`
- **Verbleibendes Risiko:** <Restrisiko oder „keines bekannt“>

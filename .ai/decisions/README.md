# Review-Entscheidungen

Entscheidungsprotokolle werden als zusammengehörige Dateien nach dem Muster `YYYY-MM-DD-<task-name>-review-decisions.json` und optional `.md` benannt und versioniert. Die JSON-Akte ist maschinenlesbar und wird mit `scripts/ai/validate_decisions.py` gegen das Review geprüft. Für jedes Finding ist genau einer der Statuswerte `ACCEPTED`, `REJECTED` oder `DEFERRED` mit passender deutscher Bezeichnung und Begründung festzuhalten. Als Ausgangspunkte dienen `DECISION_TEMPLATE.json` und `DECISION_TEMPLATE.md`.

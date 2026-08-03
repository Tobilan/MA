# Generierte Review-Pakete

`prepare_review.py` legt hier aufgabenspezifische Review-Pakete ab. Paketmetadaten identifizieren HEAD, Arbeitsbaumanteil, Diff sowie die einschließlich eingefrorenem Schema und Prompt vollständigen Review-Eingaben über SHA-256-Hashes. Jeder Aufruf von `run_claude_review.py` erzeugt ein eigenes `attempt-NN/`; nur ein vollständig gültiger Lauf wird durch `successful-attempt.json` markiert und vom Entscheidungsvalidator akzeptiert.

Die Pakete, Diffs, externen Evidenzmetadaten, Rohantworten, normalisierten JSON-Dateien und Ausführungsprotokolle sind flüchtige Artefakte und werden durch die lokale `.gitignore` ausgeschlossen. Diese README und `.gitignore` bleiben versioniert. Fehlgeschlagene Attempts werden zur Diagnose nicht überschrieben oder automatisch gelöscht.

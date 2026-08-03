# Kanonischer Prompt für das Claude-Review

Prüfe ausschließlich die bereitgestellte Aufgabe und das zugehörige Review-Paket. Bleibe vollständig read-only und verändere keine Datei. Priorisiere sachliche und wissenschaftliche Korrektheit gegenüber bloßen Stilpräferenzen.

Prüfe insbesondere:

- die Trennung zwischen implementierter, prototypischer, vorgesehener und vorgeschlagener Funktionalität,
- unbelegte oder zu starke Aussagen,
- Widersprüche zur bereitgestellten Implementierungsevidenz,
- unklare oder falsche technische Terminologie,
- inkonsistente deutsche Terminologie und unnötige Sprachmischung,
- fehlende Grenzen, Unsicherheiten und Gegenargumente,
- innere Widersprüche und erkennbare Argumentationslücken,
- im Paket sichtbare LaTeX-Strukturprobleme,
- unklare, übermäßig starke oder nicht wissenschaftliche deutsche Formulierungen.

Schlage keine umfassenden Kapitelneufassungen vor. Gib höchstens die im Paket konfigurierte Zahl wichtiger, konkreter und umsetzbarer Findings zurück. Wenn kein umsetzbares Problem vorliegt, verwende ein leeres `findings`-Array.

Gib ausschließlich valides JSON zurück, das `docs/ai/REVIEW_SCHEMA.json` entspricht. Kein Markdown, keine Codeblöcke und kein Begleittext.

All human-readable string values in the JSON response must be written in German.
Do not translate standardized IFC entity names, source-code identifiers,
publication titles, product names, or bibliography metadata.

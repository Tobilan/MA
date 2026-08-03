# Aufgabe: Review-Workflow nach erstem Testlauf härten

## Ziel

Die im ersten vollständigen Testlauf erkannten Schwachstellen des Codex–Claude-Workflows beheben, ohne die bestehenden Sicherheitsgrenzen für explizite Paketauswahl, Read-only-Reviews, strikte JSON-Validierung und unabhängige Finding-Entscheidungen abzuschwächen.

## Umfang

- früher Preflight für Python, Git, LaTeX, Claude-Version, Anmeldung, `plan`-Modus und strukturierte Ausgabe;
- verlustarme Laufzeittransformation des kanonischen Draft-2020-12-Review-Schemas;
- unveränderliche Artefakte je Claude-Versuch und eindeutige Paket-/Diff-Metadaten;
- kontrollierte Metadaten für externe Implementierungsevidenz;
- echtes `--help`, Overfull-Erkennung und differenzierte LaTeX-Lint-Befunde;
- maschinenlesbare und vollständig validierte Finding-Entscheidungen;
- dokumentierter Review-Modus für bewusst unversionierte Änderungen;
- genau ein unabhängig entscheidbares Problem je Claude-Finding.

## Nichtziele

- keine Änderung am wissenschaftlichen Fließtext;
- keine automatische Übernahme von Claude-Findings;
- kein unstrukturierter Claude-Fallback;
- kein Push oder Merge.

## Commit-Modus

`no_commit` für diesen Arbeitslauf; die Änderungen werden mit einer vorgeschlagenen Commit-Nachricht zur menschlichen Prüfung übergeben.

## Abnahmekriterien

- `py -3 scripts/ai/preflight.py` erkennt fehlende oder inkompatible Voraussetzungen vor der Schreibarbeit.
- Das kanonische Review-Schema bleibt unverändert maßgeblich; das CLI-Schema wird reproduzierbar erzeugt und protokolliert.
- Fehlgeschlagene und erfolgreiche Versuche überschreiben einander nicht.
- Pakethashes identifizieren Diff, Arbeitsbaumanteil und Review-Eingaben.
- Externe Evidenz wird nur über validierte, commitgebundene Metadaten aufgenommen.
- Quality Gate und Entscheidungsvalidator bestehen ihre Positiv- und Negativtests.

## Review-Fokus

Prüfe besonders auf Umgehungen der Read-only-Grenze, abgeschwächte Schemaanforderungen, instabile Hashberechnung, unvollständige Finding-Zuordnung und Plattformprobleme unter Windows. Formuliere genau ein Finding pro unabhängig entscheidbarem Problem.

# Kontrollierter Review-Workflow

## Rollen und Freigaben

```text
Der Mensch definiert die Aufgabe und erteilt die abschließende Freigabe
                              |
                              v
Codex bearbeitet die kanonischen LaTeX-Dateien
                              |
                              v
Codex kompiliert und prüft die Masterarbeit
                              |
                              v
Codex erzeugt ein Review-Paket
                              |
                              v
Claude führt ein unabhängiges Read-only-Review durch
                              |
                              v
Claude liefert strukturierte Findings auf Deutsch
                              |
                              v
Codex verifiziert und entscheidet jedes Finding
                              |
                              v
Codex setzt ausschließlich angenommene Änderungen um und prüft erneut
                              |
                              v
Der Mensch prüft das Ergebnis vor dem Merge
```

## Verbindliche Durchführung

1. Aus `.ai/tasks/TASK_TEMPLATE.md` eine konkrete Aufgabendatei erstellen und möglichst vor der Bearbeitung versionieren.
2. Codex genau eine zusammenhängende Änderung innerhalb des erklärten Umfangs durchführen lassen.
3. Aus dem Repository heraus die Qualitätsprüfung ausführen: `python scripts/ai/check_thesis.py`.
4. Das Paket mit `python scripts/ai/prepare_review.py --task .ai/tasks/<aufgabe>.md` erzeugen. Eine abweichende Basis wird mit `--base <ref>` angegeben. Neue unversionierte Dateien werden nie automatisch aufgenommen und müssen mit wiederholtem `--include <pfad>` ausdrücklich benannt werden; `--include-implementation` ergänzt für versionierte Änderungen die konfigurierten Implementierungspfade.
5. Den ausgegebenen Paketpfad mit `python scripts/ai/run_claude_review.py --package <paketpfad>` prüfen lassen. Der Runner verlangt eine von `claude --help` bestätigte nicht interaktive Ausgabe und den Berechtigungsmodus `plan`. Unterstützt die lokale CLI dies, deaktiviert er zusätzlich sämtliche Werkzeuge und Sitzungspersistenz und übergibt das JSON-Schema direkt an die CLI.
6. Das normalisierte Ergebnis mit `python scripts/ai/validate_review.py <paketpfad>/review.json` validieren.
7. Codex jedes Finding unabhängig anhand von Code, Quellen, Standards, Tests oder ADRs prüfen lassen.
8. Aus `.ai/decisions/DECISION_TEMPLATE.md` ein versioniertes Entscheidungsprotokoll erstellen und jedes Finding als `ACCEPTED`, `REJECTED` oder `DEFERRED` entscheiden.
9. Nur `ACCEPTED`-Findings umsetzen. Zurückgestellte Findings bleiben als Risiko oder Folgeaufgabe sichtbar.
10. `python scripts/ai/check_thesis.py` erneut ausführen.
11. `git diff --check`, `git status` und den vollständigen Diff prüfen; generierte Pakete bleiben ignoriert.
12. Genau einen zusammenhängenden Commit erstellen.
13. Pull Request mit `.github/pull_request_template.md` öffnen; weder Skripte noch Agenten pushen oder mergen automatisch.
14. Vor dem Merge menschliche Freigabe einholen und technisch über Branch Protection oder ein Ruleset absichern.

## Inhalt eines Review-Pakets

Ein Paket enthält `metadata.json`, `changes.diff`, `changed-files.json`, `task.md`, eine Kopie der Review-Konfiguration und optional `claim-inventory.*`. Der Runner ergänzt `claude-raw.txt`, `review.json`, `execution-metadata.json` und gegebenenfalls `claude-stderr.txt`. Es werden nur der Git-Diff gegen die geprüfte Basis, explizit relevante neue Dateien und die angegebene Aufgabe aufgenommen. Umgebungsvariablen, `.env`-Dateien, private Schlüssel und beliebige andere unversionierte Dateien werden nicht eingelesen. Zusätzlich bricht die Paketerzeugung bei verbreiteten Zugangsdaten- und Schlüsselmustern ab; diese Heuristik ersetzt keine menschliche Geheimnisprüfung.

## Beispiel eines gültigen Reviews

```json
{
  "schemaVersion": "1.0",
  "reviewer": "claude",
  "language": "de",
  "reviewedCommit": "622fd27",
  "baseRef": "origin/main",
  "verdict": "changes_requested",
  "summary": "Eine Implementierungsbehauptung ist im bereitgestellten Nachweis nicht belegt.",
  "findings": [
    {
      "id": "CL-001",
      "severity": "major",
      "category": "implementation_mismatch",
      "file": "inhalt/systementwurf.tex",
      "lineStart": 84,
      "lineEnd": 86,
      "statement": "Der Export erhalte sämtliche IFC-Beziehungen unverändert.",
      "problem": "Der bereitgestellte Diff zeigt nur die Verarbeitung ausgewählter Aufgabenzuordnungen; ein vollständiger Beziehungserhalt ist nicht nachgewiesen.",
      "evidence": "Im Review-Paket fehlt ein Test oder Implementierungspfad für den behaupteten vollständigen Erhalt.",
      "requiredAction": "Die Aussage auf den nachgewiesenen Umfang begrenzen oder einen reproduzierbaren Nachweis ergänzen.",
      "confidence": "high"
    }
  ]
}
```

## Fehlerfälle

- **Claude CLI fehlt:** Der Runner beendet sich ungleich null. CLI installieren, `claude --help` prüfen und erneut ausführen; kein Review vortäuschen.
- **LaTeX-Toolchain fehlt:** `check_thesis.py` nennt das fehlende erforderliche Programm und beendet sich ungleich null. TeX Live oder eine kompatible Toolchain installieren.
- **Ungültiges JSON:** Rohantwort bleibt erhalten; Validator nennt Feld und Fehler. Inhalt nicht manuell „wohlwollend“ übernehmen, sondern Review erneut ausführen.
- **Repository während des Reviews verändert:** Der Runner meldet alle erkannten Pfade und beendet sich ungleich null. Änderungen werden nicht zurückgesetzt; der Mensch prüft ihre Herkunft.
- **Unbekannte Git-Basisreferenz:** `prepare_review.py` bricht vor der Paketerzeugung ab. Referenz abrufen oder explizit eine vorhandene Basis angeben.
- **Kein LaTeX-Einstiegspunkt:** Qualitätsprüfung bricht mit Hinweis auf `.ai/config.json` ab. Erst den echten Einstiegspunkt konfigurieren; keine Scheinarbeit erzeugen.
- **Finding ohne ausreichenden Nachweis:** Codex setzt es nicht automatisch um. Je nach Prüfstand wird es begründet abgelehnt oder zurückgestellt.
- **Review nicht auf Deutsch:** Das Review gilt trotz formalem JSON nicht als freigegeben. Der Runner prüft `language: de`; die tatsächliche Sprache kontrolliert abschließend ein Mensch.
- **Widerspruch zwischen Terminologie und bestehendem Text:** Nicht massenhaft stillschweigend umschreiben. Geltende Konvention ermitteln, Entscheidung dokumentieren und gezielt migrieren.

## Sicherheitsgrenze des Read-only-Modus

Der Runner verwendet nur einen von der lokalen Hilfe bestätigten `plan`-Modus und deaktiviert, soweit unterstützt, sämtliche Claude-Werkzeuge und die Sitzungspersistenz. Er vergleicht vor und nach Claude sowohl den Git-Status als auch Inhaltsfingerabdrücke aller Dateien innerhalb des Repositorys, einschließlich ignorierter Build-Artefakte. Er verwirft nie Änderungen. Diese Kontrolle ist eine nachgelagerte Erkennung, keine Betriebssystem-Sandbox; ein separater temporärer Klon oder eine Plattform-Sandbox bietet stärkere Isolation. Änderungen außerhalb des Repositorys liegen außerhalb des Zustandsvergleichs.

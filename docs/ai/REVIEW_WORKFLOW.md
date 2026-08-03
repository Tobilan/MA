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

1. Vor jeder Textarbeit `py -3 scripts/ai/preflight.py` ausführen. Der Preflight prüft Python, Git, LaTeX, Claude-Version, Anmeldung, `plan`, deaktivierte Werkzeuge und das transformierte strukturierte Schema. Bei Fehlern wird nicht geschrieben.
2. Aus `.ai/tasks/TASK_TEMPLATE.md` eine konkrete Aufgabendatei erstellen und den Commit-Modus `commit` oder `no_commit` festlegen.
3. Codex genau eine zusammenhängende Änderung innerhalb des erklärten Umfangs durchführen lassen.
4. Aus dem Repository heraus die Qualitätsprüfung ausführen: `python scripts/ai/check_thesis.py`. Das Skript meldet Overfull-Boxen, differenziert Lint-Befunde gegen `LINT_BASELINE.json` und prüft geänderte LaTeX-Dateien zusätzlich mit vollständiger Ausgabe.
5. Das Paket mit `python scripts/ai/prepare_review.py --task .ai/tasks/<aufgabe>.md` erzeugen. Eine abweichende Basis wird mit `--base <ref>` angegeben. Neue unversionierte Dateien werden nie automatisch aufgenommen und müssen mit wiederholtem `--include <pfad>` ausdrücklich benannt werden; `--include-implementation` ergänzt für versionierte Änderungen die konfigurierten Implementierungspfade.
6. Liegt Implementierungsevidenz in einem anderen Repository, aus `.ai/tasks/EXTERNAL_EVIDENCE_TEMPLATE.json` ein Manifest erstellen und mit `--external-evidence <manifest.json>` übergeben. Aufgenommen werden nur HTTPS-Repository-URL, Commit, repository-relativer Pfad, optionaler Zeilenbereich, Beschreibung und Prüfmethode; externe Dateien werden nicht kopiert.
7. Den ausgegebenen Paketpfad mit `python scripts/ai/run_claude_review.py --package <paketpfad>` prüfen lassen. Der Runner akzeptiert nur die konfigurierte Mindestversion mit `--json-schema`, `plan`, deaktivierten Werkzeugen und deaktivierter Sitzungspersistenz. Es gibt keinen unstrukturierten Fallback.
8. Den in `successful-attempt.json` ausgewiesenen Lauf mit `python scripts/ai/validate_review.py <paketpfad>/attempt-<nn>/review.json` validieren.
9. Codex jedes Finding unabhängig anhand von Code, Quellen, Standards, Tests oder ADRs prüfen lassen.
10. Aus `.ai/decisions/DECISION_TEMPLATE.json` eine versionierte Entscheidungsakte erstellen und jedes Finding als `ACCEPTED`, `REJECTED` oder `DEFERRED` entscheiden. Mit `python scripts/ai/validate_decisions.py <review.json> <entscheidungen.json>` sicherstellen, dass jedes Finding genau einmal vorkommt.
11. Nur `ACCEPTED`-Findings umsetzen. Zurückgestellte Findings bleiben als Risiko oder Folgeaufgabe sichtbar.
12. `python scripts/ai/check_thesis.py` erneut ausführen.
13. `git diff --check`, `git status` und den vollständigen Diff prüfen; generierte Pakete bleiben ignoriert.
14. Im Modus `commit` genau einen zusammenhängenden Commit erstellen. Im durch den Menschen angeordneten Modus `no_commit` keine Commit-Aktion ausführen und den unversionierten Zustand im Abschlussbericht nennen.
15. Falls ein Commit vorgesehen ist, Pull Request mit `.github/pull_request_template.md` öffnen; weder Skripte noch Agenten pushen oder mergen automatisch.
16. Vor dem Merge menschliche Freigabe einholen und technisch über Branch Protection oder ein Ruleset absichern.

## Inhalt eines Review-Pakets

Ein Paket enthält `metadata.json`, `changes.diff`, `changed-files.json`, `task.md`, eine Kopie der Review-Konfiguration, das eingefrorene `review-schema.json`, den eingefrorenen `review-prompt.md` und optional `claim-inventory.*` sowie `external-evidence.json`. `metadata.json` identifiziert den geprüften Inhalt über `headCommit`, `workingTreeIncluded`, `diffHash`, `reviewSchemaHash`, `reviewPromptHash` und `packageHash`. Der Paket-Hash umfasst einschließlich Schema und Prompt sämtliche Review-Eingaben sowie die Metadaten ohne das zirkuläre Hashfeld. Der Runner liest Schema und Prompt ausschließlich aus dem geprüften Paket und protokolliert ihre tatsächlich verwendeten Hashes.

Jeder Runner-Aufruf erzeugt unveränderlich `attempt-01/`, `attempt-02/` usw. mit `claude-raw.txt`, `execution-metadata.json`, dem tatsächlich verwendeten `claude-cli-schema.json`, gegebenenfalls `claude-stderr.txt` und nur bei Erfolg `review.json`. Ein erfolgreicher Lauf wird im Paket durch `successful-attempt.json` markiert. Dadurch können fehlgeschlagene Versuche weder Rohantworten überschreiben noch veraltete Fehlerdateien neben erfolgreichen Metadaten hinterlassen. Der Entscheidungsvalidator bindet die Entscheidungsakte ausdrücklich an genau diesen markierten Lauf.

Es werden nur der Git-Diff gegen die geprüfte Basis, explizit relevante neue Dateien und die angegebene Aufgabe aufgenommen. Umgebungsvariablen, `.env`-Dateien, private Schlüssel und beliebige andere unversionierte Dateien werden nicht eingelesen. Zusätzlich bricht die Paketerzeugung bei verbreiteten Zugangsdaten- und Schlüsselmustern ab; diese Heuristik ersetzt keine menschliche Geheimnisprüfung.

## Pflege der Lint-Baseline

`docs/ai/LINT_BASELINE.json` enthält ausschließlich bereits geprüfte Befunde. Eine Baseline darf nur nach menschlicher Prüfung eines vollständigen Linterlaufs geändert werden. Neue Befunde werden nicht durch eine pauschale Neubaseline verborgen. Wenn sich Zeilennummern durch eine beabsichtigte Textänderung verschieben, sind als „behoben“ und „neu“ gemeldete Einträge einzeln abzugleichen. Der vollständige Einzellauf geänderter LaTeX-Dateien bleibt unabhängig von der Baseline sichtbar.

## Beispiel eines gültigen Reviews

```json
{
  "schemaVersion": "1.1",
  "reviewer": "claude",
  "language": "de",
  "reviewedCommit": "622fd27",
  "workingTreeIncluded": true,
  "diffHash": "1111111111111111111111111111111111111111111111111111111111111111",
  "packageHash": "2222222222222222222222222222222222222222222222222222222222222222",
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
- **Preflight fehlgeschlagen:** Keine Schreibarbeit beginnen. Fehlendes Werkzeug, Anmeldung, Mindestversion oder Schemaunterstützung anhand der deutschen Diagnose beheben.
- **Claude-Version zu alt oder `--json-schema` fehlt:** Runner und Preflight brechen ab. Markdown-Codeblöcke oder freie Textausgabe werden nicht als Fallback akzeptiert.
- **Kanonisches Schema nicht transformierbar:** Nicht unterstütztes Schlüsselwort bewusst im Transformationsmodul ergänzen und testen; das kanonische Schema nicht zur Umgehung abschwächen.
- **LaTeX-Toolchain fehlt:** `check_thesis.py` nennt das fehlende erforderliche Programm und beendet sich ungleich null. TeX Live oder eine kompatible Toolchain installieren.
- **Ungültiges JSON:** Rohantwort bleibt erhalten; Validator nennt Feld und Fehler. Inhalt nicht manuell „wohlwollend“ übernehmen, sondern Review erneut ausführen.
- **Repository während des Reviews verändert:** Der Runner meldet alle erkannten Pfade und beendet sich ungleich null. Änderungen werden nicht zurückgesetzt; der Mensch prüft ihre Herkunft.
- **Unbekannte Git-Basisreferenz:** `prepare_review.py` bricht vor der Paketerzeugung ab. Referenz abrufen oder explizit eine vorhandene Basis angeben.
- **Kein LaTeX-Einstiegspunkt:** Qualitätsprüfung bricht mit Hinweis auf `.ai/config.json` ab. Erst den echten Einstiegspunkt konfigurieren; keine Scheinarbeit erzeugen.
- **Finding ohne ausreichenden Nachweis:** Codex setzt es nicht automatisch um. Je nach Prüfstand wird es begründet abgelehnt oder zurückgestellt.
- **Entscheidungsakte unvollständig:** `validate_decisions.py` nennt fehlende, doppelte oder unbekannte Finding-IDs. Keine Änderungen aufgrund unvalidierter Entscheidungen übernehmen.
- **Review nicht auf Deutsch:** Das Review gilt trotz formalem JSON nicht als freigegeben. Der Runner prüft `language: de`; die tatsächliche Sprache kontrolliert abschließend ein Mensch.
- **Widerspruch zwischen Terminologie und bestehendem Text:** Nicht massenhaft stillschweigend umschreiben. Geltende Konvention ermitteln, Entscheidung dokumentieren und gezielt migrieren.

## Sicherheitsgrenze des Read-only-Modus

Der Runner verwendet nur einen von der lokalen Hilfe bestätigten `plan`-Modus und deaktiviert, soweit unterstützt, sämtliche Claude-Werkzeuge und die Sitzungspersistenz. Er vergleicht vor und nach Claude sowohl den Git-Status als auch Inhaltsfingerabdrücke aller Dateien innerhalb des Repositorys, einschließlich ignorierter Build-Artefakte. Er verwirft nie Änderungen. Diese Kontrolle ist eine nachgelagerte Erkennung, keine Betriebssystem-Sandbox; ein separater temporärer Klon oder eine Plattform-Sandbox bietet stärkere Isolation. Änderungen außerhalb des Repositorys liegen außerhalb des Zustandsvergleichs.

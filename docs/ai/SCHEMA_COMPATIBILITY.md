# Kompatibilität des Review-Schemas mit Claude Code

`docs/ai/REVIEW_SCHEMA.json` bleibt die kanonische, versionierte Wahrheit im Format JSON Schema Draft 2020-12. Dieses Schema wird weder auf die Fähigkeiten einer bestimmten CLI-Version reduziert noch durch ein zweites manuell gepflegtes Review-Schema ersetzt.

Claude Code 2.1.220 akzeptiert über `--json-schema` nicht sämtliche im kanonischen Schema verwendeten Draft‑2020‑12-Konstrukte. `scripts/ai/review_schema.py` erzeugt deshalb zur Laufzeit eine semantisch äquivalente CLI-Darstellung:

- lokale `$ref`-Verweise werden aufgelöst;
- `$defs`, `$schema`, `$id`, Titel und Beschreibungen werden aus der CLI-Darstellung entfernt;
- `const` wird als einelementiges `enum` ausgedrückt;
- Typ-Arrays wie `["integer", "null"]` werden in `anyOf`-Varianten umgewandelt;
- unbekannte Schlüsselwörter führen zum Abbruch statt zu einer stillen Abschwächung.

Der Runner speichert das tatsächlich übergebene Schema in `attempt-NN/claude-cli-schema.json` und protokolliert Hashes des kanonischen und des transformierten Schemas. Das kanonische Ergebnis wird anschließend weiterhin durch `validate_review.py` geprüft.

`preflight.py` transformiert das vollständige kanonische Schema und führt damit einen strukturierten Review-Smoke-Test mit minimaler Ausgabe und ohne Repository-Inhalt aus. Dadurch werden fehlende Anmeldung, zu alte CLI-Versionen, fehlender `plan`-Modus und Schema-Inkompatibilitäten vor Beginn der Schreibarbeit erkannt. Unstrukturierte Ausgabe und Markdown-Codeblöcke werden nicht als Fallback akzeptiert.

Die Transformation wird in `tests/ai/test_review_workflow.py` durch Positivtests für aufgelöste Referenzen, `enum`-Konstanten, Nullable-Zeilenfelder und erhaltene Constraints sowie Negativtests für unbekannte oder semantisch unpassende Schlüsselwörter geprüft. Derselbe Test prüft, dass Änderungen am eingefrorenen Schema oder Prompt den Paket-Hash ändern:

```powershell
python -m unittest discover -s tests/ai -p "test_*.py"
```

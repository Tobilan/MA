# Richtlinie für Behauptungen und Nachweise

Jede wesentliche Aussage ist einer der folgenden maschinenlesbaren Evidenzklassen zuzuordnen. Die Klassifikation kann in Aufgabendateien oder einem Claim-Inventar erfolgen.

## `IMPLEMENTATION_CLAIM`

- **Erforderlicher Nachweis:** Repository-Pfad, relevante Code- oder Teststelle und soweit angemessen geprüfter Git-Commit.
- **Zulässige Formulierung:** konkreter, begrenzter Funktionsumfang im Präsens oder Perfekt.
- **Unzulässige Formulierung:** pauschale Funktionsbehauptung ohne Implementierungs- und Testbezug.
- **Gültig:** „Der Import in `src/import/…` rekonstruiert am Commit `<hash>` die geprüften Missionsbeziehungen; Test … deckt den Fall ab.“
- **Irreführend:** „Das System unterstützt alle IFC-Missionsdaten vollständig.“

## `STANDARD_CLAIM`

- **Erforderlicher Nachweis:** normative Stelle einer offiziellen, versionsgenau benannten Spezifikation.
- **Zulässige Formulierung:** „Die Spezifikation definiert …“ mit Version und Fundstelle.
- **Unzulässige Formulierung:** normative Aussage aus Sekundärquelle oder ohne Versionsbezug.
- **Gültig:** „Die geprüfte IFC-Version definiert `IfcTask` an der angegebenen Normstelle als …“
- **Irreführend:** „IFC schreibt grundsätzlich diese Missionsstruktur vor.“

## `SCIENTIFIC_CLAIM`

- **Erforderlicher Nachweis:** einschlägige wissenschaftliche Primärquelle; bei Überblicksaussagen gegebenenfalls mehrere Quellen.
- **Zulässige Formulierung:** dem Untersuchungsumfang der Quelle entsprechende Aussage.
- **Unzulässige Formulierung:** Kausalität oder Allgemeingültigkeit, die die Quelle nicht trägt.
- **Gültig:** „Unter den in Studie … beschriebenen Bedingungen verringerte das Verfahren …“
- **Irreführend:** „Das Verfahren ist nachweislich immer effizienter.“

## `ARCHITECTURE_DECISION`

- **Erforderlicher Nachweis:** angenommene ADR mit Kontext, Folgen und Nachweisen.
- **Zulässige Formulierung:** „Gemäß ADR-… wird …“
- **Unzulässige Formulierung:** persönliche Präferenz als feststehende Architektur.
- **Gültig:** „Gemäß der angenommenen ADR-… dient … als kanonisches Persistenzformat.“
- **Irreführend:** „IFC ist offensichtlich das einzig geeignete Persistenzformat.“

## `EXPERIMENTAL_RESULT`

- **Erforderlicher Nachweis:** reproduzierbare Daten, Versuchsaufbau, Auswertungsverfahren und Randbedingungen.
- **Zulässige Formulierung:** Ergebnis mit Einheit, Unsicherheit und Geltungsbereich.
- **Unzulässige Formulierung:** erfundener, selektiv berichteter oder nicht reproduzierbarer Messwert.
- **Gültig:** „In den dokumentierten 20 Läufen betrug der Median …; der Versuchsaufbau ist in … beschrieben.“
- **Irreführend:** „Die Laufzeit ist vernachlässigbar.“

## `DESIGN_PROPOSAL`

- **Erforderlicher Nachweis:** nachvollziehbare Motivation, Anforderungen und erkennbare Alternativen; keine Implementierungsevidenz erforderlich.
- **Zulässige Formulierung:** „wird vorgeschlagen“, „könnte“ oder „ist konzeptionell vorgesehen“.
- **Unzulässige Formulierung:** Präsens, das eine bestehende Implementierung suggeriert.
- **Gültig:** „Für die virtuelle Flächenunterteilung wird ein rasterbasierter Ansatz vorgeschlagen.“
- **Irreführend:** „Der Viewer unterteilt jede Fläche automatisch.“

## `INTERPRETATION`

- **Erforderlicher Nachweis:** offengelegte Ausgangsdaten oder Quellen und nachvollziehbare Schlusskette.
- **Zulässige Formulierung:** „Dies legt nahe …“ oder „Daraus wird für diese Arbeit abgeleitet …“
- **Unzulässige Formulierung:** Interpretation als Quellenwortlaut oder gesicherte Tatsache.
- **Gültig:** „Die Ergebnisse legen für die untersuchten Modelle nahe, dass …“
- **Irreführend:** „Die Quelle beweist, dass …“, wenn dies nur eine eigene Ableitung ist.

## `FUTURE_WORK`

- **Erforderlicher Nachweis:** klarer Bezug zu einer festgestellten Grenze oder offenen Anforderung.
- **Zulässige Formulierung:** „künftig“, „zukünftige Erweiterung“, „noch zu untersuchen“.
- **Unzulässige Formulierung:** Zukunftsarbeit als bereits verfügbare Funktion.
- **Gültig:** „Eine dynamische Hindernisbehandlung bleibt einer zukünftigen Erweiterung vorbehalten.“
- **Irreführend:** „Das System behandelt dynamische Hindernisse“, wenn dies nicht implementiert ist.

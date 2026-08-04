# Task: Kapitel 4.2 – Internes Domänenmodell

> **Status:** Vor dem Codex-Lauf vervollständigen  
> **Zielsprache:** Deutsch  
> **Referenzstand IFC-Editor:** `674ede3bf2e7e6cf466bc4c16fe06c90fbb1753c`  
> **Vorgesehener Zielpfad dieser Task-Datei:** `.ai/tasks/kapitel-04-02-internes-domaenenmodell.md`

## 1. Ziel

Erstelle das Unterkapitel **4.2 „Internes Domänenmodell“** der Masterarbeit.

Das Kapitel soll das interne, IFC-unabhängige Domänenmodell des Editors erläutern. Es soll zeigen,

- welche fachlichen Typen Robotermissionen und Roboteraufgaben repräsentieren,
- wie diese Typen zusammenhängen,
- welche Verantwortlichkeiten sie besitzen,
- weshalb das Domänenmodell von Benutzeroberfläche, Viewer-Technologie, Persistenz und IFC-Serialisierung getrennt ist,
- und wie diese Trennung die spätere Abbildung auf IFC vorbereitet.

Das Kapitel muss den tatsächlichen Implementierungsstand des IFC-Editors am Commit

```text
674ede3bf2e7e6cf466bc4c16fe06c90fbb1753c
```

beschreiben. Nicht implementierte oder nur konzeptionell vorgesehene Bestandteile dürfen nicht als umgesetzt dargestellt werden.

## 2. Zieldatei und Einordnung

- Zieldatei: inhalt\kapitel4_annotationsmodell.tex
- LaTeX-Label: sec:internes-domaenenmodell
- Gewünschter Umfang: etwa `1.000–1.400` Wörter zuzüglich Abbildung und gegebenenfalls Tabelle
- Vorgänger: Kapitel 4.1 „Modellierungsziele“
- Nachfolger: Kapitel 4.3 „Robotische Aktionen“

Prüfe vor der Bearbeitung die tatsächliche Kapitelstruktur und den Schreibstil von Kapitel 4.1. Übernimm dessen Terminologie, Zitierweise, Gliederungstiefe und LaTeX-Konventionen.

Kapitel 4.1 darf nicht neu geschrieben werden. Erlaubt ist nur eine minimale Korrektur eines Labels oder Querverweises, wenn dies für Kapitel 4.2 zwingend notwendig ist.

## 3. Verbindlicher Kontext

Lies vor der Bearbeitung:

```text
AGENTS.md
docs/ai/THESIS_CONTRACT.md
docs/ai/GERMAN_WRITING_GUIDE.md
docs/ai/TERMINOLOGY.md
docs/ai/CLAIM_POLICY.md
docs/ai/REPOSITORY_MAP_IFC_EDITOR.md
inhalt\kapitel4_annotationsmodell.tex

```

Lies zusätzlich ausschließlich die im Abschnitt „Implementierungsnachweise“ genannten Dateien.

Nutze die Repository Map nur zur Orientierung. Führe keinen unbeschränkten Scan des Editor-Repositories durch. Öffne weitere Dateien nur, wenn eine konkrete Aussage sonst nicht verifiziert werden kann. Dokumentiere jede zusätzlich gelesene Datei im Abschlussbericht.

## 4. Inhaltliche Leitfragen

Das Kapitel soll mindestens folgende Fragen beantworten:

1. Welche Aufgabe übernimmt das interne Domänenmodell innerhalb des Editors?
2. Welche Verantwortung besitzt `RobotMission`?
3. Welche Verantwortung besitzt `RobotTask`?
4. Wie werden Task-Abhängigkeiten durch `RobotTaskSequence` repräsentiert?
5. Wie werden IFC-Objekte durch `RobotObjectReference` im Domänenmodell referenziert?
6. Welche Aktionsparameter werden durch `RobotActionProperties` zusammengefasst?
7. Welche zeitbezogenen Informationen enthält `RobotTaskTime`?
8. Wie wird ein optionaler Missionszeitplan im Domänenmodell abgebildet?
9. Welche Beziehungen bestehen zwischen Mission, Tasks, Sequenzen, Objektverweisen, Aktionsparametern und Zeitinformationen?
10. Welche fachlichen Invarianten werden bereits im Domänenmodell beziehungsweise in dessen Validierung abgesichert?
11. Warum ist das Domänenmodell unabhängig von IFC-STEP-Syntax, `web-ifc`, Three.js, That Open Fragments, UI-Komponenten und Browser-Persistenz?
12. Welche Bestandteile sind am Referenzcommit tatsächlich umgesetzt, und welche Erweiterungspunkte bleiben offen?

## 5. Erwartete inhaltliche Struktur

Verwende die bestehende Gliederungskonvention der Masterarbeit. Falls Untergliederungen in Kapitel 4 üblich sind, orientiere dich an folgendem Aufbau:

### 4.2.1 Rolle des Domänenmodells

- fachliches Bearbeitungsmodell des Editors,
- Trennung von fachlicher Semantik und technischer Repräsentation,
- Abgrenzung zu IFC-Persistenz, Viewer und Benutzeroberfläche,
- Nutzen für Validierung, Testbarkeit und spätere Exporte.

### 4.2.2 Zentrale Domänentypen

Beschreibe mindestens:

- `RobotMission`,
- `RobotTask`,
- `RobotTaskSequence`,
- `RobotObjectReference`,
- `RobotActionProperties`,
- `RobotTaskTime`,
- den Missionszeitplan, sofern er am Referenzcommit als eigener Typ oder als Bestandteil des Missionsmodells vorhanden ist.

Beschreibe für jeden Typ:

- fachliche Aufgabe,
- zentrale Felder,
- Beziehungen zu anderen Typen,
- verpflichtende und optionale Informationen,
- relevante Validierungsregeln,
- Implementierungsstatus.

Erzeuge keine vollständige Feldliste ohne inhaltliche Einordnung. Konzentriere dich auf die für das Annotationsmodell relevanten Eigenschaften.

### 4.2.3 Beziehungen und Aggregatgrenzen

Erläutere:

- Mission als fachlichen Container beziehungsweise Aggregat,
- Zugehörigkeit von Tasks zu einer Mission,
- Trennung zwischen Task-Liste, Hierarchie und Ausführungsabhängigkeiten,
- Verknüpfung von Tasks mit Objektverweisen,
- taskbezogene Aktions- und Zeitinformationen,
- stabile interne IDs,
- Grenzen zwischen Domain, Application Layer und Infrastruktur.

Verwende den Begriff „Aggregat“ oder „Aggregate Root“ nur, wenn die Implementierung und eine geeignete Architekturquelle diese Einordnung stützen. Andernfalls beschreibe `RobotMission` neutral als zentralen fachlichen Missionscontainer.

### 4.2.4 Begründung der technologischen Entkopplung

Erläutere, weshalb folgende Aspekte nicht Teil des Domänenmodells sind:

- Three.js-Objekte,
- Fragments-Modelle und Rendering-IDs,
- UI-Zustände,
- `localStorage`,
- IFC-Entity-Instanzen,
- STEP-Serialisierung,
- `web-ifc`-Laufzeitobjekte,
- Quellbytes und Roundtrip-Provenienz.

Stelle klar, dass diese Informationen in nachgelagerten Schichten, Adaptern oder Infrastrukturkomponenten verarbeitet werden.

### 4.2.5 Zwischenfazit und Überleitung

Fasse knapp zusammen:

- welche fachliche Grundlage das Domänenmodell bereitstellt,
- weshalb konkrete Roboteraktionen taskbezogen modelliert werden,
- und weshalb Kapitel 4.3 anschließend das Aktionsvokabular vertieft.

## 6. Abgrenzung zu anderen Unterkapiteln

Behandle in Kapitel 4.2 nur die Grundlagen des internen Domänenmodells.

Nicht im Detail vorwegnehmen:

- konkrete Aktionswerte und deren Semantik → Kapitel 4.3,
- `GlobalId`, `expressId` und `modelId` → Kapitel 4.4,
- IFC-Missionshierarchie über `IfcRelNests` → Kapitel 4.5,
- IFC-Sequenzen über `IfcRelSequence` → Kapitel 4.6,
- IFC-Objektzuordnungen → Kapitel 4.7,
- Property Sets → Kapitel 4.8,
- IFC-Zeitabbildung → Kapitel 4.9,
- vollständiges Domain-zu-IFC-Mapping → Kapitel 4.10,
- detaillierte Validierungsregeln → Kapitel 4.11,
- Persistenz und Roundtrip → Kapitel 4.12.

Kurze Vorausverweise sind zulässig und erwünscht, wenn sie Wiederholungen verhindern.

## 7. Implementierungsnachweise

Prüfe zunächst ausschließlich diese Dateien des IFC-Editor-Repositories:

```text
src/domain/robot-tasks/types.ts
src/domain/robot-tasks/builders.ts
src/domain/robot-tasks/sequencing.ts
src/domain/robot-tasks/validation.ts
src/domain/robot-tasks/index.ts
src/application/robot-tasks/missionRepository.ts
src/application/robot-tasks/robotMissionService.ts
test/robot-tasks/robot-mission-domain.test.ts
test/robot-tasks/robot-mission-service.test.ts
```

Optional, nur wenn eine konkrete Aussage dies erfordert:

```text
src/application/robot-tasks/importRobotMissions.ts
src/application/robot-tasks/robotMissionSemanticComparison.ts
src/persistence/robot-tasks/inMemoryMissionRepository.ts
src/persistence/robot-tasks/localStorageMissionRepository.ts
```

Für jede Implementierungsbehauptung gilt:

- exakten Dateipfad prüfen,
- auf den Referenzcommit beziehen,
- keine Funktion allein aus einem Typnamen ableiten,
- Tests als ergänzenden Nachweis verwenden,
- keine Implementierungsdetails behaupten, die nicht im Code oder in Tests erkennbar sind.

## 8. Quellen und Nachweise – vor dem Lauf ausfüllen

Codex darf ausschließlich vorhandene und überprüfbare Quellen zitieren. Fehlende Quellen dürfen nicht durch Modellwissen ersetzt werden.

### 8.1 Wissenschaftliche Quellen zur Architektur oder Domänenmodellierung

Hier Quellen einfügen, die die Trennung von fachlichem Domänenmodell und technischer Infrastruktur, Ports-und-Adapter-Architektur, Domain Model oder vergleichbare Architekturprinzipien stützen.

```text
- BibTeX-Key: [[BIBTEX_KEY_ARCHITEKTUR_1]]
  Datei/Pfad: [[PFAD_ZUR_QUELLE]]
  Relevante Seiten/Abschnitte: [[SEITEN_ODER_ABSCHNITTE]]
  Zu belegende Aussage: [[KONKRETE_AUSSAGE]]

- BibTeX-Key: [[BIBTEX_KEY_ARCHITEKTUR_2]]
  Datei/Pfad: [[PFAD_ZUR_QUELLE]]
  Relevante Seiten/Abschnitte: [[SEITEN_ODER_ABSCHNITTE]]
  Zu belegende Aussage: [[KONKRETE_AUSSAGE]]
```

Sind keine geeigneten wissenschaftlichen Architekturquellen vorhanden, beschreibe die Trennung als konkrete Projektarchitektur und nicht als allgemein bewiesene Best Practice.

### 8.2 Wissenschaftliche Quellen zu Robotermissionen oder Taskmodellen

Hier Quellen einfügen, die Missionen, Tasks, Sequenzen, Aktionsparameter oder zeitliche Planung in Robotiksystemen behandeln.

```text
- BibTeX-Key: [[BIBTEX_KEY_ROBOTIK_1]]
  Datei/Pfad: [[PFAD_ZUR_QUELLE]]
  Relevante Seiten/Abschnitte: [[SEITEN_ODER_ABSCHNITTE]]
  Zu belegende Aussage: [[KONKRETE_AUSSAGE]]
```

Verwende diese Quellen nur, wenn ihre Begriffe tatsächlich zum beschriebenen Modell passen. Übertrage keine fremde Taxonomie stillschweigend auf den Editor.

### 8.3 Projektinterne Architekturentscheidungen

```text
- Dokument/Pfad: [[PFAD_ZU_ARCHITECTURE_DECISIONS]]
  Status: [[ACCEPTED / PROPOSED]]
  Relevante Entscheidung: [[ID_UND_TITEL]]

- Dokument/Pfad: [[OPTIONALER_WEITERER_PROJEKTNACHWEIS]]
  Status: [[ACCEPTED / PROPOSED / DISCUSSION]]
  Nutzbare Aussage: [[KONKRETE_AUSSAGE]]
```

### 8.4 Implementierung als Primärnachweis des Projektstands

```text
Repository: Tobilan/poc_thatopen
Commit: 674ede3bf2e7e6cf466bc4c16fe06c90fbb1753c
Dateien: siehe Abschnitt „Implementierungsnachweise“
```

Der Quellcode belegt den Implementierungsstand, ersetzt aber keine wissenschaftliche Quelle für allgemeine Architektur- oder Robotikaussagen.

### 8.5 Quellenregeln

- Keine Quelle, keinen BibTeX-Key, keine Seitenzahl und kein Zitat erfinden.
- Direkte Zitate nur verwenden, wenn Wortlaut und Seitenzahl verifiziert sind.
- Bestehende BibTeX-Keys unverändert verwenden.
- Publikationstitel nicht übersetzen.
- Code und Tests nicht als wissenschaftliche Literatur zitieren.
- Fehlende Belege im Abschlussbericht als `QUELLE_FEHLT` aufführen.
- Eine Aussage ohne ausreichenden Beleg entweder auslassen, einschränken oder ausdrücklich als Projektentscheidung kennzeichnen.

## 9. Abbildungen

Mindestens **eine fachlich notwendige Abbildung** ist für dieses Kapitel zu erstellen.

### 9.1 Verpflichtende Abbildung: Internes Domänenmodell

Erzeuge eine UML-ähnliche oder vergleichbar präzise Strukturabbildung des internen Domänenmodells.

Die Abbildung soll mindestens folgende Typen enthalten, sofern sie am Referenzcommit tatsächlich vorhanden sind:

```text
RobotMission
RobotTask
RobotTaskSequence
RobotObjectReference
RobotActionProperties
RobotTaskTime
RobotMissionSchedule beziehungsweise der tatsächlich implementierte Schedule-Typ
```

Die Abbildung soll zeigen:

- zentrale Beziehungen zwischen den Typen,
- Multiplizitäten oder Optionalität, sofern eindeutig aus dem Code ableitbar,
- Zugehörigkeit von Tasks und Sequenzen zur Mission,
- taskbezogene Objektverweise,
- taskbezogene Aktionsparameter,
- taskbezogene Zeitinformationen,
- einen optionalen Missionszeitplan, sofern implementiert.

Nicht darstellen:

- IFC-Entities wie `IfcTask`, `IfcRelSequence` oder `IfcPropertySet`,
- UI-Komponenten,
- Three.js- oder Fragments-Typen,
- Persistenzadapter,
- nicht implementierte Zukunftstypen,
- erfundene Kardinalitäten.

Empfohlene Bildunterschrift:

```text
Internes Domänenmodell für Robotermissionen und Roboteraufgaben.
Eigene Darstellung auf Basis der Implementierung am Commit 674ede3.
```

Passe die Formulierung an die Zitier- und Abbildungskonventionen der Masterarbeit an.

Vorgesehene Pfade:

```text
Editierbare Diagrammquelle:
[[PFAD_ZUR_DIAGRAMMQUELLE, Z. B. figures/source/domain-model-robot-mission.puml]]

Gerenderte Vektorgrafik:
[[PFAD_ZUR_GRAFIK, Z. B. figures/domain-model-robot-mission.pdf]]

LaTeX-Label:
[[ABBILDUNGS_LABEL, Z. B. fig:domain-model-robot-mission]]
```

### 9.2 Optionale Abbildung: Architekturgrenzen

Erzeuge eine zweite Abbildung nur, wenn Kapitel 4.1 oder ein früheres Architekturkapitel keine inhaltlich gleichwertige Darstellung enthält.

Möglicher Inhalt:

```text
Benutzeroberfläche / Viewer
           ↓
Application Layer
           ↓
internes Domänenmodell
           ↓
IFC-Mapping und Persistenzadapter
```

Die Abbildung soll die Abhängigkeitsrichtung und die Entkopplung des Domänenmodells verdeutlichen. Sie darf nicht suggerieren, dass alle Adapter direkt voneinander abhängen.

Vorgesehene Pfade:

```text
Editierbare Diagrammquelle:
[[OPTIONALER_PFAD]]

Gerenderte Vektorgrafik:
[[OPTIONALER_PFAD]]

LaTeX-Label:
[[OPTIONALES_LABEL]]
```

### 9.3 Technische Anforderungen an Abbildungen

1. Prüfe zuerst, welche Diagrammtechnik das Thesis-Repository bereits verwendet.
2. Bevorzuge vorhandene Werkzeuge und Konventionen.
3. Bevorzugte Formate:
   - TikZ, wenn die Masterarbeit bereits TikZ verwendet;
   - PlantUML oder Graphviz mit versionierter Quelldatei und PDF-/SVG-Export;
   - Mermaid nur, wenn der bestehende Build reproduzierbar daraus eine druckfähige Grafik erzeugt.
4. Bevorzuge Vektorgrafiken.
5. Verwende keine Screenshots von Quellcode als Ersatz für eine Strukturabbildung.
6. Alle beschreibenden Texte in der Grafik müssen auf Deutsch sein.
7. Typ- und Codebezeichner wie `RobotMission` bleiben unverändert.
8. Die Grafik muss in Graustufen verständlich und im Druck lesbar sein.
9. Nutze keine externen Bilder oder Icons ohne überprüfte Quelle und Nutzungsrecht.
10. Speichere editierbare Diagrammquelle und gerenderte Grafik im Repository.
11. Füge die Grafik mit `\includegraphics` oder der im Repository üblichen Methode ein.
12. Führe die Abbildung vor ihrem Auftreten im Fließtext ein.
13. Interpretiere die Abbildung nach der Referenz. Sie darf nicht nur dekorativ eingebunden werden.
14. Prüfe, dass keine Beziehung in der Grafik dem Text oder der Implementierung widerspricht.
15. Wenn die Grafik nicht reproduzierbar erzeugt werden kann, dokumentiere dies als offenen Punkt und erzeuge keine nicht nachvollziehbare Binärdatei.

### 9.4 Quellen für Abbildungen

Für eine vollständig selbst erstellte, aus dem Quellcode abgeleitete Abbildung:

```text
Art: Eigene Darstellung
Basis: Implementierung des IFC-Editors am Commit 674ede3
Externe Bildquelle: keine
```

Für eine übernommene oder angepasste externe Abbildung:

```text
BibTeX-Key: [[BIBTEX_KEY]]
Seite/Abbildungsnummer: [[SEITE_ODER_ABBILDUNGSNUMMER]]
Art der Verwendung: [[ÜBERNOMMEN / ANGEPASST]]
Lizenz oder Nutzbarkeit geprüft: [[JA / NEIN]]
Erforderlicher Quellenhinweis: [[GENAUE_FORMULIERUNG]]
```

Verwende keine externe Abbildung, solange Herkunft, Zitierfähigkeit und Nutzungsrecht nicht geklärt sind.

## 10. Optionale Tabelle

Falls sie den Text verdichtet, erstelle eine Tabelle mit folgenden Spalten:

```text
Domänentyp | Fachliche Verantwortung | Zentrale Beziehungen | Implementierungsdatei
```

Die Tabelle darf die Typbeschreibungen im Fließtext nicht vollständig duplizieren. Verwende sie als Überblick, während der Text Beziehungen und Entwurfsentscheidungen erläutert.

## 11. Besonders zu prüfende Aussagen

Prüfe folgende Aussagen besonders streng:

1. `RobotMission` ist der zentrale fachliche Container für Tasks und Sequenzen.
2. Das Domänenmodell ist unabhängig von IFC-Serialisierung und Viewer-Technologien.
3. Aktionssemantik und Zeitinformationen sind taskbezogen.
4. Objektverweise werden als fachliche Referenzen und nicht als Three.js-Objekte gespeichert.
5. Hierarchie, Listenreihenfolge und Ausführungsabhängigkeiten sind unterschiedliche Konzepte.
6. Persistenz- und Roundtrip-Provenienz gehören nicht zum fachlichen Domänenmodell.
7. Ein optionaler Missionszeitplan ist tatsächlich im Referenzcommit vorhanden.
8. Verwendete Begriffe wie „Aggregat“, „Repository“ oder „Port“ entsprechen der tatsächlichen Architektur.

Formuliere keine dieser Aussagen stärker, als es Code, Tests und Quellen erlauben.

## 12. Sprachliche Anforderungen

- Schreibe in formalem, präzisem Wissenschaftsdeutsch.
- Verwende überwiegend sachliche und unpersönliche Formulierungen.
- Vermeide werbliche Begriffe wie „leistungsstark“, „optimal“, „nahtlos“ oder „robust“, sofern sie nicht evaluiert wurden.
- Verwende die Begriffe aus `docs/ai/TERMINOLOGY.md`.
- Standardisierte IFC-Bezeichner und TypeScript-Typnamen bleiben unverändert.
- Definiere zentrale Begriffe bei der ersten Verwendung.
- Vermeide unnötige Wiederholungen aus Kapitel 4.1.
- Trenne Implementierung, Entwurfsentscheidung und zukünftige Erweiterung sprachlich eindeutig.
- Verwende keine direkten Zitate, wenn eine Paraphrase ausreicht.
- Halte Bildunterschriften sachlich und vollständig.

## 13. Ausdrückliche Ausschlüsse

- Keine Änderung am IFC-Editor-Code.
- Keine neue Domain-Funktion implementieren.
- Keine umfassende Beschreibung des IFC-Mappings.
- Keine detaillierte Darstellung einzelner IFC-Entities.
- Keine ausführliche Beschreibung der Benutzeroberfläche.
- Keine Diskussion von ROS, Navigation, Waypoints oder Roboterausführung.
- Keine vollständige Persistenz- oder Roundtrip-Diskussion.
- Keine Quelle über das Internet recherchieren, sofern dies nicht ausdrücklich freigegeben wurde.
- Keine Bibliografieeinträge erfinden oder ungeprüft ergänzen.
- Keine Abbildung aus einer externen Quelle ohne dokumentierte Nutzbarkeit übernehmen.
- Keine neuen LaTeX-Pakete hinzufügen, wenn die Grafik mit vorhandenen Mitteln reproduzierbar erstellt werden kann.

## 14. Arbeitsauftrag an Codex

1. Lies die verbindlichen Kontextdateien und Kapitel 4.1.
2. Prüfe die genannten Implementierungsdateien am Referenzcommit.
3. Prüfe die eingetragenen wissenschaftlichen und projektinternen Quellen.
4. Ermittle den tatsächlichen Zielpfad, die vorhandene LaTeX-Struktur und die Abbildungskonventionen.
5. Erstelle Kapitel 4.2 vollständig in der vorgesehenen Zieldatei.
6. Erstelle mindestens die verpflichtende Domänenmodell-Abbildung.
7. Binde die Abbildung korrekt in LaTeX ein.
8. Führe die Abbildung im Text ein und interpretiere sie.
9. Ergänze nur verifizierte `\cite{...}`-Verweise.
10. Aktualisiere Glossar oder Abkürzungsverzeichnis nur, wenn dies durch bestehende Konventionen erforderlich ist.
11. Verändere keine anderen Kapitel außer unvermeidbaren Querverweisen.
12. Führe die lokale Thesis-Prüfung aus.
13. Prüfe den finalen Git-Diff auf unbeabsichtigte Änderungen.
14. Gib einen deutschsprachigen Abschlussbericht aus.
15. Erstelle keinen Push und keinen Merge.

## 15. Akzeptanzkriterien

Das Kapitel ist abgeschlossen, wenn alle folgenden Bedingungen erfüllt sind:

- [ ] Kapitel 4.2 wurde in der richtigen LaTeX-Datei erstellt.
- [ ] Der Text ist in formalem Deutsch verfasst.
- [ ] Der Text knüpft nachvollziehbar an Kapitel 4.1 an.
- [ ] `RobotMission` wird fachlich eingeordnet.
- [ ] `RobotTask` wird fachlich eingeordnet.
- [ ] `RobotTaskSequence` wird fachlich eingeordnet.
- [ ] `RobotObjectReference` wird fachlich eingeordnet.
- [ ] `RobotActionProperties` wird fachlich eingeordnet.
- [ ] `RobotTaskTime` wird fachlich eingeordnet.
- [ ] Der Missionszeitplan wird nur entsprechend seinem tatsächlichen Implementierungsstand beschrieben.
- [ ] Beziehungen zwischen den Typen werden erläutert.
- [ ] Domänenmodell, IFC-Persistenz, UI und technische Infrastruktur werden klar getrennt.
- [ ] Implementierte und geplante Bestandteile werden eindeutig unterschieden.
- [ ] Keine allgemeine Architekturbehauptung wird allein mit dem Projektcode belegt.
- [ ] Alle verwendeten BibTeX-Keys existieren und wurden geprüft.
- [ ] Mindestens eine fachlich notwendige Abbildung wurde erstellt.
- [ ] Die Domänenmodell-Abbildung basiert auf dem Referenzcommit.
- [ ] Die Abbildung enthält keine erfundenen Typen, Beziehungen oder Kardinalitäten.
- [ ] Eine editierbare Diagrammquelle ist versioniert.
- [ ] Eine druckfähige Vektorgrafik ist vorhanden.
- [ ] Die Abbildung wird im Text eingeführt, referenziert und interpretiert.
- [ ] Bildunterschrift und LaTeX-Label sind vorhanden.
- [ ] Externe Bildquellen wurden nicht ungeprüft verwendet.
- [ ] Kapitel 4.3 bis 4.12 werden nicht unnötig vorweggenommen.
- [ ] Die konfigurierte LaTeX-Prüfung läuft erfolgreich.
- [ ] Es wurden keine unbeabsichtigten Dateien verändert.
- [ ] Fehlende Belege sind als `QUELLE_FEHLT` dokumentiert.

## 16. Review-Schwerpunkte für Claude

Claude soll das Kapitel nach dem Codex-Lauf insbesondere auf folgende Punkte prüfen:

1. Widersprüche zum Referenzcommit.
2. Unvollständige oder falsche Beziehungen im Domänenmodell.
3. Vermischung von Domain, Application Layer, UI, Persistenz und IFC-Infrastruktur.
4. Übertriebene oder unbelegte Architekturbegründungen.
5. Falsche Verwendung der Begriffe `RobotMission`, `RobotTask`, `RobotTaskSequence`, `RobotObjectReference`, `RobotActionProperties` und `RobotTaskTime`.
6. Verwechslung von Hierarchie, Listenreihenfolge und Ausführungssequenz.
7. Aussagen über nicht implementierte Funktionen.
8. Fehlende wissenschaftliche Belege.
9. Unklare oder nicht wissenschaftliche deutsche Formulierungen.
10. Widersprüche zwischen Text, Abbildung, Tabelle und Quellcode.
11. Erfunden dargestellte Kardinalitäten.
12. Abbildung ohne ausreichende Erläuterung.
13. Unleserliche oder nicht reproduzierbare Grafik.
14. Unnötige Vorwegnahme späterer Unterkapitel.
15. Fehlende Limitationen oder Unsicherheiten.

## 17. Build und Workflow

Vor dem Claude-Review:

```bash
python scripts/ai/run_ai_workflow.py pre-review \
  --prepare-args "--base main --task .ai/tasks/kapitel-04-02-internes-domaenenmodell.md"
```

Falls die Einzelskripte zusätzliche Pfade benötigen, verwende deren tatsächlich implementierte CLI-Argumente.

Nach der Verifikation und Umsetzung akzeptierter Claude-Findings:

```bash
python scripts/ai/run_ai_workflow.py post-review
```

## 18. Erwarteter Abschlussbericht von Codex

Der Abschlussbericht muss auf Deutsch enthalten:

1. geänderte Dateien;
2. erstellte oder geänderte Abbildungsdateien;
3. verwendetes Diagrammformat und Reproduktionsbefehl;
4. behandelte Leitfragen;
5. verwendete Quellen und BibTeX-Keys;
6. geprüfte Implementierungsdateien;
7. zusätzlich geöffnete Dateien mit Begründung;
8. nicht belegte oder ausgelassene Aussagen;
9. ausgeführte Build- und Prüfkommandos;
10. Build-Ergebnis;
11. verbleibende Risiken oder Unsicherheiten;
12. vorgeschlagene Commit-Nachricht.

## 19. Vorgeschlagene Commit-Nachricht

```text
docs: Kapitel 4.2 zum internen Domänenmodell ergänzen
```

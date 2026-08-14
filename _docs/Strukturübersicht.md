# Ergebnis der Repository-Prüfung

Geprüft wurde der aktuelle Implementierungsstand des Repositories einschließlich des inzwischen integrierten **IFC-Roundtrips für RobotMission-Annotationen**. Der maßgebliche Roundtrip-Stand wurde mit Commit `674ede3` in `main` übernommen. Der PoC ist damit deutlich mehr als ein reiner IFC-Viewer: Er umfasst ein internes Missionsmodell, einen browserbasierten Missionseditor, Validierung, IFC-Mapping sowie einen **bidirektionalen Workflow zwischen annotierter IFC-Datei und internem Domänenmodell**.

Der wissenschaftliche Kern der Arbeit sollte deshalb weiterhin nicht nur als „Vorstellung des Editors“, sondern als **Konzeption und prototypische Umsetzung eines IFC-basierten Annotationssystems für Robotermissionen** dargestellt werden. Der inzwischen implementierte Roundtrip stärkt dabei insbesondere die Entscheidung, die annotierte IFC-Datei als fachlichen Daten- und Austauschträger zu verwenden. Die früher konzeptionell formulierte Zielarchitektur „annotierte IFC → Domänenmodell → Bearbeitung → annotierte IFC“ ist inzwischen technisch umgesetzt. 

## Tatsächlich umgesetzt

| Bereich                      | Aktueller Stand                                                                                                                                                                                                                                                                  |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Browserbasierter IFC-Viewer  | IFC- und Fragments-Modelle können mit That Open Components, Fragments und Three.js geladen und dargestellt werden. Direkt geladene IFC-Dateien werden zusätzlich als Quelldaten für den Roundtrip vorgehalten.                                                                   |
| Internes Missionsmodell      | `RobotMission`, `RobotTask`, explizite Task-Sequenzen, Zeitinformationen, Objektbezüge und Aktionsparameter sind als eigenständiges TypeScript-Domänenmodell umgesetzt. Unterstützt werden `OPEN`, `CLOSE`, `SWITCH_ON`, `SWITCH_OFF`, `MOVE`, `PASS_THROUGH` und `NAVIGATE_TO`. |
| Objektreferenzierung         | IFC-Objekte werden bevorzugt über `GlobalId` referenziert. `modelId + expressId` dient als modelllokaler Fallback. Das `modelId` wird zusätzlich für die Zuordnung einer Mission zum jeweiligen Quellmodell genutzt.                                                             |
| Verbesserte Auswahl          | Überlagernde Objekte werden als Kandidaten ermittelt, können durchlaufen, hervorgehoben und explizit bestätigt werden. Asynchrone Auswahlvorgänge, Hover, Filter und stabile Auswahlzustände werden berücksichtigt.                                                              |
| Missionseditor               | Missionen und Tasks können angelegt, bearbeitet und gelöscht werden. Ausgewählte IFC-Objekte können als Ziel, betroffenes Objekt, MOVE-Start oder MOVE-Ziel zugewiesen werden. Task-Zeiten und Reihenfolgen werden bearbeitet und Validierungsprobleme angezeigt.                |
| Validierung                  | Pflichtfelder, Aktionsarten, Objektklassen, MOVE-Referenzen, Task-Sequenzen, Zyklen und Zeitwerte werden geprüft. Die Trennung zwischen Aktionssemantik und IFC-Objekt wird explizit validiert.                                                                                  |
| Persistenz                   | Missionen können flüchtig im Arbeitsspeicher oder im Browser-`localStorage` gespeichert werden. Die Backend-Option ist weiterhin nur ein nicht funktionsfähiger Platzhalter.                                                                                                     |
| IFC-Mapping                  | Missionen werden auf Parent-`IfcTask`, Child-`IfcTask`, `IfcRelNests`, `IfcRelSequence`, `IfcWorkSchedule`, Objektzuweisungen, `IfcTaskTime` und eigene Property Sets abgebildet.                                                                                                |
| IFC-Export                   | Missionen werden in eine quellgestützte IFC-Datei geschrieben. Der Export ersetzt den vom Editor kontrollierten Missionsgraphen gezielt, anstatt bei jedem Export neue Annotationen anzuhängen.                                                                                  |
| **IFC-Missionsimport**       | **Vorhandene, vom System erzeugte RobotMission-Annotationen werden beim Laden einer IFC-Datei erkannt und wieder in `RobotMission`- und `RobotTask`-Objekte rekonstruiert.**                                                                                                     |
| **IFC-Roundtrip**            | **Importierte Missionen können im Editor verändert und anschließend erneut in die IFC-Datei exportiert werden. Der vorhandene Missionsgraph wird dabei ersetzt. Wiederholte Roundtrips sollen keine Duplikate erzeugen.**                                                        |
| **Roundtrip-Verifikation**   | **Nach dem Export wird die resultierende IFC-Datei erneut geöffnet, die Mission erneut importiert und semantisch mit dem beabsichtigten Domänenmodell verglichen. Erst danach werden die erzeugten Bytes als neue Roundtrip-Quelle akzeptiert.**                                 |
| **Identitätserhalt**         | Bestehende Building-`GlobalId`s bleiben unangetastet. Für deterministisch wiedererkennbare Missionsentitäten können bestehende IFC-`GlobalId`s über Roundtrips erhalten bleiben; `expressId`s gelten dagegen nur innerhalb der jeweiligen Serialisierung.                        |
| **Annotationsversionierung** | Die eigene Missionsannotation besitzt mit `AnnotationSchemaVersion = "1.0.0"` eine explizite Version. Legacy-Annotationen ohne diese Information werden über definierte Kompatibilitätsregeln behandelt.                                                                         |
| Tests                        | Es existieren Tests für Domänenmodell, Persistenz, Auswahl, IFC-Mapping, Reader, Writer, Replacement, semantischen Vergleich und Roundtrip-Koordination. Die Testsuite enthält auch Integrationsfälle für wiederholte Import-/Exportzyklen.                                      |

Der Roundtrip wird im Repository ausdrücklich als **quellgestützter Roundtrip für RobotMission-Annotationen** beschrieben. Er darf nicht mit einem allgemeinen verlustfreien Roundtrip beliebiger IFC-Modelländerungen gleichgesetzt werden.

## Noch nicht umgesetzt

Die folgenden Punkte sollten weiterhin klar als **Konzept, Erweiterung oder zukünftige Arbeit** gekennzeichnet werden:

* Backend-Persistenz oder serverseitige IFC-Verarbeitung
* roboterspezifischer JSON-Export
* Transformation vom IFC-Koordinatensystem in einen ROS-`map`-Frame
* Ableitung von Anfahrposen und Waypoints
* Wegplanung und direkte Robotersteuerung
* virtuelle Teilflächenauswahl beziehungsweise Surface Tiling
* Vorannotation möglicher Roboterinteraktionen durch `RobotInteractionCapability`
* automatische Verbindung von Viewer-Viewpoints mit Tasks
* vollständiger allgemeiner Roundtrip **struktureller IFC-/Fragments-Änderungen**
* allgemeine Bearbeitung von Bauteilgeometrie oder beliebigen IFC-Eigenschaften

**Nicht mehr** in diese Liste gehören:

* Rekonstruktion einer Mission beim Import einer annotierten IFC-Datei
* Missionsimport in den Editor
* erneute Bearbeitung und Export derselben Mission
* duplikatfreier RobotMission-Roundtrip

Diese Funktionen sind inzwischen implementiert. Der ursprüngliche Architekturvorschlag, eine annotierte IFC-Datei als kanonischen fachlichen Träger zu verwenden, ist dadurch wesentlich besser technisch abgesichert als zum Zeitpunkt der ersten Strukturüberlegung. 

---

# Empfohlene Gliederung der Masterarbeit

## 1 Einleitung

### 1.1 Motivation

* zunehmender Einsatz mobiler Roboter in Gebäuden
* BIM-Modelle als Informationsquelle für robotische Systeme
* fehlende durchgängige Verbindung zwischen Gebäudemodell, Aufgabenbeschreibung und Roboterausführung
* Schwierigkeiten bei der Annotation komplexer IFC-Modelle
* Bedarf an einem editierbaren und austauschbaren semantischen Missionsmodell

### 1.2 Problemstellung

Die Problemstellung sollte auf drei Ebenen formuliert werden:

1. **Semantisch:** Wie können Robotermissionen, Tasks, Aktionen und Zielobjekte in IFC beschrieben werden?
2. **Technisch:** Wie kann ein browserbasierter IFC-Editor aufgebaut werden, der komplexe Gebäudemodelle performant darstellt und zuverlässig annotierbar macht?
3. **Ausführungsbezogen:** Wie können semantische IFC-Annotationen später in roboterspezifische Navigations- und Aktionsdaten überführt werden?

Der implementierte Roundtrip ergänzt insbesondere die erste und zweite Ebene: Die Mission wird nicht nur erzeugt, sondern kann aus IFC rekonstruiert und weiterbearbeitet werden.

### 1.3 Zielsetzung

Ziel ist die Konzeption und prototypische Umsetzung eines browserbasierten IFC-Editors, mit dem Robotermissionen:

* erstellt,
* mit Gebäudeelementen verbunden,
* validiert,
* als IFC-kompatible Struktur gespeichert,
* aus annotierten IFC-Dateien rekonstruiert,
* erneut bearbeitet
* und wieder exportiert

werden können.

### 1.4 Forschungsfragen

Geeignete Forschungsfragen wären:

**F1:** Wie lassen sich Robotermissionen und ihre Ausführungsschritte semantisch konsistent mit IFC-Objekten verknüpfen?

**F2:** Wie kann ein browserbasierter IFC-Editor aufgebaut werden, der auch bei komplexen Gebäudemodellen eine zuverlässige Aufgabenannotation ermöglicht?

**F3:** Wie kann ein bidirektionaler Austausch zwischen internem Missionsmodell und annotierter IFC-Datei realisiert werden, ohne Missionsinformationen bei wiederholten Bearbeitungszyklen zu duplizieren oder semantisch zu verändern?

**F4:** Welche zusätzlichen Verarbeitungsschritte sind erforderlich, um IFC-basierte Aufgabenannotation in roboterspezifische Zielposen, Waypoints und ausführbare Missionen zu überführen?

Durch den Roundtrip ist eine zusätzliche Forschungsfrage beziehungsweise Unterfrage zur **Persistenz und bidirektionalen Abbildung** jetzt fachlich gerechtfertigt.

### 1.5 Abgrenzung

Explizit nicht Bestandteil des implementierten PoC sind beispielsweise:

* physische Robotersteuerung
* vollständige autonome Wegplanung
* produktionsreifes Backend
* Mehrbenutzerbetrieb
* vollständiger allgemeiner IFC-Editor
* verlustfreier Roundtrip beliebiger struktureller Modelländerungen
* automatische Berechnung roboterspezifischer Zielposen

Wichtig ist die präzise Formulierung:

> Der Roundtrip der **RobotMission-Annotationen** ist umgesetzt. Ein allgemeiner Roundtrip des gesamten IFC-Modells ist nicht Gegenstand des PoC.

### 1.6 Aufbau der Arbeit

Kurze Erläuterung der folgenden Kapitel.

---

# 2 Grundlagen und Stand der Forschung

Dieses Kapitel sollte weiterhin kein allgemeines IFC-Lehrbuch werden, sondern nur die für die Modellierungs- und Implementierungsentscheidungen notwendigen Grundlagen enthalten.

## 2.1 Building Information Modeling und IFC

* BIM-Grundidee
* objektorientierter Aufbau von IFC
* `IfcRoot`
* `GlobalId`
* Objektidentität
* Property Sets
* Relationen
* lokale Placements
* geometrische Repräsentationen

Die Platzierung von IFC-Objekten ist insbesondere für spätere Robotik-Erweiterungen relevant, da `ObjectPlacement`, geometrischer Referenzpunkt und tatsächlich anzufahrende Roboterpose voneinander zu unterscheiden sind. 

## 2.2 Prozess- und Aufgabenmodellierung in IFC

Hier gehören insbesondere hinein:

* `IfcTask`
* `IfcTaskTime`
* `IfcWorkSchedule`
* `IfcRelNests`
* `IfcRelSequence`
* `IfcRelAssignsToProcess`
* `IfcRelAssignsToProduct`
* `IfcRelAssignsToControl`
* `IfcRelDefinesByProperties`

## 2.3 Browserbasierte Verarbeitung von IFC-Modellen

* Three.js
* `web-ifc`
* That Open Components
* Fragments als performante Darstellungsstruktur
* Unterschied zwischen fachlichem IFC-Modell und Rendering-Modell
* Notwendigkeit, die ursprünglichen IFC-Quelldaten unabhängig von den Fragments zu erhalten

Diese Trennung ist für den Roundtrip zentral: Fragments dienen der Darstellung und Auswahl, während der Missionsimport und -export auf den IFC-Quelldaten operieren.

## 2.4 Robotermissionen und mobile Navigation

* Mission, Task und Aktion
* robotische Fähigkeiten
* Navigation und Manipulation
* Pose, Orientierung und Koordinatenrahmen
* grundlegende ROS-/ROS-2-Konzepte
* Waypoints
* Anfahrposen

## 2.5 Verwandte Arbeiten

* BIM-basierte Roboterplanung
* IFC-basierte Task- und Prozessmodellierung
* BIM-to-Robot-Ansätze
* browserbasierte BIM-Editoren
* bestehende Ansätze zur Verknüpfung von BIM-Objekten und Roboteraktionen
* persistente beziehungsweise bidirektionale BIM-Annotationen

## 2.6 Forschungslücke

Mögliche Argumentation:

> Bestehende BIM-Viewer stellen Gebäudeinformationen dar, modellieren jedoch in der Regel keine editierbaren und sequenzierten Robotermissionen mit einem definierten bidirektionalen Austausch zwischen IFC-Datei und Missionseditor. Robotiksysteme arbeiten wiederum mit Posen, Frames und ausführbaren Aktionen, besitzen aber häufig keine semantisch strukturierte Verbindung zum Gebäudemodell.

---

# 3 Anforderungen und methodisches Vorgehen

## 3.1 Anwendungsszenarien

Beispielsweise:

* Tür öffnen
* Tür schließen
* Licht ein- oder ausschalten
* zu einem Gebäudeelement navigieren
* eine Öffnung durchqueren
* von einem Objekt zu einem anderen fahren
* vorhandene Mission aus einer IFC-Datei laden und ändern

## 3.2 Funktionale Anforderungen

* IFC-Datei laden
* Modell darstellen
* IFC-Objekt auswählen
* überlagernde Objekte unterscheiden
* Mission erstellen
* vorhandene Mission aus IFC rekonstruieren
* Tasks anlegen und anordnen
* Tasks mit IFC-Objekten verbinden
* Aktionsparameter und Zeitinformationen erfassen
* Mission validieren
* annotierte IFC-Datei exportieren
* exportierte Mission erneut laden
* vorhandene Annotation ersetzen statt duplizieren

## 3.3 Nichtfunktionale Anforderungen

* browserbasierte Ausführung
* performante Darstellung großer Modelle
* stabile IFC-Objektreferenzen
* Trennung von Domänenmodell und Rendering
* Erweiterbarkeit
* nachvollziehbare Validierungsfehler
* testbare Architektur
* idempotentes beziehungsweise duplikatfreies Exportverhalten
* Erhaltung relevanter IFC-Identitäten
* Schutz nicht vom Editor verwalteter IFC-Inhalte

## 3.4 Systemgrenzen

Weiterhin sinnvoll:

```text
Gebäudemodell und IFC-Annotation
            ↕
Editor und Missionsdomänenmodell
            ↓
spätere roboterspezifische Verarbeitung
```

Durch den Roundtrip ist der obere Datenfluss jetzt bewusst **bidirektional**.

## 3.5 Entwicklungsmethodik

* Proof-of-Concept-Ansatz
* iterative prototypische Entwicklung
* domänengetriebene Trennung der Komponenten
* testbasierte Prüfung zentraler Modellierungs- und Exportfunktionen
* schrittweise Erweiterung von Export → Import → Replacement → UI-Integration

## 3.6 Evaluationskriterien

* funktionale Vollständigkeit
* semantische Korrektheit
* IFC-Struktur
* Stabilität der Objektreferenzen
* Identitätserhalt
* Roundtrip-Stabilität
* Vermeidung von Duplikaten
* Auswahlqualität
* Lade- und Darstellungsperformance
* Robustheit gegenüber ungültigen Missionsgraphen

---

# 4 Konzeption des IFC-basierten Annotationsmodells

Dieses Kapitel sollte weiterhin den **fachlich-wissenschaftlichen Schwerpunkt** der Arbeit bilden. Der Roundtrip stärkt dieses Kapitel zusätzlich, da das entworfene Modell nicht nur geschrieben, sondern auch wieder eindeutig interpretiert werden muss.

## 4.1 Modellierungsziele

* Missionen und Tasks explizit repräsentieren
* Hierarchie und Ausführungsreihenfolge trennen
* IFC-Objekte nicht mit konkreten Aktionsanforderungen überladen
* Aktionen auf Task-Ebene modellieren
* stabile Objektidentität gewährleisten
* bidirektionale Rekonstruktion ermöglichen
* spätere Roboterausleitung ermöglichen

## 4.2 Internes Domänenmodell

Vorstellung von:

* `RobotMission`
* `RobotTask`
* `RobotTaskSequence`
* `RobotObjectReference`
* `RobotActionProperties`
* `RobotTaskTime`
* `RobotMissionSchedule`

Besonders wichtig bleibt:

```text
tasks
= hierarchisch enthaltene Schritte

sequences
= explizite zeitliche Abhängigkeiten
```

Diese Trennung sollte nun zusätzlich damit begründet werden, dass beide Strukturen beim IFC-Import eindeutig rekonstruierbar sein müssen. Die bestehende Kapitelstruktur sieht genau diese eigenständige Behandlung von Domänenmodell, Hierarchie und Sequenzen bereits vor. 

## 4.3 Modellierung der Roboteraktionen

* unterstützte Aktionsarten
* Bedeutung von `OPEN`, `MOVE`, `PASS_THROUGH` usw.
* Task als Träger der konkreten Aktion
* Objekt als statische Gebäuderessource
* Rekonstruktion der Aktionssemantik aus dem taskeigenen Property Set

Zentrale Modellierungsentscheidung:

```text
RobotInteractionCapability am Objekt
= Was wäre grundsätzlich möglich?

RobotAction am Task
= Was soll in diesem konkreten Schritt geschehen?
```

Die erste Ebene ist weiterhin nur eine geplante Erweiterung. Die konkrete `RobotAction` am Task ist implementiert. 

## 4.4 Referenzierung von IFC-Objekten

* primäre Verwendung der `GlobalId`
* modelllokaler Fallback über `modelId + expressId`
* Abgrenzung zu Fragment- oder Rendering-IDs
* Verhalten bei fehlenden und mehrdeutigen Referenzen
* `modelId` zur Roundtrip-Quellzuordnung
* Ablehnung modellfremder Referenzen beim Export

## 4.5 Missionshierarchie und Task-Sequenzen

* Parent-Task für die Mission
* Child-Tasks für ausführbare Schritte
* `IfcRelNests` für Hierarchie
* `IfcRelSequence` für zeitliche Abhängigkeit
* `FINISH_START` als Standardbeziehung
* stabile Sequenz-ID
* Speicherung der Domain-Sequenz-ID in `IfcRelSequence.Name`

## 4.6 Zuordnung von Tasks zu Gebäudeelementen

Behandlung der Rollen:

* `OPERATES_ON`
* `AFFECTS`
* `PASSES_THROUGH`
* `NAVIGATES_TO`
* `MOVE_FROM`
* `MOVE_TO`

Die Zuordnungen müssen sowohl in Richtung Domain → IFC als auch IFC → Domain eindeutig interpretiert werden.

## 4.7 Eigene Property Sets

* `RobotAction`
* `RobotTask`
* `RobotMission`
* Begründung, weshalb kein reservierter `Pset_`-Präfix verwendet wird
* `ActionType`
* `TargetState`
* `RequiredCapability`
* Preconditions
* Postconditions
* `AnnotationSchemaVersion`
* `HasExplicitSchedule`

Die beiden zuletzt genannten Properties sind für Kompatibilität und Roundtrip inzwischen besonders relevant.

## 4.8 Zeitmodell

* direkte Zuordnung zu `IfcTaskTime`
* geplante und tatsächliche Zeiten
* Dauer
* Fertigstellungsgrad
* `IfcWorkSchedule`
* Unterscheidung zwischen explizitem Domänen-Schedule und technisch erzeugter Schedule-Infrastruktur

## 4.9 Abbildung des Domänenmodells auf IFC

Weiterhin bietet sich eine Mapping-Tabelle an:

| Domänenkonzept            | IFC-Abbildung               |
| ------------------------- | --------------------------- |
| `RobotMission`            | Parent-`IfcTask`            |
| `RobotTask`               | Child-`IfcTask`             |
| Missionshierarchie        | `IfcRelNests`               |
| Task-Abhängigkeit         | `IfcRelSequence`            |
| Missionsplan              | `IfcWorkSchedule`           |
| Task-Zeit                 | `IfcTaskTime`               |
| direkte Objektinteraktion | `IfcRelAssignsToProcess`    |
| MOVE-Ziel                 | `IfcRelAssignsToProduct`    |
| Aktionssemantik           | `RobotAction`-Property-Set  |
| Task-Metadaten            | `RobotTask`-Property-Set    |
| Missions-/Versionsdaten   | `RobotMission`-Property-Set |

Zusätzlich sollte nun die **inverse Abbildung IFC → Domänenmodell** erläutert werden.

## 4.10 Validierungsmodell

* syntaktische Validierung
* semantische Aktionsvalidierung
* Referenzvalidierung
* Sequenz- und Zyklusprüfung
* Fehler gegenüber Warnungen
* Export nur bei gültigen Missionen
* Validierung importierter Missionsgraphen
* partielle Importierbarkeit unabhängiger gültiger Missionen
* unsichere Quelle bei fehlerhaften eigenen Annotationen

## 4.11 Persistenz- und Austauschkonzept

Die Entscheidung kann nun wesentlich stärker formuliert werden:

```text
Kanonischer fachlicher Träger:
annotierte IFC-Datei

Laufzeitmodell:
internes TypeScript-Domänenmodell

Bearbeitungszyklus:
IFC ↔ Domänenmodell

Roboterspezifische Ausleitung:
späteres Robot-JSON

Editorzustand:
localStorage oder später Backend
```

Die früher als technische Voraussetzung formulierte Forderung, dass ein IFC-Parser die Mission vollständig rekonstruieren und Roundtrip-Tests erfolgreich sein müssen, ist inzwischen für die RobotMission-Annotation umgesetzt. 

Hier sollte der Roundtrip detailliert behandelt werden:

```text
annotierte IFC
    ↓ Import
RobotMission
    ↓ Bearbeitung
RobotMission'
    ↓ Replacement-Export
annotierte IFC'
    ↓ Reimport
RobotMission''
    ↓
semantischer Vergleich
```

## 4.12 Grenzen des Annotationsmodells

* projektspezifische Robotiksemantik
* Interpretation durch generische IFC-Viewer
* Schema- und Toolunterstützung
* Legacy-Kompatibilität
* Teilflächenreferenzen
* Änderungen am zugrunde liegenden Gebäudemodell
* kein allgemeiner IFC-Struktur-Roundtrip
* keine automatische Robot-Pose

**Nicht mehr als Grenze nennen:** fehlender Missionsimport oder fehlender Missions-Roundtrip.

---

# 5 Entwurf und Implementierung des browserbasierten Editors

Die Trennung bleibt sinnvoll:

* Kapitel 4: **Was wird modelliert?**
* Kapitel 5: **Wie wird es technisch umgesetzt?**

## 5.1 Gesamtarchitektur

Die bisherige Darstellung sollte um Import und Roundtrip-Koordination ergänzt werden:

```text
                    Benutzeroberfläche
                           ↓
                   Application Service
                           ↓
                  RobotMission-Domäne
                    ↙             ↘
             Persistenz        IFC-Mapping
                                  ↓
                          Import / Replacement
                                  ↓
                           IFC-Quelldatei
```

Zusätzlich:

```text
IFC → Fragments → Viewer-Auswahl → RobotObjectReference
```

und:

```text
IFC → Mission Reader → RobotMission
```

## 5.2 Verwendete Technologien

* TypeScript und Vite
* Three.js
* That Open Components
* That Open Fragments
* `web-ifc`
* That Open UI

## 5.3 Modellimport und Rendering

* Auswahl lokaler IFC- und `.frag`-Dateien
* IFC-zu-Fragments-Konvertierung
* Registrierung des geladenen Modells
* Speicherung beziehungsweise Aktualisierung der IFC-Quellbytes
* Missionsimport nach erfolgreichem Modellladen
* Kamera, Grid, Ambient Occlusion, Kanten und LOD

Ein wichtiger Punkt ist die Reihenfolge:

```text
IFC laden
→ Quellbytes registrieren
→ Fragments erzeugen
→ Mission importieren
→ Repository aktualisieren
```

## 5.4 Auswahl von IFC-Objekten

Weiterhin relativ ausführlich behandeln:

* workerbasierte Raycasts
* mehrere Treffer
* Entfernungssortierung
* Deduplizierung
* Kandidatenvorschau
* explizite Bestätigung
* Tastatursteuerung
* Filter
* getrennte Hover-, Kandidaten- und Bestätigungshervorhebung
* Vermeidung veralteter asynchroner Ergebnisse

## 5.5 Überführung der Auswahl in eine fachliche Referenz

* Auflösen von `GlobalId`, `expressId`, IFC-Klasse und Name
* Trennung Viewerauswahl ↔ Task-Zuweisung
* Source-`modelId`
* Behandlung nicht dauerhaft referenzierbarer Objekte
* Verwendung derselben Referenzstruktur beim späteren Reimport

## 5.6 Bedienablauf zur Missionsannotation

Aktualisierter vollständiger Workflow:

```text
IFC laden
   ↓
vorhandene Missionen rekonstruieren
   ↓
Mission auswählen oder erstellen
   ↓
Task hinzufügen / bearbeiten
   ↓
Aktion auswählen
   ↓
IFC-Objekt auswählen und bestätigen
   ↓
Objektrolle zuweisen
   ↓
Zeit und Reihenfolge festlegen
   ↓
Mission validieren
   ↓
IFC exportieren
   ↓
Export intern erneut importieren und prüfen
```

## 5.7 Missions- und Task-Editor

* Missionsverwaltung
* importierte Missionen bearbeiten
* Task-Karten
* Aktionsauswahl
* Objektrollen
* MOVE-Start und MOVE-Ziel
* Zeitinformationen
* Task-Reihenfolge
* Validierungsfeedback

## 5.8 Speicherung während der Bearbeitung

* In-Memory-Modus
* `localStorage`
* Auswahl des Persistenzmodus
* bewusste Nichtverfügbarkeit des Backends
* Source-Association
* Unterschied zwischen Editorzustand und fachlichem IFC-Inhalt
* Wechsel des Storage-Modus und dessen Auswirkungen auf die Quellzuordnung

## 5.9 IFC-Exportpipeline

Dieses Unterkapitel sollte jetzt zum **IFC-Roundtrip** erweitert werden:

```text
IFC-Quelle
    ↓
bestehende eigene Missionsgraphen erkennen
    ↓
Provenienz und Identitäten bestimmen
    ↓
aktuelles Missionsmodell validieren
    ↓
IFC-Record-Mapper
    ↓
Preflight des Replacement
    ↓
alten eigenen Missionsgraph ersetzen
    ↓
IFC speichern
    ↓
frische web-ifc-Instanz
    ↓
Mission erneut importieren
    ↓
semantisch vergleichen
    ↓
verifizierte Bytes als neue Quelle übernehmen
```

Der Export ist damit keine reine Append-Operation mehr. Der aktuelle Missionszustand ist für das jeweilige Quellmodell autoritativ; gelöschte Missionen können entfernt, veränderte ersetzt und neue ergänzt werden. Wiederholte Exportzyklen sollen keine Duplikate akkumulieren.

## 5.10 Tests und Qualitätssicherung

* Tests des Domänenmodells
* Validierungstests
* Persistenztests
* Auswahltests
* Mappingtests
* Reader-Tests
* Writer-Tests
* Replacement-Tests
* semantische Vergleichstests
* Roundtrip-Coordinator-Tests
* Exportintegrationstests
* mehrfache Import-/Edit-/Export-Zyklen

Die Testsuite enthält hierfür inzwischen eigene Dateien wie `ifc-mission-reader.test.ts`, `ifc-mission-replacement.integration.test.ts`, `ifc-mission-roundtrip-coordinator.test.ts` und `robot-mission-semantic-comparison.test.ts`.

## 5.11 Aktuelle Einschränkungen des Editors

Weiterhin:

* keine Backend-Anbindung
* keine Teilflächenauswahl
* keine automatische Robot-Pose
* kein Robot-JSON-Export
* keine direkte ROS-Kommunikation
* kein allgemeines Zurückschreiben struktureller Fragments-/IFC-Änderungen
* keine allgemeine IFC-Authoring-Funktionalität
* Viewpoint-Task-Integration nur teilweise

**Streichen:** „kein Import vorhandener Missionsannotation“.

---

# 6 Evaluation

Durch den neuen Stand gewinnt dieses Kapitel deutlich an Bedeutung.

## 6.1 Versuchsaufbau

* verwendete IFC-Testmodelle
* Dateigröße und Elementanzahl
* Browser und Hardware
* Messmethodik
* definierte Beispielmissionen
* annotierte Ausgangsdateien für Roundtrip-Tests

## 6.2 Funktionale Evaluation

Prüfung typischer Szenarien:

1. Tür auswählen und `OPEN`-Task erzeugen
2. mehrere überlagernde Objekte unterscheiden
3. MOVE-Task mit Start und Ziel erzeugen
4. mehrere Tasks sequenzieren
5. ungültige Mission erkennen
6. Mission in IFC exportieren
7. exportierte IFC-Datei erneut laden
8. rekonstruierte Mission bearbeiten
9. erneut exportieren
10. Mission löschen und Removal prüfen

## 6.3 Evaluation des Annotationsmodells

* werden alle benötigten Missionsinformationen abgebildet?
* bleiben Hierarchie und Reihenfolge unterscheidbar?
* können dieselben Objekte in unterschiedlichen Tasks verwendet werden?
* bleiben Aktionsdaten auf Task-Ebene?
* sind Referenzen eindeutig?
* ist das Modell auch invers aus IFC rekonstruierbar?

## 6.4 Prüfung der exportierten IFC-Datei

* enthaltene `IfcTask`-Entitäten
* `IfcRelNests`
* `IfcRelSequence`
* Objektzuweisungen
* Property Sets
* Task-Zeitinformationen
* `IfcWorkSchedule`
* Annotation Schema Version
* erneutes Öffnen der Datei
* Rekonstruktion des Domänenmodells
* semantischer Vergleich
* Erhaltung des Ausgangsmodells
* Abwesenheit veralteter eigener Annotationen

Im Unterschied zur ursprünglichen Fassung ist die Rekonstruktion heute nicht mehr nur ein Prüfkonzept: Sie ist Teil des implementierten Roundtrip-Workflows.

## 6.5 Performance-Evaluation

Mögliche Messgrößen:

* Ladezeit
* IFC-zu-Fragments-Konvertierungszeit
* Missionsimportzeit
* Zeit bis zur ersten Darstellung
* Bildrate
* Reaktionszeit der Auswahl
* Speicherverbrauch
* Exportzeit
* Reimport-/Verifikationszeit

## 6.6 Evaluation der Objektauswahl

* Trefferquote
* Anzahl angebotener Kandidaten
* benötigte Interaktionsschritte
* Verhalten bei Wänden, Türen, Öffnungen und Räumen
* Vergleich mit einfacher Auswahl des nächstgelegenen Raycast-Treffers

## 6.7 Diskussion der Ergebnisse

* erfüllte Anforderungen
* nicht erfüllte Anforderungen
* Roundtrip-Stabilität
* Grenzen der Interoperabilität
* Übertragbarkeit
* interne und externe Validität
* technische Risiken

---

# 7 Weiterführende Konzeption: Vom IFC-Modell zur Robotermission

Dieser Bereich bleibt überwiegend **zukünftige beziehungsweise konzeptionelle Arbeit**.

## 7.1 Verarbeitungskette

Jetzt sinnvollerweise:

```text
annotierte IFC-Datei
        ↓
RobotMission-Domänenmodell
        ↓
roboterspezifischer Export
        ↓
Koordinatentransformation
        ↓
Zielposen und Waypoints
        ↓
Pfadplanung
        ↓
Roboterausführung
```

Die erste Transformation `IFC ↔ RobotMission-Domänenmodell` ist inzwischen umgesetzt. Die nachgelagerten Robotikschritte sind es noch nicht.

## 7.2 Roboterspezifisches Exportformat

Konzeption eines `mission.robot.json` mit:

* Missionsmetadaten
* Task-IDs
* Sequenz
* Aktionsart
* IFC-Zielobjekten
* Zielposen
* Koordinatenrahmen
* Aktionsparametern
* Vor- und Nachbedingungen

Das Robot-JSON sollte weiterhin als **abgeleitetes Ausführungsformat** und nicht als zweite fachliche Hauptdatenquelle verstanden werden. 

## 7.3 Positionen von IFC-Objekten

* `IfcLocalPlacement`
* verkettete Transformationen
* Objektursprung
* geometrischer Mittelpunkt
* Oberflächenpunkt
* Roboter-Anfahrpose

Weiterhin klar unterscheiden:

```text
ObjectPlacement
= IFC-Verankerung

ReferencePoint
= geometrisch abgeleiteter Punkt

NavigationTarget
= tatsächlich anzufahrende Roboterpose
```

Diese Unterscheidung wird durch die Analyse der IFC-Geometrie beziehungsweise Placements gestützt. 

## 7.4 Transformation in das Roboterkoordinatensystem

* IFC-lokales Koordinatensystem
* Gebäudekarte
* ROS-`map`-Frame
* Translation und Rotation
* Einheiten
* Kalibrierung beziehungsweise Registrierung

## 7.5 Generierung von Anfahrposen und Waypoints

* Offset vor einer Tür
* Orientierung zur Tür
* Eintritts- und Austrittspunkt
* Position vor einem Lichtschalter
* erreichbare Manipulationspose
* Roboterabmessungen

## 7.6 Ableitung einer 2D-Navigationsdarstellung

* Geschossauswahl
* begehbare Flächen
* Hindernisse
* Türen und Durchgänge
* Occupancy Grid
* Navigation Mesh
* Pfadplanung

## 7.7 Abbildung semantischer Aktionen auf Roboterfähigkeiten

Beispiel:

```text
OPEN
→ Navigation zur Anfahrpose
→ Griff lokalisieren
→ Manipulationsaktion
→ Erfolg prüfen
```

---

# 8 Erweiterungsmöglichkeiten

## 8.1 Erweiterung des IFC-Roundtrips

Dieses Unterkapitel ersetzt inhaltlich die frühere Idee **„Import annotierter IFC-Dateien“**, da dieser Import inzwischen umgesetzt ist.

Zukünftige Erweiterung ist nun:

* Roundtrip beliebiger IFC-Properties
* strukturelle Bauteiländerungen
* Geometrieänderungen
* neu erzeugte oder gelöschte Gebäudeelemente
* Zurückschreiben von Änderungen aus Fragments
* allgemeine IFC-Editor-Funktionalität
* Migration von Missionen auf neue Revisionen eines Gebäudemodells

Die Abgrenzung zwischen RobotMission-Roundtrip und allgemeinem IFC-Roundtrip sollte hier ausdrücklich diskutiert werden.

## 8.2 Vorannotation interaktionsfähiger IFC-Objekte

Objekte könnten zukünftig mit `RobotInteractionCapability` gekennzeichnet werden:

* `SupportedActions`
* `RequiredCapability`
* `ManipulationTarget`
* `SelectionPriority`
* `RequiresApproachPose`

Dadurch könnte der Editor irrelevante Bauteile bei der Auswahl ignorieren. Dieses Konzept ist bislang nicht Bestandteil der Implementierung. 

## 8.3 Auswahl von Teilflächen

Für große Objekte wie Wände kann ein virtuelles Raster beziehungsweise Surface Tiling verwendet werden.

* unveränderte IFC-Wand als Host-Objekt
* lokales Flächenkoordinatensystem
* beispielsweise 30 × 30 cm große Rasterzellen
* dauerhafte Beschreibung über Host-`GlobalId`, Rasterursprung, Achsen, Zeile und Spalte
* keine dauerhafte Referenz auf Rendering-Dreiecke

Das Konzept sieht ausdrücklich vor, die Wand nicht künstlich in viele IFC-Bauteile zu zerlegen. 

## 8.4 Backend-Architektur

* serverseitige IFC-Verarbeitung
* Validierung
* Missionsspeicherung
* Versionierung
* Vorverarbeitung großer IFC-Dateien
* Rechteverwaltung
* API für Robotersysteme

## 8.5 Weitere Erweiterungen

* Multi-Robot-Missionen
* parallele Task-Abhängigkeiten
* bedingte Abläufe
* Ressourcen- und Fähigkeitszuweisung
* Live-Status des Roboters
* Visualisierung geplanter Pfade
* Rückschreiben von Ausführungsergebnissen
* BCF-Integration
* Multiuser-Bearbeitung
* automatisches Rebinding bei geänderten Gebäudemodellen

---

# 9 Fazit und Ausblick

## 9.1 Zusammenfassung

Jetzt sollten mindestens folgende Beiträge zusammengefasst werden:

* entwickeltes Annotationsmodell
* prototypischer browserbasierter Editor
* verbesserte Objektauswahl
* IFC-Mapping
* Missionsimport
* quellgestützter Replacement-Export
* vollständiger RobotMission-Roundtrip
* semantische Roundtrip-Verifikation

## 9.2 Beantwortung der Forschungsfragen

Die Forschungsfragen sollten einzeln und explizit beantwortet werden.

Insbesondere kann der Roundtrip nun als **implementiertes Ergebnis** und nicht nur als Ausblick behandelt werden.

## 9.3 Grenzen

* PoC-Charakter
* keine physische Roboterausführung
* projektspezifische Aktionssemantik
* begrenzte Interpretation durch generische IFC-Werkzeuge
* kein allgemeiner struktureller IFC-Roundtrip
* keine Teilflächenannotation
* keine automatische Ableitung von Navigation Targets

## 9.4 Ausblick

Überleitung zu:

* Robot-JSON
* ROS-Anbindung
* Waypoint-Generierung
* Surface Tiling
* `RobotInteractionCapability`
* Backend
* realen Roboterversuchen
* Erweiterung des Roundtrips auf weitere IFC-Bearbeitungen

---

# Empfohlene Gewichtung

Die Gewichtung der ursprünglichen Struktur würde ich **nahezu unverändert** lassen:

| Kapitel                                   | Ungefährer Anteil |
| ----------------------------------------- | ----------------: |
| Einleitung                                |             7–9 % |
| Grundlagen und Stand der Forschung        |           15–18 % |
| Anforderungen und Methodik                |            8–10 % |
| Annotationsmodell                         |           18–22 % |
| Editor und Implementierung                |           20–25 % |
| Evaluation                                |           15–20 % |
| IFC-to-Robot-Konzeption und Erweiterungen |            8–12 % |
| Fazit                                     |             4–6 % |

Die grundlegende Empfehlung aus der ersten Antwort bleibt damit bestehen:

> **Annotationsmodell und Editor sollten zwei getrennte Hauptkapitel sein.** Das Annotationsmodell ist der fachlich-wissenschaftliche Beitrag. Der Editor einschließlich des inzwischen implementierten IFC-Missionsroundtrips ist die prototypische technische Realisierung und Validierungsumgebung dieses Modells.

Die wichtigste Änderung gegenüber der ursprünglichen Antwort lautet: **Der Missionsimport und der RobotMission-Roundtrip dürfen nicht mehr als zukünftige Erweiterung beschrieben werden.** Sie sind jetzt Teil der implementierten Lösung und sollten entsprechend in **Kapitel 4 (Konzept), Kapitel 5 (Implementierung) und Kapitel 6 (Evaluation)** behandelt werden. Der Ausblick sollte sich stattdessen auf den **allgemeinen strukturellen IFC-Roundtrip** sowie die nachgelagerte Überführung der Mission in roboterspezifische Navigations- und Ausführungsdaten konzentrieren.

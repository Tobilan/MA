Ich habe die eingefügte Aufgabenfassung als verbindlichen Arbeitsauftrag verwendet. 

## A. Recherche- und Implementierungsnotiz

* Die Strukturübersicht wurde zuerst zur Abgrenzung verwendet. Für Kapitel 5 gilt die Leitfrage **„Wie wird das in Kapitel 4 entworfene Modell technisch umgesetzt?“**; Details zu Technologien, Import, Auswahl, UI, Speicherung, Roundtrip und Tests folgen erst in 5.2–5.10. 
* Die Repository-Map beschreibt den Stand `674ede3` und weist ausdrücklich eine geschichtete, an Ports und Adaptern orientierte Architektur aus.
* Der aktuelle `main`-Branch des Editor-Repositories steht weiterhin auf `674ede3bf2e7e6cf466bc4c16fe06c90fbb1753c`. Es besteht daher **keine Commit-Abweichung** zur Repository-Map.
* Die Zusammenschaltung von Viewer, Auswahl, Missionsservice, Persistenz, IFC-Import/-Export und Roundtrip wurde am zentralen Anwendungseinstieg überprüft.
* Das Missionsmodell ist tatsächlich von Viewer und IFC-Serialisierung getrennt; insbesondere gehören Aktionssemantik und Objektbezüge zum fachlichen Task-Modell und nicht zur Rendering-Geometrie.
* Die Anwendungsschicht koordiniert Missionsänderungen über eine Persistenzschnittstelle und enthält ausdrücklich keine Viewer-, `localStorage`- oder IFC-Serialisierungslogik.
* Die Viewer-Auswahl wird über eine eigene Adapterebene aufgelöst und kann eine bestätigte Auswahl als stabile fachliche IFC-Objektreferenz bereitstellen.
* Im Missionseditor wird diese bestätigte Referenz anschließend einem Task zugeordnet; die UI schreibt dabei nicht direkt in IFC.
* Persistenz im Arbeitsspeicher und über `localStorage` ist umgesetzt. Eine Backend-Option existiert nur als ausdrücklich nicht verfügbarer Platzhalter.
* Direkt geladene IFC-Dateien werden sowohl für die Fragments-Darstellung als auch als separate IFC-Quelle registriert; anschließend können vorhandene Missionsannotationen rekonstruiert werden. Reine `.frag`-Modelle besitzen diese Roundtrip-Grundlage nicht.
* Der Export ist quellgestützt und lehnt allgemeine strukturelle Fragments-Änderungen ab, für die keine zuverlässige Rückabbildung nach IFC besteht.
* Der RobotMission-Roundtrip ist umgesetzt: Exportierte Daten werden erneut importiert und mit dem vorgesehenen Missionszustand verglichen, bevor sie als neue IFC-Quelle übernommen werden.
* Im Repository wurde kein verlässlicher vorhandener Editor-Screenshot gefunden. Daher wird unten kein künstlicher Screenshot erzeugt, sondern eine konkrete Aufnahmeanweisung vorgeschlagen.

## B. Kapitel 5.1

# 5.1 Gesamtarchitektur

Das in Kapitel 4 entwickelte Annotationsmodell bildet die fachliche Grundlage für die Beschreibung von Robotermissionen, einzelnen Aufgaben, deren Reihenfolge sowie den Bezügen zu Elementen eines IFC-Gebäudemodells. Für die prototypische Umsetzung ist darüber hinaus eine Softwarearchitektur erforderlich, die diese fachlichen Strukturen mit einer interaktiven dreidimensionalen Gebäudedarstellung und dem Austausch über IFC verbindet. Der entwickelte browserbasierte Editor übernimmt diese Vermittlungsfunktion. Auf der einen Seite arbeitet der Benutzer unmittelbar mit dem dargestellten Gebäude, beispielsweise indem eine Tür ausgewählt und einer Roboteraufgabe zugeordnet wird. Auf der anderen Seite werden Missionen und Tasks in einem von der Darstellung getrennten fachlichen Modell bearbeitet. Die sichtbare Geometrie eines Bauteils wird somit nicht selbst Bestandteil der Missionsbeschreibung, sondern dient als interaktiver Zugang zu dem zugrunde liegenden IFC-Objekt.

Die Gesamtarchitektur ist hierzu in mehrere Verantwortungsbereiche gegliedert. Auf der äußeren Ebene befinden sich die Benutzeroberfläche und die dreidimensionale Darstellung des Gebäudemodells. Darunter vermitteln Viewer- und Auswahlkomponenten zwischen der sichtbaren Geometrie und fachlich verwendbaren IFC-Objektreferenzen. Die Bearbeitung von Missionen erfolgt in einer davon unabhängigen Anwendungs- und Domänenschicht. Persistenzkomponenten stellen den Missionszustand während der Bearbeitung bereit, während eine gesonderte IFC-Infrastruktur für Import, Abbildung und Export der Missionsannotation zuständig ist. Abbildung 5.x kann diese Bereiche und ihre wesentlichen Datenflüsse zusammenfassend darstellen. Die Trennung verhindert insbesondere, dass Darstellungsbibliotheken, Benutzeroberfläche und IFC-Serialisierung unmittelbar miteinander vermischt werden.

Die Benutzeroberfläche stellt sowohl das dreidimensionale Gebäudemodell als auch die Werkzeuge zur Missionsbearbeitung bereit. Für die Gebäudedarstellung wird das geladene IFC-Modell in eine für das browserbasierte Rendering geeignete Fragments-Repräsentation überführt. Diese Repräsentation unterstützt die performante Visualisierung und die Interaktion mit den dargestellten Elementen. Der Viewer übernimmt damit Aufgaben wie Darstellung, Hervorhebung und räumliche Auswahl. Er ist jedoch nicht für die fachliche Interpretation einer Robotermission verantwortlich. Ebenso erzeugt eine Auswahl im 3D-Modell nicht unmittelbar eine IFC-Annotation. Sie stellt zunächst lediglich fest, welches dargestellte Element der Benutzer adressieren möchte.

Zwischen dieser visuellen Auswahl und dem Missionsmodell liegt eine eigene Adapterebene. Ihre Aufgabe besteht darin, eine Auswahl aus der Rendering-Repräsentation auf die verfügbaren IFC-Metadaten zurückzuführen und daraus eine fachlich verwendbare Objektbeschreibung abzuleiten. Für ein ausgewähltes Gebäudeelement können dadurch beispielsweise dessen IFC-Klasse, Name und stabile Identifikation ermittelt werden. Erst diese Beschreibung wird an die Missionsbearbeitung weitergegeben. Der zentrale Datenfluss lautet damit vereinfacht: sichtbares Bauteil im 3D-Modell, Benutzerauswahl, Auflösung des zugrunde liegenden IFC-Objekts und schließlich Übernahme einer fachlichen Referenz in einen RobotTask. Die Rendering-Identität eines geometrischen Elements bleibt dadurch von der dauerhaft relevanten Referenz auf das Gebäudemodell getrennt.

Die eigentliche Missionsbearbeitung erfolgt in der Anwendungs- und Domänenschicht. Dort werden Missionen, Tasks, Aktionen, Objektbezüge, zeitliche Angaben und Abhängigkeiten verwaltet. Diese Ebene ist unabhängig davon aufgebaut, ob das Gebäude mit Three.js beziehungsweise That Open Components dargestellt wird und wie die Missionsinformation später als IFC-STEP serialisiert wird. Die Anwendungslogik koordiniert Änderungen am Missionsmodell und greift über abstrahierte Schnittstellen auf den jeweiligen Speicher zu. Dadurch kann die fachliche Logik beispielsweise unabhängig von einem geöffneten 3D-Viewer validiert und getestet werden. Gleichzeitig verhindert diese Trennung, dass eine Benutzeroberflächenaktion unmittelbar komplexe Änderungen an IFC-Entitäten ausführen muss.

Für die Speicherung während einer Editorsitzung stehen unterschiedliche lokale Varianten zur Verfügung. Missionen können ausschließlich für die aktuelle Sitzung im Arbeitsspeicher gehalten oder optional im Browser gespeichert werden. Eine funktionsfähige Backend-Persistenz ist im Prototyp nicht vorhanden. Diese Speicherung während der Bearbeitung ist von der Rolle der annotierten IFC-Datei zu unterscheiden. Der lokale Speicher stellt den aktuellen Arbeitszustand des Missionsmodells bereit, während die IFC-Datei den Austausch der Missionsannotation gemeinsam mit dem Gebäudemodell ermöglicht. Damit wird die IFC-Datei nicht zum unmittelbaren Zustandsmodell der Benutzeroberfläche; Änderungen werden zunächst im internen Missionsmodell durchgeführt und erst im Rahmen eines expliziten Exports auf die IFC-Repräsentation abgebildet.

Eine wesentliche Architekturentscheidung besteht darin, das geladene IFC-Modell auf zwei miteinander verbundenen, aber funktional unterschiedlichen Datenpfaden zu verarbeiten. Der erste Pfad dient der Darstellung und Auswahl. Aus den IFC-Daten entsteht eine für das Rendering optimierte Fragments-Repräsentation, aus der das dreidimensionale Gebäudemodell erzeugt wird. Wählt der Benutzer darin ein Bauteil aus, wird dieses über die Viewer-Adapter wieder auf eine fachliche IFC-Objektreferenz zurückgeführt. Der zweite Pfad dient der Missionsannotation und dem Roundtrip. Dafür werden bei direkt geladenen IFC-Dateien die ursprünglichen IFC-Daten unabhängig von der Rendering-Repräsentation vorgehalten. Aus ihnen können bereits vorhandene RobotMission-Annotationen rekonstruiert beziehungsweise neue oder veränderte Annotationen wieder in eine IFC-Datei geschrieben werden. Fragments sind somit primär für Darstellung und Interaktion zuständig, während die IFC-Quelldaten die Grundlage für den verlässlichen Austausch der Missionsinformation bilden.

Der Zusammenhang lässt sich am Beispiel eines Tasks zum Öffnen einer Tür veranschaulichen. Nach dem Laden eines Gebäudemodells sieht der Benutzer die Tür als Bestandteil des dreidimensionalen Gebäudes und wählt sie im Viewer aus. Die Auswahl wird anschließend auf das zugrunde liegende IFC-Objekt zurückgeführt und als fachliche Objektreferenz bestätigt. Diese Referenz kann einem Task mit der Aktion „Tür öffnen“ zugeordnet werden. Im Missionsmodell werden Aktion, Objektbezug und Ausführungsreihenfolge verwaltet, ohne dass dafür die dargestellte Türgeometrie in den Task übernommen werden muss. Beim späteren IFC-Export wird die fachliche Mission wieder mit der zugehörigen IFC-Quelldatei verbunden. Die resultierende Datei enthält damit weiterhin das Gebäude und zusätzlich die Missionsannotation. Ein Editor-Screenshot, der dieselbe hervorgehobene Tür und den zugehörigen Task unmittelbar nebeneinander zeigt, eignet sich besonders, um diesen Übergang zwischen Gebäudedarstellung und fachlicher Annotation sichtbar zu machen.

Der IFC-Austausch ist als Roundtrip der projekteigenen RobotMission-Annotationen ausgeführt. Eine bereits annotierte IFC-Datei kann eingelesen werden, worauf die enthaltenen Missionsstrukturen in das interne Domänenmodell rekonstruiert werden. Nach der Bearbeitung erfolgt erneut die Abbildung auf die IFC-Quelldaten. Das Exportergebnis wird anschließend wieder eingelesen und mit dem beabsichtigten Missionszustand abgeglichen, bevor es als Grundlage für einen weiteren Bearbeitungszyklus verwendet wird. Damit unterstützt die Architektur einen wiederholbaren Zyklus aus Import, Bearbeitung und Export. Diese Funktion ist jedoch ausdrücklich auf die vom Editor verwalteten Missionsannotationen beschränkt. Der Prototyp ist kein allgemeiner verlustfreier IFC-Editor für beliebige Änderungen an Bauteilgeometrie oder Gebäudestruktur.

Durch die Trennung von Rendering, Auswahladaption, Anwendungslogik, Domänenmodell, Persistenz und IFC-Infrastruktur bleiben die jeweiligen Verantwortlichkeiten klar abgegrenzt. Technische Komponenten des Viewers können verändert werden, ohne das fachliche Missionsmodell grundsätzlich neu zu entwerfen; umgekehrt lässt sich die Missionslogik unabhängig von der dreidimensionalen Darstellung prüfen. Gleichzeitig verbindet die Architektur die abstrakte Aufgabenbeschreibung mit konkreten Elementen des Gebäudemodells und ermöglicht deren Austausch über annotierte IFC-Dateien. Die folgenden Abschnitte vertiefen diese Gesamtstruktur, indem zunächst die eingesetzten Technologien und anschließend Modellimport, Rendering, Objektauswahl sowie die weiteren Implementierungsbereiche des Editors betrachtet werden.

## C. Abbildungen

### Abbildung 1 – Gesamtarchitektur

**Position:** nach dem zweiten Absatz von Kapitel 5.1.

**Empfohlener Aufbau:**

```text
                        Browserbasierter Editor
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  Missionseditor                         3D-Gebäudemodell      │
│        │                                      │              │
│        │                               Benutzerauswahl        │
│        │                                      │              │
│        │                              Viewer-/Auswahladapter  │
│        │                                      │              │
│        │                            IFC-Objektreferenz         │
│        │                                      │              │
│        └───────────────┬──────────────────────┘              │
│                        ▼                                     │
│                 Anwendungslogik                              │
│                        │                                     │
│                 Missionsmodell                               │
│                  ↙             ↘                             │
│          lokale Persistenz     IFC-Infrastruktur             │
│                                      ↕                       │
└──────────────────────────────────────┼───────────────────────┘
                                       ↕
                               IFC-Quelldatei
                                  │
                                  └────→ Fragments
                                           │
                                           └────→ 3D-Darstellung
```

Die endgültige Grafik würde ich gegenüber diesem ASCII-Schema noch vereinfachen: Die IFC-Quelldatei unten, darüber zwei klar erkennbare Pfade „Darstellung und Auswahl“ sowie „Missionsannotation und Roundtrip“, die sich am internen Missionsmodell beziehungsweise der Objektreferenz verbinden.

**Bildunterschrift:**
*„Schematische Gesamtarchitektur des browserbasierten IFC-Missionseditors und zentrale Datenflüsse zwischen Gebäudemodell, Missionsdomäne und IFC-Persistenz.“*

**Zweck:** Die Architektur erklären und insbesondere sichtbar machen, dass Fragments-Darstellung und IFC-Quelldaten unterschiedliche Funktionen besitzen.

**Kennzeichnung:** *Eigene Darstellung.*

---

### Abbildung 2 – Editor-Screenshot mit Gebäude-/Task-Bezug

**Position:** unmittelbar nach dem Absatz mit dem Beispiel „Tür öffnen“.

Ich würde hier **keine schematisch erzeugte Benutzeroberfläche verwenden**, sondern einen echten Screenshot des implementierten Editors aufnehmen.

**Aufnahmeanweisung:**

* Ein überschaubares Geschoss oder einen Gebäudeausschnitt laden, nicht das komplette Gebäude aus großer Entfernung.
* Kamera schräg von oben beziehungsweise in einer leicht perspektivischen Innenansicht positionieren, sodass eine konkrete Tür und ihre räumliche Einordnung in Wand und Raum gut erkennbar sind.
* Genau diese Tür im Viewer auswählen und den **bestätigten Hervorhebungszustand** anzeigen.
* Gleichzeitig das Panel „Robot Missions“ geöffnet lassen.
* Darin einen Task mit einem verständlichen Namen wie **„Tür öffnen“** und Aktion `OPEN` sichtbar machen.
* In der Objektzuordnung sollte nach Möglichkeit der Name beziehungsweise die IFC-Klasse der ausgewählten Tür erkennbar sein.
* Unwichtige Panels, Debuginformationen und weitere Werkzeuge schließen, damit Gebäude und Missionsbezug dominieren.

Anschließend nur drei dezente Callouts ergänzen:

```text
① ausgewähltes IFC-Bauteil
        │
        ▼
② aufgelöste Objektzuordnung
        │
        ▼
③ RobotTask „Tür öffnen“
```

**Bildunterschrift:**
*„Zuordnung eines im IFC-Gebäudemodell ausgewählten Bauteils zu einer Roboteraufgabe im Missionseditor.“*

**Zweck:** Direkt zeigen, dass die Annotation nicht abstrakt neben dem BIM-Modell existiert, sondern sich auf ein konkret sichtbares Gebäudeelement bezieht.

**Kennzeichnung:** *Eigene Darstellung, Screenshot des entwickelten Prototyps mit nachträglich ergänzten Hervorhebungen.*

**Bildstrategie:** Für Kapitel 5.1 ist die **Kombination aus echtem Editor-Screenshot und wenigen Callouts** am stärksten. Eine rein schematische Grafik erklärt die Softwarearchitektur besser, der Screenshot belegt dagegen gleichzeitig Implementierung und Gebäudebezug. Die beiden Abbildungen ergänzen sich daher, ohne inhaltlich redundant zu sein.

## D. Implementierungsnachweistabelle

*Nicht Bestandteil der Masterarbeit.*

| Architekturaussage                                                                                                      | Repository-Pfad / Implementierung                                                                                                                          | Status                                       |
| ----------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| Die Anwendung besitzt eine zentrale Zusammenschaltung von Viewer, Anwendungslogik, Persistenz sowie IFC-Import/-Export. | `src/main.ts` – Aufbau von Selection Manager, Mission Service, Repository, IFC-Import/-Export und Roundtrip-Koordination.                                  | Bestätigt                                    |
| Domänenmodell und Viewer sind getrennt.                                                                                 | `src/domain/robot-tasks/types.ts`; Viewer-Abhängigkeiten fehlen im Domänenmodell. `src/viewer/robot-tasks/` arbeitet über eigene Adapter.                  | Bestätigt                                    |
| Die Anwendungsschicht enthält keine konkrete Viewer- oder IFC-Serialisierungslogik.                                     | `src/application/robot-tasks/robotMissionService.ts`; dokumentierte Abgrenzung zu Viewer, UI, `localStorage` und IFC-Mapping.                              | Bestätigt                                    |
| Eine Viewerauswahl wird in eine fachliche IFC-Objektreferenz überführt.                                                 | `src/viewer/robot-tasks/selection-metadata.ts`, `viewer-object-selection-manager.ts`; Auflösung von `GlobalId`, IFC-Klasse, Name und bestätigter Referenz. | Bestätigt                                    |
| Der Missionseditor verwendet bestätigte Objektreferenzen, schreibt aber nicht direkt IFC.                               | `src/ui-templates/sections/robot-mission-tasks.ts`; Zuweisung der bestätigten Referenz über den Anwendungsservice.                                         | Bestätigt                                    |
| Missionspersistenz ist über austauschbare Speicherformen gekapselt.                                                     | `src/persistence/robot-tasks/selectableMissionRepository.ts`; In-Memory und `localStorage`, Backend nur Platzhalter.                                       | Bestätigt                                    |
| Direkt geladene IFC-Dateien werden als Roundtrip-Quelle separat vorgehalten.                                            | `src/ui-templates/sections/models.ts`, `src/ifc/model-export/ifcSourceModelRegistry.ts`.                                                                   | Bestätigt                                    |
| Vorhandene RobotMission-Annotationen werden nach direktem IFC-Import rekonstruiert.                                     | `src/ifc/model-import/ifcMissionImportService.ts`, `webIfcMissionReader.ts`, Aufruf aus `models.ts`.                                                       | Bestätigt                                    |
| Der IFC-Export arbeitet quellgestützt und nicht auf Grundlage der Fragments-Geometrie allein.                           | `src/ifc/model-export/ifcModelExportService.ts`; Export ohne gehaltene IFC-Quelle und bei nicht abbildbaren Strukturänderungen wird abgelehnt.             | Bestätigt                                    |
| Exportierte Missionen werden erneut importiert und semantisch geprüft.                                                  | `src/ifc/model-roundtrip/ifcMissionRoundtripCoordinator.ts`; Reimport, semantischer Vergleich und erst anschließend Übernahme der neuen Bytes.             | Bestätigt                                    |
| Der Roundtrip betrifft RobotMission-Annotationen, nicht beliebige IFC-Struktur- oder Geometrieänderungen.               | `src/ifc/model-export/ifcModelExportService.ts` sowie Markierung struktureller Fragments-Änderungen in `src/main.ts`.                                      | Bestätigt                                    |
| Backend, ROS, automatische Waypoints und Surface Tiling gehören nicht zum implementierten Stand.                        | Repository-Map und aktuelle Struktur-/Implementierungsübersicht.                                                                                           | Nicht implementiert / zukünftige Erweiterung |

## E. Review des Professorenfeedbacks

**1. Stehen Quellcodedetails noch zu stark im Vordergrund?**
Nein. Im eigentlichen Kapitel werden weder konkrete TypeScript-Dateien noch Klassen- und Methodennamen als Argumentationsstruktur verwendet. Der Text arbeitet mit Verantwortungsbereichen wie Viewer, Auswahladapter, Anwendungslogik, Domänenmodell, Persistenz und IFC-Infrastruktur. Die konkreten Implementierungsbezeichner sind bewusst in die separate Nachweistabelle ausgelagert.

**2. Ist der Bezug zwischen Annotation und konkretem IFC-Gebäude anschaulich genug?**
Textlich deutlich besser: Das durchgängige Türbeispiel verbindet sichtbares Gebäudeelement, Auswahl, IFC-Referenz, Task und IFC-Export. Visuell sollte unbedingt der vorgeschlagene echte Screenshot ergänzt werden. Gerade die gleichzeitige Darstellung **derselben hervorgehobenen Tür** und des zugehörigen Tasks ist vermutlich die wirksamste Umsetzung des Professorenfeedbacks.

## F. Offene Review-Punkte

1. Prüfen, ob die Bezeichnung **„Fragments-Repräsentation“** bereits in Kapitel 2 eingeführt wurde; andernfalls in 5.1 nur knapp verwenden und in 5.2/5.3 definieren.
2. Entscheiden, ob die annotierte IFC-Datei bereits in Kapitel 4 ausdrücklich als fachlicher Austauschträger beziehungsweise kanonisches Format festgelegt wurde; 5.1 sollte diese Entscheidung nur technisch aufgreifen, nicht neu begründen.
3. Nach Aufnahme des Screenshots prüfen, ob der konkrete Taskname und das ausgewählte Bauteil auch bei Druckgröße noch lesbar sind.
4. Beim Übergang zu 5.3 darauf achten, dass die genaue Importreihenfolge nicht erneut ausführlich in 5.1 erklärt wird.
5. Den Begriff **IFC-Roundtrip** im gesamten Dokument konsequent auf den *RobotMission-Annotationsroundtrip* beschränken, wenn nicht ausdrücklich der allgemeine IFC-Roundtrip gemeint ist.

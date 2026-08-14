Erstelle Kapitel **4.6 „Repräsentation ergänzender Taskinformationen in IFC“** meiner deutschsprachigen Masterarbeit.

Das Kapitel gehört zu:

**4 – Konzeption des IFC-basierten Annotationsmodells**

Die bisher getrennten Abschnitte

* Task-Objekt-Zuordnung,
* eigene Property Sets,
* Zeitmodell

werden in diesem Kapitel bewusst zusammengeführt, um Wiederholungen zu vermeiden und die Darstellung kompakt zu halten.

Halte das Kapitel auf einen Zielumfang von ungefähr:

**1.000–1.500 Wörtern**

Ich werde den Text anschließend selbst manuell reviewen und mit anderen Entwürfen vergleichen. Verwende keinen automatisierten Codex-/Claude-Workflow.

# 1. Quellenbasis

Lies zuerst die im Projektkontext verfügbaren Dateien:

1. `REPOSITORY_MAP_IFC_EDITOR_674ede3.md`
2. `Strukturübersicht.txt`
3. `repo_structure.txt`

Untersuche anschließend gezielt die tatsächliche Implementierung des IFC-Editors.

Besonders relevant sind:

* `src/domain/robot-tasks/types.ts`
* `src/ifc/robot-tasks/annotationSchema.ts`
* `src/ifc/robot-tasks/mapper.ts`
* `src/ifc/robot-tasks/records.ts`

Bei Bedarf ergänzend:

* `src/ifc/model-import/webIfcMissionReader.ts`
* `src/ifc/model-export/webIfcMissionWriter.ts`
* `src/domain/robot-tasks/validation.ts`
* `test/robot-tasks/ifc-relation-mapper.test.ts`
* `test/robot-tasks/ifc-mission-writer.test.ts`
* `test/robot-tasks/ifc-mission-reader.test.ts`

Öffne weitere Dateien nur, wenn sie zur Verifikation einer konkreten Aussage notwendig sind.

Verwende für Repository-Dateireferenzen ausschließlich Pfade aus `repo_structure.txt`.

Die Repository-Map dient als Orientierung. Konkrete Aussagen über die Implementierung müssen am tatsächlichen Quellcode geprüft werden.

# 2. Ziel des Kapitels

Erkläre, wie die über die grundlegende Missions- und Taskstruktur hinausgehenden Informationen eines `RobotTask` in IFC repräsentiert werden.

Das Kapitel soll drei eng miteinander verbundene Aspekte gemeinsam behandeln:

1. Beziehungen eines Tasks zu IFC-Objekten,
2. projektspezifische Aktions- und Metadaten,
3. Zeitinformationen.

Die zentrale Fragestellung lautet:

**Welche unterschiedlichen IFC-Mechanismen werden verwendet, um Objektbezüge, projektspezifische Semantik und zeitliche Informationen eines RobotTask abzubilden?**

Betone, dass diese Informationsarten fachlich unterschiedlich sind und deshalb nicht alle über denselben Mechanismus gespeichert werden.

# 3. Objektzuordnungen

Erkläre zunächst, dass sich ein `RobotTask` auf verschiedene Weise auf Elemente des Gebäudemodells beziehen kann.

Prüfe anhand der Implementierung insbesondere:

* `targetObjects`
* `affectedObjects`
* `startReference`
* `targetReference`

Arbeite heraus, dass diese Felder unterschiedliche Rollen eines Gebäudeelements im Kontext eines Tasks beschreiben.

Beispiele:

* direktes Ziel einer Aktion,
* indirekt betroffenes Objekt,
* Ausgangspunkt einer Bewegung,
* Ziel einer Bewegung.

Gehe anschließend knapp auf die dafür verwendeten IFC-Beziehungen ein.

Prüfe insbesondere die Nutzung von:

* `IfcRelAssignsToProcess`
* `IfcRelAssignsToProduct`

Beschreibe die Abbildung nur so detailliert, wie sie zum Verständnis des Konzepts erforderlich ist.

Die vollständige systematische Mapping-Tabelle des gesamten Domänenmodells folgt erst im nächsten Kapitel.

# 4. Projektspezifische Property Sets

Erkläre anschließend, dass nicht alle Informationen des Robotermissionsmodells durch vorhandene native IFC-Attribute ausgedrückt werden können.

Für projektspezifische Robotiksemantik werden deshalb eigene Property Sets verwendet.

Prüfe anhand der tatsächlichen Implementierung insbesondere:

* `RobotAction`
* `RobotTask`
* `RobotMission`

und die darin tatsächlich verwendeten Properties.

Mögliche relevante Angaben sind beispielsweise:

* `ActionType`
* `TargetState`
* `RequiredCapability`
* Preconditions
* Postconditions
* Erfolgskriterien
* Versionsinformationen der Annotation.

Beschreibe nur Properties, die tatsächlich implementiert sind.

Erkläre die grundlegende Designentscheidung:

**Standardisierte IFC-Strukturen werden genutzt, wo eine passende Semantik vorhanden ist; projektspezifische Robotiksemantik wird ergänzend über eigene Property Sets abgebildet.**

Falls der reservierte Präfix `Pset_` thematisiert wird, prüfe die Aussage gegen die offizielle buildingSMART-Spezifikation.

# 5. Zeitinformationen

Erkläre anschließend die Behandlung zeitlicher Informationen.

Prüfe insbesondere:

* `RobotTaskTime`
* `RobotMissionSchedule`

und deren tatsächliche IFC-Abbildung.

Arbeite die Designentscheidung heraus, dass Task-Zeitinformationen nicht als beliebige Custom Properties gespeichert werden, wenn IFC hierfür bereits geeignete Strukturen bereitstellt.

Prüfe die Verwendung von:

* `IfcTaskTime`
* `IfcWorkSchedule`
* gegebenenfalls `IfcRelAssignsToControl`

Behandle beispielsweise:

* geplanten Start,
* geplantes Ende,
* geplante Dauer,
* tatsächliche Zeiten,
* verbleibende Zeit,
* Fertigstellungsgrad.

Nicht alle Attribute müssen einzeln beschrieben werden. Der Schwerpunkt liegt auf der Trennung zwischen:

**projektspezifischer Aktionssemantik**

und

**standardisierbaren Zeitinformationen**.

# 6. Gemeinsame Einordnung

Führe die drei Informationsbereiche am Ende konzeptionell zusammen.

Eine geeignete Darstellung wäre:

```text
RobotTask
│
├── Objektbezüge
│     → IFC-Relationen
│
├── projektspezifische Aktionssemantik
│     → eigene Property Sets
│
└── Zeitinformationen
      → native IFC-Zeitstrukturen
```

Arbeite heraus, dass dadurch nicht sämtliche Taskinformationen in ein einziges benutzerdefiniertes Property Set geschrieben werden.

Die Wahl des IFC-Mechanismus orientiert sich vielmehr an der Semantik der jeweiligen Information.

# 7. Abgrenzung zum folgenden IFC-Mapping-Kapitel

Dieses Kapitel soll **nicht bereits das komplette Domain-to-IFC-Mapping erklären**.

Vermeide deshalb eine vollständige Aufzählung aller erzeugten IFC-Entities und Relationen.

Das folgende Kapitel soll anschließend systematisch zeigen, wie das vollständige Domänenmodell zusammengesetzt auf IFC abgebildet wird.

Die Trennung soll ungefähr so sein:

**Kapitel 4.6:**
Welche Mechanismen werden für Objektbezüge, Zusatzsemantik und Zeitdaten verwendet?

**Folgekapitel – IFC-Mapping:**
Wie ergibt sich daraus die vollständige Abbildung von `RobotMission` und `RobotTask` auf den IFC-Graphen?

# 8. Abgrenzung zu vorherigen Kapiteln

Verwende `Strukturübersicht.txt`.

Nicht erneut ausführlich behandeln:

* Modellierungsziele aus 4.1,
* Aufbau von `RobotMission` und `RobotTask` aus 4.2,
* Bedeutung einzelner Roboteraktionen aus 4.3,
* Identifikation von IFC-Objekten aus 4.4,
* Missionshierarchie und Sequenzen aus 4.5.

Insbesondere soll 4.6 nicht erneut erklären, wie eine `GlobalId` funktioniert oder warum `tasks` und `sequences` getrennt sind.

# 9. Keine zukünftigen Konzepte als Implementierung darstellen

Nicht als Bestandteil des aktuellen Modells beschreiben, sofern nicht durch den Quellcode belegt:

* `RobotInteractionCapability`
* Surface Tiling
* Teilflächenreferenzen
* Robot-JSON
* ROS-Anbindung
* Navigation Targets
* Waypoints
* Backend-Persistenz.

Wenn solche Konzepte erwähnt werden, ausschließlich als klar gekennzeichnete zukünftige Erweiterung.

# 10. Erwartete Argumentationsstruktur

Erstelle einen zusammenhängenden wissenschaftlichen Text.

Eine sinnvolle Struktur ist:

### Einstieg

Kurze Überleitung aus Kapitel 4.5.

Nachdem Mission, Tasks und deren Abhängigkeiten beschrieben wurden, müssen zusätzliche Informationen eines Tasks mit der IFC-Struktur verknüpft werden.

### Objektbezüge

* unterschiedliche Rollen von Gebäudeelementen,
* relationale Verknüpfung statt Kopieren von Gebäudedaten,
* passende IFC-Beziehungen.

### Projektspezifische Semantik

* Action Properties,
* eigene Property Sets,
* Ergänzung der standardisierten IFC-Strukturen.

### Zeitinformationen

* eigene Domänenstruktur,
* Nutzung nativer IFC-Zeitentitäten,
* Abgrenzung zu Custom Properties.

### Zusammenführung

* unterschiedliche Informationsart → unterschiedlicher IFC-Mechanismus,
* Vorbereitung des vollständigen IFC-Mappings.

### Überleitung

Kurze Überleitung zum nächsten Kapitel:

Die beschriebenen Einzelmechanismen werden dort zu einer vollständigen Abbildung des internen Domänenmodells auf IFC zusammengeführt.

# 11. Wissenschaftlicher Stil

Schreibe vollständig auf Deutsch.

Verwende:

* formalen wissenschaftlichen Stil,
* präzise technische Formulierungen,
* zusammenhängenden Fließtext,
* kompakte Argumentation,
* klare Unterscheidung zwischen standardisierten IFC-Strukturen und projektspezifischen Erweiterungen.

Vermeide:

* lange Listen von Properties ohne fachliche Einordnung,
* API-Dokumentation,
* lange TypeScript-Codeblöcke,
* Wiederholungen aus vorherigen Kapiteln,
* unnötige Beschreibung einzelner STEP-Zeilen.

Standardisierte Bezeichner bleiben unverändert, beispielsweise:

* `IfcTaskTime`
* `IfcWorkSchedule`
* `IfcRelAssignsToProcess`
* `IfcRelAssignsToProduct`
* `IfcPropertySet`
* `RobotAction`

# 12. Abbildung

Prüfe, ob eine kleine schematische Abbildung das Kapitel sinnvoll unterstützt.

Geeignet wäre:

```text
                    RobotTask
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
   Objektbezug    Aktionssemantik    Zeitdaten
        │              │              │
        ▼              ▼              ▼
 IFC-Relationen   Property Sets   IFC-Zeitmodell
```

Die Abbildung soll die **drei unterschiedlichen Repräsentationsmechanismen** zeigen.

Maximal eine Abbildung.

Bevorzuge ein technisches Diagramm gegenüber einer dekorativen Illustration.

Formuliere eine deutsche Bildunterschrift und schlage die Position im Text vor.

# 13. Gewünschte Ausgabe

Erstelle:

1. eine kurze Arbeitsnotiz mit den untersuchten Repository-Dateien,
2. das vollständige Kapitel **4.6 „Repräsentation ergänzender Taskinformationen in IFC“** mit ca. 1.000–1.500 Wörtern,
3. optional eine kleine technische Abbildung,
4. eine kompakte Nachweistabelle:

| Aussage | Status | Implementierungsnachweis |
| ------- | ------ | ------------------------ |

Unterscheide:

* direkt implementiert,
* aus Implementierung abgeleitet,
* konzeptionell,
* externe IFC-Quelle erforderlich.

5. maximal drei offene Punkte für mein manuelles Review.

# Wichtigste inhaltliche Aussage

Das Kapitel soll klar herausarbeiten:

**Objektbezüge, projektspezifische Robotiksemantik und Zeitinformationen eines Tasks besitzen unterschiedliche Bedeutungen und werden deshalb mit unterschiedlichen IFC-Mechanismen repräsentiert: Beziehungen für Objektzuordnungen, eigene Property Sets für projektspezifische Zusatzinformationen und native IFC-Strukturen für Zeitdaten.**

Beginne jetzt mit `REPOSITORY_MAP_IFC_EDITOR_674ede3.md`, `Strukturübersicht.txt` und `repo_structure.txt` und untersuche danach gezielt die relevante Implementierung.

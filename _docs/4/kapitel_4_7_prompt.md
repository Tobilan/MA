Erstelle Kapitel **4.7 „Abbildung des Domänenmodells auf IFC“** meiner deutschsprachigen Masterarbeit.

Das Kapitel entspricht in der ursprünglichen Struktur dem bisherigen Kapitel **4.9 „IFC-Mapping“**. Durch die Zusammenfassung der früheren Kapitel 4.6–4.8 wurde es zu Kapitel 4.7 verschoben.

Das Kapitel gehört zu:

**4 – Konzeption des IFC-basierten Annotationsmodells**

Halte das Kapitel kompakt. Zielumfang:

**ca. 1.000–1.500 Wörter**

Ich werde den Text anschließend selbst manuell reviewen und mit anderen Entwürfen vergleichen. Verwende keinen automatisierten Codex-/Claude-Workflow.

# 1. Quellenbasis

Lies zuerst die im Projektkontext verfügbaren Dateien:

1. `REPOSITORY_MAP_IFC_EDITOR_674ede3.md`
2. `Strukturübersicht.txt`
3. `repo_structure.txt`

Untersuche anschließend gezielt die tatsächliche Implementierung des IFC-Editors.

Besonders relevant sind:

* `src/ifc/robot-tasks/annotationSchema.ts`
* `src/ifc/robot-tasks/mapper.ts`
* `src/ifc/robot-tasks/records.ts`
* `src/domain/robot-tasks/types.ts`

Bei Bedarf ergänzend:

* `src/ifc/model-import/webIfcMissionReader.ts`
* `src/ifc/model-export/webIfcMissionWriter.ts`
* `src/ifc/model-export/webIfcStructuralCodec.ts`
* `src/application/robot-tasks/robotMissionSemanticComparison.ts`
* `test/robot-tasks/ifc-relation-mapper.test.ts`
* `test/robot-tasks/ifc-mission-reader.test.ts`
* `test/robot-tasks/ifc-mission-writer.test.ts`

Weitere Dateien nur öffnen, wenn sie zur Verifikation einer konkreten Aussage notwendig sind.

Verwende für Repository-Dateireferenzen ausschließlich Pfade aus `repo_structure.txt`.

Die Repository-Map dient als Orientierung. Aussagen über die konkrete Abbildung müssen am tatsächlichen Quellcode geprüft werden.

# 2. Ziel des Kapitels

Kapitel 4.7 soll die zuvor einzeln eingeführten Modellierungsentscheidungen zu einer **Gesamtabbildung des internen Robotermissionsmodells auf IFC** zusammenführen.

Die zentrale Fragestellung lautet:

**Wie werden `RobotMission`, `RobotTask` und die zugehörigen Beziehungen und Zusatzinformationen systematisch auf IFC-Entitäten und IFC-Relationen abgebildet?**

Das Kapitel soll nicht die konkrete Writer-Implementierung beschreiben, sondern die **konzeptionelle Mappinglogik**.

# 3. Grundprinzip der Abbildung

Erkläre zu Beginn die Trennung zwischen:

```text
internes Domänenmodell
        ↓
IFC-nahe Mappingrepräsentation
        ↓
IFC-Entitäten und Relationen
```

Arbeite heraus, dass das Domänenmodell nicht direkt von STEP-Syntax oder `web-ifc` abhängig ist.

Die IFC-Schicht übernimmt die Übersetzung zwischen der fachlichen Robotermissionsstruktur und der IFC-Repräsentation.

Vermeide eine detaillierte Beschreibung der technischen Exportpipeline. Diese gehört in das Implementierungskapitel.

# 4. Mission und Tasks

Prüfe die tatsächliche Abbildung von:

* `RobotMission`
* `RobotTask`

Erkläre insbesondere die grundlegende Struktur:

```text
RobotMission
    ↓
übergeordneter IfcTask

RobotTask
    ↓
untergeordneter IfcTask
```

Begründe knapp, weshalb sowohl Mission als auch ausführbare Einzelschritte als `IfcTask` repräsentiert werden können, jedoch unterschiedliche Rollen innerhalb der Hierarchie besitzen.

Die Mission bildet dabei den übergeordneten Kontext, während die einzelnen `RobotTask`-Objekte die ausführbaren Schritte darstellen.

# 5. Hierarchie und Sequenzen

Führe die in Kapitel 4.5 erläuterte Trennung jetzt auf IFC-Ebene zusammen.

Prüfe die tatsächliche Implementierung von:

* `IfcRelNests`
* `IfcRelSequence`

Stelle knapp dar:

```text
Mission → Tasks
= IfcRelNests

Task → nachfolgender Task
= IfcRelSequence
```

Wichtig:

Hierarchie und Ausführungsabhängigkeit dürfen nicht als dasselbe dargestellt werden.

Erkläre nur die Mappingentscheidung. Wiederhole nicht ausführlich die Sequenzsemantik aus Kapitel 4.5.

# 6. Objektbezüge

Führe die in Kapitel 4.6 beschriebenen Objektzuordnungen in die Gesamtübersicht ein.

Prüfe insbesondere die tatsächliche Verwendung von:

* `IfcRelAssignsToProcess`
* `IfcRelAssignsToProduct`

Zeige, wie unterschiedliche Domänenreferenzen auf passende IFC-Beziehungen abgebildet werden.

Berücksichtige insbesondere:

* direkt adressierte Zielobjekte,
* betroffene Objekte,
* Start- und Zielreferenzen von Bewegungsaufgaben,

soweit diese Rollen tatsächlich im Mapper unterschieden werden.

Vermeide eine erneute ausführliche Erklärung von `GlobalId`, `modelId` und `expressId`.

# 7. Aktions- und Metadaten

Erkläre knapp, wie projektspezifische Informationen des Domänenmodells über eigene Property Sets ergänzt werden.

Prüfe insbesondere:

* `RobotAction`
* `RobotTask`
* `RobotMission`

und deren tatsächlich implementierte Properties.

Die zentrale Aussage lautet:

**Die regulären IFC-Entitäten bilden Prozessstruktur und Beziehungen ab; projektspezifische Robotiksemantik wird ergänzend über eigene Property Sets gespeichert.**

Gehe nicht erneut jede Property einzeln durch. Kapitel 4.6 hat diese Mechanismen bereits eingeführt.

# 8. Zeitinformationen und Missionsschedule

Führe die zeitlichen Informationen ebenfalls in die Gesamtabbildung ein.

Prüfe insbesondere:

* `RobotTaskTime` → `IfcTaskTime`
* `RobotMissionSchedule` → `IfcWorkSchedule`
* gegebenenfalls die Zuordnung über `IfcRelAssignsToControl`

Beschreibe nur die systematische Zuordnung.

Das Ziel ist zu zeigen, dass für Zeitdaten vorhandene IFC-Strukturen genutzt werden, statt sämtliche Informationen über eigene Property Sets abzubilden.

# 9. Zentrale Mapping-Tabelle

Baue im Kapitel eine kompakte Tabelle ein.

Prüfe jede Zuordnung gegen die tatsächliche Implementierung.

Eine mögliche Ausgangsstruktur ist:

| Domänenkonzept                | IFC-Abbildung               |
| ----------------------------- | --------------------------- |
| `RobotMission`                | übergeordneter `IfcTask`    |
| `RobotTask`                   | untergeordneter `IfcTask`   |
| Missionshierarchie            | `IfcRelNests`               |
| Task-Abhängigkeit             | `IfcRelSequence`            |
| Missionsschedule              | `IfcWorkSchedule`           |
| Task-Zeit                     | `IfcTaskTime`               |
| direkte Objektinteraktion     | `IfcRelAssignsToProcess`    |
| produktbezogene Zielzuordnung | `IfcRelAssignsToProduct`    |
| Aktionssemantik               | `RobotAction`-Property-Set  |
| Task-Metadaten                | `RobotTask`-Property-Set    |
| Missionsmetadaten             | `RobotMission`-Property-Set |

Passe die Tabelle an, falls die tatsächliche Implementierung hiervon abweicht.

Keine Zuordnung übernehmen, die nicht durch den Code bestätigt wird.

# 10. Bidirektionale Abbildung

Da der RobotMission-Roundtrip implementiert ist, soll Kapitel 4.7 nicht ausschließlich die Richtung

```text
Domänenmodell → IFC
```

beschreiben.

Erkläre kurz, dass die verwendete IFC-Struktur auch wieder ausreichend eindeutig interpretiert werden muss, um daraus das interne Domänenmodell zu rekonstruieren.

Damit ergibt sich konzeptionell:

```text
RobotMission
     ↓
IFC-Missionsgraph
     ↓
RobotMission
```

Wichtig:

Beschreibe hier nur die **Anforderung an die bidirektionale Mappingstruktur**.

Die technische Funktionsweise von:

* IFC-Reader,
* Replacement-Export,
* Roundtrip-Coordinator,
* semantischem Vergleich,
* Source Registry

gehört in Kapitel 5.

# 11. Bedeutung der Annotationsversion

Prüfe die tatsächliche Verwendung von:

`AnnotationSchemaVersion`

und erläutere sie kurz, sofern sie Bestandteil des aktuellen Mappings ist.

Die Versionsinformation soll ermöglichen, die projektspezifische Robotermissionsannotation eindeutig zu erkennen und Änderungen des eigenen Annotationsschemas später kontrolliert zu behandeln.

Nicht mit der IFC-Schemaversion verwechseln.

Unterscheide klar zwischen beispielsweise:

* IFC4 bzw. IFC4X3 als IFC-Schema,
* eigener Version des Robotermissions-Annotationsmodells.

# 12. IFC4 und IFC4X3

Falls für dieses Kapitel relevant, erwähne knapp, dass die Implementierung unterschiedliche unterstützte IFC-Schemata berücksichtigt.

Beschreibe nur Unterschiede, die tatsächlich Einfluss auf das Mapping haben und im Repository nachweisbar sind.

Vermeide eine allgemeine Gegenüberstellung von IFC4 und IFC4X3.

# 13. Abgrenzung

Verwende `Strukturübersicht.txt`.

Nicht erneut ausführlich behandeln:

* Domänentypen aus 4.2,
* konkrete Aktionsbedeutungen aus 4.3,
* Objektidentifikation aus 4.4,
* Sequenzlogik aus 4.5,
* einzelne Objektzuordnungen, Property Sets und Zeitdaten aus 4.6.

Ebenfalls nicht detailliert behandeln:

* technische `web-ifc`-Writer-API,
* STEP-Zeilen,
* Replacement-Algorithmus,
* Importalgorithmus,
* IFC-Quelldateiverwaltung,
* Benutzeroberfläche,
* Download der IFC-Datei.

Diese Punkte gehören in Kapitel 5.

# 14. Wissenschaftlicher Stil

Schreibe vollständig auf Deutsch.

Verwende:

* formalen wissenschaftlichen Stil,
* präzise technische Sprache,
* kompakte Argumentation,
* klare Trennung zwischen Domänenkonzept und IFC-Repräsentation.

Vermeide:

* Wiederholungen aus 4.2–4.6,
* API-Dokumentation,
* lange TypeScript-Codeblöcke,
* STEP-Code,
* unnötig detaillierte Attributlisten.

Standardisierte IFC-Bezeichner bleiben unverändert.

# 15. Abbildung

Für dieses Kapitel ist eine **Gesamtübersicht des Mappings** besonders sinnvoll.

Erstelle maximal eine technische Abbildung.

Beispielsweise:

```text
RobotMission
   │
   ├──────────────→ IfcTask (Mission)
   │                    │
   │                    └── IfcRelNests
   │                           │
   ▼                           ▼
RobotTask ─────────────→ IfcTask (Task)
   │
   ├─ Sequenz ────────→ IfcRelSequence
   │
   ├─ Objektbezug ────→ IfcRelAssignsToProcess /
   │                    IfcRelAssignsToProduct
   │
   ├─ Zeit ───────────→ IfcTaskTime
   │
   └─ ActionProperties
              └───────→ RobotAction Property Set
```

Passe das Diagramm exakt an die tatsächliche Implementierung an.

Die Abbildung soll die Mappingstruktur zeigen und keine technische Softwarearchitektur.

Formuliere:

* deutsche Bildunterschrift,
* vorgeschlagene Position,
* Verweis im Fließtext.

# 16. Gewünschte Ausgabe

Erstelle:

1. eine kurze Arbeitsnotiz mit den untersuchten Repository-Dateien,
2. das vollständige Kapitel **4.7 „Abbildung des Domänenmodells auf IFC“** mit ca. 1.000–1.500 Wörtern,
3. eine kompakte Mapping-Tabelle innerhalb des Kapiteltextes,
4. sofern sinnvoll eine technische Mapping-Abbildung,
5. anschließend eine Nachweistabelle:

| Mappingaussage | Status | Implementierungsnachweis |
| -------------- | ------ | ------------------------ |

Unterscheide:

* direkt implementiert,
* aus Implementierung abgeleitet,
* konzeptionell,
* externe IFC-Quelle erforderlich.

Nenne abschließend maximal drei Punkte für mein manuelles Review.

# Wichtigste inhaltliche Aussage

Das Kapitel soll zeigen:

**Das interne Robotermissionsmodell wird nicht als proprietäre Parallelstruktur neben IFC gespeichert, sondern systematisch auf vorhandene IFC-Prozess-, Relations- und Zeitstrukturen sowie gezielt ergänzte projektspezifische Property Sets abgebildet. Die Mappingstruktur ist so definiert, dass die RobotMission-Annotationen im implementierten Roundtrip auch wieder in das interne Domänenmodell rekonstruiert werden können.**

Beginne jetzt mit `REPOSITORY_MAP_IFC_EDITOR_674ede3.md`, `Strukturübersicht.txt` und `repo_structure.txt` und untersuche anschließend gezielt die relevanten Mapping-, Reader- und Writer-Dateien.

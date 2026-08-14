Erstelle Kapitel **4.5 „Missionshierarchie und Task-Sequenzen“** meiner deutschsprachigen Masterarbeit.

Das Kapitel gehört zu:

**4 – Konzeption des IFC-basierten Annotationsmodells**

Halte das Kapitel bewusst kompakt. Zielumfang:

**ca. 700–1.000 Wörter**

Ich werde den Text anschließend selbst manuell reviewen und mit anderen Entwürfen vergleichen. Verwende keinen automatisierten Codex-/Claude-Workflow.

# 1. Quellenbasis

Lies zuerst die im Projektkontext verfügbaren Dateien:

1. `REPOSITORY_MAP_IFC_EDITOR_674ede3.md`
2. `Strukturübersicht.txt`
3. `repo_structure.txt`

Untersuche anschließend gezielt die tatsächliche Implementierung.

Besonders relevant sind:

* `src/domain/robot-tasks/types.ts`
* `src/domain/robot-tasks/sequencing.ts`
* `src/domain/robot-tasks/builders.ts`
* `src/domain/robot-tasks/validation.ts`

Bei Bedarf ergänzend:

* `src/application/robot-tasks/robotMissionService.ts`
* `test/robot-tasks/robot-mission-domain.test.ts`
* `test/robot-tasks/robot-mission-service.test.ts`
* `test/robot-tasks/ifc-relation-mapper.test.ts`

Verwende für Dateireferenzen ausschließlich Pfade aus `repo_structure.txt`.

Die Repository-Map dient der Orientierung. Konkrete Aussagen über das Verhalten des Domänenmodells müssen am Quellcode geprüft werden.

# 2. Ziel des Kapitels

Erkläre die Trennung zwischen:

**Missionshierarchie**

und

**zeitlichen bzw. logischen Ausführungsabhängigkeiten zwischen Tasks.**

Die zentrale Aussage des Kapitels lautet:

```text
RobotMission.tasks
= welche Tasks zur Mission gehören und in welcher
  deterministischen Hierarchie-/Darstellungsordnung sie vorliegen

RobotMission.sequences
= welche Ausführungsabhängigkeiten zwischen diesen Tasks bestehen
```

Begründe, weshalb beide Informationen nicht ausschließlich durch die Position eines Tasks in einem Array ausgedrückt werden.

# 3. Missionshierarchie

Beschreibe `RobotMission` als übergeordnete Einheit, die mehrere ausführbare `RobotTask`-Objekte enthält.

Gehe kurz darauf ein, dass:

* eine Mission mehrere Tasks zusammenfasst,
* Tasks stabile IDs besitzen,
* diese IDs innerhalb der Mission eindeutig sein müssen,
* `tasks` die enthaltenen ausführbaren Schritte repräsentiert.

Vermeide eine Wiederholung der vollständigen Beschreibung von `RobotMission` und `RobotTask` aus Kapitel 4.2.

Die detaillierte IFC-Abbildung soll ebenfalls noch nicht im Mittelpunkt stehen.

# 4. Task-Sequenzen

Beschreibe `RobotTaskSequence` als gerichtete Beziehung zwischen zwei Tasks.

Berücksichtige:

* `id`,
* `predecessorTaskId`,
* `successorTaskId`,
* `sequenceType`.

Erkläre die Bedeutung von Vorgänger und Nachfolger.

Eine Sequenz beschreibt nicht, dass ein Task Bestandteil einer Mission ist, sondern eine **Abhängigkeit zwischen zwei bereits zur Mission gehörenden Tasks**.

# 5. Sequenztypen

Prüfe die tatsächlich implementierten Sequenztypen:

* `FINISH_START`
* `START_START`
* `FINISH_FINISH`
* `START_FINISH`

Erläutere sie nur sehr knapp.

Der Schwerpunkt soll auf `FINISH_START` liegen, da dieser Typ für eine einfache lineare Missionsausführung besonders relevant ist.

Beispiel:

```text
Task A: Tür öffnen
        ↓ FINISH_START
Task B: Tür passieren
```

Task B darf demnach erst beginnen, nachdem Task A abgeschlossen wurde.

Die anderen Typen sollen lediglich zeigen, dass das Domänenmodell grundsätzlich komplexere zeitliche Beziehungen ausdrücken kann.

# 6. Lineare Reihenfolge und allgemeiner Abhängigkeitsgraph

Dieser Punkt ist besonders wichtig.

Untersuche `sequencing.ts`.

Erkläre, dass eine einfache Bedienoberfläche eine Mission beispielsweise als lineare Reihenfolge darstellen kann:

```text
Task A
  ↓
Task B
  ↓
Task C
```

Diese Reihenfolge kann in der aktuellen Implementierung als Folge von `FINISH_START`-Beziehungen ausgedrückt werden.

Das zugrunde liegende Domänenmodell ist jedoch allgemeiner und modelliert gerichtete Abhängigkeiten.

Damit wären grundsätzlich auch Strukturen wie folgende beschreibbar:

```text
       Task A
      /      \
     v        v
 Task B    Task C
      \      /
       v    v
       Task D
```

Stelle solche Strukturen nur als konzeptionelle Eigenschaft des Sequenzmodells dar, sofern die Implementierung sie tatsächlich zulässt.

Behaupte nicht, dass die aktuelle Benutzeroberfläche bereits komplexe parallele Missionsgraphen komfortabel bearbeiten kann, wenn dies nicht im Repository nachgewiesen ist.

# 7. Validierung der Sequenzen

Erläutere nur kompakt, dass das Domänenmodell Sequenzbeziehungen auf strukturelle Konsistenz prüfen kann.

Prüfe anhand von `sequencing.ts` und `validation.ts` insbesondere:

* Vorgänger und Nachfolger müssen existierende Tasks referenzieren,
* ein Task darf nicht sein eigener Vorgänger sein,
* Sequenz-IDs müssen gültig bzw. eindeutig sein,
* Zyklen werden erkannt.

Veranschauliche die Bedeutung der Zyklusfreiheit kurz:

```text
A → B → C → A
```

würde keine widerspruchsfreie Ausführungsreihenfolge zulassen und ist daher ungültig.

Die vollständige Beschreibung der Validierungsarchitektur gehört in Kapitel 4.10 und darf hier nicht vorweggenommen werden.

# 8. Bedeutung für IFC

Stelle nur kurz die spätere konzeptionelle Abbildung her:

* Missionshierarchie → `IfcRelNests`
* Task-Abhängigkeit → `IfcRelSequence`

Diese Unterscheidung ist ein wesentlicher Grund dafür, Hierarchie und Sequenz bereits im internen Domänenmodell getrennt zu halten.

Wichtig:

Kapitel 4.5 soll **nicht** das vollständige IFC-Mapping erklären.

Keine detaillierte Behandlung von:

* Attributen von `IfcRelNests`,
* Attributen von `IfcRelSequence`,
* STEP-Serialisierung,
* Mapper-Implementierung,
* IFC-Reader oder Writer.

Diese Aspekte folgen in Kapitel 4.9.

# 9. Abgrenzung zu anderen Kapiteln

Verwende `Strukturübersicht.txt`.

Nicht erneut ausführlich behandeln:

* Modellierungsziele aus 4.1,
* vollständiges Domänenmodell aus 4.2,
* Roboteraktionen aus 4.3,
* IFC-Objektreferenzierung aus 4.4,
* Objektzuordnungen aus 4.6,
* Zeitmodell aus 4.8,
* vollständiges IFC-Mapping aus 4.9,
* vollständige Validierungslogik aus 4.10.

Kapitel 4.5 beantwortet im Wesentlichen nur:

**Wie werden Zugehörigkeit von Tasks zu einer Mission und Abhängigkeiten zwischen diesen Tasks getrennt repräsentiert?**

# 10. Wissenschaftlicher Stil

Schreibe vollständig auf Deutsch.

Verwende:

* formalen wissenschaftlichen Stil,
* kurze und präzise Argumentation,
* zusammenhängenden Fließtext,
* eine klare begriffliche Trennung zwischen Hierarchie und Sequenz.

Bezeichner wie

* `RobotMission`
* `RobotTask`
* `RobotTaskSequence`
* `FINISH_START`
* `IfcRelNests`
* `IfcRelSequence`

bleiben unverändert.

Vermeide eine ausführliche API- oder Quellcodebeschreibung.

# 11. Abbildung

Für dieses Kapitel ist **eine kleine schematische Abbildung ausdrücklich erwünscht**, sofern sie die Trennung anschaulich macht.

Geeignet ist eine Gegenüberstellung:

```text
Missionshierarchie

RobotMission
├── Task A
├── Task B
└── Task C


Ausführungsabhängigkeit

Task A ──→ Task B ──→ Task C
       FINISH_START
```

Alternativ kann ein kleiner verzweigter Graph gezeigt werden, um zu verdeutlichen, dass Hierarchie und Sequenz unterschiedliche Informationen darstellen.

Maximal eine Abbildung.

Keine dekorative Illustration verwenden. Bevorzuge Mermaid, SVG oder ein vergleichbares technisches Diagramm.

Formuliere:

* eine deutsche Bildunterschrift,
* eine geeignete Position im Kapitel,
* einen Verweis darauf im Fließtext.

# 12. Gewünschte Ausgabe

Erstelle:

1. eine sehr kurze Arbeitsnotiz mit den untersuchten Repository-Dateien,
2. das vollständige Kapitel **4.5 „Missionshierarchie und Task-Sequenzen“** mit ca. 700–1.000 Wörtern,
3. eine kleine technische Abbildung, sofern sinnvoll,
4. eine kompakte Nachweistabelle:

| Aussage | Status | Implementierungsnachweis |
| ------- | ------ | ------------------------ |

Unterscheide:

* implementiert,
* aus Implementierung abgeleitet,
* konzeptionell.

Nenne abschließend maximal drei Punkte für mein manuelles Review.

# Wichtigste inhaltliche Aussage

Das Kapitel soll klar herausarbeiten:

**Die Zugehörigkeit eines Tasks zu einer Mission und seine zeitliche Abhängigkeit von anderen Tasks sind unterschiedliche semantische Informationen. Das Domänenmodell bildet sie deshalb getrennt durch `tasks` und `sequences` ab.**

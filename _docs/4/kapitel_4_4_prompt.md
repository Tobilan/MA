Erstelle Kapitel **4.4 „Referenzierung von IFC-Objekten“** meiner deutschsprachigen Masterarbeit.

Das Kapitel gehört zu:

**4 – Konzeption des IFC-basierten Annotationsmodells**

Halte das Kapitel bewusst kompakt. Zielumfang:

**ca. 600–900 Wörter**

Ich werde den Text anschließend selbst manuell reviewen und mit anderen Entwürfen vergleichen. Verwende keinen automatisierten Codex-/Claude-Workflow.

# 1. Quellenbasis

Lies zuerst die im Projektkontext verfügbaren Dateien:

1. `REPOSITORY_MAP_IFC_EDITOR_674ede3.md`
2. `Strukturübersicht.txt`
3. `repo_structure.txt`

Untersuche danach gezielt die tatsächliche Implementierung.

Besonders relevant sind:

* `src/domain/robot-tasks/types.ts`
* `src/domain/robot-tasks/builders.ts`
* `src/viewer/robot-tasks/selection-adapter.ts`
* `src/viewer/robot-tasks/selection-metadata.ts`
* `src/viewer/robot-tasks/selection-types.ts`
* `src/viewer/robot-tasks/model-provenance.ts`

Bei Bedarf zusätzlich:

* `src/ifc/model-roundtrip/ifcMissionSourceRegistry.ts`
* `src/ifc/model-roundtrip/ifcMissionRoundtripCoordinator.ts`
* `src/ifc/model-import/webIfcMissionReader.ts`
* `src/ifc/model-export/ifcModelExportService.ts`

Verwende für Dateireferenzen ausschließlich Pfade, die in `repo_structure.txt` enthalten sind.

Die Repository-Map dient als Orientierung. Konkrete Implementierungsbehauptungen müssen am tatsächlichen Quellcode geprüft werden.

# 2. Ziel des Kapitels

Erkläre, wie ein `RobotTask` dauerhaft und möglichst unabhängig von der momentanen Viewer-Sitzung auf ein Objekt des IFC-Gebäudemodells verweisen kann.

Die zentrale Fragestellung lautet:

**Wie wird die Identität eines ausgewählten IFC-Objekts im internen Domänenmodell repräsentiert?**

Behandle insbesondere `RobotObjectReference`.

# 3. `GlobalId` als bevorzugte Referenz

Erläutere, dass die IFC-`GlobalId` in der aktuellen Implementierung die bevorzugte dauerhafte Objektidentität darstellt.

Arbeite den grundlegenden Zusammenhang heraus:

```text
IFC-Objekt
    ↓
GlobalId
    ↓
RobotObjectReference
    ↓
RobotTask
```

Die Referenz soll damit nicht von der gerade dargestellten Three.js-/Fragments-Geometrie abhängen.

Falls normative Aussagen über die Bedeutung oder Stabilität der IFC-`GlobalId` gemacht werden, verwende dafür ausschließlich eine offizielle buildingSMART-Quelle. Erfinde keine Quellen.

# 4. `expressId` und `modelId` als Fallback

Erkläre knapp:

* `expressId` ist eine lokale Entity-ID innerhalb einer konkreten IFC-Repräsentation,
* sie wird deshalb nicht allein als dauerhafte Referenz verwendet,
* in der Implementierung wird sie zusammen mit `modelId` als modelllokaler Fallback verwendet,
* `modelId` grenzt die Referenz auf das geladene Quellmodell ein.

Stelle die zwei Varianten des aktuellen Modells vereinfacht gegenüber:

```text
bevorzugt:
GlobalId

Fallback:
modelId + expressId
```

Vermeide die Behauptung, dass eine `expressId` über unterschiedliche IFC-Serialisierungen hinweg stabil bleibt.

# 5. Metadaten der Referenz

Erkläre kurz, dass `RobotObjectReference` zusätzlich Informationen wie

* IFC-Klasse,
* Objektname,
* gegebenenfalls `expressId` und `modelId`

enthalten kann.

Unterscheide dabei:

**Identität**
von
**beschreibenden Metadaten**.

Ein Objektname oder eine IFC-Klasse dient nicht als primäre Identität.

# 6. Abgrenzung zu Rendering- und Viewer-IDs

Dieser Punkt ist wichtig.

Erkläre, weshalb temporäre Informationen der Darstellung nicht als fachliche Referenz verwendet werden sollen.

Dazu gehören beispielsweise:

* Fragment-IDs,
* Mesh-IDs,
* Raycast-Treffer,
* interne Rendering-Strukturen.

Die Objektauswahl kann solche Strukturen nutzen, muss die bestätigte Auswahl jedoch anschließend in eine fachliche `RobotObjectReference` überführen.

Die detaillierte Implementierung der Objektauswahl gehört erst in Kapitel 5 und soll hier nicht beschrieben werden.

# 7. Bedeutung für den IFC-Roundtrip

Behandle diesen Punkt nur kurz.

Da Missionen aus annotierten IFC-Dateien wieder rekonstruiert und erneut exportiert werden können, müssen Referenzen wieder dem jeweiligen Gebäudemodell zugeordnet werden können.

Erkläre deshalb die Rolle von `modelId` bei der Quellabgrenzung.

Wichtig:

* Der RobotMission-Roundtrip ist implementiert.
* Daraus folgt nicht, dass beliebige Veränderungen eines Gebäudemodells automatisch aufgelöst werden können.
* Wird ein referenziertes Bauteil in einer späteren Modellrevision entfernt oder mit einer neuen `GlobalId` erzeugt, ist eine automatische Wiederzuordnung nicht grundsätzlich gewährleistet.

Eine zukünftige Rebind-Strategie darf höchstens kurz als offene Erweiterung erwähnt werden.

# 8. Abgrenzung zu folgenden Kapiteln

Verwende `Strukturübersicht.txt`.

Nicht detailliert behandeln:

* Zuordnungsrollen wie `OPERATES_ON`, `AFFECTS`, `MOVE_FROM` oder `MOVE_TO`,
* `IfcRelAssignsToProcess`,
* `IfcRelAssignsToProduct`,
* konkretes IFC-Mapping,
* Auswahlalgorithmus des Viewers,
* Surface Tiling,
* geometrische Teilflächenreferenzen,
* Navigation Targets oder Roboterkoordinaten.

Kapitel 4.4 soll ausschließlich erklären, **wie das referenzierte IFC-Objekt identifiziert wird**.

# 9. Wissenschaftlicher Stil

Schreibe vollständig auf Deutsch.

Verwende:

* formalen wissenschaftlichen Stil,
* kurze und präzise Argumentation,
* klare Unterscheidung von dauerhafter und laufzeitlokaler Identifikation,
* konsistente technische Begriffe.

Bezeichner wie

* `RobotObjectReference`
* `GlobalId`
* `expressId`
* `modelId`

bleiben unverändert.

# 10. Abbildung

Eine Abbildung ist nur erforderlich, wenn sie das Prinzip deutlich schneller verständlich macht.

Geeignet wäre eine kleine schematische Darstellung:

```text
Viewer-Auswahl
     ↓
IFC-Metadaten auflösen
     ↓
RobotObjectReference
     ├── GlobalId        ← bevorzugt
     └── modelId +
         expressId       ← Fallback
     ↓
RobotTask
```

Maximal eine Abbildung.

Keine dekorative Illustration verwenden; ein einfaches technisches Diagramm ist ausreichend.

# 11. Gewünschte Ausgabe

Erstelle:

1. eine sehr kurze Arbeitsnotiz mit den untersuchten Repository-Dateien,
2. das vollständige Kapitel **4.4 „Referenzierung von IFC-Objekten“** mit ca. 600–900 Wörtern,
3. optional eine kleine technische Abbildung mit deutscher Bildunterschrift,
4. eine kompakte Nachweistabelle:

| Aussage | Status | Implementierungsnachweis |
| ------- | ------ | ------------------------ |

Unterscheide:

* implementiert,
* aus Implementierung abgeleitet,
* konzeptionell.

Nenne abschließend höchstens drei Punkte für mein manuelles Review.

# Wichtigste inhaltliche Aussage

Das Kapitel soll klar herausarbeiten:

**Die fachliche Referenz eines IFC-Objekts wird von der temporären Darstellung im Viewer getrennt. Die `GlobalId` dient als bevorzugte dauerhafte Identität; `modelId + expressId` bildet einen modelllokalen Fallback.**

Beginne jetzt mit den drei Projektdateien und untersuche anschließend gezielt die relevante Implementierung.

# Arbeitsnotiz: untersuchte Repository-Dateien

Geprüfter Stand: `674ede3` (laut `REPOSITORY_MAP_IFC_EDITOR_674ede3.md`).

Primär geprüft:

- `src/ifc/robot-tasks/mapper.ts`
- `src/ifc/robot-tasks/records.ts`
- `src/ifc/robot-tasks/annotationSchema.ts`
- `src/domain/robot-tasks/types.ts`

Ergänzend geprüft:

- `src/ifc/model-export/webIfcMissionWriter.ts` (Attributbelegung der erzeugten Entitäten, Preflight-Regeln)
- `src/ifc/model-export/ifcSchemaAdapter.ts` (unterstützte IFC-Schemata)
- `src/ifc/model-import/webIfcMissionReader.ts` (inverse Interpretierbarkeit der Mappingstruktur)

Nur zur Orientierung, nicht als Nachweis verwendet: `REPOSITORY_MAP_IFC_EDITOR_674ede3.md`, `Strukturübersicht.txt`, `repo_structure.txt`.

Nicht verfügbar in der bereitgestellten Projektablage und daher nicht als Nachweis herangezogen: die Testdateien unter `test/robot-tasks/`.

---

# 4.7 Abbildung des Domänenmodells auf IFC

## 4.7.1 Grundprinzip der Abbildung

Die in den Abschnitten 4.2 bis 4.6 einzeln eingeführten Modellierungsentscheidungen werden hier zu einer geschlossenen Abbildungsvorschrift zusammengeführt. Leitfrage ist, wie eine `RobotMission` mit ihren `RobotTask`-Objekten, deren Beziehungen und deren Zusatzinformationen systematisch auf IFC-Entitäten und IFC-Relationen abgebildet wird.

Die Abbildung erfolgt nicht in einem Schritt, sondern über eine dreistufige Trennung:

```text
internes Domänenmodell
        ↓
IFC-nahe Mappingrepräsentation
        ↓
IFC-Entitäten und Relationen
```

Das Domänenmodell in `src/domain/robot-tasks/types.ts` ist bewusst frei von STEP-Syntax, `web-ifc`-Konstruktoren und Express-IDs des Zielmodells. Die mittlere Stufe wird durch einen typisierten Recordgraphen gebildet (`src/ifc/robot-tasks/records.ts`), der bereits IFC-Entitätsnamen als Diskriminatoren verwendet, aber weiterhin reine TypeScript-Datenstrukturen ohne Dateizugriff enthält. Erst die äußere Stufe erzeugt konkrete IFC-Instanzen. Diese Trennung hat zwei Konsequenzen: Die fachliche Mappingentscheidung ist unabhängig von der Serialisierungstechnik prüfbar, und die Domänenschicht bleibt frei von Infrastrukturabhängigkeiten. Die technische Exportpipeline selbst wird in Kapitel 5 behandelt.

Die Übersetzung ist in `src/ifc/robot-tasks/mapper.ts` als reine Funktion realisiert: Sie nimmt eine `RobotMission` entgegen und liefert einen deterministischen, flachen Recordgraphen mit expliziten graphlokalen Referenzen. Eine Mission wird nur abgebildet, wenn die Domänenvalidierung keine blockierenden Fehler meldet; ungültige Missionen können damit gar nicht erst in eine IFC-Repräsentation überführt werden.

## 4.7.2 Mission und Tasks

Sowohl die Mission als auch die ausführbaren Einzelschritte werden auf `IfcTask` abgebildet. Diese Entscheidung nutzt aus, dass `IfcTask` in IFC nicht auf elementare Arbeitsschritte beschränkt ist, sondern auch als zusammenfassender Prozessknoten verwendet werden kann:

```text
RobotMission → übergeordneter IfcTask
RobotTask    → untergeordneter IfcTask
```

Beide Rollen werden im Recordgraphen explizit unterschieden (`role: "MISSION" | "EXECUTABLE_TASK"`) und in IFC über `ObjectType` markiert: Der Missionsknoten trägt `RobotMission`, die ausführbaren Schritte tragen `RobotTask`. Die stabile Domänenkennung wird jeweils in `Identification` geschrieben, sodass die Zuordnung zwischen Domänenobjekt und IFC-Entität nicht von einer Express-ID abhängt. `PredefinedType` wird beim Schreiben durchgängig auf `USERDEFINED` gesetzt, weil die Robotiksemantik durch das Aufzählungsspektrum von `IfcTaskTypeEnum` nicht abgedeckt ist. Optionale Domänenangaben werden auf vorhandene Attribute abgebildet: `status` auf `Status`, `priority` auf die IFC-Ganzzahlskala von 1 (niedrig) bis 4 (kritisch).

Die Mission bildet damit den übergeordneten fachlichen Kontext, ohne selbst ausführbar zu sein; die Robotiksemantik im engeren Sinne liegt ausschließlich an den untergeordneten Tasks.

## 4.7.3 Hierarchie und Sequenzen

Die in Abschnitt 4.5 begründete Trennung von Enthaltensein und Ausführungsabhängigkeit wird auf IFC-Ebene durch zwei verschiedene Relationstypen abgebildet:

```text
Mission → Tasks              = IfcRelNests
Task → nachfolgender Task    = IfcRelSequence
```

Pro Mission wird genau eine `IfcRelNests`-Relation erzeugt, deren `RelatingObject` der Missionsknoten ist und deren `RelatedObjects` die untergeordneten Tasks in der Reihenfolge der Missionsliste enthalten. Für jede Domänensequenz wird dagegen eine eigene `IfcRelSequence`-Relation mit Vorgänger- und Nachfolgerprozess sowie dem übernommenen Sequenztyp erzeugt. Die stabile Sequenz-ID der Domäne wird in `Name` abgelegt.

Entscheidend ist, dass beide Strukturen unabhängig voneinander sind: Die Nesting-Reihenfolge ist eine Darstellungs- und Zugehörigkeitsordnung, keine Ausführungsreihenfolge. Eine Mission ohne Sequenzen bleibt hierarchisch vollständig, besitzt aber keine zeitlichen Abhängigkeiten.

## 4.7.4 Objektbezüge

Die in Abschnitt 4.6 eingeführten Rollen von Objektzuordnungen werden auf zwei IFC-Zuweisungsrelationen abgebildet. Maßgeblich ist dabei, in welcher Rolle ein Gebäudeobjekt am Task beteiligt ist:

- Direkt adressierte Zielobjekte werden über `IfcRelAssignsToProcess` an den Task gebunden. Der Relationsname wird aus dem Aktionstyp abgeleitet: `PASS_THROUGH` ergibt `PASSES_THROUGH`, `NAVIGATE_TO` ergibt `NAVIGATES_TO`, alle übrigen Aktionen ergeben `OPERATES_ON`.
- Indirekt betroffene Objekte werden über eine zweite `IfcRelAssignsToProcess`-Relation mit dem Namen `AFFECTS` abgebildet.
- Bei `MOVE`-Aufgaben wird die Startreferenz als `IfcRelAssignsToProcess` mit dem Namen `MOVE_FROM` abgebildet, die Zielreferenz dagegen als `IfcRelAssignsToProduct` mit dem Namen `MOVE_TO`.

Die unterschiedliche Behandlung von Start und Ziel folgt der IFC-Richtungslogik: Bei `IfcRelAssignsToProcess` ist der Task der zuweisende Prozess und das Gebäudeobjekt das zugewiesene Objekt; bei `IfcRelAssignsToProduct` ist das Produkt der Bezugspunkt, dem der Task zugeordnet wird. Das Bewegungsziel wird damit als produktbezogener Zielpunkt und nicht als vom Task verarbeitetes Objekt modelliert. Referenzierte Gebäudeobjekte werden im Recordgraphen ausdrücklich als modellexterne Referenzen geführt und nicht als erzeugte Entitäten; die zugrunde liegende Identifikationsstrategie wurde in Abschnitt 4.4 behandelt.

## 4.7.5 Aktions- und Metadaten

Prozessstruktur und Beziehungen lassen sich vollständig mit regulären IFC-Entitäten ausdrücken. Die projektspezifische Robotiksemantik besitzt dagegen keine normative IFC-Entsprechung und wird deshalb über drei eigene Property Sets ergänzt, die über `IfcRelDefinesByProperties` an den jeweiligen `IfcTask` gebunden werden:

- `RobotAction` am ausführbaren Task trägt den Aktionstyp sowie die optionalen Aktionsparameter; mehrwertige Angaben wie Vor- und Nachbedingungen werden als Listenwerte abgelegt.
- `RobotTask` am ausführbaren Task trägt Zeitstempel der Bearbeitung sowie optionale Viewer-Annotationen.
- `RobotMission` am Missionsknoten trägt Missionszeitstempel, die Version des Annotationsschemas und einen Marker für einen explizit gepflegten Missionsplan.

Die Namen der Property Sets verwenden bewusst nicht den reservierten Präfix `Pset_`; der Export bricht ab, wenn ein solcher Name auftreten würde. Damit gilt als zentrale Regel: **Die regulären IFC-Entitäten bilden Prozessstruktur und Beziehungen ab; projektspezifische Robotiksemantik wird ergänzend über eigene Property Sets gespeichert.**

## 4.7.6 Zeitinformationen und Missionsplan

Zeitliche Angaben werden nicht über eigene Property Sets, sondern über die dafür vorgesehenen IFC-Strukturen abgebildet. `RobotTaskTime` wird auf `IfcTaskTime` abgebildet und direkt als Attribut des zugehörigen `IfcTask` referenziert; die Relation entsteht also nicht über eine Eigenschaftszuweisung. Der Missionsplan wird auf `IfcWorkSchedule` abgebildet und über `IfcRelAssignsToControl` mit dem Missionsknoten verbunden.

Diese Infrastruktur wird für jede Mission erzeugt, auch wenn das Domänenmodell keinen expliziten `RobotMissionSchedule` besitzt; in diesem Fall werden Kennung, Name und Startzeit deterministisch aus der Mission abgeleitet. Die Unterscheidung zwischen fachlich gepflegtem und technisch erzeugtem Plan bleibt dennoch erhalten, weil sie im `RobotMission`-Property-Set explizit markiert wird.

## 4.7.7 Gesamtübersicht des Mappings

| Domänenkonzept | IFC-Abbildung |
| --- | --- |
| `RobotMission` | übergeordneter `IfcTask`, `ObjectType = RobotMission` |
| `RobotTask` | untergeordneter `IfcTask`, `ObjectType = RobotTask` |
| Missionshierarchie | `IfcRelNests` |
| Task-Abhängigkeit (`RobotTaskSequence`) | `IfcRelSequence`, Domänen-ID in `Name` |
| direkt adressierte Zielobjekte | `IfcRelAssignsToProcess` mit `OPERATES_ON`, `PASSES_THROUGH` oder `NAVIGATES_TO` |
| betroffene Objekte | `IfcRelAssignsToProcess` mit `AFFECTS` |
| `MOVE`-Startreferenz | `IfcRelAssignsToProcess` mit `MOVE_FROM` |
| `MOVE`-Zielreferenz | `IfcRelAssignsToProduct` mit `MOVE_TO` |
| `RobotTaskTime` | `IfcTaskTime` als direktes `IfcTask`-Attribut |
| `RobotMissionSchedule` | `IfcWorkSchedule` mit `IfcRelAssignsToControl` |
| Aktionssemantik | Property Set `RobotAction` |
| Task-Metadaten | Property Set `RobotTask` |
| Missionsmetadaten und Schemaversion | Property Set `RobotMission` |

Abbildung 4.x fasst diese Zuordnungen als Mappingstruktur zusammen.

```text
RobotMission
   │
   ├───────────────→ IfcTask (ObjectType = RobotMission)
   │                     │
   │                     ├── IfcRelNests ──────────────┐
   │                     ├── IfcRelAssignsToControl → IfcWorkSchedule
   │                     └── RobotMission Property Set │
   │                                                   │
   ▼                                                   ▼
RobotTask ─────────────────────────────────→ IfcTask (ObjectType = RobotTask)
   │                                              │
   ├─ Sequenz ─────────→ IfcRelSequence           │
   ├─ Zielobjekte ─────→ IfcRelAssignsToProcess (OPERATES_ON /
   │                     PASSES_THROUGH / NAVIGATES_TO)
   ├─ betroffene Obj. ─→ IfcRelAssignsToProcess (AFFECTS)
   ├─ MOVE-Start ──────→ IfcRelAssignsToProcess (MOVE_FROM)
   ├─ MOVE-Ziel ───────→ IfcRelAssignsToProduct (MOVE_TO)
   ├─ Zeit ────────────→ IfcTaskTime
   ├─ ActionProperties → RobotAction Property Set
   └─ Metadaten ───────→ RobotTask Property Set
```

*Abbildung 4.x: Systematische Abbildung des internen Robotermissionsmodells auf IFC-Prozess-, Relations-, Zeit- und Property-Set-Strukturen. Vorgeschlagene Position: unmittelbar nach der Mappingtabelle in Abschnitt 4.7.7.*

## 4.7.8 Anforderung an die bidirektionale Abbildung

Da der Missionsroundtrip Bestandteil des Prototyps ist, genügt es nicht, eine Abbildungsrichtung zu definieren. Die erzeugte IFC-Struktur muss zusätzlich so eindeutig interpretierbar sein, dass daraus wieder ein gültiges Domänenmodell entsteht:

```text
RobotMission → IFC-Missionsgraph → RobotMission
```

Daraus ergeben sich Anforderungen an das Mapping selbst. Jede Missionsentität muss anhand stabiler Marker als projekteigen erkennbar sein; das leisten die `ObjectType`-Werte, der `USERDEFINED`-Typ und die eigenen Property-Set-Namen. Jede Domänenkennung muss aus IFC rekonstruierbar sein, weshalb Missions-, Task- und Sequenzkennungen in Attributen und nicht nur implizit über die Graphstruktur abgelegt werden. Die Rollen der Objektzuordnungen müssen unterscheidbar bleiben, weshalb der Relationsname semantisch belegt und nicht frei gewählt ist. Schließlich müssen abgeleitete von fachlich gepflegten Informationen unterscheidbar sein, was den Marker für den expliziten Missionsplan begründet. Die technische Umsetzung von Reader, Replacement-Export, Roundtrip-Koordination, semantischem Vergleich und Quellverwaltung wird in Kapitel 5 beschrieben.

## 4.7.9 Version des Annotationsschemas

Das Mapping schreibt in das `RobotMission`-Property-Set eine eigene Versionsangabe des Annotationsmodells, die als Konstante zentral gepflegt wird und aktuell den Wert `1.0.0` besitzt. Sie erlaubt es, projekteigene Missionsannotationen eindeutig als solche zu erkennen und spätere Änderungen des eigenen Annotationsschemas kontrolliert zu behandeln; Annotationen ohne diese Angabe werden beim Lesen als Altbestand behandelt und über definierte Kompatibilitätsregeln interpretiert.

Diese Version ist strikt von der IFC-Schemaversion zu unterscheiden. IFC4 beziehungsweise IFC4X3 beschreiben das zugrunde liegende Datenschema, während die Annotationsversion ausschließlich die projektspezifische Missionsmodellierung innerhalb dieses Schemas versioniert. Für das Mapping selbst ist die IFC-Schemaversion nachrangig: Alle verwendeten Entitäten und Relationen existieren in beiden unterstützten Schemafamilien, sodass die Schemawahl lediglich die beim Schreiben verwendeten Konstruktoren bestimmt und die Abbildungsvorschrift unverändert lässt.

---

# Nachweistabelle

| Mappingaussage | Status | Implementierungsnachweis |
| --- | --- | --- |
| Dreistufige Trennung Domäne → IFC-nahe Records → IFC-Entitäten | direkt implementiert | `src/domain/robot-tasks/types.ts`; `src/ifc/robot-tasks/records.ts`; `src/ifc/robot-tasks/mapper.ts`; `src/ifc/model-export/webIfcMissionWriter.ts` |
| Mapping nur bei fehlerfreier Domänenvalidierung | direkt implementiert | `src/ifc/robot-tasks/mapper.ts` (`validateMission`, `IfcRobotTaskMappingError`) |
| `RobotMission` → `IfcTask` mit `ObjectType = RobotMission`, Rolle `MISSION` | direkt implementiert | `src/ifc/robot-tasks/mapper.ts`; `src/ifc/robot-tasks/records.ts` |
| `RobotTask` → `IfcTask` mit `ObjectType = RobotTask`, Rolle `EXECUTABLE_TASK` | direkt implementiert | `src/ifc/robot-tasks/mapper.ts` |
| Domänen-ID in `Identification`, `PredefinedType = USERDEFINED` | direkt implementiert | `src/ifc/robot-tasks/mapper.ts`; `src/ifc/model-export/webIfcMissionWriter.ts` |
| Priorität `low/medium/high/critical` → 1…4 | direkt implementiert | `src/ifc/robot-tasks/mapper.ts` (`ifcPriority`); Preflight in `webIfcMissionWriter.ts` |
| Genau eine `IfcRelNests`-Relation pro Mission, Reihenfolge aus `mission.tasks` | direkt implementiert | `src/ifc/robot-tasks/mapper.ts` |
| Eine `IfcRelSequence` je Domänensequenz, Sequenz-ID in `Name` | direkt implementiert | `src/ifc/robot-tasks/mapper.ts`; `src/ifc/model-export/webIfcMissionWriter.ts` |
| Zielobjekte → `OPERATES_ON` / `PASSES_THROUGH` / `NAVIGATES_TO` | direkt implementiert | `src/ifc/robot-tasks/mapper.ts` (`targetAssignmentName`) |
| Betroffene Objekte → `AFFECTS` | direkt implementiert | `src/ifc/robot-tasks/mapper.ts` |
| `MOVE`-Start → `MOVE_FROM`, `MOVE`-Ziel → `IfcRelAssignsToProduct` `MOVE_TO` | direkt implementiert | `src/ifc/robot-tasks/mapper.ts` (`mapObjectAssignments`) |
| Begründung der Richtungslogik von Process- vs. Product-Zuweisung | externe IFC-Quelle erforderlich | Attributsemantik gemäß IFC-Spezifikation; im Code nur durch die gewählte Relationsart belegt |
| Drei Property Sets `RobotAction`, `RobotTask`, `RobotMission` über `IfcRelDefinesByProperties` | direkt implementiert | `src/ifc/robot-tasks/mapper.ts`; `src/ifc/robot-tasks/records.ts` |
| Kein `Pset_`-Präfix; Export bricht andernfalls ab | direkt implementiert | `src/ifc/model-export/webIfcMissionWriter.ts` (Preflight und Serialisierung) |
| Listenwertige Aktionsparameter als `IfcPropertyListValue` | direkt implementiert | `src/ifc/robot-tasks/mapper.ts` (`addListValue`) |
| `RobotTaskTime` → `IfcTaskTime` als direktes `IfcTask`-Attribut | direkt implementiert | `src/ifc/robot-tasks/records.ts` (`taskTime`); `webIfcMissionWriter.ts` |
| `IfcWorkSchedule` + `IfcRelAssignsToControl` auch ohne expliziten Domänen-Schedule | direkt implementiert | `src/ifc/robot-tasks/mapper.ts` (Fallback auf Missions-ID und `createdAt`) |
| Marker für explizit gepflegten Missionsplan im `RobotMission`-Property-Set | direkt implementiert | `src/ifc/robot-tasks/mapper.ts` (`HasExplicitSchedule`) |
| Annotationsversion `1.0.0` im `RobotMission`-Property-Set | direkt implementiert | `src/ifc/robot-tasks/annotationSchema.ts`; `src/ifc/robot-tasks/mapper.ts` |
| Fehlende Versionsangabe wird als Altbestand über Kompatibilitätsregeln behandelt | direkt implementiert | `src/ifc/model-import/webIfcMissionReader.ts` |
| Anforderung der eindeutigen Rückinterpretierbarkeit der Mappingstruktur | aus Implementierung abgeleitet | `src/ifc/model-import/webIfcMissionReader.ts` (Prüfung von `ObjectType`, `PredefinedType`, `Identification`, Relationsnamen) |
| Schemaunabhängigkeit der Abbildungsvorschrift bei IFC4 und IFC4X3 | aus Implementierung abgeleitet | `src/ifc/model-export/ifcSchemaAdapter.ts` (nur Auswahl der Konstruktornamensräume) |
| `IfcTask` auch als zusammenfassender Prozessknoten zulässig | externe IFC-Quelle erforderlich | Belegung durch IFC-Spezifikation notwendig |

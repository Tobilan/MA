# Repository Map: IFC-Viewer und Robotermissionen

> **Repository:** `Tobilan/poc_thatopen`  
> **Geprüfter Commit:** `674ede3bf2e7e6cf466bc4c16fe06c90fbb1753c`  
> **Kurzform:** `674ede3`  
> **Commit-Kontext:** Merge des Roundtrip-Features  
> **Zweck dieser Datei:** Kompakte Orientierung für Codex und Claude, damit nicht bei jeder Aufgabe das gesamte Repository erneut untersucht werden muss.

## 1. Verwendungsregel

Diese Datei ist eine **Orientierungshilfe**, keine eigenständige Beweisquelle.

Für Arbeiten an der Masterarbeit oder am Editor gilt:

1. Zuerst die konkrete Aufgabendatei lesen.
2. Danach diese Repository Map lesen.
3. Nur die für die Aufgabe genannten Dateien öffnen.
4. Kein vollständiger Repository-Scan, sofern die Aufgabe ihn nicht ausdrücklich erfordert.
5. Konkrete Implementierungsbehauptungen immer an den hier genannten Quelldateien des geprüften Commits verifizieren.
6. Bei einem anderen Commit prüfen, ob diese Map noch aktuell ist.
7. Widerspricht der Quellcode dieser Datei, ist der Quellcode maßgeblich und diese Map muss aktualisiert werden.

Empfohlene Anweisung in `AGENTS.md`:

```text
Read docs/ai/REPOSITORY_MAP_IFC_EDITOR.md before inspecting the IFC editor
repository broadly. Use it for orientation and inspect only the files required
for the current task. Treat the map as stale when the referenced commit differs
from the commit under review.
```

---

## 2. Projektzweck und Abgrenzung

Das Repository implementiert einen browserbasierten IFC- und Fragments-Viewer als Proof of Concept für eine Masterarbeit. Gebäudemodelle können geladen, performant dargestellt und für die Erstellung strukturierter Robotermissionen verwendet werden.

Zum geprüften Commit sind insbesondere umgesetzt:

- Laden lokaler IFC- und `.frag`-Dateien;
- Rendering über That Open Fragments;
- Auswahl von IFC-Objekten auch bei überlagernder Geometrie;
- internes Domänenmodell für Missionen, Tasks und Sequenzen;
- In-Memory- und `localStorage`-Persistenz;
- Validierung von Missionen, Tasks und Abhängigkeitsgraphen;
- reines Mapping des Domänenmodells auf IFC-nahe Records;
- Import erkannter, projekteigener Missionsannotationen aus direkt geladenen IFC-Dateien;
- quellgestützter Export nach IFC4 und IFC4X3;
- Ersetzen statt Anhängen des projekteigenen Missionsgraphen;
- Wiederöffnen, Reimport und semantischer Vergleich des Exports;
- Erhalt bestehender IFC-`GlobalId`s für deterministisch wiedererkannte Missionsrecords.

Nicht Bestandteil des Proof of Concept sind:

- physische Robotersteuerung;
- Pfadplanung und Navigation;
- allgemeine strukturelle IFC-Bearbeitung;
- verlustfreier Roundtrip beliebiger Fragments-Änderungen;
- IFC2X3-Schreiben;
- Backend-Persistenz;
- Mehrbenutzerbetrieb;
- Authentifizierung;
- vollständige BCF-Workflows.

---

## 3. Technologiestack

| Bereich | Technologie |
|---|---|
| Sprache | TypeScript |
| Build und Entwicklungsserver | Vite, Node.js, npm |
| 3D-Darstellung | Three.js |
| BIM-Komponenten | `@thatopen/components`, `@thatopen/components-front` |
| performante Modelldarstellung | `@thatopen/fragments` |
| IFC-Lesen und STEP-Schreiben | `web-ifc` |
| UI | `@thatopen/ui`, `@thatopen/ui-obc` |
| Tests | Node.js Test Runner, Bündelung mit esbuild |

Wichtige Versionen am geprüften Commit:

```text
@thatopen/components        ~3.2.0
@thatopen/components-front  ~3.2.0
@thatopen/fragments         ~3.2.0
@thatopen/ui                ~3.2.0
@thatopen/ui-obc            ~3.2.0
three                       ^0.175.0
web-ifc                     ^0.0.72
typescript                  5.2.2
vite                        ^7.1.5
```

---

## 4. Build- und Prüfkommandos

```bash
npm install
npm run dev
npm run build
npm test
npm run typecheck:test
npx eslint src test --ext .ts
```

Zuordnung:

| Kommando | Bedeutung |
|---|---|
| `npm run dev` | Vite-Entwicklungsserver |
| `npm run build` | TypeScript-Kompilierung und Vite-Produktionsbuild |
| `npm test` | vollständige Robotermissions-Test-Suite |
| `npm run typecheck:test` | TypeScript-Prüfung der Tests |
| `npx eslint src test --ext .ts` | statische Codeprüfung |

---

## 5. Top-Level-Struktur

```text
.
├── IFC/
│   ├── 01_Haus.ifc
│   └── 03_Institute.ifc
├── src/
│   ├── application/robot-tasks/
│   ├── domain/robot-tasks/
│   ├── ifc/
│   │   ├── model-export/
│   │   ├── model-import/
│   │   ├── model-roundtrip/
│   │   └── robot-tasks/
│   ├── persistence/robot-tasks/
│   ├── ui-templates/
│   ├── viewer/robot-tasks/
│   ├── globals.ts
│   ├── main.ts
│   └── style.css
├── test/robot-tasks/
├── AGENTS.md
├── README.md
├── package.json
├── tsconfig.json
├── tsconfig.test.json
└── vite.config.ts
```

Die IFC-Referenzmodelle dienen Entwicklung und Evaluation. Die Anwendung ist nicht auf diese Dateien festgelegt.

---

## 6. Architekturüberblick

Das Projekt folgt einer geschichteten, an Ports und Adaptern orientierten Architektur.

```text
UI / That Open
      |
      v
Composition Root: src/main.ts
      |
      +-------------------------+
      |                         |
      v                         v
Application                  Viewer-Adapter
      |                         |
      v                         v
Domain                    Fragments / Metadaten
      |
      +-------------------------+
      |
      v
Persistenz und IFC-Infrastruktur
```

Abhängigkeiten sollen zum Domänenmodell zeigen. Three.js, Fragments, Browser-Persistenz und `web-ifc` bleiben an den äußeren Schichten.

### Schichten und Hauptpfade

| Schicht | Hauptpfad | Verantwortung |
|---|---|---|
| Composition Root | `src/main.ts` | Aufbau von Viewer, Services, Repositories, Roundtrip und UI |
| Domain | `src/domain/robot-tasks/` | Framework-unabhängige Typen, Builder, Sequenzen und Validierung |
| Application | `src/application/robot-tasks/` | Anwendungsfälle, Repository-Port, Import-Upsert und semantischer Vergleich |
| Persistenz | `src/persistence/robot-tasks/` | In-Memory-, `localStorage`- und auswählbare Adapter |
| Viewer-Adapter | `src/viewer/robot-tasks/` | Auswahl, Metadaten, Highlights und stabile IFC-Referenzen |
| IFC-Mapping | `src/ifc/robot-tasks/` | Reines Mapping auf typisierte IFC-nahe Records |
| IFC-Export | `src/ifc/model-export/` | Quellregister, Schemaadapter, Schreiben, Ersetzen und Verifikation |
| IFC-Import | `src/ifc/model-import/` | Read-only-Rekonstruktion projekteigener Missionsgraphen |
| Roundtrip-Orchestrierung | `src/ifc/model-roundtrip/` | Quellzuordnung, Import-Upsert, Export-Sicherheit und Source Advancement |
| UI | `src/ui-templates/` | Modelle, Selektion, Missionen, Viewpoints und Viewer-Werkzeuge |
| Tests | `test/robot-tasks/` | Unit-, Integrations- und Roundtrip-Tests |

---

## 7. Zentrale Einstiegsdateien

### `src/main.ts`

Composition Root der Browseranwendung.

Die Datei:

- initialisiert That Open Components und die UI;
- erstellt World, Kamera, Renderer, Grid und Postprocessing;
- initialisiert Fragments und den IFC-Loader;
- konfiguriert `web-ifc` mit Version `0.0.72`;
- erstellt das Quellregister für direkte IFC-Imports;
- markiert strukturell geänderte Fragments-Modelle als unsicher für Export;
- erstellt Auswahlquelle, Metadatenresolver, Highlight-Port und Selection Manager;
- erstellt das auswählbare Mission Repository und den `RobotMissionService`;
- erstellt `IfcMissionImportService`;
- erstellt `IfcModelExportService`;
- verbindet Import, Export, Speicher und Provenienz über den `IfcMissionRoundtripCoordinator`;
- verbindet Pointer-, Kamera-, Clipping- und UI-Ereignisse.

Diese Datei zuerst lesen, wenn die Aufgabe die Gesamtintegration, die Laufzeitverdrahtung oder den Datenfluss zwischen UI und Infrastruktur betrifft.

### `src/ui-templates/sections/models.ts`

Zentrale UI-Datei für:

- direkten IFC-Import;
- `.frag`-Import;
- Modell-ID-Erzeugung;
- Registrierung der IFC-Quellbytes;
- Start des Missionsimports nach erfolgreichem IFC-Laden;
- Auswahl des Exportmodells;
- Aufruf des source-scoped Exports;
- Download des verifizierten IFC;
- Anzeige von Warnungen und Fehlern;
- Aktualisierung des Missionspanels.

Wichtige Reihenfolge beim direkten IFC-Laden:

```text
Datei lesen
-> Modell-ID bestimmen
-> IFC über That Open laden
-> direkte IFC-Provenienz registrieren
-> ursprüngliche IFC-Bytes registrieren
-> Missionsimport ausführen
-> Repository aktualisieren
-> Missions-UI aktualisieren
```

---

## 8. Domänenmodell

### Pfad

```text
src/domain/robot-tasks/
```

### Öffentliche Dateien

```text
builders.ts
sequencing.ts
types.ts
validation.ts
index.ts
```

### Zentrale Typen

```text
RobotMission
RobotTask
RobotTaskSequence
RobotMissionSchedule
RobotTaskTime
RobotActionProperties
RobotObjectReference
TaskViewpoint
```

### Unterstützte Aktionen

```text
OPEN
CLOSE
SWITCH_ON
SWITCH_OFF
MOVE
PASS_THROUGH
NAVIGATE_TO
```

Diese Werte sind projektspezifische Robotikwerte und keine nativen IFC-Enumerationen.

### Wichtige Domänenregeln

- `RobotMission` ist das Aggregat-Root.
- Die Task-Liste bildet Hierarchie und Anzeigeordnung ab.
- Ausführungsabhängigkeiten werden separat als Sequenzen gespeichert.
- Aktionssemantik gehört an den `RobotTask`, nicht an das IFC-Zielobjekt.
- Das Domänenmodell darf nicht von Three.js, Fragments, Browser-Speicher oder STEP-Syntax abhängen.
- `GlobalId` ist die bevorzugte dauerhafte Objektidentität.
- `modelId + expressId` ist nur ein modelllokaler Fallback.
- `modelId` dient der Quellabgrenzung im Roundtrip.
- Zeitinformationen gehören in `RobotTaskTime`.
- Validierung unterscheidet blockierende Fehler und Warnungen.

---

## 9. Application Layer

### Pfad

```text
src/application/robot-tasks/
```

### Öffentliche Dateien

```text
missionRepository.ts
importRobotMissions.ts
robotMissionService.ts
robotMissionServiceError.ts
robotMissionSemanticComparison.ts
index.ts
```

### Verantwortlichkeiten

#### `missionRepository.ts`

Port für die Speicherung vollständiger Mission-Aggregate.

#### `robotMissionService.ts`

Anwendungsservice für das Erstellen, Bearbeiten, Löschen, Sequenzieren und Validieren von Missionen und Tasks.

#### `importRobotMissions.ts`

Atomarer Bulk-Upsert rekonstruierter Missionen:

- vorhandene Missionen mit gleicher ID werden ersetzt;
- neue Missionen werden ergänzt;
- nicht betroffene Missionen bleiben erhalten;
- doppelte IDs im Import werden abgelehnt;
- importierte Zeitstempel werden nicht durch normale Erstellungslogik überschrieben.

#### `robotMissionSemanticComparison.ts`

Kanonisiert Missionen und vergleicht die beabsichtigten Domain-Aggregate mit den erneut aus IFC importierten Aggregaten.

Der Vergleich berücksichtigt unter anderem:

- stabile Objektidentität;
- sortierte mengenartige Objektzuordnungen;
- Task-Zeiten und deren IFC-kompatible Lexikalisierung;
- Missionen, Tasks und Sequenzen;
- Action Properties;
- Viewpoints und Markerpositionen;
- explizite oder nicht explizite Schedule-Daten.

---

## 10. Persistenz

### Pfad

```text
src/persistence/robot-tasks/
```

### Öffentliche Dateien

```text
inMemoryMissionRepository.ts
localStorageMissionRepository.ts
robotMissionPersistenceError.ts
selectableMissionRepository.ts
index.ts
```

### Speicherarten

| Modus | Adapter | Lebensdauer |
|---|---|---|
| kein persistenter Speicher | `InMemoryRobotMissionRepository` | aktuelle Browser-Sitzung |
| lokaler Speicher | `LocalStorageRobotMissionRepository` | Browserprofil und Origin |
| auswählbarer Speicher | `SelectableRobotMissionRepository` | Fassade über die verfügbaren Modi |
| Backend | kein aktiver Adapter | nicht implementiert |

Local-Storage-Key:

```text
ifc-viewer:robot-missions:domain-v1
```

Wichtige Grenze:

```text
Mission-Persistenz != IFC-Quellregister
```

Die ursprünglichen IFC-Bytes bleiben nur in der Browser-Sitzung im `IfcSourceModelRegistry`.

Das Umschalten des Speichermodus kopiert oder migriert keine Missionen.

---

## 11. Viewer-Auswahl und IFC-Objektreferenzen

### Pfad

```text
src/viewer/robot-tasks/
```

### Öffentliche Dateien

```text
model-provenance.ts
selection-adapter.ts
selection-metadata.ts
selection-types.ts
that-open-selection-candidate-source.ts
that-open-selection-highlight-port.ts
viewer-object-selection-manager.ts
viewerSelectionReferenceError.ts
index.ts
```

### Verantwortlichkeiten

- Raycasts über geladene Fragments-Modelle;
- Sortieren und Deduplizieren von Treffern;
- Ausschließen geclippter oder optional verborgener Objekte;
- Auflösen von IFC-Klasse, `GlobalId`, `expressId` und Name;
- Vorschau mehrerer überlagernder Kandidaten;
- getrennte Hervorhebungen für Hover, Kandidat und bestätigte Auswahl;
- Schutz vor veralteten asynchronen Raycast-Ergebnissen;
- Konvertierung der bestätigten Auswahl in `RobotObjectReference`;
- Unterscheidung direkt geladener IFC-Modelle und reiner `.frag`-Modelle.

Für Aufgaben zur Objektauswahl zuerst lesen:

```text
viewer-object-selection-manager.ts
that-open-selection-candidate-source.ts
selection-metadata.ts
selection-adapter.ts
model-provenance.ts
```

---

## 12. Reines IFC-Mapping

### Pfad

```text
src/ifc/robot-tasks/
```

### Öffentliche Dateien

```text
annotationSchema.ts
mapper.ts
records.ts
index.ts
```

### Verantwortung

Diese Schicht übersetzt gültige Domain-Missionen in typisierte, IFC-nahe Records.

Sie:

- verändert keine IFC-Datei;
- lädt kein WASM;
- serialisiert keinen STEP-Text;
- enthält keine Viewerlogik;
- enthält keine Importlogik.

Die Trennung erlaubt Tests der IFC-Modellierung ohne `web-ifc`.

---

## 13. IFC-Annotationsmodell

### Abbildung

| Domänenkonzept | IFC-Struktur |
|---|---|
| Mission | Parent-`IfcTask`, `ObjectType = RobotMission` |
| ausführbarer Task | Child-`IfcTask`, `ObjectType = RobotTask` |
| Missionhierarchie | `IfcRelNests` |
| Task-Abhängigkeit | `IfcRelSequence`; Domain-ID in `Name` |
| Task-Zeit | `IfcTask.TaskTime -> IfcTaskTime` |
| Missionsplan | `IfcWorkSchedule` und `IfcRelAssignsToControl` |
| direkte Interaktion | `IfcRelAssignsToProcess`, meist `OPERATES_ON` |
| indirekte Wirkung | `IfcRelAssignsToProcess`, `AFFECTS` |
| Durchqueren | Relation mit `PASSES_THROUGH` |
| Navigation | Relation mit `NAVIGATES_TO` |
| MOVE-Start | `IfcRelAssignsToProcess`, `MOVE_FROM` |
| MOVE-Ziel | `IfcRelAssignsToProduct`, `MOVE_TO` |
| konkrete Aktion | task-eigenes `IfcPropertySet` `RobotAction` |
| Task-Metadaten | task-eigenes `IfcPropertySet` `RobotTask` |
| Missionsmetadaten | mission-eigenes `IfcPropertySet` `RobotMission` |

### Property-Set-Regeln

- Custom Property Sets verwenden nicht den reservierten Präfix `Pset_`.
- `RobotAction` enthält unter anderem `ActionType`.
- Optionale Action-Werte sind beispielsweise:
  - `TargetState`
  - `TargetObjectRole`
  - `AffectedObjectRole`
  - `RequiredCapability`
  - `Preconditions`
  - `Postconditions`
  - `SuccessCondition`
- `RobotMission` speichert:
  - Audit-Metadaten;
  - `AnnotationSchemaVersion = "1.0.0"`;
  - `HasExplicitSchedule`.

---

## 14. IFC-Export

### Pfad

```text
src/ifc/model-export/
```

### Öffentliche Dateien

```text
ifcModelExportError.ts
ifcMissionReplacementError.ts
ifcModelExportService.ts
ifcSchemaAdapter.ts
ifcSourceModelRegistry.ts
webIfcMissionWriter.ts
webIfcMissionReplacer.ts
webIfcStructuralCodec.ts
index.ts
```

### Rollen

#### `ifcSourceModelRegistry.ts`

Verwaltet pro direkt geladenem IFC-Modell:

- Runtime-`modelId`;
- Dateiname;
- ursprüngliche beziehungsweise zuletzt verifizierte IFC-Bytes;
- Sicherheitsstatus für strukturelle Änderungen.

#### `ifcModelExportService.ts`

Zentrale Exportfassade. Sie verbindet:

- Quellregister;
- Domain-to-IFC-Mapping;
- Replacement;
- strukturelles Speichern und Wiederöffnen;
- Verifikation.

#### `webIfcMissionWriter.ts`

Erzeugt die schemaabhängigen `web-ifc`-Entities und Relationen aus den gemappten Records.

#### `webIfcMissionReplacer.ts`

Ersetzt ausschließlich den erkannten projekteigenen Missionsgraphen. Vor dem ersten Löschen müssen Ownership-, Referenz- und Identitätsprüfungen abgeschlossen sein.

#### `webIfcStructuralCodec.ts`

Öffnet das Quell-IFC in einer isolierten `web-ifc`-Instanz, führt Schreiben und Speichern aus und öffnet das Ergebnis in einer frischen Instanz erneut.

### Unterstützte Schemas

```text
IFC4
IFC4X3
IFC4X3_ADD1
IFC4X3_ADD2
```

Nicht unterstützt:

```text
IFC2X3
```

### Exportprinzip

Der Export ist kein Append-Vorgang.

```text
ausgewählte IFC-Quelle
+ aktuelle, dieser Quelle zugeordnete Missionen
-> vollständiges Ersetzen des erkannten projekteigenen Missionsgraphen
-> Speichern
-> erneutes Öffnen
-> Reimport
-> semantischer Vergleich
-> erst danach Download und Source Advancement
```

---

## 15. IFC-Import

### Pfad

```text
src/ifc/model-import/
```

### Öffentliche Dateien

```text
ifcMissionImportError.ts
ifcMissionImportService.ts
ifcMissionImportTypes.ts
webIfcMissionReader.ts
index.ts
```

### Rollen

#### `ifcMissionImportService.ts`

Besitzt die isolierte `web-ifc`-Laufzeit für den Read-only-Import aus IFC-Bytes.

#### `webIfcMissionReader.ts`

- liest IFC-Entities;
- erkennt projekteigene Missionen;
- validiert deren Graphen;
- rekonstruiert Domain-Aggregate;
- erzeugt strukturierte Issues;
- erzeugt Roundtrip-Provenienz;
- führt Domainvalidierung aus.

#### `ifcMissionImportTypes.ts`

Enthält Importresultate, Issues und Provenienztypen.

### Ownership-Erkennung

Ein Missions-Root muss unter anderem sein:

```text
IfcTask
ObjectType = RobotMission
PredefinedType = USERDEFINED
stabile Identification
```

Ausführbare Kinder müssen unter anderem:

```text
über genau eine passende IfcRelNests-Struktur zugeordnet sein
ObjectType = RobotTask
PredefinedType = USERDEFINED
task-eigene Property Sets RobotAction und RobotTask besitzen
```

Unabhängige, nicht zum Projekt gehörende Prozesspläne werden ignoriert.

Eine IFC-Datei ohne erkannte Robotermission ist ein erfolgreicher leerer Import.

---

## 16. Roundtrip-Orchestrierung

### Pfad

```text
src/ifc/model-roundtrip/
```

### Öffentliche Dateien

```text
ifcMissionRoundtripCoordinator.ts
ifcMissionRoundtripError.ts
ifcMissionSourceRegistry.ts
loadedModelMissionImport.ts
index.ts
```

### `IfcMissionRoundtripCoordinator`

Verbindet:

- aktives Mission Repository;
- ausgewählten Speichermodus;
- IFC-Importer;
- IFC-Exporter;
- IFC-Quellregister;
- Zuordnung von Missionen zu geladenen Quellen;
- Import- und Export-Sicherheitsstatus.

### Importablauf

```text
direktes IFC erfolgreich laden
-> Quellbytes registrieren
-> Missionen read-only importieren
-> gültige Missionen über importRobotMissions upserten
-> Missionen der Quelle und dem aktiven Speichermodus zuordnen
-> Warnungen und Fehler registrieren
```

Blockierende Importfehler:

- verhindern den Export für diese Quelle;
- verhindern nicht das Anzeigen des Gebäudemodells;
- können andere unabhängige gültige Missionen unberührt lassen.

### Exportablauf

```text
Quellzustand prüfen
-> aktiven Speichermodus prüfen
-> Missionen auf ausgewähltes Modell begrenzen
-> modellfremde Referenzen ablehnen
-> Added/Updated/Removed bestimmen
-> IFC exportieren und Missionsgraph ersetzen
-> Ergebnis erneut importieren
-> Domain-Aggregate semantisch vergleichen
-> verifizierte Bytes als neue Quelle registrieren
-> Mission-Source-Zuordnung fortschreiben
```

### Infrastrukturgrenzen

Folgende Informationen gehören nicht in `RobotMission`:

- Runtime-Quellmodell;
- Import-Provenienz;
- Storage-Mode-Zuordnung;
- Export-Sicherheitsstatus;
- bisher verifizierte Quellbytes.

---

## 17. Export-Sicherheitsregeln

Der Export muss abgebrochen werden, wenn mindestens eine der folgenden Bedingungen vorliegt:

- keine direkte IFC-Quelle vorhanden;
- nur ein `.frag`-Modell vorhanden;
- strukturelle Fragments-Änderungen erkannt;
- blockierende Import-Issues für die Quelle;
- aktiver Speichermodus stimmt nicht mit der Quellzuordnung überein;
- Mission verweist ausdrücklich auf ein anderes geladenes Modell;
- Missionvalidierung schlägt fehl;
- IFC-Zielobjekt kann nicht eindeutig aufgelöst werden;
- doppelte Mission-, Task-, Record-, Provenienz- oder `GlobalId`-Ansprüche;
- unbekannte externe IFC-Relation referenziert einen zu löschenden Missionsrecord;
- Ergebnis kann nicht im gleichen Schema wieder geöffnet werden;
- erneuter Missionsimport enthält Fehler;
- semantischer Vergleich unterscheidet sich von den erwarteten Aggregaten.

Bestehende Gebäudeobjekte und deren `GlobalId`s dürfen durch den Annotationsroundtrip nicht ersetzt werden.

---

## 18. Identität und Provenienz

### Dauerhafte fachliche Identität

```text
IFC GlobalId
```

### Modelllokaler Fallback

```text
modelId + expressId
```

`expressId` ist keine dauerhafte Identität über Schreibvorgänge hinweg.

Beim Replacement:

- erkannte Records desselben deterministischen Domain-Konzepts behalten ihre IFC-`GlobalId`;
- neue Konzepte erhalten neue IFC-`GlobalId`s;
- neu serialisierte Records erhalten neue lokale `expressId`s;
- Gebäudeobjekte behalten ihre bestehenden `GlobalId`s.

Die Roundtrip-Provenienz liegt außerhalb des Domain-Modells und kann enthalten:

- Mission-ID;
- Task-ID;
- IFC-Entity-Typ;
- bisherige `expressId`;
- optionale IFC-`GlobalId`;
- deterministische Record-Identität;
- Quell-`modelId`.

---

## 19. UI-Struktur

### Root

```text
src/ui-templates/index.ts
```

Exportiert:

```text
sections
groups
toolbars
buttons
grids
```

### Relevante Sections

```text
src/ui-templates/sections/models.ts
src/ui-templates/sections/elements-data.ts
src/ui-templates/sections/robot-mission-tasks.ts
src/ui-templates/sections/viewpoints.ts
src/ui-templates/sections/robotMissionPanelRefresh.ts
```

### Zuständigkeiten

| Datei | Zuständigkeit |
|---|---|
| `models.ts` | Laden, Quellregistrierung, Missionsimport, Exportauswahl und IFC-Download |
| `elements-data.ts` | Darstellung der IFC- und Auswahlmetadaten |
| `robot-mission-tasks.ts` | Missions- und Taskeditor |
| `viewpoints.ts` | Viewer-Viewpoints |
| `robotMissionPanelRefresh.ts` | gezieltes Aktualisieren des Missionspanels nach Import |

Die UI darf keine eigene parallele Missionswahrheit erzeugen. Fachliche Änderungen laufen über den Application Service und das aktive Repository.

---

## 20. Tests

### Einstiegspunkt

```text
test/robot-tasks/index.test.ts
```

### Registrierte Test-Suites

```text
robot-mission-domain.test.ts
ifc-relation-mapper.test.ts
ifc-model-export.test.ts
ifc-mission-writer.test.ts
ifc-mission-replacer.test.ts
ifc-mission-export.integration.test.ts
ifc-mission-replacement.integration.test.ts
ifc-mission-roundtrip-coordinator.test.ts
ifc-mission-reader.test.ts
import-robot-missions.test.ts
robot-mission-semantic-comparison.test.ts
robot-mission-persistence.test.ts
robot-mission-service.test.ts
selectable-mission-repository.test.ts
selection-candidate-source.test.ts
viewer-selection-adapter.test.ts
viewer-object-selection-manager.test.ts
```

### Relevante Testgruppen nach Thema

| Thema | Primäre Tests |
|---|---|
| Domain und Validierung | `robot-mission-domain.test.ts` |
| Application Service | `robot-mission-service.test.ts` |
| Persistenz | `robot-mission-persistence.test.ts`, `selectable-mission-repository.test.ts` |
| Selection | `selection-candidate-source.test.ts`, `viewer-selection-adapter.test.ts`, `viewer-object-selection-manager.test.ts` |
| reines IFC-Mapping | `ifc-relation-mapper.test.ts` |
| IFC-Writer | `ifc-mission-writer.test.ts` |
| IFC-Exportfassade | `ifc-model-export.test.ts` |
| Replacement | `ifc-mission-replacer.test.ts`, `ifc-mission-replacement.integration.test.ts` |
| IFC-Import | `ifc-mission-reader.test.ts`, `import-robot-missions.test.ts` |
| Roundtrip-Koordination | `ifc-mission-roundtrip-coordinator.test.ts` |
| semantische Gleichheit | `robot-mission-semantic-comparison.test.ts` |
| realer Export/Reimport | `ifc-mission-export.integration.test.ts` |

Der Build- und Testzustand wurde für diese Map nicht lokal ausgeführt. Die Kommandos und Testabdeckung wurden aus dem Repository am angegebenen Commit rekonstruiert.

---

## 21. Bekannte Einschränkungen am geprüften Commit

- Backend-Missionsspeicher ist nur als architektonischer Platzhalter vorhanden.
- `.frag`-Dateien besitzen keine vertrauenswürdige IFC-Quelle für den Export.
- Strukturelle Fragments-Änderungen werden nicht in IFC zurückgeschrieben.
- IFC2X3 wird vom Missionswriter nicht unterstützt.
- Alte Annotierungsdateien ohne Schema-Version, Sequenz-ID oder Schedule-Marker benötigen Kompatibilitätsinferenz.
- Pfadplanung und physische Robotersteuerung sind nicht implementiert.
- Viewpoint- und Markerfelder sind im Domain- und Mapping-Layer vorhanden, aber nicht vollständig in den Missionseditor integriert.
- Vollständige IFC-Bearbeitung ist nicht implementiert.
- BCF, Authentifizierung und Mehrbenutzerbetrieb sind nicht implementiert.
- Entwicklungsressourcen für Fragments-Worker und `web-ifc`-WASM sollten für eine produktive Bereitstellung selbst gehostet und versionsgebunden werden.

---

## 22. Empfohlene minimale Dateimengen für Codex

### Beschreibung der Gesamtarchitektur

```text
README.md
src/main.ts
src/domain/robot-tasks/index.ts
src/application/robot-tasks/index.ts
src/persistence/robot-tasks/index.ts
src/viewer/robot-tasks/index.ts
src/ifc/robot-tasks/index.ts
src/ifc/model-import/index.ts
src/ifc/model-export/index.ts
src/ifc/model-roundtrip/index.ts
```

### Kapitel zum Domänen- und Annotationsmodell

```text
src/domain/robot-tasks/types.ts
src/domain/robot-tasks/validation.ts
src/ifc/robot-tasks/annotationSchema.ts
src/ifc/robot-tasks/records.ts
src/ifc/robot-tasks/mapper.ts
test/robot-tasks/robot-mission-domain.test.ts
test/robot-tasks/ifc-relation-mapper.test.ts
```

### Kapitel zum IFC-Import

```text
src/ifc/model-import/ifcMissionImportTypes.ts
src/ifc/model-import/ifcMissionImportService.ts
src/ifc/model-import/webIfcMissionReader.ts
src/application/robot-tasks/importRobotMissions.ts
test/robot-tasks/ifc-mission-reader.test.ts
test/robot-tasks/import-robot-missions.test.ts
```

### Kapitel zum IFC-Export und Roundtrip

```text
src/ifc/model-export/ifcModelExportService.ts
src/ifc/model-export/ifcSourceModelRegistry.ts
src/ifc/model-export/webIfcMissionWriter.ts
src/ifc/model-export/webIfcMissionReplacer.ts
src/ifc/model-export/webIfcStructuralCodec.ts
src/ifc/model-roundtrip/ifcMissionRoundtripCoordinator.ts
src/ifc/model-roundtrip/ifcMissionSourceRegistry.ts
src/application/robot-tasks/robotMissionSemanticComparison.ts
test/robot-tasks/ifc-mission-export.integration.test.ts
test/robot-tasks/ifc-mission-replacement.integration.test.ts
test/robot-tasks/ifc-mission-roundtrip-coordinator.test.ts
```

### Kapitel zur Objektauswahl

```text
src/viewer/robot-tasks/viewer-object-selection-manager.ts
src/viewer/robot-tasks/that-open-selection-candidate-source.ts
src/viewer/robot-tasks/selection-metadata.ts
src/viewer/robot-tasks/selection-adapter.ts
src/viewer/robot-tasks/model-provenance.ts
src/ui-templates/sections/elements-data.ts
test/robot-tasks/selection-candidate-source.test.ts
test/robot-tasks/viewer-selection-adapter.test.ts
test/robot-tasks/viewer-object-selection-manager.test.ts
```

### Kapitel zur Benutzeroberfläche

```text
src/main.ts
src/ui-templates/sections/models.ts
src/ui-templates/sections/robot-mission-tasks.ts
src/ui-templates/sections/elements-data.ts
src/ui-templates/sections/viewpoints.ts
src/style.css
```

---

## 23. Aktualisierung dieser Map

Diese Datei muss aktualisiert werden, wenn sich mindestens einer dieser Punkte ändert:

- Layer oder Verzeichnisstruktur;
- Composition Root;
- öffentliche Barrel-Exports;
- Domain-Typen oder Aktionen;
- IFC-Annotationsschema;
- Import-Ownership-Regeln;
- Replacement-Grenze;
- Source- oder Storage-Zuordnung;
- Export-Sicherheitsregeln;
- unterstützte IFC-Schemas;
- Test-Einstiegspunkt;
- Build-Kommandos;
- wesentliche implementierte oder nicht implementierte Features.

Bei einer Aktualisierung angeben:

```text
Reviewed commit: <vollständiger Commit-Hash>
Updated: <Datum>
Reason: <kurze Änderungsbeschreibung>
```

---

## 24. Kurzfassung für Agenten

```text
Das Repository ist ein geschichteter TypeScript/Vite-PoC.

Domain:
src/domain/robot-tasks/

Use Cases:
src/application/robot-tasks/

Persistence:
src/persistence/robot-tasks/

Selection:
src/viewer/robot-tasks/

Pure IFC mapping:
src/ifc/robot-tasks/

Read-only mission import:
src/ifc/model-import/

Safe source-backed export:
src/ifc/model-export/

Source-scoped roundtrip:
src/ifc/model-roundtrip/

UI:
src/ui-templates/

Composition:
src/main.ts

Tests:
test/robot-tasks/

Die annotierte IFC-Datei ist der fachliche Roundtrip-Träger.
Das interne Domain-Modell bleibt davon getrennt.
Robotik-Aktionssemantik liegt am Task.
GlobalId ist die bevorzugte dauerhafte Objektidentität.
expressId ist nur modelllokal.
Mission-Source-Zuordnung und Provenienz sind Infrastrukturmetadaten.
Export ersetzt nur erkannte projekteigene Missionsgraphen.
Verifizierte Source-Bytes werden erst nach Save/Reopen/Reimport/Compare fortgeschrieben.
Strukturelle Fragments-Änderungen sind nicht roundtripfähig.
```

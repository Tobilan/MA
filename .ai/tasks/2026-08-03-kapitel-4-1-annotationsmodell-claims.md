# Claim-Inventar: Kapitel 4.1 zum IFC-basierten Annotationsmodell

## Geprüfter Implementierungsstand

- **Repository:** `https://github.com/Tobilan/poc_thatopen`
- **Branch:** `main`
- **Commit:** `674ede3bf2e7e6cf466bc4c16fe06c90fbb1753c`
- **Prüfart:** flacher, temporärer Read-only-Checkout; Quell- und Testdateien wurden gelesen, aber die Viewer-Tests wurden nicht ausgeführt, weil im Checkout keine Abhängigkeiten installiert waren und das Viewer-Repository für diese Thesis-Aufgabe nicht verändert werden sollte.

## IMPLEMENTATION_CLAIM I-01: Getrenntes internes Domänenmodell

Der Prototyp besitzt ein von IFC-Serialisierung und Viewerzustand getrenntes TypeScript-Domänenmodell für Robotermissionen, Roboteraufgaben, Aktionsparameter, Objektbezüge, Sequenzen und optionale Zeitangaben.

- `src/domain/robot-tasks/types.ts:6` definiert das Laufzeitvokabular `ROBOT_ACTION_TYPES`.
- `src/domain/robot-tasks/types.ts:59` definiert `RobotObjectReference` mit bevorzugter `globalId` sowie modellgebundenem Fallback aus `modelId` und `expressId`.
- `src/domain/robot-tasks/types.ts:151` definiert `RobotTask`.
- `src/domain/robot-tasks/types.ts:86-106` definiert die taskbezogenen Felder `requiredCapability`, `preconditions`, `postconditions` und `successCondition` in `RobotActionProperties`.
- `src/domain/robot-tasks/types.ts:212` definiert `RobotTaskSequence`.
- `src/domain/robot-tasks/types.ts:249` definiert `RobotMission`; Zeile 269 führt Sequenzen getrennt von der Task-Hierarchie.

## IMPLEMENTATION_CLAIM I-02: Explizite Validierung

Der Prototyp validiert Referenzen, aktionsspezifische Pflichtbezüge, Missionseigenschaften, eindeutige Task-IDs und Ausführungsabhängigkeiten einschließlich Selbstbezügen und Zyklen.

- `src/domain/robot-tasks/validation.ts:42` prüft IFC-Objektreferenzen.
- `src/domain/robot-tasks/validation.ts:125-151` behandelt fehlende IFC-Klasseninformation als Warnung und bekannte, aktionsbezogen unzulässige Klassen als Fehler.
- `src/domain/robot-tasks/validation.ts:165` prüft Start- und Zielreferenz von `MOVE`.
- `src/domain/robot-tasks/validation.ts:200` prüft objektbezogene Aktionen.
- `src/domain/robot-tasks/validation.ts:331` aggregiert die Missionsvalidierung.
- `src/domain/robot-tasks/sequencing.ts:105` validiert Ausführungsabhängigkeiten und Zyklen.
- Entsprechende Testfälle sind in `test/robot-tasks/robot-mission-domain.test.ts:70-363` definiert; sie wurden in dieser Thesis-Aufgabe nicht ausgeführt.

## IMPLEMENTATION_CLAIM I-03: Aufgabenbezogene Aktionssemantik und IFC-Mapping

Das Mapping schreibt die konkrete Aktionssemantik in ein dem erzeugten `IfcTask` zugeordnetes Property Set `RobotAction`, nicht in die referenzierten Gebäudeobjekte. Hierarchie und Ausführungsabhängigkeiten werden getrennt abgebildet.

- `src/ifc/robot-tasks/mapper.ts:131` erzeugt die taskbezogenen `RobotAction`-Properties.
- `src/ifc/robot-tasks/mapper.ts:433` beginnt das validierte Missionsmapping.
- `src/ifc/robot-tasks/mapper.ts:464` erzeugt `IfcRelNests`.
- `src/ifc/robot-tasks/mapper.ts:501` erzeugt `IfcRelSequence`.
- `src/ifc/robot-tasks/annotationSchema.ts:2` versioniert die projektspezifische Annotation mit `1.0.0`.
- `AGENTS.md:401-415` dokumentiert die projektinterne Benennung eigener Property Sets ohne `Pset_`; `test/robot-tasks/ifc-relation-mapper.test.ts:360-376` definiert den zugehörigen Mapping-Test.
- Zugehörige, nicht ausgeführte Testfälle stehen in `test/robot-tasks/ifc-relation-mapper.test.ts:174-400`.

## IMPLEMENTATION_CLAIM I-04: Begrenzte Rekonstruktion und Missionsroundtrip

Für direkt geladene IFC-Quelldaten rekonstruiert der Prototyp erkannte projektspezifische Robotermissionsgraphen. Beim Missions-Export werden die exportierten Bytes erneut importiert und semantisch verglichen, bevor sie als nächste verifizierte Quelle registriert werden. Der Nachweis ist ausdrücklich auf Robotermissionsannotationen begrenzt.

- `src/ifc/model-import/ifcMissionImportService.ts` öffnet IFC-Bytes in einer isolierten `web-ifc`-Instanz und delegiert die Rekonstruktion.
- `src/ifc/model-import/webIfcMissionReader.ts:1451` liest erkannte Missionsgraphen; die rekonstruierte Mission wird zuvor ab Zeile 1414 gegen das Domänenmodell validiert.
- `src/ifc/model-roundtrip/ifcMissionRoundtripCoordinator.ts:152` koordiniert den quellgebundenen Export.
- `src/ifc/model-roundtrip/ifcMissionRoundtripCoordinator.ts:228-253` exportiert, importiert erneut, vergleicht semantisch und ersetzt die registrierten Quellbytes nur nach erfolgreicher Prüfung.
- `src/ifc/model-roundtrip/loadedModelMissionImport.ts` überspringt den Missionsimport bei reinen Fragments-Modellen.
- Integrationsszenarien sind in `test/robot-tasks/ifc-mission-export.integration.test.ts:178-299` und `test/robot-tasks/ifc-mission-replacement.integration.test.ts:374-739` definiert; sie wurden in dieser Thesis-Aufgabe nicht ausgeführt.

## Grenzen und nicht belegte Aussagen

- Kein allgemeiner verlustfreier IFC-Roundtrip für beliebige strukturelle Änderungen.
- Keine Rekonstruktion eines reinen Fragments-Modells ohne zugehörige IFC-Quelldaten.
- Kein am Commit belegter roboterbezogener JSON-Export als eigenständiges Ausführungsformat; JSON wird lediglich für lokale Browserpersistenz verwendet.
- Keine belegte ROS-Integration, reale Robotersteuerung, Wegpunktplanung, Anfahrposenberechnung oder virtuelle Flächenunterteilung.
- Die vorhandenen Viewer-Testdateien belegen definierte Prüfszenarien, aber in diesem Arbeitszyklus keinen erfolgreichen Testlauf.

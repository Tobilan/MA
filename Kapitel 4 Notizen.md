## Kapitel 4 – Konzeption des IFC-basierten Annotationsmodells

### 4.1 Modellierungsziele

* Robotermissionen
* ausführbare Tasks
* IFC-Objektbezug
* Erweiterbarkeit
* Interoperabilität
* stabile Identitäten
* Trennung von Semantik und Geometrie

### 4.2 Internes Domänenmodell

* `RobotMission`
* `RobotTask`
* `RobotTaskSequence`
* `RobotObjectReference`
* `RobotActionProperties`
* `RobotTaskTime`
* Missionszeitplan

### 4.3 Robotische Aktionen

* `OPEN`
* `CLOSE`
* `SWITCH_ON`
* `SWITCH_OFF`
* `MOVE`
* `PASS_THROUGH`
* `NAVIGATE_TO`
* Aktionsparameter
* Vorbedingungen
* Nachbedingungen
* Erfolgskriterien

### 4.4 IFC-Objektreferenzierung

* `GlobalId`
* `expressId`
* `modelId`
* IFC-Klasse
* Objektname
* dauerhafte Referenz
* Rendering-ID
* Referenzauflösung

### 4.5 Missionshierarchie

* Parent-Task
* Child-Tasks
* Mission
* Teilaufgaben
* `IfcTask`
* `IfcRelNests`

### 4.6 Task-Sequenzen

* Vorgänger
* Nachfolger
* Ausführungsreihenfolge
* Abhängigkeiten
* `FINISH_START`
* `IfcRelSequence`
* Zyklusfreiheit

### 4.7 Task-Objekt-Zuordnung

* Zielobjekt
* betroffenes Objekt
* Startreferenz
* Zielreferenz
* `OPERATES_ON`
* `AFFECTS`
* `PASSES_THROUGH`
* `NAVIGATES_TO`
* `MOVE_FROM`
* `MOVE_TO`
* `IfcRelAssignsToProcess`
* `IfcRelAssignsToProduct`

### 4.8 Task-spezifische Property Sets

* `RobotAction`
* `RobotTask`
* `RobotMission`
* `IfcPropertySet`
* `IfcRelDefinesByProperties`
* `ActionType`
* `TargetState`
* `RequiredCapability`
* Custom Properties

### 4.9 Zeitmodell

* `IfcTaskTime`
* Startzeit
* Endzeit
* Dauer
* Restzeit
* Fertigstellungsgrad
* Missionszeitplan
* `IfcWorkSchedule`
* `IfcRelAssignsToControl`

### 4.10 IFC-Mapping

* Domänenmodell
* IFC-Zwischenrepräsentation
* Mappingregeln
* Entity-Erzeugung
* Relationsgraph
* Schemaabhängigkeit
* IFC4
* IFC4X3

### 4.11 Validierung

* Pflichtfelder
* Aktionsvalidierung
* Objektklassen
* Referenzprüfung
* MOVE-Validierung
* Sequenzprüfung
* Zyklenerkennung
* Fehler
* Warnungen
* Exportfreigabe

### 4.12 Persistenz- und Austauschkonzept

* annotierte IFC-Datei
* kanonisches Format
* internes Laufzeitmodell
* `localStorage`
* Backend-Persistenz
* Robot-JSON
* Editorzustand
* Roundtrip

### 4.13 Grenzen und Erweiterungen

* projektspezifische Semantik
* generische IFC-Viewer
* Missionsimport
* vollständiger Roundtrip
* Teilflächenreferenzen
* `RobotInteractionCapability`
* Waypoints
* ROS-Transformation
* Roboterausführung

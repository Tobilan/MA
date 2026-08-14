# Arbeitsnotiz zur Quellenprüfung

**Gelesene Orientierungsdateien:** `REPOSITORY_MAP_IFC_EDITOR_674ede3.md`, `Strukturübersicht.txt`, `repo_structure.txt`

**Gezielt geprüfte Implementierungsdateien**

| Datei | Für Kapitel 4.3 relevante Befunde |
| --- | --- |
| `src/domain/robot-tasks/types.ts` | `ROBOT_ACTION_TYPES` als `readonly`-Tupel mit sieben Werten (`OPEN`, `CLOSE`, `SWITCH_ON`, `SWITCH_OFF`, `MOVE`, `PASS_THROUGH`, `NAVIGATE_TO`); `RobotActionType` als davon abgeleiteter Union-Typ; `actionType` ist ein Pflichtfeld von `RobotTask`; `RobotActionProperties` mit ausschließlich optionalen Feldern (`targetState`, `targetObjectRole`, `affectedObjectRole`, `requiredCapability`, `preconditions`, `postconditions`, `successCondition`); Quellcode-Kommentar an `RobotObjectReferenceMetadata` hält ausdrücklich fest, dass Objektreferenzen keine Aktionsanforderung enthalten. |
| `src/domain/robot-tasks/builders.ts` | `createRobotTask` verlangt `actionType`, übernimmt `properties` unverändert; `assignRobotActionProperties` ersetzt das Property-Objekt immutabel am Task; `assignMovementReferences` ändert `actionType` bewusst **nicht**. |
| `src/domain/robot-tasks/validation.ts` | Laufzeitprüfung der Aktionsart gegen `ROBOT_ACTION_TYPES` (`TASK_ACTION_TYPE_REQUIRED`, `TASK_ACTION_TYPE_UNSUPPORTED`); aktionsabhängige Regeln (`MOVE_START_REQUIRED`, `MOVE_TARGET_REQUIRED`, `TASK_TARGET_REQUIRED`, `PASS_THROUGH_REFERENCE_REQUIRED`); Klassenprüfung „door-like“ bzw. „switch-like“ mit Warnung `TARGET_TYPE_UNKNOWN` bei fehlender `ifcClass`; Regel `OBJECT_ACTION_PROPERTIES_FORBIDDEN` weist Aktionsproperties an Objektreferenzen ab. Für `NAVIGATE_TO` existiert **keine** aktionsspezifische Regel. |
| `src/ifc/robot-tasks/mapper.ts` (nur zur Verifikation) | `ActionType` wird stets in das taskeigene Property Set `RobotAction` geschrieben, die optionalen Properties nur bei Vorhandensein; Zielrelationen heißen `PASSES_THROUGH`, `NAVIGATES_TO` bzw. `OPERATES_ON`. Details gehören zu 4.6/4.7. |

**Nicht durch die Implementierung gedeckt:** `INVESTIGATE`, QR-Code-Verarbeitung, Skill-/Verhaltensketten. Diese Inhalte sind im Kapitel ausdrücklich als konzeptionelle Beispiele gekennzeichnet.

---

# 4.3 Modellierung der Roboteraktionen

## Aktionsart als Pflichtangabe des Tasks

Jeder ausführbare Schritt einer Mission wird durch einen `RobotTask` repräsentiert, der die beabsichtigte Roboteraktion über das Pflichtfeld `actionType` trägt. Der zulässige Wertebereich ist in `src/domain/robot-tasks/types.ts` als unveränderliches Tupel `ROBOT_ACTION_TYPES` mit den Werten `OPEN`, `CLOSE`, `SWITCH_ON`, `SWITCH_OFF`, `MOVE`, `PASS_THROUGH` und `NAVIGATE_TO` definiert. Aus derselben Konstante leitet sich der Union-Typ `RobotActionType` ab, so dass Compile-Zeit-Typisierung und Laufzeitprüfung auf eine einzige Quelle zurückgeführt werden. Diese doppelte Absicherung ist notwendig, weil Missionen auch aus deserialisierten JSON- oder IFC-Daten entstehen, die die statische Typprüfung umgehen; `src/domain/robot-tasks/validation.ts` meldet unbekannte oder fehlende Werte deshalb als eigene Befunde. Die Aktionswerte sind projektspezifische Bezeichner und keine native IFC-Enumeration.

## Abstraktionsgrad der Aktionsbezeichner

Die implementierten Aktionsarten sind bewusst als **prototypische semantische Bezeichner** zu verstehen. Sie benennen den fachlich beabsichtigten Zielzustand oder Vorgang, nicht den technischen Ablauf auf Roboterebene. Der Bezeichner `OPEN` beschreibt, dass ein Bedienobjekt anschließend als geöffnet gelten soll; er legt weder eine Anfahrstrategie noch eine Greif- oder Betätigungsstrategie fest. Auf Robotikseite kann derselbe Task auf eine deutlich längere Handlungskette abgebildet werden, etwa: Objekt anfahren, Bedienelement erkennen, Manipulationspose bestimmen, Betätigung ausführen und das Ergebnis überprüfen. Der IFC-basierte Task beschreibt somit primär, *was* erreicht werden soll, während die spätere roboterspezifische Ausführung festlegt, *wie* dieses Ziel erreicht wird. Diese Zurückhaltung ist eine Modellierungsentscheidung: Eine Annotation, die bereits Bewegungsprimitive oder Skill-Parameter enthielte, wäre an eine konkrete Roboterplattform gebunden und im Gebäudemodell nicht mehr allgemein interpretierbar.

## Erweiterbarkeit der Aktionssemantik

Der vorliegende Wertebereich ist kein abschließender Aktionskatalog, sondern der Umfang, der für den Proof of Concept benötigt wurde. Da die Aktionswerte an einer einzigen Stelle definiert sind, wirkt eine Ergänzung unmittelbar auf Typisierung, Validierung und Editor. Als konzeptionelles Beispiel lässt sich eine Aktion `INVESTIGATE` denken, die einen definierten Bereich untersuchen, dort hinterlegte Handlungsanweisungen erfassen, eine Informationsquelle wie einen QR-Code erkennen, deren Inhalt interpretieren und daraus weitere roboterspezifische Aktionen ableiten würde. Weder `INVESTIGATE` noch eine QR-Code-Verarbeitung sind Bestandteil der aktuellen Implementierung; das Beispiel dient ausschließlich dazu, die angestrebte Abstraktionsebene zu verdeutlichen. Es zeigt zugleich, dass auch eine im Ablauf sehr komplexe Aktion auf Modellebene ein einzelner semantischer Bezeichner bleiben kann, sofern die Interpretation der Ausführungsschicht überlassen wird.

## Ergänzende Aktionssemantik über `RobotActionProperties`

Der reine `actionType` ist häufig zu grob, um eine Aufgabe eindeutig zu beschreiben. `RobotTask` besitzt deshalb das optionale Feld `properties` vom Typ `RobotActionProperties`, dessen sämtliche Felder ihrerseits optional sind: `targetState` benennt den erwarteten Zustand nach der Ausführung, `targetObjectRole` und `affectedObjectRole` präzisieren die semantische Rolle der referenzierten Objekte, `requiredCapability` benennt die erforderliche Roboterfähigkeit, `preconditions` und `postconditions` halten Bedingungen vor und nach der Ausführung fest, und `successCondition` beschreibt das beobachtbare Erfolgskriterium. Ein Task mit `actionType = OPEN` kann damit um einen gewünschten Zielzustand, eine benötigte Fähigkeit, Vor- und Nachbedingungen sowie ein Erfolgskriterium ergänzt werden, ohne dass die Aktionsart selbst weiter ausdifferenziert werden muss. Die Werte sind als Freitext modelliert; kontrollierte Vokabulare sind im Prototyp bewusst nicht vorgegeben. Zugewiesen wird das gesamte Property-Objekt über `assignRobotActionProperties` in `src/domain/robot-tasks/builders.ts`, das eine unveränderte Kopie des Tasks mit neuem Änderungszeitstempel liefert.

## Trennung von Aktion und IFC-Objekt

Die konkrete Aktionssemantik gehört ausschließlich zum `RobotTask` und nicht zur Objektreferenz. `RobotObjectReference` trägt nur Identitäts- und Beschreibungsdaten wie `globalId`, `modelId`, `expressId`, `ifcClass` und `name`; der Quellcode hält ausdrücklich fest, dass hier keine angeforderte Roboteraktion abgelegt wird. Diese Regel wird nicht nur typisiert, sondern auch zur Laufzeit geprüft: Enthält eine deserialisierte Objektreferenz ein Property-Objekt mit Feldern aus `RobotActionProperties`, meldet die Validierung dies als eigenen Fehlerfall. Fachlich bedeutet das, dass eine `IfcDoor` ein Gebäudeelement bleibt und keine Missionsabsicht trägt. Mehrere Tasks können dieselbe Tür referenzieren, um sie zu öffnen, zu schließen, sie anzufahren oder sie zu passieren; ebenso können mehrere Missionen unabhängig voneinander auf dasselbe Gebäudemodell verweisen. Die Aktionsart wirkt lediglich als Interpretationsrahmen für die Referenzen: Für `MOVE` sind Start- und Zielreferenz erforderlich, `PASS_THROUGH` verlangt mindestens eine Referenz, und bei `OPEN`, `CLOSE`, `SWITCH_ON` und `SWITCH_OFF` wird die bekannte IFC-Klasse auf Plausibilität geprüft, während fehlende Klasseninformation nur zu einer Warnung führt. Diese Kopplung bleibt damit bewusst schwach; die Prüflogik selbst wird in Kapitel 4.10 behandelt.

## Einordnung zwischen Gebäudemodell und Roboterausführung

Aus den beschriebenen Entscheidungen ergibt sich eine dreistufige Abstraktion: Das Gebäudeobjekt beschreibt die statische Ressource, der semantische `RobotTask` beschreibt die beabsichtigte Wirkung auf diese Ressource, und die roboterspezifische Ausführung beschreibt die tatsächliche Handlungskette. Der Editor deckt gegenwärtig ausschließlich die mittlere Ebene ab. Aspekte wie Manipulationsplanung, Bildverarbeitung, Waypoint-Erzeugung oder konkrete Roboter-Skills sind nicht Gegenstand des Annotationsmodells und werden hier nur als mögliche Interpretationen einer abstrakten Aktion erwähnt. Damit bleibt das Modell gegenüber unterschiedlichen Roboterplattformen offen, und die Verantwortung für die Ausführbarkeit verbleibt in der nachgelagerten Robotikschicht.

---

## Abbildung

**Vorgeschlagene Position:** unmittelbar nach dem Abschnitt „Abstraktionsgrad der Aktionsbezeichner“, spätestens vor der Einordnung am Kapitelende.

```text
implementierte Abstraktion            |  beispielhafte spätere Ausführung
                                      |  (nicht Bestandteil der Implementierung)
--------------------------------------+------------------------------------------
IFC-Objekt (z. B. IfcDoor)            |
        |                             |
        v                             |
RobotTask                             |
  actionType = OPEN                   |      Objekt anfahren
  properties: targetState,            |   -> Bedienelement erkennen
              requiredCapability,     |   -> Manipulationspose bestimmen
              pre-/postconditions,    |   -> Betätigung ausführen
              successCondition        |   -> Ergebnis prüfen
        |                             |
        v                             |
- - - - - - - - - - - - - - - - - - - + - - - - - - - - - - - - - - - - - - - - -
konzeptionelle Erweiterung            |
                                      |
RobotTask                             |      Bereich anfahren
  actionType = INVESTIGATE            |   -> Informationsquelle erkennen
  (nicht implementiert)               |   -> Handlungsanweisung interpretieren
                                      |   -> weitere Aktionen ableiten
```

*Abbildung 4.x: Abstraktionsebenen der Aktionsmodellierung. Die linke Spalte zeigt die im Editor implementierte semantische Beschreibung am `RobotTask`, die rechte Spalte lediglich beispielhafte roboterspezifische Ausführungsketten. Der untere Block kennzeichnet mit `INVESTIGATE` eine konzeptionelle Erweiterung, die nicht Bestandteil der Implementierung ist.*

---

## Nachweistabelle

| Aussage | Status | Implementierungsnachweis |
| --- | --- | --- |
| `actionType` ist ein Pflichtfeld von `RobotTask`. | implementiert | `src/domain/robot-tasks/types.ts` (`RobotTask.actionType: RobotActionType`) |
| Der Wertebereich umfasst genau sieben Aktionsarten und dient als einzige Quelle für Typ und Laufzeitprüfung. | implementiert | `src/domain/robot-tasks/types.ts` (`ROBOT_ACTION_TYPES`, `RobotActionType`); `src/domain/robot-tasks/validation.ts` (`validateTask`) |
| Unbekannte oder fehlende Aktionswerte werden zur Laufzeit gemeldet. | implementiert | `src/domain/robot-tasks/validation.ts` (`TASK_ACTION_TYPE_UNSUPPORTED`, `TASK_ACTION_TYPE_REQUIRED`) |
| `RobotActionProperties` ergänzt den Aktionstyp um optionale semantische Angaben. | implementiert | `src/domain/robot-tasks/types.ts` (`RobotActionProperties`); `src/domain/robot-tasks/builders.ts` (`assignRobotActionProperties`) |
| Aktionsproperties gehören zum Task; an Objektreferenzen werden sie abgelehnt. | implementiert | `src/domain/robot-tasks/types.ts` (`RobotObjectReferenceMetadata`); `src/domain/robot-tasks/validation.ts` (`OBJECT_ACTION_PROPERTIES_FORBIDDEN`) |
| Die Aktionsart bestimmt, welche Objektreferenzen erforderlich bzw. plausibel sind. | implementiert | `src/domain/robot-tasks/validation.ts` (`validateMovementTask`, `validateObjectInteractionTask`) |
| Dasselbe IFC-Objekt kann von mehreren Tasks mit unterschiedlichen Aktionen referenziert werden. | aus Implementierung abgeleitet | Aktionsdaten liegen ausschließlich am Task; Referenzen tragen nur Identität und Metadaten (`types.ts`, `builders.ts`) |
| Die Aktionswerte sind prototypische semantische Bezeichner ohne festgelegten Roboterablauf. | aus Implementierung abgeleitet | Weder Domänentypen noch Builder oder Validierung enthalten Ausführungs-, Pose- oder Skill-Daten |
| Der Wertebereich ist punktuell erweiterbar. | aus Implementierung abgeleitet | Zentrale Definition in `ROBOT_ACTION_TYPES`, von der Typ und Prüfung abhängen |
| `OPEN` entspricht auf Roboterebene einer Kette aus Anfahren, Erkennen, Posebestimmung, Betätigung und Kontrolle. | konzeptionelles Beispiel | kein Implementierungsnachweis; illustrative Ausführungssicht |
| `INVESTIGATE` einschließlich QR-Code-Auswertung als mögliche zusätzliche Aktion. | konzeptionelles Beispiel | nicht implementiert; nicht in `ROBOT_ACTION_TYPES` enthalten |

---

## Offene Review-Punkte

1. **`NAVIGATE_TO` ohne aktionsspezifische Regel:** Die Validierung stellt für `NAVIGATE_TO` keine Referenzanforderung, obwohl der Mapper eine `NAVIGATES_TO`-Relation erzeugt. Zu klären ist, ob dieser Befund in 4.3 als bewusste Offenheit erwähnt oder vollständig nach 4.10 verschoben wird.
2. **Freitextcharakter der Properties:** `targetState`, `requiredCapability` und die Bedingungen sind nicht vokabularisiert. Möglicherweise sollte diese Grenze bereits hier kurz benannt und ansonsten konsequent in 4.12 diskutiert werden.
3. **Redundanz mit Kapitel 8:** Das `INVESTIGATE`-Beispiel berührt den Ausblick (unter anderem `RobotInteractionCapability`). Es ist zu prüfen, ob die Ausführungsbeispiele hier weiter gekürzt und im Ausblick vertieft werden.

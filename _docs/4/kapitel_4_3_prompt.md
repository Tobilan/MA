Erstelle Kapitel **4.3 „Modellierung der Roboteraktionen“** meiner deutschsprachigen Masterarbeit.

Das Kapitel gehört zu:

**4 – Konzeption des IFC-basierten Annotationsmodells**

Halte dieses Unterkapitel bewusst kompakt. Zielumfang:

**ca. 700–1.000 Wörter**

Ich werde den Text anschließend manuell reviewen und mit anderen Entwürfen vergleichen. Verwende keinen automatisierten Writer-/Reviewer-Workflow.

# Quellenbasis

Lies zuerst die im Projektkontext verfügbaren Dateien:

1. `REPOSITORY_MAP_IFC_EDITOR_674ede3.md`
2. `Strukturübersicht.txt`
3. `repo_structure.txt`

Prüfe anschließend gezielt die tatsächliche Implementierung des Editor-Repositories aus dem Projektkontext.

Für Kapitel 4.3 sind insbesondere relevant:

* `src/domain/robot-tasks/types.ts`
* `src/domain/robot-tasks/builders.ts`
* `src/domain/robot-tasks/validation.ts`

Weitere Dateien nur öffnen, wenn sie zur Verifikation einer konkreten Aussage benötigt werden.

Verwende für Dateireferenzen ausschließlich Pfade aus `repo_structure.txt`.

# Ziel des Kapitels

Erkläre, wie Roboteraktionen innerhalb eines `RobotTask` repräsentiert werden und welche Abstraktionsebene diese Aktionen besitzen.

Wichtig ist folgende konzeptionelle Einordnung:

Die derzeit implementierten Aktionsarten wie

* `OPEN`
* `CLOSE`
* `SWITCH_ON`
* `SWITCH_OFF`
* `MOVE`
* `PASS_THROUGH`
* `NAVIGATE_TO`

sind **prototypische semantische Aktionsbezeichner**.

Sie sollen nicht den vollständigen technischen Ablauf auf Roboterebene beschreiben.

Eine Aktion wie

`OPEN`

kann beispielsweise auf Robotikseite auf einen komplexeren Ablauf abgebildet werden:

Objekt anfahren
→ Bedienelement erkennen
→ Manipulationspose bestimmen
→ Greif- oder Betätigungsaktion durchführen
→ Ergebnis überprüfen

Der IFC-basierte Task beschreibt damit primär **was erreicht werden soll**, während die konkrete Roboterausführung später festlegt, **wie dieses Ziel erreicht wird**.

# Erweiterbarkeit der Aktionssemantik

Arbeite heraus, dass die aktuell implementierten Aktionsarten nicht als abschließender Aktionskatalog verstanden werden sollen.

Weitere abstrakte Aktionen könnten ergänzt werden.

Verwende als **klar gekennzeichnetes konzeptionelles Beispiel**:

`INVESTIGATE`

Eine solche Aktion könnte auf Robotikseite beispielsweise bedeuten:

* einen definierten Bereich untersuchen,
* dort hinterlegte Handlungsanweisungen erfassen,
* eine Informationsquelle wie einen QR-Code erkennen,
* die darin enthaltenen Informationen interpretieren,
* darauf basierend weitere roboterspezifische Aktionen ausführen.

Wichtig:

`INVESTIGATE` und die QR-Code-Verarbeitung sind **nicht Bestandteil der aktuellen Implementierung**. Sie dienen ausschließlich dazu, die Erweiterbarkeit und Abstraktionsebene des Aktionsmodells zu veranschaulichen.

Formuliere deshalb beispielsweise:

„Eine denkbare Erweiterung stellt eine Aktion `INVESTIGATE` dar …“

und nicht:

„Der Editor unterstützt `INVESTIGATE`.“

# `RobotActionProperties`

Erläutere knapp die Funktion von `RobotActionProperties`.

Prüfe anhand der Implementierung insbesondere:

* `targetState`
* `targetObjectRole`
* `affectedObjectRole`
* `requiredCapability`
* `preconditions`
* `postconditions`
* `successCondition`

Zeige, dass der reine `actionType` durch zusätzliche semantische Informationen ergänzt werden kann.

Beispielhaft:

`actionType = OPEN`

kann kombiniert werden mit:

* gewünschtem Zielzustand,
* benötigter Roboterfähigkeit,
* Vorbedingungen,
* Nachbedingungen,
* Erfolgskriterium.

Vermeide eine vollständige API-Dokumentation aller Properties.

# Trennung von Aktion und IFC-Objekt

Dieser Punkt ist besonders wichtig.

Erkläre anhand der Implementierung:

**Die konkrete Aktionssemantik gehört zum `RobotTask`, nicht zum `RobotObjectReference`.**

Beispiel:

Eine `IfcDoor` bleibt ein Gebäudeelement.

Verschiedene Tasks können sich auf dieselbe Tür beziehen:

* Tür öffnen,
* Tür schließen,
* zur Tür navigieren,
* Tür passieren.

Dadurch bleibt die Beschreibung des Gebäudes von der konkreten Mission getrennt.

# Abstraktion gegenüber der Roboterausführung

Diskutiere kurz die Trennung zwischen drei Ebenen:

```text
Gebäudeobjekt
    ↓
semantischer RobotTask
    ↓
roboterspezifische Ausführung
```

Beispielsweise:

```text
IfcDoor
    ↓
RobotTask: OPEN
    ↓
konkrete Roboter-Skill-/Verhaltenskette
```

Der Editor beschreibt aktuell die mittlere Ebene.

Folgende Aspekte gehören **nicht** detailliert in Kapitel 4.3:

* ROS-Kommunikation,
* Manipulationsplanung,
* Computer Vision,
* QR-Code-Erkennung,
* Waypoint-Generierung,
* konkrete Roboter-Skills,
* Behavior Trees,
* Pfadplanung.

Diese dürfen ausschließlich als Beispiele für eine spätere Interpretation der abstrakten Aktion erwähnt werden.

# Abgrenzung zu anderen Kapiteln

Verwende `Strukturübersicht.txt`.

Nicht erneut ausführlich behandeln:

* allgemeine Modellierungsziele aus 4.1,
* vollständiges Domänenmodell aus 4.2,
* IFC-Objektreferenzierung aus 4.4,
* Sequenzen aus 4.5,
* IFC-Property-Set-Mapping aus 4.7,
* vollständiges IFC-Mapping aus 4.9,
* Robot-JSON und ROS aus späteren Kapiteln.

Kapitel 4.3 beantwortet im Wesentlichen nur:

**Wie wird die beabsichtigte Roboteraktion fachlich am Task beschrieben und auf welcher Abstraktionsebene befindet sich diese Beschreibung?**

# Wissenschaftlicher Stil

Schreibe vollständig auf Deutsch.

* formaler wissenschaftlicher Stil,
* kompakte Argumentation,
* keine unnötige Wiederholung,
* keine Marketing-Sprache,
* keine erfundenen Quellen,
* Implementierung und konzeptionelle Erweiterungen klar unterscheiden.

Bezeichner wie `RobotTask`, `RobotActionProperties`, `OPEN` oder `PASS_THROUGH` bleiben unverändert.

# Abbildung

Prüfe, ob **eine einzige kleine schematische Abbildung** hilfreich ist.

Geeignet wäre beispielsweise:

```text
IFC-Objekt
   ↓
RobotTask
ActionType = OPEN
   ↓
roboterspezifische Umsetzung
Navigation → Erkennung → Manipulation → Kontrolle
```

oder als Erweiterungsbeispiel:

```text
RobotTask
ActionType = INVESTIGATE
   ↓
Bereich anfahren
   ↓
Informationsquelle erkennen
   ↓
Handlungsanweisung interpretieren
   ↓
weitere Aktionen ableiten
```

Die Abbildung muss deutlich zwischen implementierter Abstraktion und beispielhafter zukünftiger Roboterausführung unterscheiden.

Maximal eine Abbildung. Wenn sie keinen zusätzlichen Erkenntnisgewinn liefert, verzichte darauf.

# Gewünschte Ausgabe

Erstelle:

1. **Kurze Arbeitsnotiz** mit den untersuchten Repository-Dateien und den für das Kapitel relevanten Befunden.
2. **Kapitel 4.3 „Modellierung der Roboteraktionen“** mit ca. 700–1.000 Wörtern.
3. Falls sinnvoll, **eine technische Abbildung** mit deutscher Bildunterschrift und vorgeschlagener Position.
4. Eine kurze **Nachweistabelle**:

| Aussage | Status | Implementierungsnachweis |
| ------- | ------ | ------------------------ |

Unterscheide insbesondere:

* implementiert,
* aus Implementierung abgeleitet,
* konzeptionelles Beispiel.

5. Maximal drei **offene Review-Punkte**.

Die wichtigste inhaltliche Regel lautet:

**Die implementierten Aktionswerte sind prototypische semantische Bezeichner und dürfen nicht so dargestellt werden, als würden sie bereits einen vollständigen roboterspezifischen Handlungsablauf definieren.**

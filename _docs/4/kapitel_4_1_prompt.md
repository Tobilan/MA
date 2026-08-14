Erstelle Kapitel **4.1 „Modellierungsziele“** meiner deutschsprachigen Masterarbeit.

Das Kapitel ist Teil des übergeordneten Kapitels:

**4 – Konzeption des IFC-basierten Annotationsmodells**

Es handelt sich um einen ersten eigenständigen Kapitelentwurf. Verwende keinen automatisierten Writer-/Reviewer-Workflow und führe keine Änderungen an den Repositories durch. Ich werde den erzeugten Text anschließend selbst manuell prüfen, mit anderen Entwürfen vergleichen und überarbeiten.

# 1. Verbindliche Quellenbasis

Arbeite repository-basiert und prüfe Aussagen über die Implementierung tatsächlich am Quellcode.

## Schritt 1: Repository-Übersicht lesen

Lies **zuerst vollständig** diese Repository-Map:

https://github.com/Tobilan/MA/blob/kapitel_4/docs/ai/REPOSITORY_MAP_IFC_EDITOR_674ede3.md

Die Repository-Map dient als Orientierung über Architektur, relevante Dateien, Datenmodelle und Zusammenhänge des IFC-Editors.

Beachte:

* Die Map beschreibt den Stand des Editors zum Commit `674ede3`.
* Nutze sie deshalb primär zur Orientierung und zum Auffinden relevanter Implementierungsstellen.
* Übernimm daraus keine Aussage über den aktuellen Implementierungsstand ungeprüft.

## Schritt 2: Tatsächliche Implementierung prüfen

Untersuche anschließend das tatsächliche Editor-Repository:

https://github.com/Tobilan/poc_thatopen

Bestimme zunächst den aktuell geprüften Commit bzw. `HEAD` und nenne dessen Commit-ID in einer kurzen Arbeitsnotiz vor dem Kapitel.

Für Aussagen wie

* „ist implementiert“,
* „der Editor verwendet“,
* „das Domänenmodell enthält“,
* „die Validierung prüft“,
* „der Export bildet ab“

muss der aktuelle Quellcode die Aussage tatsächlich stützen.

**Das Editor-Repository ist für den Implementierungsstand die maßgebliche Quelle.**

Falls Repository-Map und aktueller Code voneinander abweichen, gilt der aktuelle Code. Weise auf relevante Abweichungen hin, sofern sie Kapitel 4.1 betreffen.

# 2. Ziel von Kapitel 4.1

Kapitel 4.1 soll die **Modellierungsziele und daraus resultierenden grundlegenden Entwurfsprinzipien** des IFC-basierten Annotationsmodells erklären.

Es soll noch **keine vollständige Detailbeschreibung des Domänenmodells oder IFC-Mappings** liefern. Diese Inhalte folgen in späteren Unterkapiteln.

Kapitel 4.1 soll insbesondere verständlich machen:

1. welches Problem das Annotationsmodell lösen soll,
2. welche Anforderungen sich daraus an das Datenmodell ergeben,
3. welche grundlegenden Modellierungsentscheidungen getroffen wurden,
4. weshalb diese Entscheidungen für die spätere Verknüpfung von BIM- und Robotikdaten relevant sind.

# 3. Inhaltliche Schwerpunkte

Prüfe anhand der tatsächlichen Implementierung, welche der folgenden Aspekte für Kapitel 4.1 relevant und nachweisbar sind.

## Robotermissionen und ausführbare Aufgaben

* Beschreibung einer Mission als strukturierte Folge bzw. Menge von Roboteraufgaben,
* Trennung zwischen Mission und einzelnen Tasks,
* Möglichkeit, mehrere Tasks zu einer Mission zusammenzufassen,
* explizite Beschreibung von Beziehungen bzw. Ausführungsreihenfolgen.

Erkläre hier nur das Modellierungsziel. Die konkrete Struktur von `RobotMission`, `RobotTask`, `RobotTaskSequence` usw. wird erst in Kapitel 4.2 detailliert behandelt.

## Verknüpfung mit IFC-Objekten

* Roboteraufgaben sollen sich auf Elemente des Gebäudemodells beziehen können,
* beispielsweise Türen, Schalter oder andere relevante Gebäudeelemente,
* Objektbezüge müssen auch außerhalb der momentanen Viewer-Sitzung nachvollziehbar sein.

Leite daraus die Anforderung nach möglichst stabilen Objektidentitäten ab.

Die konkrete Verwendung von `GlobalId`, `expressId` und `modelId` soll in Kapitel 4.1 nur soweit erläutert werden, wie sie zur Begründung dieses Modellierungsziels notwendig ist. Die technische Detailbehandlung folgt später.

## Trennung von Roboteraktion und Gebäudeobjekt

Untersuche besonders die in der Implementierung erkennbare Trennung zwischen:

* dem IFC-Objekt als Gebäude- bzw. Zielobjekt und
* der konkreten Aktion, die ein Roboter im Rahmen eines Tasks ausführen soll.

Beispielhaft:

* Eine Tür ist ein Gebäudeobjekt.
* `OPEN` beschreibt eine konkrete Aktion eines Tasks auf dieser Tür.
* Die Tür selbst soll nicht dadurch semantisch zu einer „OPEN-Tür“ werden.

Erkläre, weshalb diese Trennung für wiederverwendbare Gebäudemodelle und unterschiedliche Missionen sinnvoll ist.

Vermeide dabei Aussagen über geplante `RobotInteractionCapability`-Annotationen, sofern diese im aktuellen Repository nicht implementiert sind. Solche Konzepte dürfen höchstens klar als mögliche Erweiterung abgegrenzt werden und gehören grundsätzlich nicht zum Kern von Kapitel 4.1.

## Trennung von Semantik, IFC-Persistenz und Darstellung

Prüfe, ob und wie die Implementierung zwischen folgenden Ebenen trennt:

* fachliches Missions-/Taskmodell,
* IFC-Repräsentation,
* Viewer- bzw. Rendering-Struktur.

Erkläre das daraus resultierende Modellierungsziel:

**Robotermissionsdaten sollen nicht von temporären Rendering-Strukturen oder Viewer-spezifischen IDs abhängig sein.**

Gehe noch nicht detailliert auf die technische Implementierungsarchitektur ein; diese gehört in das spätere Implementierungskapitel.

## IFC als Austausch- und Annotationsträger

Beschreibe die Zielsetzung, Missionsinformationen soweit sinnvoll in der IFC-Struktur abzubilden, sodass Gebäudeinformationen und Robotermissionsbezug gemeinsam transportiert werden können.

Wichtig:

Unterscheide streng zwischen

* bereits implementiertem IFC-Export,
* aktuellem Import-/Roundtrip-Stand,
* konzeptionell vorgesehenen Erweiterungen.

Behaupte keinen vollständigen IFC-Roundtrip, falls dieser im geprüften Repository nicht vollständig implementiert ist.

## Erweiterbarkeit

Das Modell soll so aufgebaut sein, dass zusätzliche

* Aktionsarten,
* Task-Eigenschaften,
* Objektrollen,
* zeitliche Beziehungen,
* roboterspezifische Ausleitungen

ergänzt werden können, ohne die grundlegende Modellstruktur neu entwerfen zu müssen.

Begründe Erweiterbarkeit anhand konkreter Architekturentscheidungen nur dann, wenn diese im Repository erkennbar sind.

## Interoperabilität

Diskutiere Interoperabilität vorsichtig.

Unterscheide:

1. syntaktische bzw. strukturelle Nutzung regulärer IFC-Entitäten,
2. projektspezifische Robotiksemantik,
3. tatsächliche Interpretation dieser Semantik durch Fremdsysteme.

Vermeide Aussagen wie:

„Die Annotation kann von beliebigen IFC-Systemen vollständig interpretiert werden.“

wenn das nicht nachgewiesen werden kann.

## Vorbereitung einer späteren Roboterausführung

Das Annotationsmodell soll die fachliche Grundlage für eine spätere Verarbeitungskette liefern, beispielsweise:

IFC-Annotation
→ internes Missionsmodell
→ roboterspezifischer Export
→ Zielpose / Navigation
→ Roboterausführung

Kapitel 4.1 soll diese Verbindung nur motivieren.

Folgende Themen werden **nicht detailliert in Kapitel 4.1 behandelt**:

* ROS,
* Koordinatentransformation,
* Waypoint-Generierung,
* Pfadplanung,
* Robot-JSON,
* Surface Tiling,
* physische Roboterausführung.

Diese gehören in spätere Kapitel bzw. Erweiterungen.

# 4. Erwartete Argumentationsstruktur

Entwickle aus der Implementierung eine zusammenhängende wissenschaftliche Argumentation.

Eine mögliche Struktur ist:

### Einstieg

* Ziel des Annotationsmodells,
* Verbindung von Gebäudemodell und Robotermissionsbeschreibung,
* Anforderungen an eine persistente und maschinenlesbare Repräsentation.

### Modellierungsziele

Darauf aufbauend beispielsweise:

* strukturierte Repräsentation von Missionen und Tasks,
* explizite Verknüpfung mit IFC-Objekten,
* stabile Objektidentität,
* Trennung von Gebäudeobjekt und Roboteraktion,
* Trennung von fachlicher Semantik und Rendering,
* Abbildbarkeit in IFC,
* Validierbarkeit,
* Erweiterbarkeit,
* Vorbereitung roboterspezifischer Weiterverarbeitung.

### Abschließende Überleitung

Schließe Kapitel 4.1 mit einer kurzen Überleitung zu Kapitel 4.2 ab:

Die formulierten Modellierungsziele werden dort durch das konkrete interne Domänenmodell mit Missionen, Tasks, Sequenzen, Objektbezügen und Aktionsparametern umgesetzt.

# 5. Abgrenzung zu den folgenden Kapiteln

Vermeide unnötige Wiederholungen mit späteren Unterkapiteln.

Insbesondere sollen in 4.1 **noch nicht ausführlich erklärt werden**:

* alle Attribute von `RobotMission`,
* alle Attribute von `RobotTask`,
* vollständige TypeScript-Interfaces,
* sämtliche Aktionsarten,
* vollständiges IFC-Entity-Mapping,
* `IfcRelNests`,
* `IfcRelSequence`,
* alle Objektrollen,
* Property Sets im Detail,
* Zeitmodell im Detail,
* Exportalgorithmus,
* Roundtrip-Algorithmus,
* UI des Editors,
* Selection Manager.

Diese Punkte dürfen kurz erwähnt werden, wenn sie zur Begründung einer Designentscheidung notwendig sind. Ihre detaillierte Behandlung folgt später.

# 6. Umgang mit Implementierung und zukünftigen Konzepten

Kennzeichne den Status jeder technischen Aussage korrekt.

Verwende beispielsweise Formulierungen wie:

* **„ist implementiert“** nur bei eindeutigem Code-Nachweis,
* **„wird im Prototyp verwendet“** bei tatsächlich genutzten PoC-Mechanismen,
* **„ist konzeptionell vorgesehen“** für geplante Funktionen,
* **„stellt eine mögliche Erweiterung dar“** für Zukunftsideen.

Vermische diese Kategorien nicht.

Insbesondere dürfen folgende Punkte nicht ohne Code-Nachweis als umgesetzt beschrieben werden:

* vollständiger IFC-Roundtrip,
* Rekonstruktion beliebiger Missionen aus annotierten IFC-Dateien,
* Backend-Persistenz,
* Robot-JSON-Export,
* ROS-Anbindung,
* automatische Waypoint-Generierung,
* automatische Anfahrposen,
* Surface Tiling,
* direkte Robotersteuerung,
* `RobotInteractionCapability`.

# 7. Wissenschaftlicher Stil

Schreibe vollständig auf **Deutsch**.

Verwende:

* formalen wissenschaftlichen Stil,
* präzise technische Formulierungen,
* überwiegend sachliche bzw. unpersönliche Formulierungen,
* zusammenhängende Argumentation statt Aufzählungen,
* klare Übergänge zwischen Absätzen.

Vermeide:

* Marketing-Sprache,
* unnötige Superlative,
* Umgangssprache,
* unbelegte Verallgemeinerungen,
* unnötige Anglizismen,
* Wiederholungen,
* sehr kurze, abgehackte Absätze.

Standardisierte technische Bezeichnungen bleiben unverändert, beispielsweise:

* `IfcTask`
* `IfcRelSequence`
* `GlobalId`
* `RobotMission`
* `RobotTask`
* `web-ifc`
* That Open Components

Erfinde keine deutschen Übersetzungen für Quellcode- oder IFC-Bezeichner.

# 8. Quellen und Nachweise

Dieses Kapitel basiert primär auf dem entwickelten System.

Für **Implementierungsbehauptungen**:

* nenne die relevante Repository-Datei oder den relevanten Modulbereich,
* nenne nach Möglichkeit konkrete Klassen, Interfaces oder Funktionen,
* nenne den geprüften Commit.

Verwende keine erfundenen Literaturquellen.

Falls für eine Aussage zusätzlich eine normative IFC-Quelle erforderlich ist, beispielsweise für die Bedeutung einer IFC-Entität:

* recherchiere ausschließlich in offiziellen buildingSMART-Spezifikationen,
* kennzeichne diese externe Quelle klar getrennt vom Implementierungsnachweis.

Falls wissenschaftliche Aussagen über den Stand der Forschung notwendig wären, die weder Repository noch bereitgestellte Quellen stützen:

* erfinde keine Quelle,
* markiere stattdessen `[QUELLE ERFORDERLICH]`.

Kapitel 4.1 soll jedoch primär die **eigenen Modellierungsziele und Designentscheidungen** begründen und deshalb keine unnötige Literaturdiskussion enthalten.

# 9. Abbildungen

Prüfe nach der Analyse des Repositories, ob eine Abbildung Kapitel 4.1 tatsächlich verständlicher macht.

Erstelle nur Abbildungen mit erkennbarem fachlichem Mehrwert.

Geeignete Kandidaten wären beispielsweise:

### Abbildung A – Grundidee des Annotationsmodells

Schematische Beziehung:

Gebäudemodell
→ IFC-Objekt
← RobotTask
← RobotMission

bzw. eine übersichtlichere, fachlich korrekte Variante auf Grundlage des tatsächlichen Modells.

### Abbildung B – Trennung der Ebenen

Beispielsweise:

Gebäudeobjekt / IFC
↕
fachliche Missionsannotation
↕
spätere roboterspezifische Verarbeitung

Wichtig:

* Keine Architekturkomponente darstellen, die im Repository nicht existiert.
* Implementiertes und konzeptionelles Verhalten visuell unterscheiden.
* Keine erfundenen Klassen oder Relationen hinzufügen.
* Bei technischen Diagrammen mit exakten Bezeichnern bevorzugt eine präzise Diagrammform wie Mermaid, SVG oder eine vergleichbar reproduzierbare Darstellung verwenden.
* Bildgenerierung nur verwenden, wenn eine illustrative Darstellung gegenüber einem technischen Diagramm einen tatsächlichen Mehrwert hat.
* Maximal zwei Abbildungen für Kapitel 4.1.
* Für jede Abbildung eine wissenschaftlich geeignete deutsche Bildunterschrift formulieren.
* Im Kapiteltext auf die Abbildung verweisen.
* Schlage eine konkrete Position im Text vor.
* Wenn keine Abbildung sinnvoll ist, erkläre kurz, warum.

# 10. Gewünschte Ausgabe

Arbeite in dieser Reihenfolge:

## A. Kurze Recherche- und Implementierungsnotiz

Noch **vor dem eigentlichen Kapitel**, maximal ca. 10–15 Stichpunkte:

* geprüfter Commit des Editor-Repositories,
* wichtigste für 4.1 untersuchte Dateien/Module,
* relevante tatsächlich implementierte Modellierungsentscheidungen,
* relevante Punkte, die bewusst nicht als implementiert dargestellt werden,
* gegebenenfalls Abweichungen zwischen Repository-Map und aktuellem Code.

Diese Notiz ist **nicht Bestandteil der Masterarbeit** und dient meiner manuellen Kontrolle.

## B. Kapitel 4.1

Erstelle anschließend den vollständigen Entwurf:

**4.1 Modellierungsziele**

Umfang als Richtwert:

**ca. 1.000–1.500 Wörter**

Der Text soll direkt als Grundlage für die Masterarbeit verwendbar sein.

Verwende Fließtext und nur dann Unterüberschriften, wenn sie die Lesbarkeit deutlich verbessern. Vermeide eine übermäßige Fragmentierung des relativ kurzen Unterkapitels.

## C. Nachweistabelle

Erstelle anschließend eine kompakte Tabelle:

| Aussage im Kapitel | Status | Implementierungsnachweis | ggf. externe Quelle |
| ------------------ | ------ | ------------------------ | ------------------- |

Status beispielsweise:

* implementiert,
* aus Implementierung abgeleitet,
* konzeptionell,
* Quelle erforderlich.

Diese Tabelle ist **nicht Bestandteil der Masterarbeit**.

## D. Abbildungen

Falls Abbildungen sinnvoll sind:

* erstelle sie,
* gib die vorgesehene Kapitelposition an,
* formuliere Bildunterschrift und gegebenenfalls Legendentext.

## E. Offene Review-Punkte

Nenne abschließend maximal fünf Punkte, die ich beim manuellen Review besonders prüfen sollte, beispielsweise:

* eine Designentscheidung, deren Begründung diskutierbar ist,
* eine Aussage, die zusätzliche Literatur benötigt,
* eine Grenze zwischen Implementierung und Konzept,
* eine Terminologieentscheidung.

# 11. Wichtigste Regel

Der Text darf **nicht beschreiben, wie der Editor idealerweise funktionieren sollte**, sondern muss von dem tatsächlich implementierten System und den daraus nachvollziehbaren Modellierungsentscheidungen ausgehen.

Wo Implementierung, Repository-Map, IFC-Standard oder konzeptionelle Zielsetzung auseinanderfallen, muss diese Trennung transparent bleiben.

Beginne jetzt mit dem Lesen der Repository-Map und untersuche danach gezielt das aktuelle Editor-Repository.

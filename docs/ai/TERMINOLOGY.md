# Terminologie

Die Tabelle ist ein kontrolliertes Ausgangsvokabular. Eine fachliche Definition belegt noch nicht, dass die bezeichnete Funktion implementiert ist.

| Bevorzugter deutscher Begriff | Zulässiges englisches oder technisches Äquivalent | Kurzdefinition | Zu vermeiden / Verwendungshinweis |
|---|---|---|---|
| annotierte IFC-Datei | annotated IFC file | IFC-Datei mit zusätzlich gespeicherten missionsbezogenen Informationen | Nicht mit einem beliebigen externen Sidecar gleichsetzen. |
| internes Domänenmodell | internal domain model | Anwendungsinterne Repräsentation fachlicher Entitäten und Beziehungen | „Datenmodell“ nur verwenden, wenn die allgemeinere Bedeutung gemeint ist. |
| Robotermission | robot mission | Zusammengehörige, auf ein Missionsziel ausgerichtete Folge oder Menge von Roboteraufgaben | Nicht ungeprüft mit einer einzelnen Aufgabe gleichsetzen. |
| Roboteraufgabe | robot task | Abgrenzbarer Arbeitsschritt innerhalb einer Robotermission | Der standardisierte Klassenname `IfcTask` bleibt unverändert. |
| Roboteraktion | robot action | Elementare ausführbare Aktion innerhalb einer Aufgabe | Nur verwenden, wenn diese Granularität im Modell nachgewiesen ist. |
| Zielobjekt | target object | Gebäudemodellobjekt, auf das eine Aufgabe primär ausgerichtet ist | Nicht pauschal als „betroffenes Objekt“ bezeichnen. |
| betroffenes Objekt | affected object | Objekt, das durch eine Aufgabe berührt oder verändert wird, ohne zwingend ihr Ziel zu sein | Beziehung zur Aufgabe explizit benennen. |
| Objektplatzierung | object placement | IFC-basierte räumliche Platzierung eines Objekts einschließlich Bezugssystem | Nicht auf bloße Weltkoordinaten reduzieren. |
| geometrischer Referenzpunkt | geometric reference point | Definierter Punkt, von dem räumliche Ableitungen ausgehen | Berechnungsmethode und Koordinatensystem nennen. |
| Navigationsziel | navigation goal | Zielzustand oder Zielposition für die Navigation | Von „Anfahrpose“ unterscheiden. |
| Anfahrpose | approach pose | Position und Orientierung, aus der eine Aufgabe ausgeführt werden soll | Nicht verwenden, wenn nur ein Punkt ohne Orientierung vorliegt. |
| Teilflächenreferenz | sub-surface reference | Referenz auf einen abgegrenzten Bereich einer Fläche | Abgrenzungsverfahren dokumentieren. |
| virtuelle Flächenunterteilung | Surface Tiling | Logische Zerlegung einer Fläche in Teilflächen ohne zwingende Änderung der IFC-Geometrie | Englischen Begriff beim ersten Auftreten einführen. |
| Surface Tiling | Surface Tiling | Etablierter technischer Begriff für virtuelle Flächenunterteilung | Im deutschen Fließtext nach Einführung konsistent verwenden. |
| IFC-Roundtrip | IFC round-trip | Import, interne Bearbeitung und erneuter Export mit definiertem Erhalt relevanter Semantik | „Vollständig“ nur bei belegtem Erhaltungsumfang. |
| kanonisches Persistenzformat | canonical persistence format | Maßgebliches dauerhaftes Datenformat, aus dem weitere Darstellungen abgeleitet werden | Nur nach entsprechender Architekturentscheidung verwenden. |
| abgeleiteter Roboterexport | derived robot export | Roboterbezogene Ausgabe, die aus dem kanonischen Bestand erzeugt wird | Nicht als eigenständige Wahrheitsquelle darstellen. |
| implementiert | implemented | Im referenzierten Code vorhanden und geprüft | Ohne Pfad und geeigneten Nachweis vermeiden. |
| prototypisch implementiert | prototypically implemented | Realisiert, jedoch mit dokumentierten Einschränkungen | Einschränkungen unmittelbar nennen. |
| vorgeschlagen | proposed | Als mögliche Lösung formuliert, aber nicht angenommen oder umgesetzt | Nicht mit „vorgesehen“ oder „implementiert“ vermischen. |
| evaluiert | evaluated | Mit dokumentierter Methode und nachvollziehbaren Kriterien untersucht | Nicht für eine bloße Demonstration verwenden. |
| zukünftige Erweiterung | future work / future extension | Noch nicht realisierte, ausdrücklich nachgelagerte Entwicklung | Im Ausblick oder als Zukunftsarbeit markieren. |

Standardisierte IFC-Entitäten wie `IfcTask`, `IfcRelSequence`, `IfcRelAssignsToProcess` und `IfcPropertySet` werden weder übersetzt noch frei umbenannt.

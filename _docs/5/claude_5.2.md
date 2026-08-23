# Kapitel 5.2 – Verwendete Technologien (Entwurf)

Erstellt für die manuelle Review. Teil B ist der eigentliche Kapiteltext; die Teile A, E, F und G gehören **nicht** in die Masterarbeit.

---

## A. Rechercheübersicht (nicht Bestandteil der Arbeit)

1. `Strukturübersicht.txt` gelesen: 5.1 = Gesamtarchitektur, 5.2 = Technologieauswahl, 5.3 = Modellimport/Rendering (Ladepipeline, Kamera, LOD, Ambient Occlusion, Kanten). 5.2 wurde entsprechend abgegrenzt.
2. `REPOSITORY_MAP_IFC_EDITOR_674ede3.md` als Orientierung genutzt; Technologiestack-Tabelle und deklarierte Versionen am Commit `674ede3` entnommen.
3. `repo_structure.txt` bestätigt die Projektstruktur (`package.json`, `tsconfig.json`, `vite.config.ts`, `src/`, `test/`) und damit TypeScript + Vite als Sprach- und Buildumgebung.
4. Im Projektkontext liegende Quelldateien wurden auf tatsächliche Importe geprüft (`three`, `@thatopen/components`, `@thatopen/components-front`, `@thatopen/fragments`, `@thatopen/ui`, `@thatopen/ui-obc`, `web-ifc`). Alle sieben geforderten Technologien sind real im Einsatz.
5. Live-Zugriff auf GitHub war nicht erforderlich; die Repository-Aussagen stützen sich auf die im Projektkontext vorliegenden Dateien.
6. `web-ifc` wird sowohl lesend (Missionsrekonstruktion) als auch schreibend/serialisierend (Export, Ersetzen, Verifikation) verwendet – belegt durch Importe von `IfcAPI`, `IFC4`/`IFC4X3` sowie `OpenModel`/`SaveModel`-Signaturen in der Export-Schicht.
7. Offizielle Quelle Fragments: binäres, kompaktes Format auf FlatBuffers-Basis, Geometrien/Properties/Beziehungen, Three.js-basierter Viewer, Highlighting, Raycast, Filtern.
8. Offizielle Quelle Components: BIM-Werkzeugsammlung auf Basis von Three.js; Three.js-Kenntnisse werden vorausgesetzt; Aufteilung in Core- und Front-Paket.
9. Offizielle Quelle Components (Tutorial `FragmentsManager`): Culling und LOD als Optimierungsmechanismen der Fragments-Darstellung; IFC-Parsing gilt als teuer und blockierend, weshalb eine workerbasierte Konvertierung erfolgt. Herstellerangabe, keine eigene Messung.
10. Offizielle Quelle That Open UI: Web Components, Framework-Unabhängigkeit (React/Angular/Vue/Svelte möglich), Trennung `@thatopen/ui` (generische Bedienelemente) und `@thatopen/ui-obc` (vorgefertigte, an Components gekoppelte Komponenten).
11. Offizielle Quelle `web-ifc`: JavaScript-Bibliothek zum Lesen **und** Schreiben von IFC; Fokus auf WebAssembly-Einsatz im Browser und in Node.js; zusätzlich als C++-Bibliothek nutzbar.
12. Status der Vorgängerbibliotheken geprüft: `web-ifc-viewer` und `web-ifc-three` wurden nach offizieller Aussage des Projekts durch Components abgelöst und werden nicht weiter gepflegt. Beleg ist eine Projektaussage im offiziellen Repository-Issue-Tracker (kein Blogartikel), aber keine formale Deprecation-Notiz – im Text daher vorsichtig formuliert.
13. Offizielle Quelle IfcOpenShell: C++- und Python-API, High-Level-API, Validierung bis hin zu Where-Rules (gleiche Basis wie die buildingSMART-Validierung), Unterstützung von IFC2X3/IFC4/IFC4.3 sowie Laufzeit-Ladbarkeit eigener Schemata, Lesen/Schreiben von IFC-SPF, IFCJSON, IFCXML, IFCHDF5, MySQL, SQLite; Ökosystem mit IfcConvert und Bonsai.
14. Wichtige Korrektur gegenüber älterer Literatur: IfcOpenShell nennt WebAssembly ausdrücklich als unterstützte Plattform und JavaScript-Nutzung via Pyodide. Die Aussage „IfcOpenShell läuft nicht im Browser“ wäre falsch und wird im Kapitel vermieden.
15. Abgeleitet (nicht dokumentiert): Sämtliche Begründungen der Technologieauswahl sind Rekonstruktionen aus den technischen Eigenschaften und der Architektur, nicht aus einer dokumentierten Entscheidungshistorie. Der Text formuliert sie deshalb durchgängig als Eignungsargumente.

---

## B. Kapitel 5.2 – Verwendete Technologien

### 5.2.1 Anforderungen als Ausgangspunkt der Technologieauswahl

Der Ausgangspunkt der Technologieauswahl ist kein abstraktes Softwareproblem, sondern ein konkreter Arbeitsablauf am Gebäudemodell. Eine Nutzerin öffnet im Browser das IFC-Modell eines Institutsgebäudes. Sie sieht Geschosse, Wände, Türen und Räume, dreht das Modell, blendet ein Geschoss frei und klickt im zweiten Obergeschoss auf eine bestimmte Tür. Diese Tür soll das Ziel einer Roboteraufgabe werden: Der Roboter fährt in den Flur davor und öffnet sie. Anschließend soll genau diese Zuordnung so in der IFC-Datei abgelegt werden, dass sie beim erneuten Öffnen derselben Datei wieder an derselben Tür erscheint.

Aus diesem Ablauf ergeben sich die Anforderungen, an denen sich der Technologiestack messen lassen muss: Ausführung im Browser ohne Installation, interaktive dreidimensionale Darstellung eines vollständigen Gebäudemodells, Umgang mit Modellen aus einer sehr großen Zahl einzelner Bauteile, Zugriff auf die Semantik des Modells – das angeklickte Objekt ist nicht bloß eine Fläche im Raum, sondern eine Tür mit dauerhaft gültiger Kennung –, eindeutige Auswahl eines einzelnen Bauteils sowie lesender **und** schreibender Zugriff auf IFC, weil die Missionsannotation in dieselbe Datei zurückgeführt wird. Hinzu kommt eine Anforderung, die keine Einzelfunktion betrifft: Die eingesetzten Bausteine müssen sich mit vertretbarem Aufwand miteinander verbinden lassen.

Die tragende Begründung der Auswahl liegt deshalb nicht darin, dass jede einzelne Bibliothek für sich genommen die leistungsfähigste verfügbare Lösung wäre, sondern darin, dass die eingesetzten Technologien einen weitgehend aufeinander abgestimmten Web- und BIM-Stack bilden, dessen Komponenten unterschiedliche Aufgaben übernehmen und dabei auf gemeinsamen technischen Grundlagen aufsetzen.

### 5.2.2 TypeScript und Vite als Sprach- und Entwicklungsumgebung

TypeScript ergänzt JavaScript um eine statische Typprüfung: Typen werden vor der Ausführung geprüft, und eine Reihe von Fehlern wird bereits während der Entwicklung sichtbar statt erst zur Laufzeit [Q1]. Der übersetzte Code ist gewöhnliches JavaScript und läuft überall dort, wo JavaScript läuft.

Für den Editor ist das aus fachlichen Gründen relevant. Zwischen der angeklickten Tür und der gespeicherten IFC-Datei liegen mehrere ineinandergreifende Datenstrukturen: die Beschreibung einer Mission, die einzelnen Aufgaben mit ihren Aktionen, die Referenzen auf Gebäudeobjekte, die Reihenfolge der Aufgaben sowie IFC-nahe Zwischenstrukturen. Diese werden an mehreren Stellen der Anwendung gelesen, verändert und wieder zusammengesetzt; explizit beschriebene Schnittstellen erleichtern es, ein solches Modell konsistent zu halten. JavaScript wäre grundsätzlich ausreichend gewesen; TypeScript bietet jedoch eine zusätzliche statische Absicherung, die bei einem umfangreicheren fachlichen Datenmodell hilfreich ist. Eine höhere Laufzeitgeschwindigkeit ergibt sich daraus nicht.

Vite bündelt Entwicklungsserver und Produktionsbuild. Der Entwicklungsserver liefert Quelldateien über native ES-Module aus und aktualisiert geänderte Module über Hot Module Replacement, ohne die Anwendung vollständig neu zu bündeln; für die Auslieferung erzeugt ein vorkonfigurierter Buildbefehl optimierte statische Ausgabedateien [Q2]. Für die Arbeit am Editor bedeutet das kurze Rückkopplungszeiten: Eine Änderung an der Missionsbearbeitung lässt sich unmittelbar am geladenen Gebäudemodell überprüfen. Etablierte Alternativen wie webpack oder Parcel sind nicht grundsätzlich unterlegen; webpack bietet insbesondere weitergehende Konfigurationsmöglichkeiten. Für den vorliegenden Funktionsumfang bietet Vite jedoch eine zweckmäßige Kombination aus geringem Konfigurationsaufwand und schnellen Entwicklungszyklen, ohne dass die zusätzliche Konfigurierbarkeit einen erkennbaren Mehrwert schaffen würde.

### 5.2.3 Three.js als gemeinsame 3D-Grundlage

Three.js ist eine allgemeine 3D-Bibliothek für das Web, die Szenen, Kameras, Geometrien, Materialien und Transformationen bereitstellt und die darunterliegende WebGL-Ebene abstrahiert [Q3]. Im Editor ist Three.js die Ebene, auf der das Gebäude überhaupt sichtbar wird: die Szene, in der die Geschosse stehen, die Kamera, mit der die Nutzerin um das Gebäude kreist, und die Materialien, mit denen eine ausgewählte Tür hervorgehoben wird.

Der entscheidende Grund für Three.js ist jedoch nicht die Bibliothek selbst, sondern ihre Rolle im übrigen Stack: Sowohl die eingesetzten BIM-Komponenten als auch die Fragments-Darstellung bauen auf Three.js auf [Q4][Q5]. Dadurch entsteht kein zusätzlicher, isolierter Grafikstack neben der BIM-Infrastruktur.

Als Alternativen wären direktes WebGL oder Babylon.js denkbar. Direktes WebGL böte maximale Kontrolle über das Rendering, würde aber erheblichen Eigenaufwand für Grafik- und Infrastrukturfunktionen erfordern, der mit der Fragestellung dieser Arbeit – der Verbindung von Gebäudemodell und Robotermission – wenig zu tun hat. Babylon.js ist eine technisch leistungsfähige 3D-Engine und keineswegs grundsätzlich schwächer als Three.js; da die verwendeten BIM-Bibliotheken jedoch auf Three.js aufsetzen, hätte es eine alternative 3D-Infrastruktur eingeführt und die unmittelbare Integration mit dem gewählten BIM-Stack erschwert.

### 5.2.4 That Open Components und Fragments: das Gebäude als darstellbares Modell

That Open Components ist eine Sammlung BIM-orientierter Werkzeuge oberhalb von Three.js, die vorgefertigte Bausteine für browserbasierte 3D-BIM-Anwendungen bereitstellt [Q4]. Konzeptionell übernimmt diese Schicht die Verwaltung geladener Modelle, die Einrichtung von Szene, Kamera und Renderer, Werkzeuge wie Raycasting, Hervorhebung und Schnittebenen sowie den Zugriff auf Modellinformationen. Der Unterschied zu reinem Three.js ist damit klar umrissen: Three.js weiß nichts von Gebäuden, sondern von Dreiecken; Components ergänzt die BIM-spezifische Ebene, sodass diese Infrastruktur nicht vollständig selbst entwickelt werden muss. Ältere Bibliotheken desselben Projekts wurden nach Angaben des Projekts durch die Components-Architektur abgelöst und werden nicht weiter gepflegt [Q6].

Fragments ist die für BIM-Daten optimierte Repräsentations- und Darstellungsschicht. Nach Angaben des Herstellers handelt es sich um ein offenes, binäres und kompaktes Format, das Geometrien, Eigenschaften und Beziehungen speichert; mitgeliefert wird ein auf Three.js aufbauender Viewer, der auf die Darstellung sehr großer Modelle sowie auf Hervorheben, Filtern, Raycasting und Eigenschaftszugriff ausgelegt ist [Q5]. Zur Optimierung der Darstellung werden Culling und Level-of-Detail-Verfahren eingesetzt; das Parsen von IFC wird als aufwendige, den Hauptthread blockierende Operation beschrieben, weshalb die Konvertierung workerbasiert erfolgt [Q7]. Diese Leistungsaussagen sind Herstellerangaben; eigene Messungen an den verwendeten Gebäudemodellen finden sich in Kapitel 6.

Für den Editor folgt daraus eine Architekturentscheidung, die wichtiger ist als die Beschreibung des Dateiformats: Die IFC-Datei und die dargestellte Geometrie werden bewusst getrennt behandelt.

```text
IFC-Modell des Gebäudes
│
├── fachliche IFC-Quelle
│     → Semantik der Bauteile
│     → Import vorhandener Missionen
│     → Export der Missionsannotation
│
└── Fragments-Repräsentation
      → 3D-Darstellung des Gebäudes
      → Auswahl einzelner Bauteile
      → Hervorhebung
      → performante Interaktion
```

Die Tür im zweiten Obergeschoss ist damit zweifach präsent: als anklickbares Objekt in der Fragments-Repräsentation und als semantisch identifizierbare Entität in der IFC-Quelle. Beide Sichten werden über die Objektidentität zusammengeführt.

Alternativ hätte die Darstellung direkt aus der IFC-Repräsentation erfolgen können, oder es hätten optimierte Formate wie glTF beziehungsweise XKT mit der Viewer-Technologie xeokit eingesetzt werden können. Solche Formate sind für große Modelle grundsätzlich geeignet; für Fragments spricht hier vor allem die enge Verzahnung mit That Open Components, Three.js und dem übrigen Stack.

### 5.2.5 `web-ifc` und IfcOpenShell: der Zugriff auf die IFC-Semantik

Während Fragments die Darstellung trägt, benötigt der Editor eine zweite Schicht für den fachlichen Zugriff auf die IFC-Datei selbst. `web-ifc` ist eine JavaScript-Bibliothek zum Lesen und Schreiben von IFC-Dateien, die primär als WebAssembly-Modul im Browser oder in Node.js eingesetzt wird [Q8]. Sie erlaubt es, ein IFC-Modell aus Byte-Daten zu öffnen, Entitäten und ihre Attribute auszulesen und ein verändertes Modell wieder zu serialisieren.

Dieser schreibende Zugriff ist kein Nebenaspekt, sondern ein zentrales Auswahlkriterium. Der Editor liest die Mission aus der Datei, lässt sie bearbeiten und führt sie in dieselbe Datei zurück:

```text
IFC-Datei des Gebäudes
        ↓
Mission einlesen
        ↓
Mission am Modell bearbeiten
        ↓
IFC-Datei schreiben
```

Die wichtigste Alternative hierzu ist IfcOpenShell, die älteste und ausgereifteste quelloffene IFC-Bibliothek, deren Funktionsumfang denjenigen von `web-ifc` deutlich übersteigt. Nach der offiziellen Dokumentation stehen eine C++- und eine Python-API sowie eine High-Level-API für IFC-Authoring zur Verfügung, mit der auch komplexe Vorgänge wie das Kopieren von Objekten, Kostenermittlungen oder 4D-Simulationen umgesetzt werden können [Q9]. Unterstützt werden IFC2X3, IFC4 und IFC4.3 sowie zur Laufzeit ladbare eigene Schemata; gelesen und geschrieben werden neben IFC-SPF unter anderem IFCJSON, IFCXML, IFCHDF5 und Datenbankformate. Die eingebaute Validierung reicht von der Syntaxprüfung bis zu Where-Rule-Prüfungen und bildet die Grundlage der offiziellen buildingSMART-Validierung. Hinzu kommt ein umfangreiches Ökosystem mit dem Konvertierungswerkzeug IfcConvert und der grafischen Authoring-Umgebung Bonsai; die Plattformunterstützung schließt WebAssembly und die Nutzung aus JavaScript heraus über Pyodide ausdrücklich ein [Q9].

Für eine Reihe von Aufgaben wäre IfcOpenShell daher die stärkere Wahl: für serverseitige IFC-Verarbeitung, umfangreiches Authoring, komplexe geometrische Operationen, detaillierte Modellvalidierung, automatisierte BIM-Pipelines und die Konvertierung zwischen Formaten.

Die Entscheidung zugunsten von `web-ifc` folgt deshalb nicht aus einem größeren Funktionsumfang, sondern aus der Gesamtarchitektur der Anwendung. `web-ifc` ist auf die Nutzung aus JavaScript beziehungsweise TypeScript heraus ausgelegt, fügt sich unmittelbar in die bestehende Laufzeitumgebung des Editors ein und gehört demselben Ökosystem an wie die eingesetzte Darstellungsinfrastruktur, sodass Darstellung und IFC-Verarbeitung technisch eng anschlussfähig bleiben. Für die benötigten Operationen – eine IFC-Datei öffnen, Entitäten und Relationen lesen, Property Sets auswerten, Missionsstrukturen erzeugen und verändern sowie das Modell wieder serialisieren – ist der Funktionsumfang ausreichend. Das bedeutet ausdrücklich nicht, dass IfcOpenShell zwingend einen Server erfordern würde; der Vorteil besteht darin, dass sich `web-ifc` ohne zusätzliche Systemgrenze und ohne parallele Verarbeitungsumgebung in die vorhandene Architektur einfügt. Für eine spätere ergänzende serverseitige Verarbeitungs- oder Validierungsschicht bliebe IfcOpenShell eine naheliegende Technologie.

### 5.2.6 That Open UI als Bedienschicht

Die Benutzeroberfläche des Editors basiert auf That Open UI, einer Sammlung von Web Components für BIM-Anwendungen. Bereitgestellt werden generische Bedienelemente wie Panels, Werkzeugleisten, Tabellen und Eingabefelder sowie ergänzend vorgefertigte Komponenten, die bereits an die Funktionalität von That Open Components angebunden sind; da es sich um Web Components handelt, sind sie grundsätzlich unabhängig von einem bestimmten Frontend-Framework einsetzbar [Q10]. Im Editor tragen diese Elemente die Seitenbereiche, in denen Modelle geladen, ausgewählte Bauteile angezeigt und Missionen mit ihren Aufgaben bearbeitet werden.

Alternativ wäre ein etabliertes Frontend-Framework wie React oder Vue mit zugehöriger UI-Bibliothek oder eine Eigenentwicklung aus HTML und CSS möglich gewesen; beides ist technisch tragfähig und keineswegs ungeeignet. Für die vorliegende Anwendung bietet That Open UI jedoch unmittelbare Anschlussfähigkeit an die BIM-Komponenten, bereits passend zugeschnittene Bedienelemente und eine geringere zusätzliche Framework-Komplexität.

### 5.2.7 Zusammenspiel und Einordnung

Die eingesetzten Technologien lassen sich vier Aufgabenbereichen zuordnen: TypeScript und Vite als Sprach-, Entwicklungs- und Auslieferungsbasis, Three.js mit That Open Components und Fragments als 3D- und BIM-Schicht, in der das Gebäude sichtbar und adressierbar wird, `web-ifc` als lesender und schreibender Zugriff auf die IFC-Datei sowie That Open UI als Bedienschicht. Entscheidend sind dabei zwei getrennte Datenpfade:

```text
Darstellung:   IFC → Fragments → 3D-Gebäudemodell im Browser
Fachdaten:     IFC ↔ web-ifc  ↔ Missionsmodell
```

Der erste Pfad führt vom Gebäudemodell zur sichtbaren und anklickbaren Tür, der zweite von derselben Tür zur dauerhaft in der Datei hinterlegten Aufgabe. Beide gehen von derselben IFC-Datei aus, verfolgen aber unterschiedliche Ziele.

**Tabelle 5.1:** Überblick über den eingesetzten Technologiestack (eigene Darstellung)

| Technologie | Aufgabe im Editor | wesentlicher Vorteil im vorliegenden Kontext | betrachtete Alternative |
|---|---|---|---|
| TypeScript | Anwendungs- und Domänenlogik | statische Typprüfung für ein umfangreicheres fachliches Datenmodell | JavaScript |
| Vite | Entwicklungs- und Buildumgebung | kurze Entwicklungszyklen bei geringem Konfigurationsaufwand | webpack, Parcel |
| Three.js | allgemeine 3D-Grundlage | etablierte Web-3D-Abstraktion und zugleich Basis des übrigen Stacks | direktes WebGL, Babylon.js |
| That Open Components | BIM-Werkzeuge und Modellverwaltung | BIM-spezifische Ebene oberhalb allgemeiner 3D-Funktionalität | Eigenentwicklung auf Three.js |
| That Open Fragments | Darstellung großer Gebäudemodelle | auf BIM-Daten ausgelegte Repräsentation, eng an Components gekoppelt | direkte IFC-Darstellung, glTF, XKT/xeokit |
| `web-ifc` | IFC lesen und schreiben | unmittelbare Integration in Browser-, TypeScript- und That-Open-Umgebung | IfcOpenShell |
| That Open UI | Benutzeroberfläche | BIM-orientierte Web Components mit direkter Anbindung an die BIM-Schicht | React, Vue, eigene UI-Komponenten |

Der wesentliche Nachteil dieser Auswahl liegt in der Bindung an ein einzelnes Ökosystem. Components, Fragments und die UI-Bibliothek sind eng aufeinander abgestimmt und teilen eine gemeinsame technische Grundlage; das senkt den Integrationsaufwand erheblich, erhöht aber den Aufwand, einen zentralen Baustein später auszutauschen – ein Wechsel der Darstellungsschicht würde absehbar auch die Auswahl- und Oberflächenschicht betreffen. Hinzu kommt die aktive Weiterentwicklung der Bibliotheken; die Ablösung der Vorgängerbibliotheken zeigt, dass mit Migrationsaufwand zu rechnen ist. Für die hier verfolgte Untersuchung der Verbindung von Gebäudemodell und Robotermission überwiegt der Vorteil der geringen Integrationskomplexität; für eine längerfristige Weiterentwicklung wäre diese Abhängigkeit bewusst zu berücksichtigen.

Damit ist begründet, warum dieser Stack gewählt wurde. Wie ein IFC-Gebäudemodell konkret geladen, in die Darstellungsstruktur überführt und im Browser gerendert wird, behandelt das folgende Kapitel.

---

## D. Optionale Abbildung

**Empfehlung:** Die Abbildung liefert gegenüber Tabelle 5.1 nur dann einen Mehrwert, wenn die Schichtung (UI oben, TypeScript/Vite als Basis, IFC-Pfad neben dem Darstellungspfad) betont werden soll. Da Abschnitt 5.2.7 die beiden Datenpfade bereits explizit macht, ist der Verzicht vertretbar. Falls sie verwendet wird, Platzierung am Ende von 5.2.7, direkt vor Tabelle 5.1:

```text
                     Browserbasierter Editor
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
   Bedienschicht        3D-/BIM-Schicht        IFC-Datenzugriff
   That Open UI       That Open Components         web-ifc
                              │                       │
                          Fragments            IFC lesen/schreiben
                              │
                           Three.js
        ─────────────────────────────────────────────
                    TypeScript · Vite (Basis)
```

**Bildunterschrift:** *Abbildung 5.x: Einordnung der eingesetzten Technologien in Bedienschicht, 3D-/BIM-Schicht und IFC-Datenzugriff über einer gemeinsamen Sprach- und Entwicklungsbasis (eigene Darstellung).*

---

## E. Quellenübersicht

| Kürzel | Aussage/Thema | Quelle | Quellentyp | Verwendungszweck |
|---|---|---|---|---|
| Q1 | TypeScript ist ein statischer Typprüfer für JavaScript; Typfehler werden vor der Ausführung erkannt, der Code wird zu JavaScript übersetzt | Microsoft: *The TypeScript Handbook – The Basics*, https://www.typescriptlang.org/docs/handbook/2/basic-types.html (Abruf: 22.08.2026) | offizielle Dokumentation | Begründung der Sprachwahl |
| Q2 | Vite besteht aus Entwicklungsserver über native ES-Module mit HMR und einem vorkonfigurierten Produktionsbuild | Vite: *Getting Started* / *Why Vite*, https://vite.dev/guide/ und https://vite.dev/guide/why (Abruf: 22.08.2026) | offizielle Dokumentation | Begründung der Buildumgebung |
| Q3 | Three.js ist eine allgemeine, browserübergreifende 3D-Bibliothek mit WebGL-/WebGPU-Renderern | three.js: *Documentation* / *Manual*, https://threejs.org/docs/ und https://threejs.org/manual/ (Abruf: 22.08.2026) | offizielle Dokumentation | Einordnung der 3D-Grundlage |
| Q4 | That Open Components ist eine BIM-Werkzeugsammlung auf Basis von Three.js; Aufteilung in Core- und Front-Paket | That Open Company: *Components – Introduction*, https://docs.thatopen.com/Tutorials/Components/ (Abruf: 22.08.2026) | offizielle Dokumentation | Einordnung der BIM-Schicht |
| Q5 | Fragments: offenes, binäres, kompaktes Format auf FlatBuffers-Basis für Geometrien, Properties und Beziehungen; Three.js-basierter Viewer für große Modelle mit Highlighting, Filtern, Raycasting | That Open Company: *Fragments – Introduction*, https://docs.thatopen.com/Tutorials/Fragments/ (Abruf: 22.08.2026) | offizielle Dokumentation (Herstellerangabe zur Leistungsfähigkeit) | Begründung der Darstellungsschicht |
| Q6 | `web-ifc-viewer` und `web-ifc-three` wurden durch Components abgelöst und werden nicht weiter gepflegt | ThatOpen: Projektaussage im offiziellen Repository, https://github.com/ThatOpen/web-ifc-viewer/issues/247 (Abruf: 22.08.2026) | offizielle Projektaussage (Issue-Tracker) | Einordnung der Vorgängerbibliotheken |
| Q7 | Fragments nutzt Culling und LOD; IFC-Parsing gilt als aufwendig und blockierend, daher workerbasierte Konvertierung | That Open Company: *FragmentsManager*-Tutorial, https://docs.thatopen.com/Tutorials/Components/Core/FragmentsManager (Abruf: 22.08.2026) | offizielle Dokumentation (Herstellerangabe) | Leistungsargument, ausdrücklich als Herstellerangabe |
| Q8 | `web-ifc` liest und schreibt IFC-Dateien, primär als WebAssembly-Modul in Browser und Node.js | ThatOpen: *engine_web-ifc*, https://github.com/ThatOpen/engine_web-ifc und https://thatopen.github.io/engine_web-ifc/docs/ (Abruf: 22.08.2026) | offizielles Repository und Dokumentation | Begründung der IFC-Verarbeitungsschicht |
| Q9 | IfcOpenShell: C++-/Python-API, High-Level-Authoring-API, Validierung bis Where-Rules als Basis der buildingSMART-Validierung, IFC2X3/IFC4/IFC4.3 und Laufzeit-Schemata, Formate IFC-SPF/IFCJSON/IFCXML/IFCHDF5/SQL, IfcConvert, Bonsai, Plattformen inkl. WebAssembly und Pyodide | IfcOpenShell: *Introduction*, https://docs.ifcopenshell.org/introduction.html (Abruf: 22.08.2026) | offizielle Dokumentation | fairer Vergleich der IFC-Alternative |
| Q10 | That Open UI: Web Components für BIM-Oberflächen, Trennung `@thatopen/ui` und `@thatopen/ui-obc`, Framework-Unabhängigkeit | That Open Company: *UserInterface – Introduction*, https://docs.thatopen.com/Tutorials/UserInterface/ (Abruf: 22.08.2026) | offizielle Dokumentation | Begründung der Bedienschicht |

Ergänzend für die Validierungsaussage in Q9 nutzbar: IfcOpenShell: *Validation*, https://docs.ifcopenshell.org/ifcopenshell-python/validation.html; für IfcConvert: https://docs.ifcopenshell.org/ifcconvert.html (jeweils Abruf 22.08.2026).

---

## F. Implementierungsnachweise (nicht Bestandteil des Kapiteltextes)

| Implementierungsaussage | Repository-Nachweis (Commit `674ede3`) |
|---|---|
| Projekt ist eine TypeScript-Anwendung mit Vite als Entwicklungs- und Buildumgebung | `package.json`, `tsconfig.json`, `tsconfig.test.json`, `vite.config.ts`; Skripte `npm run dev` (Vite-Server) und `npm run build` (TypeScript-Kompilierung + Vite-Build) |
| Deklarierte Versionen der Kernbibliotheken | `package.json`: `@thatopen/components ~3.2.0`, `@thatopen/components-front ~3.2.0`, `@thatopen/fragments ~3.2.0`, `@thatopen/ui ~3.2.0`, `@thatopen/ui-obc ~3.2.0`, `three ^0.175.0`, `web-ifc ^0.0.72`, `typescript 5.2.2`, `vite ^7.1.5` |
| Three.js wird direkt für Szene, Farben und Grid-Material verwendet | `src/main.ts` (`import * as THREE from "three"`), `src/viewer/robot-tasks/that-open-selection-highlight-port.ts`, `src/ui-templates/toolbars/viewer-toolbar.ts` |
| That Open Components/Components-Front bilden World, Kamera, Renderer, Grid, Postprocessing | `src/main.ts` (`OBC.Components`, `OBC.Worlds`, `OBC.SimpleScene`, `OBC.OrthoPerspectiveCamera`, `OBF.PostproductionRenderer`, `OBC.Grids`) |
| Fragments trägt Modellrepräsentation, Raycasting und Auswahl | `src/viewer/robot-tasks/that-open-selection-candidate-source.ts` (`FragmentsModel`, `RaycastResult`), `src/viewer/robot-tasks/selection-metadata.ts`, `src/ui-templates/toolbars/viewer-toolbar.ts` |
| That Open UI trägt Viewport, Panels, Toolbars und Missionsbereiche | `src/main.ts` (`BUI.Manager.init()`, `BUI.Viewport`), `src/ui-templates/**` (`grids/`, `groups/`, `sections/`, `toolbars/`, `buttons/`), zusätzlich `@thatopen/ui-obc` in `sections/models.ts`, `sections/elements-data.ts`, `sections/viewpoints.ts` |
| `web-ifc` wird lesend für den Missionsimport verwendet | `src/ifc/model-import/ifcMissionImportService.ts` (`IfcAPI`, `LocateFileHandlerFn`), `src/ifc/model-import/webIfcMissionReader.ts` (`GetLine`, `GetLineType`, `GetLineIDsWithType`) |
| `web-ifc` wird schreibend für Export, Ersetzung und Verifikation verwendet | `src/ifc/model-export/webIfcStructuralCodec.ts` (`OpenModel`, `SaveModel`), `src/ifc/model-export/webIfcMissionWriter.ts` (`IfcLineObject`), `src/ifc/model-export/webIfcMissionReplacer.ts` |
| Schemaabhängigkeit wird über eine eigene Adapterschicht auf `web-ifc`-Schemata abgebildet | `src/ifc/model-export/ifcSchemaAdapter.ts` (`IFC4`, `IFC4X3` aus `web-ifc`) |
| Domänenmodell ist frei von Three.js-, Fragments- und `web-ifc`-Abhängigkeiten | `src/domain/robot-tasks/` (`types.ts`, `builders.ts`, `sequencing.ts`, `validation.ts`) ohne Importe der genannten Bibliotheken |
| Konfiguration der `web-ifc`-Version zur Laufzeit | `src/main.ts` (WASM-Konfiguration `0.0.72`) |

---

## G. Review-Punkte (max. 5)

1. **Fairness gegenüber IfcOpenShell.** Abschnitt 5.2.5 stellt IfcOpenShell zuerst mit seinen Stärken dar und benennt ausdrücklich Aufgabenfelder, in denen es die stärkere Wahl wäre. Bitte prüfen, ob dir dieser Umfang im Verhältnis zum Gesamtkapitel angemessen erscheint – er ist bewusst länger als die übrigen Alternativenbetrachtungen.
2. **Argumentationsgrund für `web-ifc`.** Die Entscheidung ist durchgehend aus Browserintegration, gemeinsamer Laufzeitumgebung, Ökosystem-Anschluss und dem benötigten Schreibzugriff begründet, nicht aus einem größeren Funktionsumfang. Prüfe, ob an keiner Stelle doch eine pauschale Überlegenheitsaussage durchscheint.
3. **Herstellerangaben vs. eigene Aussagen.** Leistungsaussagen zu Fragments sind explizit als Herstellerangaben markiert und auf Kapitel 6 verwiesen. Prüfe, ob dir diese Kennzeichnung deutlich genug ist oder ob sie in der Endfassung noch expliziter erfolgen soll.
4. **Status der Vorgängerbibliotheken (Q6).** Der Beleg ist eine Projektaussage im offiziellen Issue-Tracker, keine formale Deprecation-Notiz in der Dokumentation. Falls dir das als Quelle zu schwach ist, kann der Halbsatz zu `web-ifc-viewer`/`web-ifc-three` ersatzlos entfallen, ohne dass die Argumentation leidet.
5. **Codeferne und Gebäudebezug.** Der Kapiteltext nennt keine Dateipfade, Klassen oder Methoden; Bezeichner erscheinen nur als Paketnamen. Der Gebäudebezug wird über das durchgehende Tür-/Institutsgebäude-Beispiel hergestellt. Prüfe, ob dieses Beispiel an den richtigen Stellen wiederaufgenommen wird und ob es sich mit dem in Kapitel 4 verwendeten Beispiel deckt.

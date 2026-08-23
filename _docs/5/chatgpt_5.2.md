# A. Rechercheübersicht

- Die Struktur der Arbeit grenzt Kapitel 5.2 als Begründung der Technologieauswahl von der Gesamtarchitektur in 5.1 und der konkreten Modellimport- und Rendering-Pipeline in 5.3 ab.
- Das Repository befindet sich auf `main` weiterhin bei Commit `674ede3`. 
- `package.json` weist TypeScript 5.2.2, Vite 7.1.x, Three.js 0.175.x, That Open Components 3.2.x, Fragments 3.2.x, That Open UI 3.2.x und `web-ifc` 0.0.72 aus. 
- TypeScript wird zusammen mit Vite im Buildprozess eingesetzt; der Produktions-Build führt zunächst die TypeScript-Prüfung und anschließend den Vite-Build aus. 
- Die TypeScript-Dokumentation beschreibt TypeScript als statischen Typprüfer, der bestimmte Fehler bereits vor der Ausführung erkennen kann.
- Vite stellt einen Entwicklungsserver mit HMR sowie einen vorkonfigurierten Produktions-Build bereit und baut seine Entwicklungsarchitektur auf moderner Modulverarbeitung auf.
- Three.js stellt die allgemeine 3D-Grundlage mit Szene, Kamera und Renderer bereit; der `WebGLRenderer` nutzt WebGL 2.
- That Open Components bezeichnet sich als modularen BIM-Werkzeugkasten auf Grundlage von Fragments und Three.js und ergänzt unter anderem Modellverwaltung, Clipping, Raycasting und weitere BIM-Werkzeuge.
- Das frühere `web-ifc-viewer` wird von That Open ausdrücklich als veraltet bezeichnet und verweist auf Components als Nachfolger.
- Fragments verwendet ein kompaktes, auf FlatBuffers basierendes Binärformat und unterstützt Geometrien, Properties und Relationen; die Laufzeit verteilt Verarbeitung zwischen Hauptthread und Worker.
- Fragments unterstützt unter anderem Raycasting sowie kameraabhängige Culling- und LOD-Verarbeitung.
- `web-ifc` stellt JavaScript-/TypeScript-nahe APIs zum Lesen und Schreiben von IFC bereit und nutzt hierfür eine in WebAssembly kompilierte C++-Implementierung.
- Im Repository wird `web-ifc` tatsächlich für das Öffnen, Serialisieren und erneute Prüfen von IFC-Dateien verwendet; Darstellung und Interaktion werden parallel durch That Open Components und Fragments realisiert.  
- IfcOpenShell bietet einen erheblich breiteren BIM-Funktionsumfang mit C++-/Python-API, High-Level-Authoring, Geometrieverarbeitung, Validierung, Konvertierung und zahlreichen Werkzeugen; WebAssembly-Nutzung ist ebenfalls möglich.
- Die Entscheidung zugunsten von `web-ifc` lässt sich daher nicht durch generelle funktionale Überlegenheit, sondern vor allem durch die geringere Integrationsdistanz zur bestehenden TypeScript-/That-Open-Browserarchitektur begründen.

# B. 5.2 Verwendete Technologien

Die technische Umsetzung des Editors stellt unterschiedliche Anforderungen an die eingesetzten Bibliotheken. Neben der Ausführung im Browser sind eine interaktive dreidimensionale Darstellung umfangreicher Gebäudemodelle, der Zugriff auf die semantischen Informationen einer IFC-Datei und die eindeutige Adressierung einzelner Gebäudeelemente erforderlich. Darüber hinaus dient IFC nicht ausschließlich als Eingabeformat für die Visualisierung. Die Missionsannotation muss aus einer vorhandenen Datei gelesen, im Editor bearbeitet und anschließend wieder in eine IFC-Datei geschrieben werden können. Der aktuelle Implementierungsstand kombiniert hierfür TypeScript und Vite mit Three.js, That Open Components, That Open Fragments, `web-ifc` und That Open UI. 

Die Auswahl ist weniger als Entscheidung für einzelne, jeweils isoliert optimale Bibliotheken zu verstehen. Wesentlicher ist ihr Zusammenspiel zu einem weitgehend aufeinander abgestimmten Web- und BIM-Technologiestack. Dabei übernehmen die Bibliotheken unterschiedliche Aufgaben: TypeScript und Vite bilden die Entwicklungsgrundlage, Three.js stellt grundlegende 3D-Funktionen bereit, Components und Fragments ergänzen BIM-spezifische Darstellungs- und Interaktionsfunktionen, `web-ifc` ermöglicht den strukturellen Zugriff auf die IFC-Daten und That Open UI stellt passende Elemente für die Benutzeroberfläche bereit.

## TypeScript und Vite

TypeScript erweitert JavaScript um ein statisches Typsystem. Der TypeScript-Compiler kann dadurch bestimmte Inkonsistenzen erkennen, bevor der betreffende Programmcode ausgeführt wird. Typen und Schnittstellen erlauben zudem die explizite Beschreibung der Struktur von Daten und ihrer erwarteten Verwendung.

Diese Eigenschaften sind insbesondere für das fachliche Datenmodell des Editors relevant. Neben Informationen aus dem IFC-Modell verarbeitet die Anwendung Missionsstrukturen, Aufgaben, Sequenzen und unterschiedliche Arten von Objektreferenzen. Die statische Typisierung unterstützt dabei die Trennung dieser Konzepte und reduziert die Wahrscheinlichkeit, dass strukturell inkompatible Daten zwischen verschiedenen Teilen der Anwendung ausgetauscht werden. JavaScript wäre grundsätzlich ebenfalls für eine browserbasierte Anwendung geeignet. TypeScript ergänzt dessen dynamisches Typsystem jedoch um zusätzliche Prüfungen während der Entwicklung. Daraus ergibt sich kein grundsätzlicher Laufzeitvorteil; der Nutzen liegt primär in der Entwicklungs- und Wartbarkeit komplexerer Datenstrukturen.

Vite ergänzt diese Sprachumgebung als Entwicklungs- und Buildwerkzeug. Die offizielle Dokumentation beschreibt Vite als Kombination aus Entwicklungsserver mit Hot Module Replacement und vorkonfiguriertem Produktions-Build. Die Entwicklungsarchitektur nutzt moderne Modulmechanismen und ist auf kurze Aktualisierungszyklen während der Entwicklung ausgerichtet. Im vorliegenden Repository sind sowohl der Entwicklungsserver als auch der Produktions-Build direkt über Vite konfiguriert.  Alternative Werkzeuge wie webpack oder Parcel wären ebenfalls einsetzbar. Für die Anwendung bietet Vite jedoch einen ausreichend vollständigen Entwicklungsworkflow bei vergleichsweise geringem zusätzlichem Konfigurationsbedarf.

## Three.js, That Open Components und Fragments

Die allgemeine 3D-Grundlage des Editors bildet Three.js. Die Bibliothek strukturiert eine 3D-Anwendung unter anderem anhand von Szene, Kamera und Renderer und abstrahiert damit wesentliche Aufgaben oberhalb der unmittelbaren WebGL-Schnittstelle. Der klassische `WebGLRenderer` verwendet dafür WebGL 2. Für die Anwendung sind außerdem Materialien, Transformationen und Kameraoperationen relevant.

Entscheidend für die Auswahl von Three.js ist jedoch nicht ausschließlich dessen allgemeiner Funktionsumfang. That Open Components ist selbst auf Three.js und Fragments aufgebaut. Die offizielle Projektbeschreibung bezeichnet Components als modularen BIM-Werkzeugkasten und nennt unter anderem Modellverwaltung, Szenen- und Kamerainfrastruktur, Clipping, Raycasting und Werkzeuge für den Zugriff auf BIM-Informationen. Three.js bildet damit keine unabhängig parallel betriebene Grafikschicht, sondern eine gemeinsame technische Grundlage des BIM-Stacks.

Eine direkte Implementierung auf Basis von WebGL hätte zwar eine weitergehende Kontrolle über das Rendering ermöglicht, gleichzeitig aber zusätzliche Entwicklung für grundlegende 3D-Funktionen erfordert. Auch eine eigenständige 3D-Engine wie Babylon.js wäre grundsätzlich geeignet. In Verbindung mit den gewählten That-Open-Komponenten würde sie jedoch eine zusätzliche beziehungsweise alternative 3D-Infrastruktur darstellen. Die enge technische Verbindung von Components und Three.js reduziert dagegen Schnittstellen zwischen der allgemeinen 3D-Darstellung und den BIM-spezifischen Funktionen.

That Open Components ergänzt Three.js um genau solche BIM-orientierten Funktionen. Dadurch müssen grundlegende Mechanismen zur Modellverwaltung, Interaktion, Auswahl, Hervorhebung oder zum Clipping nicht vollständig innerhalb der Anwendung entwickelt werden. Für die Wahl der aktuellen Components-Architektur spricht zusätzlich, dass That Open das frühere `web-ifc-viewer` inzwischen ausdrücklich als veraltet kennzeichnet und auf Components als Nachfolgearchitektur verweist.

Für die Verarbeitung umfangreicher BIM-Modelle kommt zusätzlich That Open Fragments zum Einsatz. Fragments definiert ein kompaktes Binärformat auf Grundlage von FlatBuffers, das neben Geometrien auch Properties und Relationen abbilden kann. Die zugehörige Laufzeit trennt Aufgaben zwischen Hauptthread und Web Worker; modellbezogene Verarbeitung wie Abfragen und Raycasting kann dabei im Worker stattfinden. Darüber hinaus sind Culling und Level-of-Detail-Verfahren Bestandteil der Fragments-Infrastruktur. Diese Eigenschaften machen Fragments nach Angaben des Herstellers insbesondere für große BIM-Datenmengen geeignet. Eigene quantitative Aussagen zur Leistungsfähigkeit werden daraus nicht abgeleitet; diese wären gesondert zu evaluieren.

Für den Editor ist vor allem die damit ermöglichte funktionale Trennung relevant. Die Fragments-Repräsentation dient der dreidimensionalen Gebäudedarstellung und der interaktiven Auswahl von Elementen. Die ursprünglichen IFC-Daten bleiben dagegen für die fachliche Interpretation sowie für Import und Export der Missionsannotation erhalten. Diese Trennung ist auch im aktuellen Repository erkennbar: Components und Fragments werden für die Viewer-Infrastruktur verwendet, während IFC-Quelldaten separat für die strukturelle Verarbeitung vorgehalten werden.  Optimierte Formate wie glTF oder XKT beziehungsweise andere BIM-Viewer-Technologien wären ebenfalls denkbar. Für Fragments spricht hier insbesondere die unmittelbare Integration in Components und damit in den bereits verwendeten Three.js-basierten Stack.

## `web-ifc` und IfcOpenShell

Während Fragments primär der interaktiven Repräsentation dient, übernimmt `web-ifc` den strukturellen Zugriff auf die IFC-Dateien. Das Projekt stellt eine JavaScript-Schnittstelle zum Lesen und Schreiben von IFC bereit. Die zugrunde liegende C++-Implementierung wird über Emscripten nach WebAssembly übersetzt und steht sowohl für Browser- als auch für Node.js-Umgebungen zur Verfügung.

Diese Eigenschaft ist für den Editor wesentlich, da der Umgang mit IFC nicht mit dem Laden der Gebäudedarstellung endet. Die Missionsinformationen werden aus IFC rekonstruiert und nach einer Bearbeitung wieder in das Modell geschrieben. Im Repository wird `web-ifc` entsprechend sowohl zum Öffnen als auch zum erneuten Serialisieren von IFC-Daten verwendet. Der implementierte strukturelle Verarbeitungsweg öffnet IFC-Bytes, greift auf Entitäten zu, speichert ein verändertes Modell und kann das Ergebnis anschließend erneut öffnen.  Damit erfüllt die Bibliothek die für den bidirektionalen Missionsaustausch benötigten grundlegenden Lese- und Schreiboperationen.

Als wichtigste Alternative ist IfcOpenShell zu betrachten. Dessen Funktionsumfang reicht deutlich über die für diese Anwendung unmittelbar benötigten Operationen hinaus. IfcOpenShell stellt einen C++-Kern und Python-Bindings sowie eine High-Level-API für IFC-Authoring und -Bearbeitung bereit. Darüber hinaus gehören umfangreiche Geometrieverarbeitung, Schemaunterstützung für IFC2X3, IFC4 und IFC4.3, Validierungsfunktionen sowie verschiedene Werkzeuge zur Konvertierung und Analyse zum Ökosystem. Der Geometrie-Iterator unterstützt beispielsweise Mehrkernverarbeitung und Wiederverwendung geometrischer Ergebnisse. Mit IfcConvert steht außerdem ein eigenständiges Werkzeug zur Umwandlung von IFC-Geometrie in zahlreiche weitere Formate zur Verfügung; Bonsai ergänzt das Ökosystem um eine grafische IFC-Authoring-Umgebung auf Basis von Blender.

IfcOpenShell kann daher insbesondere für umfangreiche serverseitige IFC-Verarbeitung, komplexes Authoring, geometrische Operationen, Validierungsaufgaben oder automatisierte BIM-Pipelines die funktional umfassendere Wahl darstellen. Auch eine Nutzung im Browser ist grundsätzlich möglich. Die offizielle Dokumentation nennt WebAssembly-Pakete für Pyodide sowie eine WebAssembly-basierte Technologievoransicht. Letztere wird allerdings als umfangreich hinsichtlich Ladevolumen und Ladezeit beschrieben. Eine grundsätzliche Beschränkung von IfcOpenShell auf serverseitige Anwendungen besteht somit nicht.

Für das vorliegende Gesamtsystem spricht dennoch mehr für `web-ifc`. Die Bibliothek ist unmittelbar auf JavaScript sowie WebAssembly ausgerichtet und fügt sich dadurch direkt in die TypeScript-basierte Browseranwendung ein. Gleichzeitig gehört sie zum selben That-Open-Ökosystem wie Components und Fragments. Die Anwendung benötigt dadurch für die vorgesehenen IFC-Lese- und Schreiboperationen keine zusätzliche Python-Laufzeit oder eigenständige Verarbeitungsgrenze. Dies bedeutet nicht, dass IfcOpenShell zwingend einen Server erfordern würde, sondern dass `web-ifc` innerhalb der vorhandenen Architektur eine geringere Integrationsdistanz besitzt.

Der Vergleich zeigt damit unterschiedliche Stärken: IfcOpenShell bietet den breiteren Werkzeugkasten für umfassendes IFC-Authoring, Geometrieverarbeitung, Validierung und Konvertierung. `web-ifc` deckt dagegen den benötigten IFC-Lese-/Schreibworkflow ab und lässt sich unmittelbar mit der bestehenden Browser-, TypeScript- und That-Open-Infrastruktur verbinden. Für eine spätere ergänzende serverseitige Verarbeitungs- oder Validierungsschicht bliebe IfcOpenShell daher weiterhin eine relevante Technologie.

## That Open UI und Gesamtbewertung

That Open UI bildet die Benutzeroberflächenschicht des Stacks. Die Kernbibliothek stellt Web Components wie Buttons, Panels, Toolbars, Tabellen und Eingabeelemente bereit. Ergänzend enthält `@thatopen/ui-obc` bereits auf That Open Components abgestimmte funktionale UI-Komponenten. Da Web Components auf Browserstandards basieren, sind diese Bedienelemente nicht an ein bestimmtes Frontend-Framework gebunden. Im Editor wird die UI-Bibliothek gemeinsam mit Components und Three.js initialisiert und für die Viewer-Oberfläche eingesetzt. 

Ein eigenständiges Framework wie React oder Vue sowie vollständig selbst entwickelte HTML-/CSS-Komponenten wären ebenfalls möglich gewesen. Für die vorhandene Anwendung reduziert die That-Open-Lösung jedoch die Zahl zusätzlicher Frameworkgrenzen und stellt bereits Bedienelemente bereit, die auf die verwendete BIM-Infrastruktur abgestimmt sind.

Die Gesamtarchitektur lässt sich damit in zwei zentrale Datenpfade gliedern. Für die Darstellung werden IFC-Daten in eine Fragments-Repräsentation überführt und dort für die interaktive 3D-Darstellung genutzt. Für die fachliche Verarbeitung verbleibt IFC dagegen als strukturierte Quelle, die über `web-ifc` gelesen und geschrieben werden kann. Die Technologien ergänzen sich somit entlang ihrer jeweiligen Aufgaben, anstatt dieselben Funktionen mehrfach bereitzustellen.

| Technologie | Aufgabe im Editor | Wesentlicher Vorteil im Gesamtsystem | Betrachtete Alternative |
|---|---|---|---|
| TypeScript | Anwendungs- und Domänenlogik | statische Typprüfung strukturierter Daten | JavaScript |
| Vite | Entwicklung und Build | integrierter Entwicklungsserver und Produktions-Build | webpack, Parcel |
| Three.js | allgemeine 3D-Grundlage | zugleich technische Grundlage des That-Open-Stacks | direktes WebGL, Babylon.js |
| That Open Components | BIM-spezifische Anwendungsfunktionen | vorgefertigte BIM-Werkzeuge auf Three.js und Fragments | Eigenentwicklung |
| Fragments | 3D-Repräsentation von BIM-Daten | kompakte, workerbasierte und interaktive BIM-Infrastruktur | direkte IFC-Darstellung, glTF, XKT |
| `web-ifc` | IFC lesen und schreiben | direkte Integration in Browser, JavaScript und That Open | IfcOpenShell |
| That Open UI | Benutzeroberfläche | BIM-nahe, frameworkunabhängige Web Components | React, Vue, eigene Komponenten |

Eine verbleibende Einschränkung der gewählten Architektur ist ihre deutliche Bindung an das That-Open-Ökosystem. Components, Fragments, `web-ifc` und die UI-Bibliotheken sind technisch eng aufeinander abgestimmt. Dies reduziert den gegenwärtigen Integrationsaufwand, kann den späteren Austausch einzelner zentraler Komponenten jedoch aufwendiger machen. Die Technologieentscheidung ist daher vor allem als Abwägung zugunsten eines kohärenten und unmittelbar browserintegrierten BIM-Stacks zu verstehen und nicht als Aussage über eine generelle Überlegenheit der einzelnen Bibliotheken.

Auf dieser Grundlage kann das folgende Kapitel die konkrete Verarbeitung eines IFC-Gebäudemodells betrachten und erläutern, wie aus der IFC-Quelldatei die für die interaktive Darstellung verwendete Modellrepräsentation entsteht.

# C. Vergleichstabelle

Die Vergleichstabelle wurde bewusst **in Kapitel 5.2 integriert**, damit die Einzelentscheidungen unmittelbar auf die Gesamtarchitektur zurückgeführt werden können. Eine zweite Tabelle im Fließtext würde keinen zusätzlichen Informationsgewinn bieten.

# D. Optionale Abbildung

Für die aktuelle Fassung würde ich **keine zusätzliche Abbildung** aufnehmen. Die Tabelle und die im Text herausgearbeitete Trennung zwischen

**Darstellung:** `IFC → Fragments → 3D-Gebäudemodell`

und

**Fachdaten:** `IFC ↔ web-ifc ↔ Missionsmodell`

vermitteln die entscheidende Architekturbeziehung bereits ausreichend. Eine zusätzliche Stack-Grafik würde Kapitel 5.1 teilweise wiederholen.

# E. Quellenübersicht

| Aussage/Thema | Quelle | Quellentyp | Verwendungszweck |
|---|---|---|---|
| statische Typprüfung | Microsoft, *TypeScript Handbook – The Basics* | offizielle Dokumentation | Eigenschaften von TypeScript |
| Entwicklungsserver, HMR und Build | Vite, *Getting Started* / *Why Vite* | offizielle Dokumentation | Begründung Vite |
| Szene, Kamera und Renderer | Three.js, *Creating a scene* | offizielle Dokumentation | grundlegende 3D-Struktur |
| WebGL-Rendering | Three.js, *WebGLRenderer* | offizielle API-Dokumentation | Renderingbasis |
| Components auf Three.js/Fragments | That Open, *engine_components* | offizielles Repository | BIM-Abstraktionsschicht |
| Status `web-ifc-viewer` | That Open, *web-ifc-viewer* | offizielles Repository | Einordnung der Vorgängerbibliothek |
| Fragments-Format und Fähigkeiten | That Open, *engine_fragment* | offizielles Repository | Binärformat, BIM-Daten, Interaktion |
| Workerarchitektur von Fragments | That Open, *Fragments CONTRIBUTING* | offizielles Repository | workerbasierte Verarbeitung |
| Culling und LOD | That Open, Fragments-Beispiele | offizielle Beispiele | performante Darstellungsinfrastruktur |
| IFC lesen/schreiben und WASM | That Open, *engine_web-ifc* | offizielles Repository | Eigenschaften von `web-ifc` |
| UI und Web Components | That Open, *engine_ui-components* | offizielles Repository | That Open UI |
| IfcOpenShell Überblick | IfcOpenShell, *Introduction* | offizielle Dokumentation | Funktionsumfang und Ökosystem |
| High-Level-Authoring | IfcOpenShell, `ifcopenshell.api` | offizielle API-Dokumentation | Authoring-Funktionen |
| Geometrieverarbeitung | IfcOpenShell, *Geometry processing* | offizielle Dokumentation | Geometrie und Mehrkernverarbeitung |
| IFC-Schemata | IfcOpenShell, `create_file` | offizielle API-Dokumentation | IFC2X3, IFC4 und IFC4X3 |
| Validierung | IfcOpenShell, *Introduction* / `validate` | offizielle Dokumentation | Validierungsmöglichkeiten |
| WebAssembly | IfcOpenShell, *Installation* | offizielle Dokumentation | browserbezogene Nutzung |
| IfcConvert | IfcOpenShell, *IfcConvert* | offizielle Dokumentation | Konvertierungsmöglichkeiten |
| Bonsai | IfcOpenShell, *Introduction* / *Bonsai* | offizielle Dokumentation | BIM-Ökosystem |

Abruf der Webquellen: **22. August 2026**.

# F. Implementierungsnachweise

Diese Tabelle ist **nicht für die Übernahme in die Masterarbeit** vorgesehen.

| Implementierungsaussage | Repository-Nachweis |
|---|---|
| Verwendeter Technologie-Stack und Versionsbereiche | `package.json`: TypeScript, Vite, Three.js, `@thatopen/components`, `@thatopen/components-front`, `@thatopen/fragments`, `@thatopen/ui`, `@thatopen/ui-obc`, `web-ifc`.  |
| aktueller untersuchter Stand | Repository-Tree verweist für `main` auf Commit `674ede3bf2e7e6cf466bc4c16fe06c90fbb1753c`.  |
| Three.js, Components und UI werden gemeinsam eingesetzt | `src/main.ts` importiert Three.js, Components, Components Front und That Open UI und initialisiert die gemeinsame Viewer-Infrastruktur.  |
| Fragments übernimmt die Viewer-Modellinfrastruktur | `src/main.ts` initialisiert den `FragmentsManager`, dessen Worker und die kameraabhängige Modellverarbeitung.  |
| `web-ifc` ist in den IFC-Lese-/Schreibpfad integriert | `webIfcStructuralCodec.ts` verwendet `IfcAPI`, `OpenModel` und `SaveModel`.  |
| IFC-Quelle und Fragments-Modell werden für den Roundtrip getrennt behandelt | `src/main.ts` hält IFC-Quelldaten gesondert vor und kennzeichnet beliebige `.frag`-Modelle als nicht für diesen strukturellen Export geeignet.  |
| IFC wird nach der Serialisierung erneut geprüft | `webIfcStructuralCodec.ts` definiert einen erneuten Parse- und Validierungsschritt auf Basis einer separaten `web-ifc`-Instanz.  |

# G. Review-Punkte

1. **Gewichtung von IfcOpenShell:** Prüfen, ob die positive Darstellung ausreichend deutlich macht, dass IfcOpenShell bei umfassendem IFC-Authoring, Geometrieverarbeitung und Validierung funktional stärker sein kann, ohne den Fokus des Kapitels von der tatsächlichen Anwendung wegzulenken.
2. **Begründung von `web-ifc`:** Prüfen, ob eindeutig bleibt, dass die Entscheidung auf Browser-, TypeScript- und That-Open-Integration basiert und nicht auf einer behaupteten generellen Überlegenheit gegenüber IfcOpenShell.
3. **Abgrenzung zu Kapitel 5.3:** Prüfen, ob Aussagen zu Worker, LOD und Modellimport noch auf Entscheidungsebene bleiben und nicht zu viele Implementierungsdetails des folgenden Kapitels vorwegnehmen.
4. **Quellcodedetails:** Im eigentlichen Kapitel sind konkrete Dateinamen und Klassen nahezu vollständig vermieden; sie erscheinen nur in der separaten Implementierungsnachweistabelle.
5. **Herstellerangaben:** Insbesondere Aussagen zur Verarbeitung großer BIM-Modelle durch Fragments sollten weiterhin als Herstellerbeschreibung verstanden werden. Eigene Leistungsbehauptungen sollten erst auf Basis der Evaluation formuliert werden.
# Arbeitsnotiz: untersuchte Repository-Dateien

Orientierung: `REPOSITORY_MAP_IFC_EDITOR_674ede3.md`, `Strukturübersicht.txt`, `repo_structure.txt`.

Am Quellcode geprüft:

- `src/domain/robot-tasks/types.ts` (Definition von `RobotObjectReference`, Verwendung in `RobotTask`)
- `src/domain/robot-tasks/builders.ts` (`referenceKey`, `addUniqueReference`, Zuweisungsfunktionen)
- `src/domain/robot-tasks/validation.ts` (Prüfregeln für Referenzen)
- `src/viewer/robot-tasks/selection-adapter.ts` (Umwandlung Viewer-Auswahl → Domänenreferenz)
- `src/viewer/robot-tasks/selection-metadata.ts` (Auflösung von `GlobalId`, IFC-Klasse, Name)
- `src/viewer/robot-tasks/selection-types.ts` (Trennung von `localId` und Domänenreferenz)
- `src/viewer/robot-tasks/model-provenance.ts` (Bestätigung von `expressId` nach Modellherkunft)
- `src/ifc/model-import/webIfcMissionReader.ts` (Rekonstruktion der Referenz beim Import)
- `src/ifc/model-roundtrip/ifcMissionRoundtripCoordinator.ts` (Prüfung modellfremder Referenzen)
- `src/ifc/model-export/webIfcMissionWriter.ts` (Auflösung der Referenz gegen die Quell-IFC)
- `src/ifc/robot-tasks/mapper.ts` (Übernahme der Referenz in die IFC-Abbildung)

---

# 4.4 Referenzierung von IFC-Objekten

Ein `RobotTask` beschreibt eine Handlung, die sich auf ein konkretes Bauteil des Gebäudemodells bezieht – etwa eine Tür, die geöffnet, oder einen Raum, der durchquert werden soll. Damit diese Zuordnung über eine einzelne Viewer-Sitzung, über einen Speichervorgang und über einen vollständigen IFC-Roundtrip hinweg gültig bleibt, muss das Domänenmodell die Identität des referenzierten Objekts unabhängig von seiner momentanen Darstellung repräsentieren. Die zentrale Entwurfsentscheidung dieses Abschnitts lautet deshalb: Die fachliche Referenz eines IFC-Objekts wird konsequent von der temporären Darstellung im Viewer getrennt.

## 4.4.1 `RobotObjectReference` als Trägerstruktur

Das Domänenmodell kapselt die Objektidentität im eigenständigen Typ `RobotObjectReference`. Ein `RobotTask` verweist ausschließlich über diesen Typ auf Gebäudeelemente, und zwar in den Feldern `targetObjects`, `affectedObjects`, `startReference` und `targetReference`. Der Typ ist als Vereinigung zweier Varianten definiert: Die erste Variante trägt eine `globalId` und optional eine `expressId`; die zweite Variante besitzt keine `globalId`, verlangt dafür aber zwingend `modelId` und `expressId`. Diese Modellierung erzwingt bereits auf Typebene, dass jede Referenz mindestens eine auswertbare Identität besitzt.

Der grundlegende Zusammenhang lässt sich damit wie folgt zusammenfassen:

```text
IFC-Objekt
    ↓
GlobalId
    ↓
RobotObjectReference
    ↓
RobotTask
```

## 4.4.2 `GlobalId` als bevorzugte dauerhafte Identität

Die IFC-`GlobalId` ist die bevorzugte dauerhafte Objektidentität. Ihre Eignung ergibt sich aus dem IFC-Schema selbst: Jede von `IfcRoot` abgeleitete Entität – und damit jedes eigenständig referenzierbare Bauteil – besitzt das Attribut `GlobalId` vom Typ `IfcGloballyUniqueId`, das als global eindeutige Kennung über Softwaregrenzen hinweg vorgesehen und im Schema durch eine Eindeutigkeitsregel abgesichert ist [buildingSMART, IFC 4.3, `IfcRoot`].

Die Implementierung setzt diesen Vorrang an mehreren Stellen konsistent um. Der Domänenschlüssel für Vergleich und Duplikaterkennung wird in `builders.ts` als `global:<globalId>` gebildet, sofern eine `GlobalId` vorliegt. Beim Export löst der Writer eine Referenz primär über die `GlobalId` gegen die Quelldatei auf und verwendet dafür die IFC-eigene GUID-Zuordnung. Entscheidend ist, dass diese Auflösung keinerlei Bezug zur dargestellten Three.js- beziehungsweise Fragments-Geometrie besitzt.

## 4.4.3 `modelId` und `expressId` als modelllokaler Fallback

Die `expressId` ist demgegenüber eine Entity-Nummer innerhalb einer konkreten IFC-Repräsentation. Sie ist an die jeweilige Serialisierung gebunden; die Arbeit trifft daher bewusst keine Aussage darüber, dass eine `expressId` über unterschiedliche Serialisierungen desselben Modells hinweg erhalten bliebe. Als alleinige dauerhafte Referenz ist sie deshalb ungeeignet.

Verwendet wird sie ausschließlich in Verbindung mit `modelId`, also mit der Kennung des geladenen Quellmodells, das die Nummer überhaupt erst interpretierbar macht. Die Validierung erzwingt diese Kopplung explizit: Eine Referenz ohne `globalId` wird zurückgewiesen, wenn keine nichtleere `modelId` vorhanden ist. Der Vergleichsschlüssel lautet in diesem Fall `express:<modelId>:<expressId>`. Damit ergibt sich die folgende Abstufung:

```text
bevorzugt:
GlobalId

Fallback:
modelId + expressId
```

Bemerkenswert ist zudem, dass die `expressId` im Viewer nicht angenommen, sondern bestätigt werden muss. Eine eigene Registratur der Modellherkunft gibt eine `expressId` nur für solche Modelle zurück, die über den direkten IFC-Importpfad geladen wurden; für beliebige Fragments-Dateien liefert sie bewusst kein Ergebnis.

## 4.4.4 Identität und beschreibende Metadaten

Neben den identifizierenden Feldern kann eine `RobotObjectReference` beschreibende Metadaten aufnehmen, insbesondere die IFC-Klasse (`ifcClass`), den Objektnamen (`name`) sowie – im Fall der `GlobalId`-Variante – ergänzend `modelId` und `expressId` für den effizienten modelllokalen Zugriff. Diese Angaben dienen der Anzeige im Editor und der Plausibilitätsprüfung von Aktionen, etwa ob eine `OPEN`-Aktion auf eine plausible Objektklasse zielt. Sie sind jedoch ausdrücklich keine Identität: Weder Name noch IFC-Klasse gehen in die Schlüsselbildung ein, da beide weder eindeutig noch änderungsstabil sind.

## 4.4.5 Abgrenzung zu Rendering- und Viewer-Identifikatoren

Die Darstellung arbeitet mit laufzeitlokalen Strukturen: Fragments- und Mesh-Identifikatoren, Raycast-Treffer mit Trefferpunkt und Distanz sowie viewer-interne Elementnummern. Diese Werte beschreiben den Zustand einer Renderpipeline, nicht ein Bauteil des Bauwerks. Sie sind an Ladevorgang, Detailstufe und Sichtbarkeitszustand gebunden und eignen sich daher grundsätzlich nicht als fachliche Referenz.

Die Implementierung zieht diese Grenze scharf. Ein Auswahlkandidat führt seine viewer-lokale Kennung ausdrücklich nur für Laufzeitoperationen und hält die dauerhafte Domänenreferenz in einem separaten Feld. Der Auswahladapter überführt eine bestätigte Auswahl in eine `RobotObjectReference`, wobei die viewer-lokale Kennung nie als `expressId` umgedeutet wird; lässt sich weder eine `GlobalId` noch eine bestätigte `expressId` ermitteln, bricht die Umwandlung mit einem eigenen Fehler ab, statt eine unsichere Referenz zu erzeugen. Die Objektauswahl darf Rendering-Strukturen also nutzen, muss ihr Ergebnis aber vor der Übergabe an die Domäne in eine fachliche Referenz übersetzen. Der Auswahlvorgang selbst wird in Kapitel 5 behandelt.

## 4.4.6 Bedeutung für den IFC-Roundtrip

Da Missionen aus annotierten IFC-Dateien rekonstruiert und erneut exportiert werden können, müssen Referenzen wieder einem Gebäudemodell zugeordnet werden. Diese Quellabgrenzung leistet `modelId`. Beim Import wird jeder rekonstruierten Referenz die Kennung des Quellmodells zugewiesen; vor dem Export lehnt der Koordinator Missionen ab, deren Referenzen auf ein anderes geladenes Modell als das Exportziel verweisen. Der Writer akzeptiert eine reine `expressId` folgerichtig nur dann, wenn `modelId` mit dem Quellmodell übereinstimmt, und meldet einen Fehler, wenn eine `GlobalId` auf eine abweichende Entität oder auf keine Entität der Quelldatei auflöst.

Aus dem implementierten RobotMission-Roundtrip folgt jedoch nicht, dass beliebige Änderungen eines Gebäudemodells automatisch aufgelöst werden könnten. Wird ein referenziertes Bauteil in einer späteren Modellrevision entfernt oder mit neuer `GlobalId` neu erzeugt, ist eine automatische Wiederzuordnung nicht grundsätzlich gewährleistet; die Referenz bleibt dann unauflösbar und wird als Fehler sichtbar. Eine Rebind-Strategie für Modellrevisionen bleibt eine offene Erweiterung (Kapitel 8).

---

```text
Viewer-Auswahl
     ↓
IFC-Metadaten auflösen
     ↓
RobotObjectReference
     ├── GlobalId        ← bevorzugt
     └── modelId +
         expressId       ← Fallback
     ↓
RobotTask
```

*Abbildung 4.x: Überführung einer bestätigten Viewer-Auswahl in eine dauerhafte fachliche Objektreferenz. Laufzeitlokale Darstellungsinformationen enden an der Auflösungsstufe und werden nicht Teil der Referenz.*

---

## Nachweistabelle

| Aussage | Status | Implementierungsnachweis |
| ------- | ------ | ------------------------ |
| `RobotObjectReference` ist der einzige Referenztyp eines `RobotTask` auf IFC-Objekte | implementiert | `src/domain/robot-tasks/types.ts` (`targetObjects`, `affectedObjects`, `startReference`, `targetReference`) |
| `GlobalId` ist die bevorzugte dauerhafte Identität | implementiert | `src/domain/robot-tasks/types.ts`; `builders.ts` (`referenceKey` → `global:<globalId>`) |
| `modelId + expressId` bildet den modelllokalen Fallback | implementiert | `types.ts` (zweite Typvariante); `builders.ts` (`express:<modelId>:<expressId>`) |
| Eine `expressId` ohne `modelId` wird abgelehnt | implementiert | `src/domain/robot-tasks/validation.ts` |
| IFC-Klasse und Name sind beschreibende Metadaten, keine Identität | aus Implementierung abgeleitet | `types.ts` (`RobotObjectReferenceMetadata`); `builders.ts` (nicht Teil von `referenceKey`) |
| Viewer-lokale Kennungen werden nicht als `expressId` umgedeutet | implementiert | `selection-adapter.ts`; `selection-types.ts`; `model-provenance.ts` |
| Ohne verwertbare Identität wird keine Referenz erzeugt | implementiert | `selection-adapter.ts` (`ViewerSelectionReferenceError`) |
| Beim Import erhält jede Referenz die Kennung des Quellmodells | implementiert | `src/ifc/model-import/webIfcMissionReader.ts` (`objectReference`) |
| Modellfremde Referenzen werden vor dem Export abgelehnt | implementiert | `ifcMissionRoundtripCoordinator.ts` (`CROSS_MODEL_MISSION_REFERENCE`) |
| Beim Export wird primär über `GlobalId` aufgelöst, `expressId` nur bei passender `modelId` | implementiert | `src/ifc/model-export/webIfcMissionWriter.ts` (`resolveExternalObjects`) |
| Referenzen sind unabhängig von der dargestellten Geometrie | aus Implementierung abgeleitet | Auflösungspfade in `webIfcMissionWriter.ts` und `webIfcMissionReader.ts` ohne Fragments-/Three.js-Bezug |
| Keine automatische Wiederzuordnung bei geänderter Modellrevision | konzeptionell | keine Rebind-Logik im Repository; Abgrenzung gemäß `Strukturübersicht.txt` |

---

## Hinweise für das manuelle Review

1. **Quellenangabe prüfen.** Der normative Satz zur `GlobalId` stützt sich auf die buildingSMART-Dokumentation zu `IfcRoot` (IFC 4.3, `IfcGloballyUniqueId`, Eindeutigkeitsregel `UR1`). Bitte Zitierweise, Schemaversion und Abrufdatum an die Konvention der Arbeit anpassen.
2. **Abschnitt 4.4.5 gegen Kapitel 5 abgleichen.** Die Trennung von Auswahl und Referenz wird hier nur begründet, nicht algorithmisch beschrieben; prüfen, ob Formulierungen mit dem Auswahlkapitel überlappen.
3. **Verhalten bei fehlenden oder mehrdeutigen Referenzen.** Die Gliederung sieht diesen Punkt in 4.4 vor; er ist hier bewusst knapp gehalten (Abbruch statt unsicherer Referenz, Fehler bei nicht auflösbarer `GlobalId`) und könnte bei Bedarf um ein bis zwei Sätze erweitert werden.

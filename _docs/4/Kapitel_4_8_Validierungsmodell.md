# Arbeitsnotiz: untersuchte Repository-Dateien

Orientierung: `REPOSITORY_MAP_IFC_EDITOR_674ede3.md`, `Strukturübersicht.txt`, `repo_structure.txt` (Commit `674ede3`).

Geprüfte Implementierung (Pfade gemäß `repo_structure.txt`):

- `src/domain/robot-tasks/validation.ts`
- `src/domain/robot-tasks/sequencing.ts`
- `src/domain/robot-tasks/types.ts`
- `src/domain/robot-tasks/builders.ts`
- `src/application/robot-tasks/robotMissionService.ts`
- `src/application/robot-tasks/importRobotMissions.ts`
- `src/ifc/robot-tasks/mapper.ts`
- `src/ifc/model-import/webIfcMissionReader.ts`
- `src/ifc/model-roundtrip/ifcMissionRoundtripCoordinator.ts`
- `src/ui-templates/sections/robot-mission-tasks.ts` (nur Prüfung, wo Validierungsergebnisse konsumiert werden)

Zugehörige Testdateien laut `repo_structure.txt`: `test/robot-tasks/robot-mission-domain.test.ts`, `test/robot-tasks/robot-mission-service.test.ts`, `test/robot-tasks/ifc-mission-reader.test.ts`, `test/robot-tasks/import-robot-missions.test.ts`, `test/robot-tasks/ifc-mission-roundtrip-coordinator.test.ts`, `test/robot-tasks/robot-mission-semantic-comparison.test.ts`.

---

# 4.8 Validierungsmodell

## 4.8.1 Motivation und Fragestellung

Ein Annotationsmodell besteht nicht ausschließlich aus Datenstrukturen. Eine Datenstruktur kann syntaktisch korrekt befüllt sein und dennoch eine fachlich sinnlose Robotermission beschreiben: ein Task ohne Zielobjekt, eine Bewegung ohne Startpunkt oder ein Abhängigkeitsgraph ohne widerspruchsfreie Ausführungsreihenfolge. Kapitel 4.8 beantwortet deshalb die Frage, welche fachlichen Invarianten eine Mission erfüllen muss, damit sie innerhalb des Modells als konsistent gilt.

Die Validierung ist in der Umsetzung Bestandteil der Domänenschicht (`src/domain/robot-tasks/validation.ts`) und nicht der Benutzeroberfläche. Sie ist damit unabhängig von Viewer, Persistenz und IFC-Serialisierung und wird von mehreren Aufrufern gemeinsam genutzt: vom Anwendungsservice als explizite Abfrage, vom IFC-Mapping vor dem Export und vom Reader bei der Rekonstruktion importierter Missionen. Die Prüfung sammelt Befunde, statt beim ersten Verstoß abzubrechen, sodass ein vollständiges Bild des Missionszustands entsteht.

## 4.8.2 Strukturelle Validierung

Die strukturelle Ebene sichert die Identität und Vollständigkeit des Aggregats. Eine `RobotMission` benötigt eine nicht leere Kennung und einen nicht leeren Namen sowie mindestens einen ausführbaren Task; jeder `RobotTask` benötigt ebenfalls Kennung und Name. Task-Kennungen müssen innerhalb einer Mission eindeutig sein, weil Hierarchie und Sequenzbeziehungen ausschließlich über diese Kennungen aufgelöst werden. Der Aktionstyp wird zur Laufzeit gegen die Menge der unterstützten Werte geprüft, da deserialisierte Daten die statische Typisierung umgehen können; ein fehlender und ein unbekannter Aktionswert werden dabei unterschieden.

Ergänzend erzwingen die Builder in `src/domain/robot-tasks/builders.ts` einen Teil dieser Invarianten bereits konstruktiv: leere Kennungen oder Namen sowie doppelte Task- und Sequenz-Kennungen führen dort unmittelbar zu einem Domänenfehler. Die deklarative Validierung bleibt dennoch notwendig, weil Missionen auch aus Persistenz oder IFC-Import stammen können.

## 4.8.3 Aktionsbezogene Validierung

Aktionstypen stellen unterschiedliche Anforderungen an einen Task. Direkt manipulierende Aktionen (`OPEN`, `CLOSE`, `SWITCH_ON`, `SWITCH_OFF`) verlangen mindestens ein Zielobjekt, `PASS_THROUGH` mindestens eine Objektreferenz, die wahlweise als Ziel- oder als betroffenes Objekt hinterlegt sein darf. `MOVE` verlangt sowohl eine Start- als auch eine Zielreferenz, da eine Bewegung ohne beide Endpunkte nicht ausführbar beschrieben ist. Für `NAVIGATE_TO` sind keine zusätzlichen Anforderungen implementiert.

Darüber hinaus wird die Aktionssemantik gegen den Objektbezug geprüft: Für türbezogene und schalterbezogene Aktionen wird die bekannte IFC-Klasse der Zielobjekte auf Plausibilität untersucht. Eine bekannte, aber unpassende Klasse gilt als Fehler; eine fehlende Klasseninformation wird lediglich als Warnung geführt, weil die Annotation trotzdem zutreffend sein kann. Schließlich stellt die Validierung sicher, dass Aktionsparameter am Task und nicht an einer Objektreferenz hängen: Referenzen, die aktionsspezifische Eigenschaften mitführen, werden zurückgewiesen. Damit wird die in Kapitel 4.3 begründete Trennung von Objektidentität und Aktionssemantik auch gegen fremde oder ältere Daten durchgesetzt.

## 4.8.4 Referenzvalidierung

Die Referenzvalidierung fragt nicht, wie eine Referenz technisch aufgelöst wird — dies wurde in Kapitel 4.4 behandelt —, sondern ob die gespeicherte Referenz im Kontext der Mission zulässig und verwendbar ist. Geprüft werden alle referenztragenden Felder eines Tasks gemeinsam: Ziel- und betroffene Objekte sowie Start- und Zielreferenz. Eine vorhandene, aber leere `GlobalId` ist unzulässig; ein `expressId`-Wert muss eine nicht negative ganze Zahl sein; und eine rein modelllokale Referenz ohne `GlobalId` erfordert zwingend eine Modellkennung, da sie andernfalls außerhalb ihres Ursprungsmodells nicht mehr eindeutig ist.

## 4.8.5 Sequenz- und Graphvalidierung

Die Abhängigkeiten zwischen Tasks werden getrennt vom Hierarchiebaum geprüft (`src/domain/robot-tasks/sequencing.ts`). Jede Sequenz benötigt eine Kennung; Vorgänger und Nachfolger müssen auf Tasks derselben Mission verweisen, und ein Task darf nicht sein eigener Vorgänger sein. Ergänzend wird der gesamte gerichtete Graph über eine Tiefensuche auf Zyklen untersucht.

```text
Task A → Task B → Task C → Task A
```

Ein solcher Zyklus besitzt keine widerspruchsfreie Ausführungsreihenfolge und wird deshalb als Fehler gemeldet. Die Ordnungsfunktion des Modells verhält sich dazu konsistent: Lässt sich keine vollständige topologische Reihenfolge bilden, wird die Hierarchieordnung unverändert zurückgegeben, sodass keine Tasks stillschweigend verschwinden, während die Validierung den Widerspruch ausweist. Auch Operationen, die den Graphen verändern, prüfen den vollständigen resultierenden Graphen und schlagen atomar fehl, statt eine zyklische Zwischenlage zu erzeugen.

## 4.8.6 Zeitbezogene Validierung

Auf Zeitebene ist bewusst nur eine Prüfung implementiert: Der Fertigstellungsgrad eines Tasks muss ein endlicher Wert im Intervall von 0 bis 1 sein. Eine Konsistenzprüfung zwischen Start- und Endzeit oder eine Dauerprüfung findet auf Domänenebene nicht statt; die Zeitangaben werden als ISO-8601-Zeichenketten geführt und erst bei der IFC-Lexikalisierung interpretiert (vgl. Kapitel 4.6).

## 4.8.7 Fehler und Warnungen

Das Modell kennt genau zwei Schweregrade. Fehler kennzeichnen eine fachlich ungültige Mission und blockieren die Weiterverarbeitung; Warnungen kennzeichnen Unsicherheit, die die Gültigkeit nicht aufhebt. In der aktuellen Implementierung ist die fehlende IFC-Klasseninformation eines Zielobjekts der einzige als Warnung geführte Befund — alle übrigen Regeln sind blockierend. Jeder Befund trägt einen stabilen Code sowie optional Task- und Sequenzbezug, sodass Aufrufer nicht auf Meldungstexte angewiesen sind.

| Validierungsebene | Beispielhafte Prüfung | Zweck |
| --- | --- | --- |
| Struktur | nicht leere und eindeutige Task-Kennungen, Pflichtnamen, mindestens ein Task | konsistentes Domänenobjekt |
| Aktion | Zielobjekt bzw. Start-/Zielreferenz je Aktionstyp, plausible IFC-Klasse | fachlich sinnvoller Task |
| Referenz | gültige `GlobalId` bzw. `modelId` + `expressId`, keine Aktionsparameter an der Referenz | gültige Verknüpfung |
| Sequenz | Sequenz-Kennung, existierende Endpunkte, keine Selbstreferenz | konsistenter Missionsgraph |
| Graph | keine Zyklen | ausführbare Abhängigkeiten |
| Zeit | Fertigstellungsgrad im Bereich 0 bis 1 | konsistentes Zeitmodell |

## 4.8.8 Validierung vor dem Export

Eine syntaktisch erzeugbare IFC-Datei ist nicht automatisch eine fachlich gültige Robotermissionsannotation. Das Modell prüft daher bereits vor dem Schreiben: Die Abbildung des Domänenmodells auf IFC-nahe Records bricht ab, sobald blockierende Validierungsfehler vorliegen. Unvollständige Tasks oder zyklische Graphen können damit gar nicht erst in eine Form gebracht werden, die wie eine exportfertige Annotation aussieht. Die technische Exportpipeline selbst wird im Implementierungskapitel behandelt.

## 4.8.9 Validierung beim Import

Die inverse Richtung nutzt dieselben Regeln. Eine aus IFC rekonstruierte Mission durchläuft die vollständige Domänenvalidierung; die Befunde werden als Importbefunde mit vorangestelltem Domänen-Präfix übernommen. Enthält die Rekonstruktion Fehler, gilt die betroffene Mission als ungültig und wird verworfen. Da jeder Missionsknoten unabhängig rekonstruiert wird, bleiben andere, in sich gültige Missionen derselben Datei importierbar. Auf Roundtrip-Ebene wird eine IFC-Quelle, deren eigene Annotationen fehlerhaft sind, als unsicher markiert; ein Export in diese Quelle wird anschließend verweigert, um bekannt fehlerhafte Annotationen nicht zu überschreiben oder fortzuschreiben.

## 4.8.10 Abgrenzung zum semantischen Roundtrip-Vergleich

Die Domänenvalidierung prüft Invarianten einer einzelnen Mission: Pflichtfelder, Referenzen, Aktionsregeln, Sequenzgraph und Zeitwerte. Der semantische Vergleich prüft demgegenüber eine Relation zwischen zwei Aggregaten, nämlich ob die nach dem Export erneut importierte Mission dem beabsichtigten Domänenmodell entspricht. Beide Mechanismen sind in der Implementierung getrennt und wirken im Roundtrip komplementär; der Vergleich wird im Implementierungs- und Evaluationskapitel vertieft.

---

# Nachweistabelle

| Aussage | Status | Implementierungsnachweis |
| --- | --- | --- |
| Validierung liegt in der Domänenschicht und ist infrastrukturunabhängig | direkt implementiert | `src/domain/robot-tasks/validation.ts` |
| Mission benötigt Kennung, Name und mindestens einen Task | direkt implementiert | `validateMission` in `src/domain/robot-tasks/validation.ts` |
| Task-Kennungen müssen innerhalb der Mission eindeutig sein | direkt implementiert | `validateMission`; zusätzlich `addTaskToMission` in `src/domain/robot-tasks/builders.ts` |
| Aktionstyp wird zur Laufzeit gegen die unterstützte Menge geprüft | direkt implementiert | `validateTask` gegen `ROBOT_ACTION_TYPES` in `src/domain/robot-tasks/types.ts` |
| `OPEN`/`CLOSE`/`SWITCH_ON`/`SWITCH_OFF` erfordern ein Zielobjekt | direkt implementiert | `validateObjectInteractionTask` |
| `PASS_THROUGH` erfordert mindestens eine Objektreferenz | direkt implementiert | `validateObjectInteractionTask` |
| `MOVE` erfordert Start- und Zielreferenz | direkt implementiert | `validateMovementTask` |
| `NAVIGATE_TO` besitzt keine zusätzlichen Referenzregeln | aus Implementierung abgeleitet | keine Behandlung in `validateMovementTask`/`validateObjectInteractionTask` |
| Unpassende bekannte IFC-Klasse = Fehler, fehlende Klasse = Warnung | direkt implementiert | `validateTargetClass` |
| Aktionsparameter dürfen nicht an Objektreferenzen hängen | direkt implementiert | `validateReference` |
| Referenzregeln zu `GlobalId`, `expressId`, `modelId` | direkt implementiert | `validateReference` |
| Sequenzen: Kennung, existierende Endpunkte, keine Selbstreferenz, keine Zyklen | direkt implementiert | `validateTaskSequence`, `hasTaskSequenceCycle` in `src/domain/robot-tasks/sequencing.ts` |
| Bei Zyklus bleibt die Hierarchieordnung erhalten | direkt implementiert | `getTasksInExecutionOrder` in `src/domain/robot-tasks/sequencing.ts` |
| Graphverändernde Operationen schlagen atomar fehl | direkt implementiert | `addTaskSequence`, `setMissionTaskExecutionOrder` |
| Einzige Zeitprüfung ist der Fertigstellungsgrad 0–1 | direkt implementiert | `validateTask`; keine weiteren Zeitprüfungen in `validation.ts` |
| Genau zwei Schweregrade; Warnung nur bei unbekannter Zielklasse | direkt implementiert / abgeleitet | `RobotTaskValidationSeverity` in `types.ts`; einzige `"warning"`-Stelle in `validation.ts` |
| Export wird bei blockierenden Fehlern verhindert | direkt implementiert | `mapMissionToIfcRecords` in `src/ifc/robot-tasks/mapper.ts` |
| Importierte Missionen durchlaufen dieselbe Domänenvalidierung | direkt implementiert | `src/ifc/model-import/webIfcMissionReader.ts` |
| Ungültige Mission wird verworfen, gültige Missionen bleiben importierbar | direkt implementiert | Fehlerbehandlung je Missionsknoten in `WebIfcMissionReader.read` |
| Fehlerhafte Quelle wird als unsicher markiert und blockiert den Export | direkt implementiert | `src/ifc/model-roundtrip/ifcMissionRoundtripCoordinator.ts` |
| Domänenvalidierung und semantischer Roundtrip-Vergleich sind getrennte Konzepte | aus Implementierung abgeleitet | `validation.ts` gegenüber `src/application/robot-tasks/robotMissionSemanticComparison.ts` |
| Validierung als Bestandteil des fachlichen Modells statt UI-Komfort | konzeptionell | Argumentation auf Basis der gemeinsamen Nutzung durch Mapper, Reader und Service |

---

# Punkte für das manuelle Review

1. **Zeitmodell:** Prüfen, ob die bewusst schmale Zeitvalidierung (nur Fertigstellungsgrad) in Kapitel 4.6 oder erst in Kapitel 4.12 als Grenze diskutiert werden soll — im Text ist sie derzeit nur knapp benannt.
2. **Warnungsbegriff:** Aktuell existiert genau ein Warnungsfall. Prüfen, ob die Warnungs-Kategorie im Kapiteltext so prominent bleiben soll oder stärker als Erweiterungspunkt formuliert wird.
3. **Umfang und Überschneidung:** Abschnitt 4.8.9 berührt Import- und Roundtrip-Verhalten; prüfen, ob diese Aussagen im späteren Implementierungskapitel redundant werden.

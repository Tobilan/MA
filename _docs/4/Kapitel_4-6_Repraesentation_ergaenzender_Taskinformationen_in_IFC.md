# Arbeitsnotiz: untersuchte Repository-Dateien

Grundlage der Prüfung ist der in der Repository-Map dokumentierte Commit `674ede3`. Pfadangaben folgen `repo_structure.txt`.

**Primär untersucht (vollständig gelesen):**

- `src/domain/robot-tasks/types.ts` — Domänentypen `RobotTask`, `RobotActionProperties`, `RobotTaskTime`, `RobotMissionSchedule`, `RobotObjectReference`
- `src/ifc/robot-tasks/records.ts` — typisierte IFC-nahe Recordarten und zulässige Relationsnamen
- `src/ifc/robot-tasks/mapper.ts` — tatsächliche Erzeugung von Relationen, Property Sets und Zeitrecords
- `src/ifc/robot-tasks/annotationSchema.ts` — `ROBOT_MISSION_ANNOTATION_SCHEMA_VERSION = "1.0.0"`

**Punktuell zur Verifikation einzelner Aussagen geprüft:**

- `src/ifc/model-export/webIfcMissionWriter.ts` — Konstruktion von `IfcTaskTime`, `IfcWorkSchedule`, `IfcRelAssignsToProcess`, `IfcRelAssignsToProduct`, `IfcRelAssignsToControl`; Guard gegen den Präfix `Pset_`
- `src/ifc/model-import/webIfcMissionReader.ts` — inverse Interpretation der Relationsnamen und der Property Sets
- `src/domain/robot-tasks/validation.ts` — Pflichtbedingungen für Objektbezüge und MOVE-Referenzen

**Orientierung, nicht als Nachweis verwendet:** `REPOSITORY_MAP_IFC_EDITOR_674ede3.md`, `Strukturübersicht.txt`.

**Nicht verfügbar:** Die Dateien unter `test/robot-tasks/` sind im Projektkontext nicht als Inhalt hinterlegt und wurden deshalb nicht als Nachweisquelle herangezogen; alle Aussagen stützen sich auf den Produktivcode.

---

# 4.6 Repräsentation ergänzender Taskinformationen in IFC

Mit der in Abschnitt 4.5 beschriebenen Hierarchie aus übergeordnetem Missions-Task, ausführbaren Teilaufgaben und deren Abhängigkeitsbeziehungen ist das Grundgerüst der Annotation festgelegt. Ein `RobotTask` trägt jedoch über diese strukturelle Einordnung hinaus Informationen, die für eine spätere robotische Auswertung wesentlich sind: Er verweist auf konkrete Elemente des Gebäudemodells, er beschreibt eine auszuführende Aktion mitsamt ihrer Vorbedingungen und Erfolgskriterien, und er kann geplante sowie tatsächliche Ausführungszeiten führen. Diese drei Informationsarten sind fachlich verschieden. Ein Objektbezug stellt eine Beziehung zwischen zwei bereits existierenden Entitäten her, eine Aktionsangabe beschreibt projektspezifische Robotiksemantik ohne Entsprechung im IFC-Kernschema, und eine Zeitangabe entspricht einem in IFC bereits standardisierten Konzept. Das Annotationsmodell nutzt deshalb bewusst drei unterschiedliche IFC-Mechanismen, statt sämtliche Zusatzinformationen einheitlich in ein benutzerdefiniertes Property Set zu schreiben. Der vorliegende Abschnitt begründet diese Zuordnung; die vollständige, systematische Abbildung des Domänenmodells folgt in Abschnitt 4.9.

## 4.6.1 Objektbezüge als Relationen

Das Domänenmodell unterscheidet vier Felder, über die ein `RobotTask` auf Gebäudeelemente verweist. `targetObjects` bezeichnet die unmittelbar bearbeiteten oder als Handlungskontext genutzten Objekte, `affectedObjects` die lediglich mittelbar betroffenen Objekte. Für Bewegungsaufgaben treten `startReference` als Ausgangspunkt und `targetReference` als Ziel hinzu. Diese Felder sind keine redundanten Varianten derselben Zuordnung, sondern kodieren unterschiedliche Rollen, die dasselbe Bauteil im Kontext verschiedener Aufgaben einnehmen kann: Eine Tür ist beim Öffnen direktes Ziel, bei einer Durchfahrt Durchgangselement und bei einer Bewegungsaufgabe möglicherweise nur Zwischenraumgrenze. Die Domänenvalidierung behandelt diese Rollen entsprechend differenziert, indem sie beispielsweise für `OPEN`, `CLOSE`, `SWITCH_ON` und `SWITCH_OFF` mindestens ein Zielobjekt und für `MOVE` sowohl Start- als auch Zielreferenz verlangt.

Die Abbildung dieser Rollen erfolgt ausschließlich relational. Beim Mapping wird aus einer `RobotObjectReference` eine externe Objektreferenz erzeugt, die neben `GlobalId` und dem modelllokalen Rückfallpaar aus Modell- und Express-ID lediglich IFC-Klasse und Namen übernimmt. Es werden weder Geometrie noch Eigenschaften des Bauteils dupliziert, und es wird umgekehrt keine Aktionssemantik an das Gebäudeelement geschrieben. Das annotierte Modell bleibt dadurch in seinem bautechnischen Bestand unverändert; die Mission wird ihm als zusätzlicher Beziehungsgraph beigestellt.

Als Trägerbeziehung dient überwiegend `IfcRelAssignsToProcess`, die einen Prozess mit den von ihm in Anspruch genommenen Objekten verknüpft. Die konkrete Rolle wird über das `Name`-Attribut der Beziehung geführt und nimmt die Werte `OPERATES_ON`, `AFFECTS`, `PASSES_THROUGH`, `NAVIGATES_TO` und `MOVE_FROM` an. Direkte Zielobjekte erhalten dabei einen aktionsabhängigen Namen: Für `PASS_THROUGH` und `NAVIGATE_TO` werden die spezifischeren Rollen gewählt, in allen übrigen Fällen `OPERATES_ON`. Eine Ausnahme bildet das Bewegungsziel. Da es kein vom Prozess genutztes, sondern ein den Prozess bestimmendes Produkt darstellt, wird es über `IfcRelAssignsToProduct` mit dem Namen `MOVE_TO` abgebildet, wobei das Zielobjekt als `RelatingProduct` und der Task als zugeordnetes Objekt auftritt. Die Richtungsumkehr gegenüber den übrigen Zuordnungen ist damit nicht willkürlich, sondern folgt der Semantik der jeweiligen IFC-Beziehung. Weil sämtliche Rollen als eigenständige Beziehungsobjekte mit sprechendem Namen vorliegen, lässt sich der Objektbezug beim Reimport eindeutig in dasselbe Domänenfeld zurückführen.

## 4.6.2 Projektspezifische Semantik in eigenen Property Sets

Wo IFC bereits eine passende Semantik bereitstellt, nutzt das Annotationsmodell native Attribute: Die Domänen-ID eines Tasks wird nach `Identification` geschrieben, der Lebenszyklusstatus nach `Status`, die vierstufige Priorität in das ganzzahlige `Priority`-Attribut, und die Unterscheidung zwischen Missions- und Taskebene erfolgt über `ObjectType` in Verbindung mit einem benutzerdefinierten vordefinierten Typ. Für die eigentliche Robotiksemantik existiert eine solche Entsprechung jedoch nicht. Weder die unterstützten Aktionsarten noch Angaben zu geforderten Roboterfähigkeiten oder zu Vor- und Nachbedingungen lassen sich verlustfrei auf Attribute des IFC-Kernschemas abbilden. Diese Informationen werden deshalb ergänzend über eigene Property Sets geführt, die dem generierten `IfcTask` über `IfcRelDefinesByProperties` zugeordnet werden — und ausdrücklich nur diesem, nicht den referenzierten Bauteilen.

Implementiert sind drei Property Sets. `RobotAction` trägt am ausführbaren Task die Aktionssemantik: `ActionType` ist stets vorhanden, da es das angeforderte Verhalten benennt; optional treten `TargetState`, `TargetObjectRole`, `AffectedObjectRole`, `RequiredCapability` und `SuccessCondition` als Einzelwerte sowie `Preconditions` und `Postconditions` als Listenwerte hinzu. `RobotTask` führt taskbezogene Metadaten, namentlich die Änderungszeitstempel sowie die optionalen Viewer-Annotationsdaten aus Kamerastellung und Markerposition. `RobotMission` führt am übergeordneten Missions-Task die entsprechenden Zeitstempel sowie zwei für Kompatibilität und Wiedereinlesen wesentliche Angaben: die Version des Annotationsschemas, derzeit `1.0.0`, und ein boolesches Kennzeichen, ob die Mission einen fachlich gesetzten Zeitplan besitzt. Der reservierte Präfix `Pset_` wird für diese Sets nicht verwendet; der Writer bricht den Export ab, sobald ein Property-Set-Name mit diesem Präfix beginnt. Die zugrunde liegende Designentscheidung lässt sich damit knapp fassen: Standardisierte IFC-Strukturen werden genutzt, wo eine passende Semantik vorhanden ist, während projektspezifische Robotiksemantik ergänzend und klar erkennbar abgegrenzt in eigenen Property Sets abgelegt wird.

## 4.6.3 Zeitinformationen über native IFC-Strukturen

Zeitangaben bilden den Gegenfall zur Aktionssemantik. Die Domänenstruktur `RobotTaskTime` führt geplanten Start, geplantes Ende, geplante Dauer, tatsächliche Start- und Endzeitpunkte, die verbleibende Restdauer sowie einen Fertigstellungsgrad. Für genau diese Angaben stellt IFC mit `IfcTaskTime` eine etablierte Struktur bereit. Das Annotationsmodell schreibt Zeitinformationen deshalb nicht als beliebige Custom Properties, sondern erzeugt bei vorhandener Zeitangabe einen eigenen Zeitrecord, der über das native `TaskTime`-Attribut des Tasks referenziert wird und ausdrücklich nicht über eine Property-Beziehung. Beim Schreiben werden die Werte in die typisierten IFC-Wertarten überführt; die Ableitung des Dauertyps aus dem Vorhandensein einer Dauerangabe und die Behandlung des Fertigstellungsgrads als positives Verhältnismaß zeigen dabei, dass die Abbildung den Typrestriktionen des Schemas folgt und nicht lediglich Zeichenketten ablegt.

Auf Missionsebene wird die optionale Struktur `RobotMissionSchedule` auf `IfcWorkSchedule` abgebildet und über `IfcRelAssignsToControl` mit dem übergeordneten Missions-Task verbunden. Bemerkenswert ist, dass ein Zeitplan auch dann deterministisch erzeugt wird, wenn die Mission keinen fachlich gesetzten Plan besitzt; die Unterscheidung zwischen technisch notwendiger Infrastruktur und fachlicher Planungsaussage bleibt jedoch erhalten, weil sie über die genannte Kennzeichnung im Property Set `RobotMission` explizit festgehalten wird. Damit entsteht kein Informationsverlust, obwohl der IFC-Graph in beiden Fällen strukturell gleich aufgebaut ist.
TODO
## 4.6.4 Zusammenführung

Die drei Bereiche folgen damit einem gemeinsamen Auswahlprinzip: Nicht die Herkunft der Information aus dem Missionsmodell, sondern ihre Bedeutung bestimmt den IFC-Mechanismus. Beziehungen zwischen bestehenden Entitäten werden als Beziehungsobjekte modelliert, standardisierbare Sachverhalte über native Entitäten und Attribute, und ausschließlich das fachlich Neue wird als projektspezifische Erweiterung ergänzt. Der Umfang der eigenen Property Sets bleibt dadurch begrenzt und beschreibt genau jene Semantik, für die IFC keine Entsprechung anbietet.

```text
                    RobotTask
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
   Objektbezug    Aktionssemantik    Zeitdaten
        │              │              │
        ▼              ▼              ▼
 IFC-Relationen   Property Sets   IFC-Zeitmodell
```

**Abbildung 4.x:** Zuordnung der drei Informationsarten eines `RobotTask` zu den jeweils verwendeten IFC-Repräsentationsmechanismen.

*Positionsvorschlag:* unmittelbar nach dem ersten Absatz von 4.6.4, vor dem abschließenden Übergang.

Aus dieser Aufteilung ergibt sich zugleich die Aufgabe des folgenden Abschnitts. Die hier einzeln begründeten Mechanismen greifen im erzeugten Modell ineinander: Derselbe `IfcTask` ist Ausgangspunkt mehrerer Zuweisungsbeziehungen, Träger zweier Property Sets und Inhaber eines Zeitobjekts, während er zugleich in Hierarchie- und Abfolgebeziehungen eingebettet ist. Abschnitt 4.9 führt diese Einzelmechanismen deshalb zu einer geschlossenen Darstellung zusammen und zeigt systematisch, wie das vollständige interne Domänenmodell aus `RobotMission` und `RobotTask` auf den resultierenden IFC-Graphen abgebildet wird.

---

# Nachweistabelle

| Aussage | Status | Implementierungsnachweis |
| ------- | ------ | ------------------------ |
| `RobotTask` besitzt die Objektbezugsfelder `targetObjects`, `affectedObjects`, `startReference`, `targetReference` | direkt implementiert | `src/domain/robot-tasks/types.ts` |
| `OPEN`/`CLOSE`/`SWITCH_ON`/`SWITCH_OFF` erfordern mindestens ein Zielobjekt; `MOVE` erfordert Start- und Zielreferenz | direkt implementiert | `src/domain/robot-tasks/validation.ts` |
| Objektbezüge werden als `IfcRelAssignsToProcess` mit Rollennamen `OPERATES_ON`, `AFFECTS`, `PASSES_THROUGH`, `NAVIGATES_TO`, `MOVE_FROM` abgebildet | direkt implementiert | `src/ifc/robot-tasks/mapper.ts`, `src/ifc/robot-tasks/records.ts` |
| Bewegungsziel wird über `IfcRelAssignsToProduct` mit Namen `MOVE_TO` abgebildet (Objekt als `RelatingProduct`) | direkt implementiert | `src/ifc/robot-tasks/mapper.ts`, `src/ifc/model-export/webIfcMissionWriter.ts` |
| Rollenname wird in das `Name`-Attribut der Beziehung geschrieben | direkt implementiert | `src/ifc/model-export/webIfcMissionWriter.ts` |
| Es werden nur Identität und beschreibende Metadaten des Bauteils übernommen, keine Aktionssemantik am Objekt | direkt implementiert | `src/ifc/robot-tasks/mapper.ts` (`externalObjectReference`) |
| Rollen sind beim Reimport eindeutig auf die Domänenfelder rückführbar | direkt implementiert | `src/ifc/model-import/webIfcMissionReader.ts` |
| Property Sets `RobotAction`, `RobotTask`, `RobotMission` existieren und werden über `IfcRelDefinesByProperties` nur dem generierten `IfcTask` zugeordnet | direkt implementiert | `src/ifc/robot-tasks/mapper.ts`, `src/ifc/robot-tasks/records.ts` |
| `RobotAction` enthält `ActionType` sowie optional `TargetState`, `TargetObjectRole`, `AffectedObjectRole`, `RequiredCapability`, `SuccessCondition`, `Preconditions`, `Postconditions` | direkt implementiert | `src/ifc/robot-tasks/mapper.ts` |
| `RobotMission` enthält Zeitstempel, `AnnotationSchemaVersion = "1.0.0"` und `HasExplicitSchedule` | direkt implementiert | `src/ifc/robot-tasks/mapper.ts`, `src/ifc/robot-tasks/annotationSchema.ts` |
| Präfix `Pset_` wird für eigene Property Sets nicht verwendet; Export bricht andernfalls ab | direkt implementiert | `src/ifc/model-export/webIfcMissionWriter.ts` |
| Begründung, dass `Pset_` normativ für standardisierte Sets reserviert ist | externe IFC-Quelle erforderlich | buildingSMART-Spezifikation zu zitieren |
| Native Attribute werden genutzt, wo Semantik vorhanden ist (`Identification`, `Status`, `Priority`, `ObjectType`) | direkt implementiert | `src/ifc/robot-tasks/mapper.ts`, `src/ifc/model-export/webIfcMissionWriter.ts` |
| `RobotTaskTime` wird auf `IfcTaskTime` abgebildet und über das native `TaskTime`-Attribut referenziert, nicht über eine Property-Beziehung | direkt implementiert | `src/ifc/robot-tasks/records.ts`, `src/ifc/robot-tasks/mapper.ts` |
| Zeitwerte werden typisiert geschrieben; Dauertyp und Fertigstellungsgrad folgen den Schemarestriktionen | direkt implementiert | `src/ifc/model-export/webIfcMissionWriter.ts` |
| `RobotMissionSchedule` wird auf `IfcWorkSchedule` und `IfcRelAssignsToControl` am Missions-Task abgebildet | direkt implementiert | `src/ifc/robot-tasks/mapper.ts` |
| Ein Zeitplan wird auch ohne fachlichen Domänen-Schedule deterministisch erzeugt; die Unterscheidung bleibt über `HasExplicitSchedule` erhalten | aus Implementierung abgeleitet | `src/ifc/robot-tasks/mapper.ts` |
| Dasselbe Bauteil kann in verschiedenen Tasks unterschiedliche Rollen einnehmen | aus Implementierung abgeleitet | `src/domain/robot-tasks/types.ts` (Kommentierung zu `RobotActionProperties`) |
| Die Wahl des IFC-Mechanismus richtet sich nach der Bedeutung der Information | konzeptionell | Argumentation dieses Abschnitts |

---

# Offene Punkte für das manuelle Review

1. **Abschnittsnummerierung.** Die Strukturübersicht führt die Inhalte getrennt als 4.6, 4.7 und 4.8. Der vorliegende Text fasst sie zu 4.6 zusammen; die Verweise auf die Mapping-Tabelle sind derzeit auf 4.9 gesetzt und müssen an die endgültige Nummerierung angepasst werden.
2. **Belegstelle zum `Pset_`-Präfix.** Der Code erzwingt die Vermeidung, begründet sie aber nicht normativ. Für die Aussage im Fließtext ist eine Referenz auf die buildingSMART-Spezifikation zu ergänzen.
3. **Detailtiefe zu `TargetObjectRole` und `AffectedObjectRole`.** Diese beiden Properties überschneiden sich thematisch mit den Rollennamen der Beziehungen. Zu prüfen ist, ob die Abgrenzung im Text ausreichend deutlich wird oder ob sie besser in Abschnitt 4.9 vertieft wird.

Erstelle Kapitel **4.8 „Validierungsmodell“** meiner deutschsprachigen Masterarbeit.

Das Kapitel gehört zu:

**4 – Konzeption des IFC-basierten Annotationsmodells**

Durch die Zusammenfassung früherer Unterkapitel entspricht dieses Kapitel inhaltlich dem ursprünglich später vorgesehenen Abschnitt zur Validierung.

Halte das Kapitel bewusst kompakt. Zielumfang:

**ca. 700–1.000 Wörter**

Ich werde den Text anschließend selbst manuell reviewen und mit anderen Entwürfen vergleichen. Verwende keinen automatisierten Codex-/Claude-Workflow.

# 1. Quellenbasis

Lies zuerst die im Projektkontext verfügbaren Dateien:

1. `REPOSITORY_MAP_IFC_EDITOR_674ede3.md`
2. `Strukturübersicht.txt`
3. `repo_structure.txt`

Untersuche anschließend gezielt die tatsächliche Implementierung.

Besonders relevant sind:

* `src/domain/robot-tasks/validation.ts`
* `src/domain/robot-tasks/sequencing.ts`
* `src/domain/robot-tasks/types.ts`
* `src/domain/robot-tasks/builders.ts`

Bei Bedarf ergänzend:

* `src/application/robot-tasks/robotMissionService.ts`
* `src/application/robot-tasks/robotMissionServiceError.ts`
* `src/application/robot-tasks/importRobotMissions.ts`
* `src/ifc/model-import/ifcMissionImportService.ts`
* `src/application/robot-tasks/robotMissionSemanticComparison.ts`

Berücksichtige außerdem die zugehörigen Tests, insbesondere soweit in `repo_structure.txt` vorhanden:

* Domain-Tests,
* Service-Tests,
* Import-Tests,
* Roundtrip-Tests,
* semantische Vergleichstests.

Verwende für Repository-Dateireferenzen ausschließlich Pfade aus `repo_structure.txt`.

Die Repository-Map dient als Orientierung. Konkrete Aussagen über Validierungsregeln müssen am tatsächlichen Quellcode geprüft werden.

# 2. Ziel des Kapitels

Kapitel 4.8 soll erläutern, wie verhindert wird, dass strukturell oder semantisch widersprüchliche Robotermissionen als gültige Annotationen behandelt oder exportiert werden.

Die zentrale Fragestellung lautet:

**Welche fachlichen Invarianten muss eine Robotermission erfüllen, damit sie innerhalb des Annotationsmodells als konsistent gilt?**

Das Kapitel soll deutlich machen, dass Validierung nicht nur eine UI-Komfortfunktion ist, sondern Bestandteil des fachlichen Modells.

# 3. Validierungsebenen

Strukturiere die Validierung in wenige nachvollziehbare Kategorien.

## Strukturelle Validierung

Prüfe anhand der Implementierung unter anderem:

* erforderliche IDs,
* erforderliche Namen oder Pflichtinformationen,
* eindeutige Task-IDs,
* eindeutige Sequenz-IDs,
* gültige Wertebereiche,
* Konsistenz optionaler und verpflichtender Felder.

Beschreibe nicht jede einzelne Prüfung, sondern erkläre das Prinzip.

## Aktionsbezogene Validierung

Erkläre, dass unterschiedliche `RobotActionType`-Werte unterschiedliche Anforderungen an einen Task stellen können.

Prüfe die tatsächlich implementierten Regeln.

Beispiele dürfen unter anderem sein:

* eine Aktion benötigt ein geeignetes Zielobjekt,
* `MOVE` benötigt Start- und Zielreferenzen,
* bestimmte Aktionsparameter sind nur für bestimmte Aktionen sinnvoll,
* Aktionssemantik und Objektbezug dürfen sich nicht widersprechen.

Nutze nur Regeln, die durch die Implementierung bestätigt werden.

Vermeide eine erneute ausführliche Beschreibung der Aktionsarten aus Kapitel 4.3.

# 4. Referenzvalidierung

Erkläre kompakt, dass Objekt- und Taskreferenzen auf tatsächlich existierende Elemente verweisen müssen.

Prüfe insbesondere:

* Gültigkeit von Ziel- und betroffenen Objekten,
* Start- und Zielreferenzen,
* unbekannte oder unvollständige Referenzen,
* modellfremde Referenzen, sofern dies tatsächlich validiert wird.

Die technische Auflösung von `GlobalId`, `modelId` und `expressId` wurde bereits in Kapitel 4.4 behandelt und soll hier nicht wiederholt werden.

Hier geht es nur um die Frage:

**Ist die gespeicherte Referenz im Kontext der Mission zulässig und verwendbar?**

# 5. Sequenz- und Graphvalidierung

Erkläre die Prüfung der Task-Abhängigkeiten.

Prüfe anhand von `sequencing.ts` und `validation.ts` insbesondere:

* Vorgänger und Nachfolger müssen existierende Tasks referenzieren,
* ein Task darf nicht von sich selbst abhängen,
* ungültige Sequenzreferenzen werden erkannt,
* Zyklen werden erkannt.

Veranschauliche knapp:

```text
Task A → Task B → Task C → Task A
```

Ein solcher Zyklus besitzt keine widerspruchsfreie Ausführungsreihenfolge und muss daher als ungültig erkannt werden.

Wiederhole nicht die ausführliche Modellierung von `RobotTaskSequence` aus Kapitel 4.5.

# 6. Zeitbezogene Validierung

Prüfe, welche zeitlichen Plausibilitätsprüfungen tatsächlich implementiert sind.

Beispiele können sein:

* gültige Zeitwerte,
* gültige Dauer,
* Wertebereich des Fertigstellungsgrads,
* Konsistenz zwischen Start- und Endzeit.

Nur tatsächlich vorhandene Prüfungen beschreiben.

Das Zeitmodell selbst wurde bereits in Kapitel 4.6 behandelt.

# 7. Fehler und Warnungen

Untersuche, ob die Implementierung unterschiedliche Schweregrade oder Kategorien von Validierungsproblemen unterscheidet.

Erkläre, sofern nachweisbar:

* welche Probleme als Fehler gelten,
* welche Probleme lediglich als Warnung behandelt werden,
* welche Konsequenzen sich daraus für Bearbeitung oder Export ergeben.

Die zentrale Idee soll sein:

```text
Fehler
→ fachlich ungültige Mission
→ Export bzw. Weiterverarbeitung verhindern

Warnung
→ auffälliger oder unvollständiger Zustand
→ kann je nach Regel weiterverarbeitet werden
```

Passe diese Aussage an das tatsächliche Verhalten im Repository an.

Keine Severity-Kategorien erfinden.

# 8. Validierung vor Export

Prüfe, ob und wie die Mission vor dem IFC-Export validiert wird.

Erkläre kurz:

**Eine syntaktisch erzeugbare IFC-Datei ist nicht automatisch eine fachlich gültige Robotermissionsannotation.**

Das Domänenmodell soll deshalb bereits vor dem Schreiben auf relevante Invarianten geprüft werden.

Beschreibe die technische Exportpipeline nicht im Detail; diese gehört in das Implementierungskapitel.

# 9. Validierung beim Import und Roundtrip

Da der Missionsimport und der RobotMission-Roundtrip implementiert sind, soll auch die inverse Richtung kurz berücksichtigt werden.

Prüfe anhand der Implementierung:

* wie importierte Missionen auf Konsistenz geprüft werden,
* wie ungültige oder teilweise ungültige Missionsgraphen behandelt werden,
* ob einzelne gültige Missionen trotz anderer fehlerhafter Annotationen importierbar bleiben,
* wann eine IFC-Quelle als unsicher oder nicht weiterverwendbar behandelt wird.

Beschreibe ausschließlich das tatsächlich implementierte Verhalten.

Der technische Reader, Replacement-Export und Roundtrip-Coordinator werden später ausführlicher behandelt.

# 10. Abgrenzung zu semantischem Roundtrip-Vergleich

Unterscheide zwei Konzepte:

**Domänenvalidierung**

prüft beispielsweise:

* Pflichtfelder,
* Referenzen,
* Aktionsregeln,
* Sequenzgraph,
* Zeitwerte.

**Semantischer Roundtrip-Vergleich**

prüft dagegen, ob die nach dem IFC-Export erneut importierte Mission fachlich dem beabsichtigten Domänenmodell entspricht.

Wenn diese Trennung durch die Implementierung bestätigt wird, erwähne sie kurz.

Der semantische Roundtrip-Vergleich soll nicht ausführlich erklärt werden; er gehört stärker zum Implementierungs- und Evaluationskapitel.

# 11. Abgrenzung zu anderen Kapiteln

Verwende `Strukturübersicht.txt`.

Nicht erneut ausführlich behandeln:

* Domänenmodell aus 4.2,
* Aktionen aus 4.3,
* Objektreferenzierung aus 4.4,
* Sequenzmodell aus 4.5,
* Taskinformationen und IFC-Zuordnungen aus 4.6,
* vollständiges IFC-Mapping aus 4.7.

Ebenfalls nicht detailliert behandeln:

* konkrete UI-Fehlermeldungen,
* Editor-Panels,
* konkrete Testimplementierungen,
* interne Error-Klassen,
* technische Exportpipeline,
* Roundtrip-Coordinator.

Kapitel 4.8 beantwortet im Wesentlichen nur:

**Welche Bedingungen definieren eine fachlich gültige Robotermission?**

# 12. Keine vollständige Regelreferenz erstellen

Das Kapitel soll kein Validierungshandbuch oder API-Nachschlagewerk werden.

Vermeide deshalb:

* Aufzählung jeder einzelnen `if`-Bedingung,
* lange Listen aller möglichen Fehlermeldungen,
* vollständige TypeScript-Codeblöcke,
* detaillierte Beschreibung jeder Testdatei.

Fasse Regeln sinnvoll zu Kategorien zusammen.

# 13. Geeignete kompakte Übersicht

Baue nach Möglichkeit eine kleine Tabelle in das Kapitel ein:

| Validierungsebene | Beispielhafte Prüfung              | Zweck                      |
| ----------------- | ---------------------------------- | -------------------------- |
| Struktur          | eindeutige IDs und Pflichtfelder   | konsistentes Domänenobjekt |
| Aktion            | erforderliche Referenzen/Parameter | fachlich sinnvoller Task   |
| Referenz          | Zielobjekt bzw. Task existiert     | gültige Verknüpfung        |
| Sequenz           | gültige Vorgänger/Nachfolger       | konsistenter Missionsgraph |
| Graph             | keine Zyklen                       | ausführbare Abhängigkeiten |
| Zeit              | plausible Zeitwerte                | konsistentes Zeitmodell    |

Passe die Tabelle an die tatsächlich implementierten Regeln an.

# 14. Wissenschaftlicher Stil

Schreibe vollständig auf Deutsch.

Verwende:

* formalen wissenschaftlichen Stil,
* kompakte Argumentation,
* klare Trennung der Validierungsebenen,
* präzise technische Formulierungen.

Vermeide:

* Marketing-Sprache,
* unnötig detaillierte Codebeschreibung,
* Wiederholungen vorheriger Kapitel,
* Aussagen über Regeln, die nur vorgeschlagen, aber nicht implementiert sind.

Technische Bezeichner wie

* `RobotMission`,
* `RobotTask`,
* `RobotTaskSequence`,
* `MOVE`

bleiben unverändert.

# 15. Abbildung

Für dieses Kapitel ist keine große Abbildung erforderlich.

Prüfe lediglich, ob ein sehr kleines Schema hilfreich ist:

```text
RobotMission
     ↓
Domänenvalidierung
     ↓
┌───────────────┬─────────────────┐
│ gültig        │ ungültig        │
│               │                 │
│ Weitergabe /  │ Fehler bzw.     │
│ IFC-Export    │ keine Freigabe  │
└───────────────┴─────────────────┘
```

Verwende maximal eine kleine technische Abbildung.

Wenn die Tabelle den Sachverhalt bereits ausreichend erklärt, verzichte auf die Abbildung.

# 16. Gewünschte Ausgabe

Erstelle:

1. eine kurze Arbeitsnotiz mit den untersuchten Repository-Dateien,
2. das vollständige Kapitel **4.8 „Validierungsmodell“** mit ca. 700–1.000 Wörtern,
3. eine kompakte Validierungstabelle innerhalb des Kapiteltextes,
4. optional eine kleine technische Abbildung,
5. anschließend eine Nachweistabelle:

| Aussage | Status | Implementierungsnachweis |
| ------- | ------ | ------------------------ |

Unterscheide:

* direkt implementiert,
* aus Implementierung abgeleitet,
* konzeptionell.

Nenne abschließend maximal drei Punkte für mein manuelles Review.

# Wichtigste inhaltliche Aussage

Das Kapitel soll klar herausarbeiten:

**Das Annotationsmodell besteht nicht nur aus Datenstrukturen, sondern definiert auch fachliche Invarianten. Die Validierung verhindert, dass unvollständige, widersprüchliche oder zyklische Robotermissionen als gültige Missionsannotation behandelt und weiterverarbeitet werden.**

Beginne jetzt mit `REPOSITORY_MAP_IFC_EDITOR_674ede3.md`, `Strukturübersicht.txt` und `repo_structure.txt` und untersuche anschließend gezielt die relevante Domain-, Sequenz- und Validierungsimplementierung.

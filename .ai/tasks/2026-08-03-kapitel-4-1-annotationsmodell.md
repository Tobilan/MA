# Aufgabe: Kapitel 4.1 zum IFC-basierten Annotationsmodell

## Ziel

Unterabschnitt 4.1 der deutschsprachigen Masterarbeit führt die Modellierungsziele und zentralen Designentscheidungen des IFC-basierten Annotationsmodells ein. Er begründet die Verbindung von Robotermissionen, Roboteraufgaben, konkreten Roboteraktionen, IFC-Gebäudeobjekten, Ausführungsabhängigkeiten, aktionsspezifischen Parametern und optionalen Zeitangaben und schafft die konzeptionelle Grundlage für die nachfolgende Formalisierung.

## Umfang

Erstellt wird ein zusammenhängender wissenschaftlicher Unterabschnitt von ungefähr 1.000 bis 1.500 deutschen Wörtern. Behandelt werden das Modellierungsproblem, die aufgabenbezogene Aktionssemantik, die Trennung von internem Domänenmodell, IFC-Repräsentation und UI-Zustand, die Rolle der annotierten IFC-Datei, Hierarchie und Ausführungsfolge, stabile Objektbezüge, die Abgrenzung semantischer und geometrischer Referenzen sowie Validierung und kontrollierte Erweiterbarkeit. Der aktuelle Implementierungsstand wird nur in dem Umfang beschrieben, der am geprüften Viewer-Commit nachweisbar ist.

## Betroffene Dateien

- `.ai/tasks/2026-08-03-kapitel-4-1-annotationsmodell.md`
- `.ai/tasks/2026-08-03-kapitel-4-1-annotationsmodell-claims.md`
- `Abschlussarbeit.tex`
- `inhalt/kapitel4_annotationsmodell.tex`
- `.ai/decisions/2026-08-03-kapitel-4-1-annotationsmodell-review-decisions.md`
- flüchtige, ignorierte Review-Artefakte unter `.ai/reviews/`

## Ausdrückliche Ausschlüsse

- Keine Ausarbeitung des gesamten vierten Kapitels oder anderer noch fehlender Kapitel.
- Kein detailliertes Mapping einzelner IFC-Entitäten; `IfcRelNests` und `IfcRelSequence` werden höchstens vorausblickend eingeordnet.
- Keine detaillierte Beschreibung der Editorimplementierung und keine Evaluation.
- Keine Leistungswerte, keine Aussage über implementierte ROS-Integration und keine detaillierten Wegpunkt- oder Pfadplanungsalgorithmen.
- Keine vollständige Ausarbeitung von Surface Tiling, Koordinatentransformationen oder Anfahrposen.
- Keine Behauptung eines allgemeinen IFC- oder Fragments-Roundtrips.
- Keine ungeprüften Quellen, Bibliografieeinträge, Standardsaussagen, APIs, IFC-Entitäten, Relationen oder Repository-Pfade.

## Erforderliche Nachweise

- Thesis-Regeln in `docs/ai/THESIS_CONTRACT.md`, `docs/ai/GERMAN_WRITING_GUIDE.md`, `docs/ai/TERMINOLOGY.md` und `docs/ai/CLAIM_POLICY.md`.
- Viewer-Repository `https://github.com/Tobilan/poc_thatopen` am geprüften Commit `674ede3bf2e7e6cf466bc4c16fe06c90fbb1753c`.
- Internes Domänenmodell und Referenztypen in `src/domain/robot-tasks/types.ts`.
- Sequenz- und Validierungslogik in `src/domain/robot-tasks/sequencing.ts` und `src/domain/robot-tasks/validation.ts`.
- IFC-Mapping und Schemakennzeichnung in `src/ifc/robot-tasks/mapper.ts` und `src/ifc/robot-tasks/annotationSchema.ts`.
- Begrenzter Missionsimport und -roundtrip in `src/ifc/model-import/ifcMissionImportService.ts`, `src/ifc/model-import/webIfcMissionReader.ts`, `src/ifc/model-export/ifcModelExportService.ts` und `src/ifc/model-roundtrip/ifcMissionRoundtripCoordinator.ts`.
- Zugehörige Tests unter `test/robot-tasks/`, insbesondere `robot-mission-domain.test.ts`, `ifc-relation-mapper.test.ts`, `ifc-mission-reader.test.ts`, `ifc-mission-export.integration.test.ts` und `ifc-mission-replacement.integration.test.ts`.

## Besonders zu prüfende Aussagen

- `IMPLEMENTATION_CLAIM`: Domänenmodell, Validierung, Mapping sowie der auf Robotermissionsannotationen begrenzte IFC-Import und -Roundtrip sind am genannten Commit prototypisch implementiert.
- `DESIGN_PROPOSAL`: Die annotierte IFC-Datei wird für die Arbeit als kanonisches Persistenzformat festgelegt; ein roboterbezogener JSON-Export ist lediglich als abgeleitete Ausgabe vorgesehen.
- `DESIGN_PROPOSAL`: Ein IFC-Objektbezug, eine Objektplatzierung, ein geometrischer Referenzpunkt, eine Teilflächenreferenz und ein Navigationsziel werden nicht gleichgesetzt.
- `FUTURE_WORK`: Allgemeine strukturelle IFC-/Fragments-Änderungen, detaillierte Navigationsableitungen und ein roboterbezogener JSON-Export sind nicht als vollständig implementiert darzustellen.
- Projektbezogene Aktionswerte dürfen nicht als standardisierte IFC-Aufzählung erscheinen.

## Sprachliche Anforderungen

Formales wissenschaftliches Deutsch gemäß `docs/ai/GERMAN_WRITING_GUIDE.md`; etablierte technische Bezeichner bleiben unverändert. Die Begriffe aus `docs/ai/TERMINOLOGY.md` sind konsistent zu verwenden, und Implementiertes, prototypisch Implementiertes, konzeptionell Vorgesehenes und zukünftige Erweiterungen sind eindeutig zu unterscheiden.

## Akzeptanzkriterien

- [x] Unterabschnitt 4.1 ist im kanonischen LaTeX-Bestand eingebunden und trägt eine konsistente Überschrift und ein eindeutiges Label.
- [x] Der Text erläutert Modellierungsproblem, Ziele und aufgabenbezogene Aktionssemantik als zusammenhängende Argumentation.
- [x] Internes Domänenmodell, IFC-Repräsentation, Laufzeitmodell und UI-Zustand werden getrennt.
- [x] Annotierte IFC-Datei, abgeleiteter Roboterexport und Grenzen des Roundtrips werden präzise unterschieden.
- [x] Hierarchie und zeitliche Ausführungsabhängigkeiten werden getrennt behandelt.
- [x] Dauerhafte IFC-Objektbezüge und modellgebundene Fallback-Identifikatoren werden eingeordnet.
- [x] Semantische Objektbezüge werden nicht mit geometrischen Referenzpunkten oder Navigationszielen gleichgesetzt.
- [x] Validierung, Versionierung und projektspezifische Erweiterungen einschließlich der Benennung eigener Property Sets werden erläutert.
- [x] Es werden keine unbelegten Zitate, Quellen, Standardsbehauptungen oder Implementierungsdetails eingeführt.
- [x] Baseline, Entwurf und Endstand werden mit dem konfigurierten Quality Gate geprüft.
- [x] Das Claude-Review wird read-only ausgeführt und validiert oder seine technische Nichtverfügbarkeit präzise dokumentiert.
- [x] Jedes vorhandene Finding erhält eine deutsche Entscheidung; nur angenommene Änderungen werden umgesetzt.

## Build-Befehl

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error Abschlussarbeit.tex
```

## Review-Schwerpunkte

- Überzogene oder unbelegte Implementierungs- und IFC-Aussagen.
- Trennung zwischen prototypisch implementiertem Missionsroundtrip und nicht belegtem allgemeinem IFC-Roundtrip.
- Trennung von Hierarchie und Ausführungsreihenfolge sowie von Objektbezug und Navigationsziel.
- Kennzeichnung der Aktionswerte und Property Sets als projektspezifische, versionierte Erweiterungen.
- Fehlende Grenzen, unklare Terminologie, Wiederholungen und Abweichungen von deutscher Wissenschaftssprache.
- LaTeX-Struktur, Abschnittsnummerierung, Label und Übergang zur folgenden Formalisierung.

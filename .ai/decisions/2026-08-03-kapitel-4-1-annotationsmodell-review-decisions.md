# Review-Entscheidungen: Kapitel 4.1 zum IFC-basierten Annotationsmodell

## CL-001

- **Status:** `ACCEPTED`
- **Deutsche Bezeichnung:** angenommen
- **Aussage des Reviewers:** Die Aussagen zu Vorbedingungen, Nachbedingungen, Fähigkeiten, Erfolgskriterien und einer Objektfähigkeitsannotation seien im Claim-Inventar nicht ausreichend als implementiert oder konzeptionell belegt.
- **Verifikation durch Codex:** Die Definition `RobotActionProperties` wurde am geprüften Viewer-Commit erneut kontrolliert. Die vier taskbezogenen Felder sind implementiert; eine allgemeine Fähigkeitsannotation am IFC-Objekt ist dagegen im Domänenmodell nicht implementiert und war nur als Möglichkeit gemeint.
- **Geprüfte Nachweise:** Viewer-Commit `674ede3bf2e7e6cf466bc4c16fe06c90fbb1753c`, `src/domain/robot-tasks/types.ts:86-106`, `src/ifc/robot-tasks/mapper.ts:131-214`, `docs/ai/CLAIM_POLICY.md`.
- **Begründung:** Das Finding trifft als Nachweis- und Reifegradproblem zu. Die implementierten Felder waren im Claim-Inventar zu grob belegt; die Fähigkeitsannotation musste ausdrücklich als konzeptionell gekennzeichnet werden.
- **Resultierende Maßnahme:** Fundstellen im Claim-Inventar ergänzt, Fähigkeitsannotation als konzeptionell vorgesehen formuliert und die vier Felder ausdrücklich dem prototypisch implementierten Domänenmodell zugeordnet.
- **Betroffene Dateien:** `inhalt/kapitel4_annotationsmodell.tex`, `.ai/tasks/2026-08-03-kapitel-4-1-annotationsmodell-claims.md`
- **Prüfkommando:** `rg -n "RobotActionProperties|requiredCapability|preconditions|postconditions|successCondition" src/domain/robot-tasks/types.ts`
- **Verbleibendes Risiko:** Die Viewer-Tests wurden in diesem Arbeitszyklus nicht ausgeführt; die Implementierungsevidenz beruht auf der Quell- und Testcodeprüfung am genannten Commit.

## CL-002

- **Status:** `ACCEPTED`
- **Deutsche Bezeichnung:** angenommen
- **Aussage des Reviewers:** Die Fehler-/Warnungsunterscheidung der Objektvalidierung und die Benennung eigener Property Sets ohne `Pset_` seien im Claim-Inventar nicht mit konkreten Fundstellen belegt.
- **Verifikation durch Codex:** Die Validierungsfunktion unterscheidet tatsächlich zwischen fehlender IFC-Klasseninformation als Warnung und einer bekannten, zur Aktion unzulässigen Klasse als Fehler. Die Projektanweisung und ein Mapper-Test legen eigene Property-Set-Namen ohne `Pset_` fest.
- **Geprüfte Nachweise:** Viewer-Commit `674ede3bf2e7e6cf466bc4c16fe06c90fbb1753c`, `src/domain/robot-tasks/validation.ts:125-151`, `AGENTS.md:401-415`, `test/robot-tasks/ifc-relation-mapper.test.ts:360-376`.
- **Begründung:** Die Aussagen sind inhaltlich belegt, das Claim-Inventar war jedoch unvollständig. Zudem war „Objektrollen“ für die implementierte Prüfung zu ungenau; geprüft werden IFC-Objektklassen.
- **Resultierende Maßnahme:** Konkrete Fundstellen ergänzt, den Text auf IFC-Objektklassen präzisiert und die `Pset_`-Regel als Festlegung dieser Arbeit statt als unbelegte allgemeine Standardaussage formuliert.
- **Betroffene Dateien:** `inhalt/kapitel4_annotationsmodell.tex`, `.ai/tasks/2026-08-03-kapitel-4-1-annotationsmodell-claims.md`
- **Prüfkommando:** `rg -n "TARGET_TYPE_UNKNOWN|TARGET_TYPE_MISMATCH|Pset_" src/domain/robot-tasks/validation.ts AGENTS.md test/robot-tasks/ifc-relation-mapper.test.ts`
- **Verbleibendes Risiko:** Die Aussage beschreibt nur die im Prototyp implementierten Tür- und Schalterklassenprüfungen, keine vollständige IFC-Typvalidierung.

## CL-003

- **Status:** `ACCEPTED`
- **Deutsche Bezeichnung:** angenommen
- **Aussage des Reviewers:** Die absolute Zählersetzung `\setcounter{section}{3}` sei fragil und müsse beim späteren Einfügen der Kapitel 2 und 3 ausdrücklich entfernt oder angepasst werden.
- **Verifikation durch Codex:** Das aktuelle Template enthält vor der neuen Datei nur die Abschnitte 1 und 2; ohne vorläufige Zählersetzung wäre der verlangte Unterabschnitt als 3.1 nummeriert. Die Datei `Kapitel 4 Notizen.md` bestätigt zugleich die Zielnummer 4.1 und die noch nicht integrierte Kapitelgliederung.
- **Geprüfte Nachweise:** `Abschlussarbeit.tex:114-131`, `inhalt/kapitel4_annotationsmodell.tex:1-4`, unveränderte Gliederungsnotiz `Kapitel 4 Notizen.md`.
- **Begründung:** Die Zählersetzung ist für den gegenwärtigen Aufgabenumfang notwendig, kann nach der Integration der fehlenden Kapitel jedoch zu einer falschen Nummerierung führen. Ein expliziter Entfernungshinweis reduziert dieses Wartungsrisiko.
- **Resultierende Maßnahme:** Kommentar um die eindeutige Anweisung ergänzt, die vorläufige Zählersetzung nach Integration der Kapitel 2 und 3 zu entfernen.
- **Betroffene Dateien:** `inhalt/kapitel4_annotationsmodell.tex`
- **Prüfkommando:** `rg -n "setcounter\{section\}|section\{|subsection\{" Abschlussarbeit.tex inhalt/kapitel4_annotationsmodell.tex`
- **Verbleibendes Risiko:** Bis zur Ergänzung der Kapitel 2 und 3 bleibt die Nummerierung bewusst durch einen absoluten Zählerwert abgesichert.

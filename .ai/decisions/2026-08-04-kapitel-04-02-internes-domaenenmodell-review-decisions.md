# Review-Entscheidungen: Kapitel 4.2 – Internes Domänenmodell

## CL-001

- **Status:** `ACCEPTED` (angenommen)
- **Verifikation:** `RobotObjectReference` enthält IFC-Identifikatoren und `ifcClass`; die Validierung verwendet bekannte IFC-Klassen.
- **Begründung und Maßnahme:** Die Trennung betrifft technische Laufzeiten, nicht die fachlichen IFC-Werte. Diese Grenze wurde im Text präzisiert, ohne eine nicht dokumentierte ADR zu behaupten.

## CL-002

- **Status:** `ACCEPTED` (angenommen)
- **Verifikation:** `tasks` und `sequences` sind getrennte Felder; die Ordnungsfunktion nutzt die Aufgabenreihenfolge als Tie-Breaker, während `setMissionTaskExecutionOrder` beide Strukturen gemeinsam ersetzt.
- **Begründung und Maßnahme:** Die Schlussfolgerung wurde auf die getrennten Felder gestützt und die Linearisierung als bewusst gekoppelte Operation beschrieben.

## CL-003

- **Status:** `ACCEPTED` (angenommen)
- **Verifikation:** Der Builder übernimmt einen optionalen Zeitplan; `validateMission` enthält keine eigene Zeitplanprüfung.
- **Begründung und Maßnahme:** Der Text nennt nun die Builder-Unterstützung und die fehlende Fachvalidierung.

## CL-004

- **Status:** `DEFERRED` (zurückgestellt)
- **Verifikation:** Die editierbare DOT-Quelle und die eingebundene PDF existieren. Die Versionierung lässt sich ohne den ausdrücklich untersagten Git-Einsatz weder prüfen noch durchführen.
- **Begründung und Maßnahme:** Keine Änderung an fremden, derzeit unversionierten Artefakten. Die Versionsaufnahme und der Reproduktionsnachweis bleiben vor einem späteren Commit offen.

## CL-005

- **Status:** `ACCEPTED` (angenommen)
- **Verifikation:** Der feste Verweis `Abschnitt~4.4` besitzt im aktuellen Kapitel kein Ziel-Label.
- **Begründung und Maßnahme:** Er wurde durch eine nummernfreie Vorausverweisung ersetzt.

## CL-006

- **Status:** `REJECTED` (abgelehnt)
- **Verifikation:** Die Aufgabendatei fordert ausdrücklich das Label `sec:internes-domaenenmodell`.
- **Begründung und Maßnahme:** Der geforderte stabile Labelname bleibt erhalten; eine Umbenennung würde den verbindlichen Aufgabenrahmen verletzen.

## CL-007

- **Status:** `ACCEPTED` (angenommen)
- **Verifikation:** Die Aktions- und Sequenzwerte sind TypeScript-Bezeichner, keine Pfade.
- **Begründung und Maßnahme:** Alle genannten Werte werden einheitlich mit `\texttt` und maskierten Unterstrichen gesetzt.

## CL-008

- **Status:** `ACCEPTED` (angenommen)
- **Verifikation:** `Abschlussarbeit.tex` erzeugt ein Abbildungsverzeichnis; vorhandene Beispielabbildungen verwenden Kurztitel.
- **Begründung und Maßnahme:** Die Abbildungsunterschrift erhielt ein Kurzargument.

## CL-009

- **Status:** `REJECTED` (abgelehnt)
- **Verifikation:** Vor Kapitel 4 existieren im Template die Abschnitte 1 und 2; die Datei dokumentiert direkt über `\setcounter{section}{3}` die vorläufige Zählung und deren spätere Entfernung.
- **Begründung und Maßnahme:** Die vom Finding verlangte Dokumentation ist bereits vorhanden. Das Anlegen weiterer Platzhalter liegt außerhalb des Auftrags.

## CL-010

- **Status:** `ACCEPTED` (angenommen)
- **Verifikation:** Builder und `addTaskSequence` erzwingen Regeln beim Ändern; `validateMission` prüft weitere Regeln erst bei explizitem Aufruf.
- **Begründung und Maßnahme:** Die Durchsetzungsorte und die Grenze nicht validierter Werte wurden getrennt beschrieben.

## CL-011

- **Status:** `ACCEPTED` (angenommen)
- **Verifikation:** Die Builder verwenden standardmäßig `new Date().toISOString()`, prüfen explizit übergebene Zeichenketten jedoch nicht; für `RobotTaskTime` existiert keine ISO-8601-Formatprüfung in der Domänenvalidierung.
- **Begründung und Maßnahme:** Der Text unterscheidet nun Standarderzeugung und nicht geprüfte Eingabewerte.

## CL-012

- **Status:** `ACCEPTED` (angenommen)
- **Verifikation:** `InMemoryRobotMissionRepository` und `LocalStorageRobotMissionRepository` implementieren beide den Repository-Port.
- **Begründung und Maßnahme:** Die überstarke allgemeine Behauptung wurde durch den konkreten Nachweis für diese beiden Adapter ersetzt.

## CL-013

- **Status:** `ACCEPTED` (angenommen)
- **Verifikation:** Die betroffenen Formulierungen beschreiben vorhandene Typfelder.
- **Begründung und Maßnahme:** „vorgesehen“ wurde dort durch „enthält“ ersetzt; die Kennzeichnung konzeptioneller Funktionalität in Abschnitt 4.1 bleibt unberührt.

## CL-014

- **Status:** `REJECTED` (abgelehnt)
- **Verifikation:** Die Aussage zu `IfcRelNests` und `IfcRelSequence` beschreibt das projektspezifische Mapping und nicht die normative Semantik der IFC-Spezifikation. Die vorhandenen Einträge können späteren Unterabschnitten dienen.
- **Begründung und Maßnahme:** Ohne konkrete normative Behauptung oder vorliegenden Belegbedarf werden keine Zitate ergänzt und keine fremden Bibliographieänderungen verschoben.

## CL-015

- **Status:** `ACCEPTED` (angenommen)
- **Verifikation:** Die Ordnungsfunktion sortiert verfügbare, gleichrangige Aufgaben nach ihrem Index in `tasks`.
- **Begründung und Maßnahme:** „Entscheidungshilfe“ wurde durch das präzisere nachrangige Ordnungskriterium mit deterministischem Ergebnis ersetzt.

## CL-016

- **Status:** `ACCEPTED` (angenommen)
- **Verifikation:** `RobotMissionService.deleteTask` entfernt alle Kanten, die die gelöschte Aufgabe als Vorgänger oder Nachfolger referenzieren.
- **Begründung und Maßnahme:** Diese Regel steht nun im Abschnitt zu Beziehungen; die Testaufzählung wurde entsprechend verkürzt.

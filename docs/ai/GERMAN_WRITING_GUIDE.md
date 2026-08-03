# Leitfaden für deutsche Wissenschaftssprache

Der vorhandene Repository-Stand ist ein deutschsprachiges LaTeX-Template und enthält noch keinen ausgearbeiteten fachlichen Haupttext. Deshalb gelten zunächst gegenwärtige deutsche Standardorthografie und ein formales, präzises, unpersönliches Register. Etablierte spätere Konventionen des Haupttexts haben Vorrang, sofern sie konsistent und wissenschaftlich angemessen sind.

## Register und Satzbau

- Aussagen präzise, überprüfbar und ohne werbende Zuspitzung formulieren.
- Pro Satz möglichst einen Hauptgedanken entwickeln. Lange Ketten aus Nebensätzen aufteilen, wenn Bezüge unklar werden.
- Pronomen nur verwenden, wenn ihr Bezug eindeutig ist.
- Unpersönliche Formulierungen wie „Die Untersuchung zeigt …“ oder „Im Folgenden wird … betrachtet“ sind zu bevorzugen. Die erste Person ist nur zu verwenden, wenn der spätere Haupttext sie konsistent für methodische Entscheidungen nutzt.
- Unsicherheit durch „deutet darauf hin“, „unter der Annahme“ oder „im untersuchten Fall“ kenntlich machen.

Zu vermeiden sind vage Wendungen wie „irgendwie“, „relativ gut“, „in gewisser Weise“, „problemlos“, „offensichtlich“ und „bekanntlich“, sofern sie nicht präzisiert werden. Werbliche Aussagen wie „revolutionär“, „einzigartig“, „nahtlos“, „vollständig“ oder „optimal“ sind ohne belastbaren Nachweis unzulässig.

## Technische Begriffe und Namen

Ein etablierter englischer Fachbegriff darf erhalten bleiben, wenn eine künstliche Übersetzung unpräzise wäre. Beim ersten Auftreten kann eine deutsche Einordnung folgen, beispielsweise „Surface Tiling (virtuelle Flächenunterteilung)“. Danach ist die in `TERMINOLOGY.md` festgelegte Form konsistent zu verwenden.

Standardisierte IFC-Klassennamen wie `IfcTask`, `IfcRelSequence`, `IfcRelAssignsToProcess` und `IfcPropertySet` werden in Maschinenschreibweise gesetzt und nicht übersetzt. Dasselbe gilt für Quellcodebezeichner. Produkt- und Frameworknamen behalten ihre offizielle Schreibweise; ihre Funktionen werden in deutschem Satzbau beschrieben.

Zusammensetzungen werden nach deutscher Orthografie verbunden: „IFC-Datei“, „Browseranwendung“, „Roboterexport“ und „Git-Commit“. Unübersichtliche Mehrwortverbindungen können mit Bindestrichen gegliedert werden. Englische Pluralformen sind nur zu verwenden, wenn sie fachlich etabliert sind.

## Abkürzungen

Nicht allgemein bekannte Abkürzungen werden beim ersten Auftreten ausgeschrieben und anschließend konsistent verwendet. IFC als etablierte Standardbezeichnung darf nach einer ersten fachlichen Einordnung verwendet werden. Bestehende LaTeX-Akronymbefehle sind beizubehalten. Abkürzungen dürfen nicht mehrere Bedeutungen tragen.

## Zitate und Belege

Direkte Zitate stehen in deutschen Anführungszeichen „…“ oder in der repositoryweit etablierten LaTeX-Form und benötigen eine genaue Fundstelle. Auslassungen und Ergänzungen werden kenntlich gemacht. Übersetzungen direkter Zitate werden ausdrücklich als eigene oder übernommene Übersetzung ausgewiesen. Indirekte Zitate werden ohne Anführungszeichen paraphrasiert und belegt. Titel, Zitate und Bibliografiemetadaten bleiben in ihrer Originalsprache.

## Abbildungen, Tabellen, Zahlen und Einheiten

Im Fließtext wird mit „Abbildung~\\ref{…}“ beziehungsweise „Tabelle~\\ref{…}“ auf nummerierte Elemente verwiesen. Abbildungen und Tabellen müssen im Text eingeordnet werden; ein bloßer Verweis „siehe unten“ genügt nicht. Bild- und Tabellenunterschriften sind knapp, sachlich und deutschsprachig, sofern kein unveränderter Originaltitel wiedergegeben wird.

Dezimalzahlen verwenden im deutschen Fließtext das Komma, etwa „2,5 m“. Zwischen Zahlenwert und Einheit steht ein geschütztes Leerzeichen, vorzugsweise über eine im Projekt etablierte LaTeX-Lösung. SI-Einheiten werden nicht flektiert. Punkte dienen als Tausendertrennzeichen nur, wenn keine Verwechslungsgefahr besteht.

## Gendergerechte Sprache

Der vorhandene Template-Text etabliert keine konsistente Genderkonvention. Deshalb wird keine neue typografische Konvention wie Sternchen, Doppelpunkt oder Binnen-I eingeführt. Personenbezeichnungen sind nach Möglichkeit neutral zu formulieren, etwa „Nutzende“ nur dann, wenn dies sprachlich natürlich ist, sonst „Personen, die …“. Sobald eine explizite Repository-Entscheidung vorliegt, ist sie einheitlich anzuwenden.

## Reifegrad von Funktionen

- **umgesetzt:** im referenzierten Code vorhanden und durch geeignete Prüfung belegt;
- **prototypisch umgesetzt:** lauffähig realisiert, aber erkennbar hinsichtlich Robustheit, Abdeckung oder Integration begrenzt;
- **konzeptionell vorgesehen:** Bestandteil eines dokumentierten Konzepts, noch nicht als Implementierung belegt;
- **vorgeschlagen:** mögliche Lösung ohne angenommene Architekturentscheidung;
- **nicht untersucht:** außerhalb der tatsächlich durchgeführten Untersuchung;
- **zukünftige Erweiterung:** bewusst auf spätere Arbeiten verschoben.

Unzulässig: „Der Viewer ermöglicht den vollständigen IFC-Roundtrip.“

Zulässig, wenn nur das Konzept beschrieben wird: „Für den Viewer ist ein vollständiger IFC-Roundtrip vorgesehen.“

Zulässig, wenn die Implementierung nachgewiesen wurde: „Der implementierte Import rekonstruiert die Missionsstruktur aus den annotierten IFC-Entitäten. Dies wird durch den Test … überprüft.“

Weiteres Beispiel: Statt „Die Software berechnet optimale Anfahrposen“ ist je nach Evidenz zu schreiben: „Der Prototyp erzeugt für die untersuchten Testfälle Anfahrposen nach dem in Abschnitt … beschriebenen Verfahren.“

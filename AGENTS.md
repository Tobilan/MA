# Arbeitsanweisungen für Codex

Vor jeder Arbeit an diesem Repository sind zuerst `docs/ai/THESIS_CONTRACT.md` und vor Änderungen am Fließtext zusätzlich `docs/ai/GERMAN_WRITING_GUIDE.md` vollständig zu lesen.

Codex ist der primäre Autor und alleinige Integrationsagent für die kanonischen Dateien der Masterarbeit. Dazu gehören insbesondere `.tex`- und `.bib`-Dateien, Glossare, Abkürzungsverzeichnisse sowie die LaTeX-Konfiguration. Claude ist standardmäßig ausschließlich als unabhängiger Reviewer einzusetzen.

- Halte Zeilen in `.tex`-Dateien grundsätzlich unter 150 Zeichen.
- Brich Fließtext semantisch sinnvoll um.
- Verändere durch Zeilenumbrüche nicht die LaTeX-Semantik.

## Verbindlicher Arbeitsablauf

1. Vor Änderungen Repository-Struktur, `git status`, Einstiegspunkt, Build-Konfiguration und einschlägige Projektanweisungen prüfen. Anschließend `python scripts/ai/preflight.py` ausführen; ohne erfolgreichen Preflight keine Schreibaufgabe beginnen.
2. Änderungen auf den erklärten Aufgabenumfang begrenzen und bestehende Konventionen bewahren.
3. Fließtext der Arbeit ausschließlich in formalem, wissenschaftlichem Deutsch verfassen.
4. Implementierungsbehauptungen anhand des tatsächlichen Codes und möglichst eines Git-Commits prüfen; wissenschaftliche Aussagen anhand geeigneter Primärquellen oder maßgeblicher Standards prüfen.
5. Keine Quellen, Zitate, Messwerte, APIs, IFC-Entitäten oder bibliografischen Angaben erfinden. Titel, Zitate und Bibliografiemetadaten nicht stillschweigend übersetzen.
6. Die Arbeit vor dem Claude-Review mit dem in `.ai/config.json` hinterlegten Befehl kompilieren und prüfen.
7. Claude-Findings niemals automatisch übernehmen. Jedes Finding anhand des Repositorys, der Implementierung, der zitierten Quelle oder einer dokumentierten Entscheidung verifizieren.
8. Für jedes Finding den Status `ACCEPTED`, `REJECTED` oder `DEFERRED` mit deutscher Begründung unter `.ai/decisions/` dokumentieren. Nur angenommene Änderungen umsetzen.
9. Nach angenommenen Änderungen erneut kompilieren und prüfen. Eine zusammenhängende logische Änderung entspricht grundsätzlich einem Commit. Untersagt der konkrete menschliche Auftrag einen Commit, gilt der dokumentierte `no_commit`-Modus; die Änderungen bleiben dann bewusst unversioniert.
10. Niemals automatisch pushen oder mergen. Vor dem Merge ist eine menschliche Freigabe erforderlich.

Claude darf angenommene Architekturentscheidungen beanstanden, aber Codex darf sie nur durch eine neue ADR ersetzen; die Historie in `docs/ai/ARCHITECTURE_DECISIONS.md` bleibt nachvollziehbar.

## Abschlussbericht

Der abschließende Bericht ist knapp und auf Deutsch zu verfassen. Er nennt mindestens geänderte Dateien, tatsächlich ausgeführte Prüfungen, Review-Entscheidungen, ungelöste Probleme und eine vorgeschlagene Commit-Nachricht. Nicht ausgeführte Prüfungen sind mit Grund zu nennen.

# Kapitel-Workflow mit Codex und Claude

## Vorbereitung

1. Feature-Branch für das Kapitel anlegen.
2. Aufgabendatei aus `.ai/tasks/TASK_TEMPLATE.md` erstellen.
3. In der Aufgabendatei folgende Punkte eintragen:
   - Ziel
   - Umfang
   - Zieldateien
   - Quellen
   - Akzeptanzkriterien
4. Benötigte Quellen und BibTeX-Einträge im Repository bereitstellen.
5. Codex mit dem Kapitelprompt ausführen und nur die relevanten Dateien bearbeiten lassen.
6. Ersten Entwurf und Git-Diff kurz manuell prüfen.


## Modellauswahl

| Aufgabe | Modell | Reasoning-Aufwand |
|---|---|---|
| Erster Kapitelentwurf | Terra | Medium |
| Claude-Review | Claude außerhalb von Codex | Read-only |
| Klare Review-Korrekturen | Terra | Medium |
| Kleine mechanische Arbeiten | Luna | Low |
| Schwierige fachliche Fragen | Sol | High |
| Max/Ultra | Nur in Ausnahmefällen | Nach Bedarf |

## Prompt 1 ausführen (Kapitelerstellung)
[file](1_kapitelprompt.md)

## Vollständigen Vorab-Workflow starten

```bash
python scripts/ai/run_ai_workflow.py pre-review --task .ai/tasks/<aufgabe>.md
```

## Prompt 2 ausführen (Claude-Findings verifizieren)
[file](2_reviewprompt.md)


## Abschlussprüfung starten

```bash
python scripts/ai/run_ai_workflow.py post-review
```

## Manuelle Endkontrolle

Vor dem Abschluss sind folgende Punkte manuell zu kontrollieren:

- finales PDF
- Quellen
- Zitate
- Terminologie
- Git-Diff

## Abschluss

1. Commit erstellen.
2. Branch pushen.
3. Pull Request öffnen.
4. Kapitel fachlich selbst freigeben.
5. Pull Request mergen.

## Rollenverteilung

Der Workflow sieht ausdrücklich folgende Rollenverteilung vor:

- **Codex schreibt und überarbeitet.**
- **Claude prüft ausschließlich.**
- **Die fachliche Freigabe vor dem Merge erfolgt durch dich.**



# Modelleinsatz im Kapitel-Workflow

## Empfohlene Zuordnung

| Aufgabe | Modell | Reasoning-Aufwand |
|---|---|---|
| Erster Kapitelentwurf | Terra | Medium |
| Claude-Review | Claude außerhalb von Codex | Read-only |
| Klare Review-Korrekturen | Terra | Medium |
| Kleine mechanische Arbeiten | Luna | Low |
| Schwierige fachliche Fragen | Sol | High |
| Max/Ultra | Nur in Ausnahmefällen | Nach Bedarf |

## Einsatz nach Arbeitsschritt

### Erster Kapitelentwurf

**Terra + Medium**

Terra erstellt den vollständigen ersten Entwurf des Kapitels.

### Wissenschaftliches Review

**Claude außerhalb von Codex**

Claude führt ein wissenschaftliches Read-only-Review durch. Das Review wird außerhalb von Codex gestartet. Claude prüft den Entwurf, nimmt jedoch selbst keine Änderungen an den Dateien vor.

### Akzeptierte inhaltliche Korrekturen

**Terra + Low oder Medium**

Terra setzt die akzeptierten inhaltlichen Korrekturen aus dem Review um. Der Reasoning-Aufwand richtet sich nach Umfang und Komplexität der Änderungen.

### Mechanische Korrekturen

**Luna + Low**

Luna übernimmt ausschließlich kleine, klar abgegrenzte und mechanische Arbeiten, insbesondere:

- LaTeX-Korrekturen
- Formatierungsanpassungen
- Rechtschreibkorrekturen

### Schwierige fachliche Fragen

**Sol + High**

Sol wird nur bei anspruchsvollen fachlichen Problemen eingesetzt, insbesondere bei:

- schwierigen fachlichen Widersprüchen
- kritischen Architekturbehauptungen
- komplexen Abwägungen, die eine vertiefte Prüfung erfordern

## Einsatz von Max oder Ultra

**Max** und **Ultra** sollen nur in begründeten Ausnahmefällen verwendet werden, wenn die Aufgabe mit den vorgesehenen Standardmodellen nicht zuverlässig gelöst werden kann.

# GitHub-Einrichtung für menschliche Freigabe

Repository-Dateien allein können eine menschliche Freigabe vor dem Merge nicht erzwingen. Dafür ist auf GitHub ein Branch-Protection-Rule oder vorzugsweise ein Repository-Ruleset für den Standardbranch erforderlich. Die Bezeichnungen in der Oberfläche können sich ändern; die folgenden Einstellungen sind sinngemäß anzuwenden.

## Empfohlene Einrichtung

1. In den Repository-Einstellungen „Rules“ beziehungsweise „Rulesets“ öffnen.
2. Ein aktives Branch-Ruleset für den Standardbranch, beispielsweise `main`, anlegen.
3. Pull Requests vor Änderungen am geschützten Branch verpflichtend machen.
4. Mindestens eine genehmigende Reviewentscheidung verlangen.
5. Veraltete Freigaben bei neuen Commits verwerfen und die Lösung aller Review-Konversationen verlangen.
6. Sofern eine CI eingerichtet wird, den Thesis-Build und die Review-Validierung als erforderliche Statusprüfungen auswählen.
7. Direkte Pushes, Force-Pushes und Branch-Löschung einschränken; Ausnahmen nur ausdrücklich benannten administrativen Rollen gewähren.
8. Regeln speichern, ihre Ziel-Branch-Auswahl kontrollieren und mit einem Test-Pull-Request überprüfen.

Die konkrete Zahl erforderlicher Freigaben und zulässige Bypass-Rollen sind organisatorisch festzulegen. Dieses Repository nimmt keinen Benutzernamen und keine Organisation an. Das Pull-Request-Template dokumentiert den Prozess, ersetzt aber keine serverseitige Regel.

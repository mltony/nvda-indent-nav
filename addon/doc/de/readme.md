# IndentNav #

Mit dieser NVDA-Erweiterung können Benutzer nach der Einrückungsebene von
Zeilen navigieren.  Bei der Bearbeitung von Quellcode in vielen
Programmiersprachen ermöglicht es, zwischen den Zeilen der gleichen
Einrückungsebene zu springen und schnell Zeilen mit größerer oder kleinerer
Einrückungsebene zu finden.  Ähnliche Tastenkombinationen sind auch in
Baumansichten möglich.

Bitte beachten Sie, dass die Befehle zur Baumnavigation in die
NVDA-Erweiterung [TreeNav](https://github.com/mltony/nvda-tree-nav)
verschoben wurden.

## Download
Bitte aus dem Store für NVDA-Erweiterungen  installieren

## Hinweis zur Kompatibilität mit VSCode

Die in VSCode eingebaute Barrierefreiheit ist sehr begrenzt: Seit 2024
werden nur 500 Zeilen Code über die API der Barrierefreiheit zugänglich
gemacht, was dazu führt, dass IndentNav in VSCode nicht korrekt
funktioniert.

Standardmäßig funktioniert IndentNav nicht mit VSCode und wenn Sie
versuchen, es zu verwenden, müssen Sie zwischen zwei Optionen wählen:

* Installieren Sie die VSCode-Erweiterung ([von der
  Seite](https://marketplace.visualstudio.com/items?itemName=TonyMalykh.nvda-indent-nav-accessibility))([Quellcode](https://github.com/mltony/vscode-nvda-indent-nav-accessibility))
  - empfohlener Weg. Nach der Installation der Erweiterung ist NVDA in der
  Lage, auf das gesamte Dokument zuzugreifen, egal wie groß es ist.
* Verwenden Sie VSCode weiterhin im Legacy-Modus - aktivieren Sie diesen
  Modus in den IndentNav-Einstellungen. Dies wird nicht empfohlen, da NVDA
  nur 500 Zeilen des Dokuments sieht und fälschlicherweise fehlende Einträge
  in der Hierarchie mitteilt.

## Kompatibilitätsprobleme

IndentNav hat bekannte Kompatibilitätsprobleme mit der NVDA-Erweiterung
[Zeichen-Informationen](https://addons.nvda-project.org/addons/charInfo.en.html).
Es ist derzeit nicht möglich, sowohl IndentNav als auch den Prüfcursor auf
dem Ziffernblock zu konfigurieren, während dieser NVDA-Erweiterung
läuft. Bitte deinstallieren Sie entweder sie es oder verwenden Sie eine
alternative Tastaturbelegung in IndentNav.

## Layouts der Tastenbefehle

IndentNav bietet drei eingebaute Tastenzuordnungen:

* Legacy- oder Laptop-Layout: Dies ist für diejenigen, die IndentNav V1.x
  benutzt haben und keine neuen Layouts lernen wollen oder für
  Laptop-Tastaturen, die keine Zifferntasten haben.
* Alt+Nummernblock-Layout.
* Layout der Nummernblock-Tasten. Es gibt zwei Möglichkeiten, mit Konflikten
  bei der Überprüfung der Cursor-Tasten umzugehen:

    * Verwenden Sie den Nummernblock für IndentNav in Eingabefeldern und den
      NVDA-Cursor überall sonst. Wenn Sie ihn in Dateien zum Bearbeiten
      trotzdem verwenden müssen, können Sie IndentNav vorübergehend
      deaktivieren, indem Sie die Tastenkombination `Alt+Nummernblock-Taste`
      drücken.
    * Die Befehle für den Cursor werden auf Alt+Nummernblock umgestellt,
      wodurch Tastenkonflikte vermieden werden.

Das Tasten-Layout kann in den IndentNav-Einstellungen ausgewählt werden.

## Tastenbefehle

| Aktion | Legacy-Layout | `Alt+Nummernblock`-Layout | Nummernblock-Layout | Beschreibung |
| -- | -- | -- | -- | -- |
| IndentNav umschalten | `Alt+Nummernblock` | `Alt+Nummernblock` | `Alt+Nummernblock` | Dies ist nützlich, wenn sowohl NVDA- als auch Tastenbefehle für Cursor dem Nummernblock zugewiesen sind. |
| Jump to previous/next sibling | `NVDA+Alt+Pfeiltasten nach oben/unten` | `Alt+Nummernblock-Taste 8/2` | `Nummernblock-Taste 8/2` | Sibling is defined as a line with the same indentation level.<br>This command will not take cursor beyond current code block. |
| Jump to previous/next sibling skipping over clutter | Keine | `Strg+Alt+Nummernblock-Taste 8/2` | `Strg+Nummernblock-Taste 8/2` | You can configure clutter regular expression in settings. |
| Jump to first/last sibling | `NVDA+Alt+Umschalt+Pfeiltasten nach oben/unten` | `Alt+Nummernblock-Taste 4/6` | `Nummernblock-Taste 4/6` | Sibling is defined as a line with the same indentation level.<br>This command will not take cursor beyond current code block. |
| Jump to previous/last sibling potentially outside of current block | `NVDA+Strg+Alt+Pfeiltasten nach oben/unten` | `Strg+Alt+Nummernblock-Taste 4/6` | `Strg+Nummernblock-Taste 4/6` | This command allows you to jump to a sibling in another block. |
| Jump to previous/next parent | `NVDA+Alt+Pfeiltaste nach links`,<br>`NVDA+Alt+Strg+Pfeiltaste nach links` | `Alt+Nummernblock-Taste 7/1` | `Nummernblock-Taste 7/1` | Parent is defined as a line with lower indentation level. |
| Jump to previous/next child | `NVDA+Alt+Strg+Pfeiltaste nach rechts`,<br>`NVDA+Alt+Pfeiltaste nach rechts` | `Alt+Nummernblock-Taste 9/3` | `Nummernblock-Taste 9/3` | Child is defined as a line with greater indentation level.<br>This command will not take cursor beyond current code block. |
| Select current block | `NVDA+Strg+I` | `Strg+Alt+Nummernblock-Taste 7` | `Strg+Nummernblock-Taste 7` | Selects current line plus all following lines having strictly greater indentation level.<br>Press repeatedly to select multiple blocks. |
| Select current block and all following blocks on the same indentation level | `NVDA+Alt+I` | `Strg+Alt+Nummernblock-Taste 9` | `Strg+Nummernblock-Taste 9` | Selects current line plus all following lines having  greater or equal indentation level. |
| Indent-paste | `NVDA+V` | `NVDA+V` | `NVDA+V` | When you need to paste a block of code to a place with different indentation level, this command will adjust indentation level before pasting. |
| Weiter/Zurück im Verlauf | N/A | `Strg+Alt+Nummernblock-Taste 1/3` | `Strg+Nummernblock-Taste 1/3` | IndentNav speichert einen Verlauf der Zeilen, die Sie mit IndentNav-Befehlen besucht haben. |
| Aktuelle Zeile mitteilen | Keine | `Alt+Nummernblock-Taste 5` | `Nummernblock-Taste 5` | Dies ist in Wirklichkeit ein Cursor-Befehl, der der Einfachheit halber neu zugeordnet wurde. |
| Übergeordnete Zeile mitteilen | `NVDA+I` | Keine | Keine | |

## Weitere Features

### Lesezeichen für die Schnellsuche

Mit IndentNav können Sie eine beliebige Anzahl von Lesezeichen
konfigurieren, zu denen Sie einfach springen können. Ein Lesezeichen wird
durch einen regulären Ausdruck und eine benutzerdefinierte Tastenkombination
definiert, um zu einer Übereinstimmung zu springen. Drücken Sie die
Tastenkombination "Umschalt+", um das vorherige Vorkommen zu finden.

### Knack-Geräusche:

Beim Überspringen vieler Code-Zeilen versucht IndentNav, die
Einrückungsebenen schnell als Töne der übersprungenen Zeilen
wiederzugeben. Diese Funktion ist nur aktiviert, wenn in den
NVDA-Einstellungen die Option Einrückung als Töne wiedergeben aktiviert
ist. Die Lautstärke des Knackens kann in den IndentNav-Einstellungen
angepasst oder deaktiviert werden.

## Quellcode

Der Quellcode ist verfügbar unter
<http://github.com/mltony/nvda-indent-nav>.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=indentnav

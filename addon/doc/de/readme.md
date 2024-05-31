# IndentNav #

Mit dieser NVDA-Erweiterung können Benutzer nach der Einrückungsebene von
Zeilen navigieren.  Bei der Bearbeitung von Quellcode in vielen
Programmiersprachen ermöglicht es, zwischen den Zeilen der gleichen
Einrückungsebene zu springen und schnell Zeilen mit größerer oder kleinerer
Einrückungsebene zu finden.  Ähnliche Tastenkombinationen sind auch in
Baumansichten möglich.

Please note that tree navigation commands have been moved to [TreeNav
add-on](https://github.com/mltony/nvda-tree-nav).

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

## Keystroke layouts

IndentNav bietet drei eingebaute Tastenzuordnungen:

* Legacy- oder Laptop-Layout: Dies ist für diejenigen, die IndentNav V1.x
  benutzt haben und keine neuen Layouts lernen wollen oder für
  Laptop-Tastaturen, die keine Zifferntasten haben.
* Alt+numpad layout.
* Numpad keys layout. There are two modes of dealing with review cursor
  keystroke conflict:

    * Verwenden Sie den Nummernblock für IndentNav in Eingabefeldern und den
      NVDA-Cursor überall sonst. Wenn Sie ihn in Dateien zum Bearbeiten
      trotzdem verwenden müssen, können Sie IndentNav vorübergehend
      deaktivieren, indem Sie die Tastenkombination `Alt+Nummernblock-Taste`
      drücken.
    * Remap review cursor commands to alt+numpad, thus avoiding keystroke
      conflict.

Keystroke layout can be selected in IndentNav settings.

## Keystrokes

| Action | Legacy layout | `Alt+numpad` layout | Numpad layout | Description |
| -- | -- | -- | -- | -- |
| Toggle IndentNav | `alt+numLock` | `alt+numLock` | `alt+numLock` | This is useful when both NVDA and review cursor gestures are assigned to numPad. |
| Jump to previous/next sibling | `NVDA+Alt+up/downArrow` | `alt+numPad8/numPad2` | `numPad8/numPad2` | Sibling is defined as a line with the same indentation level.<br>This command will not take cursor beyond current code block. |
| Jump to previous/next sibling skipping over clutter | N/A | `control+alt+numPad8/numPad2` | `control+numPad8/numPad2` | You can configure clutter regular expression in settings. |
| Jump to first/last sibling | `NVDA+Alt+shift+up/downArrow` | `alt+numPad4/numPad6` | `numPad4/numPad6` | Sibling is defined as a line with the same indentation level.<br>This command will not take cursor beyond current code block. |
| Jump to previous/last sibling potentially outside of current block | `NVDA+control+Alt+up/downArrow` | `control+alt+numPad4/numPad6` | `control+numPad4/numPad6` | This command allows you to jump to a sibling in another block. |
| Jump to previous/next parent | `NVDA+Alt+leftArrow`,<br>`NVDA+alt+control+leftArrow` | `alt+numPad7/numPad1` | `numPad7/numPad1` | Parent is defined as a line with lower indentation level. |
| Jump to previous/next child | `NVDA+Alt+control+rightArrow`,<br>`NVDA+alt+rightArrow` | `alt+numPad9/numPad3` | `numPad9/numPad3` | Child is defined as a line with greater indentation level.<br>This command will not take cursor beyond current code block. |
| Select current block | `NVDA+control+i` | `control+alt+numPad7` | `control+numPad7` | Selects current line plus all following lines having strictly greater indentation level.<br>Press repeatedly to select multiple blocks. |
| Select current block and all following blocks on the same indentation level | `NVDA+alt+i` | `control+alt+numPad9` | `control+numPad9` | Selects current line plus all following lines having  greater or equal indentation level. |
| Indent-paste | `NVDA+v` | `NVDA+v` | `NVDA+v` | When you need to paste a block of code to a place with different indentation level, this command will adjust indentation level before pasting. |
| Go back/forward in history | N/A | `control+alt+numPad1/numPad3` | `control+numPad1/numPad3` | IndentNav keeps a history of lines which you visited via IndentNav commands. |
| Speak current line | N/A | `alt+numPad5` | `numPad5` | This is really a review cursor command remapped for convenience. |
| Speak parent line | `NVDA+i` | N/A | N/A | |

## Weitere Features

### Lesezeichen für die Schnellsuche

IndentNav allows you to configure any number of bookmarks that you can
easily jump to. A bookmark is defined by a regular expression and a custom
keystroke to jump to a match. Press `shift+` keystroke to find previous
occurrence.

### Crackling:

When jumping over many lines of code, IndentNav will try to quickly play
indentation levels as tones of the lines skipped over. This feature is only
enabled when report indentation as tones is turned on in NVDA
settings. Crackling volume can be adjusted or disabled in IndentNav
settings.

## Quellcode

Der Quellcode ist verfügbar unter
<http://github.com/mltony/nvda-indent-nav>.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=indentnav

# IndentNav addon for NVDA
This addon allows NVDA users to navigate by indentation level of lines.
While editing source code in many programming languages, it allows to jump between the lines of the same indentation level, as well as quickly find lines with greater or lesser indentation level.
It also provides similar keystrokes in tree views.

## Download
Please install from NVDA add-on store

## Note on compatibility with VSCode

Builtin VSCode accessibility is very limited: as of 2024 it only exposes 500 lines of code through accessibility API, which makes IndentNav to work incorrectly in VSCode.

By default IndentNav won't work with VSCode and when you try to use it, you will need to select from two options:

* Install VSCode extension ([extension page](https://marketplace.visualstudio.com/items?itemName=TonyMalykh.nvda-indent-nav-accessibility))([source code](https://github.com/mltony/vscode-nvda-indent-nav-accessibility)) - recommended way. After installing extension NVDA will be able to access entire document no matter how large it is.
* Continue using VSCode in legacy mode - enable this mode in IndentNav settings. This is not recommended since NVDA will only see 500 lines of document and will erroneously report missing siblings/parents.

## Compatibility issues

IndentNav has known compatibility issues with [Character Information add-on](https://addons.nvda-project.org/addons/charInfo.en.html). It is currently impossible to configure both IndentNav and review cursor on numpad while this add-on is running. Please either uninstall this add-on, or use an alternative keystroke map in IndentNav.

## Keystroke layouts

IndentNav offers 3 builtin  keystroke mappings:

* Legacy or laptop layout: this is for people who were using IndentNav v1.x and don't want to learn new layouts or for laptop keyboards that don;t have numpads.
* Alt+numpad layout.
* Numpad keys layout. There are two modes of dealing with review cursor keystroke conflict:
    * Use numpad for IndentNav in editables and review cursor everywhere else. If you still need to use review cursor in editables, you can temporarily disable IndentNav by pressing `alt+numLock`.
    * Remap review cursor commands to alt+numpad, thus avoiding keystroke conflict.

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

## Other features

### QuickFind bookmarks

IndentNav allows you to configure any number of bookmarks that you can easily jump to. A bookmark is defined by a regular expression and a custom keystroke to jump to a match. Press `shift+` keystroke to find previous occurrence.

### Crackling:

When jumping over many lines of code, IndentNav will try to quickly play indentation levels as tones of the lines skipped over. This feature is only enabled when report indentation as tones is turned on in NVDA settings. Crackling volume can be adjusted or disabled in IndentNav settings.

## Source code

Source code is available at <http://github.com/mltony/nvda-indent-nav>.

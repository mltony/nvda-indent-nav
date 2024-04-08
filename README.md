# IndentNav addon for NVDA
This addon allows NVDA users to navigate by indentation level or offset of lines.
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

IndentNav has compatibility issues with [Character Information add-on](https://addons.nvda-project.org/addons/charInfo.en.html). It is currently impossible to configure both IndentNav and review cursor on numpad while this add-on is running. Please either uninstall this add-on, or use an alternative keystroke map in IndentNav.

## Keystroke layouts

IndentNav offers 3 builtin  keystroke mappings:

* Legacy or laptop layout: this is for people who were using IndentNav v1.x and don't want to learn new layouts or for laptop keyboards that don;t have numpads.
* Alt+numpad layout.
* Numpad keys layout. There are two modes of dealing with review cursor keystroke conflict:
    * Use numpad for IndentNav in editables and review cursor everywhere else. If you still need to use review cursor in editables, you can temporarily disable IndentNav by pressing `alt+numLock`.
    * Remap review cursor commands to alt+numpad, thus avoiding keystroke conflict.
    
## Keystrokes

| Action | Legacy layout | `Alt+numpad` layout | Numpad layout |
| -- | -- | -- | -- |
| Toggle IndentNav | `alt+numLock` | `alt+numLock` | `alt+numLock` |
| Jump to next/previous sibling | `NVDA+Alt+Down/UpArrow` | `alt+numPad2/numPad8` | `numPad2/numPad8` |

## Usage 
IndentNav can  be useful for editing source code in many programming languages. 
Languages like Python require the source code to be properly indented, while in many other programming languages it is strongly recommended.
With IndentNav you can press NVDA+Alt+DownArrow or UpArrow to jump to next or previous line with the same indentation level.
You can also press NVDA+Alt+LeftArrow to jump to a parent line, that is a previous line with lower indentation level.
In Python you can easily find current function definition or class definition.
You can also press NVDA+Alt+RightArrow to go to the first child of current line, that is next line with greater indentation level.

If your NVDA is set to express line indentation as tones, then IndentNav will quickly play the tones of all the skipped lines.
Otherwise it will only crackle to roughly denote the number of skipped lines.

IndentNav also works in tree views.

Keystrokes:

* NVDA+Alt+UpArrow or DownArrow: Jump to previous or next line with the same indentation level within the current indentation block.
* NVDA+Alt+Control+UpArrow or DownArrow: Force-jump to previous or next line with the same indentation level. This command will jump to other indentation blocks (such as other Python functions) if necessary.
* NVDA+Alt+Shift+UpArrow or DownArrow: Jump to first or last line with the same indentation level within the current indentation block.
* NVDA+alt+LeftArrow: Jump to parent - that is previous line with lesser indentation level.
* NVDA+control+alt+LeftArrow: Jump to next parent - that is next line with lesser indentation level.
* NVDA+Alt+RightArrow: Jump to first child - that is next line with greater indentation level within the same indentation block.
* NVDA+control+Alt+RightArrow: Jump to previous  child - that is previous line with greater indentation level within the same indentation block.
* NVDA+I: Announce parent line without moving the cursor there. Press twice or multiple times to query second level or further level parent.
* NVDA+control+I: Select current indentation block. Press repeatedly to select multiple indentation blocks.
* NVDA+Alt+I: Select current indentation block and all the following indentation blocks on the same level. Press twice to copy to clipboard.
* NVDA+V: Indent paste, that is first reindent current clipboard text to match indentation level of current file and then paste.

## Known issues
* IndentNav doesn't  support VSCode at this time. Due to its internal optimizations, VSCode doesn't load the entire document in the editable control, which makes it impossible to find lines far from current line.  
  Please use [IndentNav VSCode extension](https://github.com/mltony/vscode-indent-nav/) instead.
  Or alternatively, please consider using [Indentation Level Movement](https://marketplace.visualstudio.com/items?itemName=kaiwood.indentation-level-movement) VSCode extension instead.
* Experimental VSCode support has been added in vscode branch, but at this time it doesn't work well enough.

## Source code
Source code is available at <http://github.com/mltony/nvda-indent-nav>.

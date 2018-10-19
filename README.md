# IndentNav addon for NVDA
This addon allows NVDA users to navigate by indentation level or offset of lines or paragraphs.
In browsers it allows to quickly find paragraphs with the same offset from the left edge of the screen, such as first level comments in a hierarchical tree of comments.
Also while editing source code in many programming languages, it allows to jump between the lines of the same indentation level, as well as quickly find lines with greater or lesser indentation level.
## Download
Current stable release: [IndentNav v1.3](https://github.com/mltony/nvda-indent-nav/releases/download/v1.3/IndentNav-1.3.nvda-addon)

## Usage in browsers
IndentNav can be used to navigate by  offset from the left edge of the screen. 
IN particular, you can press NVDA+Alt+DownArrow or UpArrow to jump to the next or previous paragraph that has the same offset. 
For example, this can be useful when browsing hierarchical trees of comments (e.g. on reddit.com) to jump between  first level comments and skipping all the higher level comments.

Strictly speaking, IndentNav can be used in any application, for which NVDA provides a tree interceptor object.

Keystrokes:

* NVDA+Alt+UpArrow or DownArrow: Jump to previous or next paragraph with the same offset.
* NVDA+alt+LeftArrow: Jump to previous paragraph with lesser offset.
* NVDA+Alt+RightArrow: Jump to next paragraph with greater offset.

## Usage in text editors
IndentNav can also be useful for editing source code in many programming languages. 
Languages like Python require the source code to be properly indented, while in many other programming languages it is strongly recommended.
With IndentNav you can press NVDA+Alt+DownArrow or UpArrow to jump to next or previous line with the same indentation level.
You can also press NVDA+Alt+LeftArrow to jump to a parent line, that is a previous line with lower indentation level.
In Python you can easily find current function definition or class definition.
You can also press NVDA+Alt+RightArrow to go to the first child of current line, that is next line with greater indentation level.

If your NVDA is set to express line indentation as tones, then IndentNav will quickly play the tones of all the skipped lines.
Otherwise it will only crackle to roughly denote the number of skipped lines.

Keystrokes:

* NVDA+Alt+UpArrow or DownArrow: Jump to previous or next line with the same indentation level within the current indetnation block.
* NVDA+Alt+Control+UpArrow or DownArrow: Force-jump to previous or next line with the same indentation level. This command will jump to other indentation blocks (such as other Python functions) if necessary.
* NVDA+alt+LeftArrow: Jump to parent - that is previous line with lesser indentation level.
* NVDA+Alt+RightArrow: Jump to first child - that is next line with greater indentation level within the same indentation block.

## Known issues
* IndentNav doesn't  support VSCode at this time. Due to its internal optimizations, VSCode doesn't load the entire document in the editable control, which makes it impossible to find lines far from current line.  
  Please consider using [Indentation Level Movement](https://marketplace.visualstudio.com/items?itemName=kaiwood.indentation-level-movement) VSCode extension instead.

## Release history
* [v1.3](https://github.com/mltony/nvda-indent-nav/releases/download/v1.3/IndentNav-1.3.nvda-addon)
  * French translation.
  * Bugfixes.
* [v1.2](https://github.com/mltony/nvda-indent-nav/releases/download/v1.2/IndentNav-1.2.nvda-addon)
  * Added support for i18n.
  * Added GPL headers in the source files.
  * Minor fixes.
* v1.1
  * Initial release.

## Source code
Source code is available at <http://github.com/mltony/nvda-indent-nav>.

## Feedback
If you have any questions or comments, or if you find this addon useful, please don't hesitate to contact me at anton.malykh *at* gmail.com.

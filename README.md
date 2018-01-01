# IndentNav addon for NVDA
This addon allows NVDA users to navigate by indentation level or offset of lines or paragraphs.
In browsers it allows to quickly find paragraphs with the same offset from the left edge of the screen, such as first level comments in a hierarchical tree of comments.
Also while editing source code in many programming languages, it allows to jump between the lines of the same indentation level, as well as quickly find lines with greater or lesser indentation level.
## Download
TBB
## Usage in browsers
IndentNav can be used to navigate by  offset from the left edge of the screen. 
IN particular, you can press NVDA+Alt+DownArrow or UpArrow to jump to the next or previous paragraph that has the same offset. 
For example, this can be useful when browsing hierarchical trees of comments (e.g. on reddit.com) to jump between  first level comments and skipping all the higher level comments.

Strictly speaking, IndentNav can be used in any application, for which NVDA provides a tree interceptor object.
## Usage in text editors
IndentNav can also be useful for editing source code in many programming languages. 
Languages like Python require the source code to be properly indented, while in many other programming languages it is strongly recommended.
With IndentNav you can press NVDA+Alt+DownArrow or UpArrow to jump to next or previous line with the same indentation level.
You can also press NVDA+Alt+LeftArrow to jump to a parent line, that is a previous line with lower indentation level.
In Python you can easily find current function definition or class definition.
You can also press NVDA+Alt+RightArrow to go to the first child of current line, that is next line with greater indentation level.

If your NVDA is set to express line indentation as tones, then IndentNav will quickly play the tones of all the skipped lines.
Otherwise it will only crackle to roughly denote the number of skipped lines.

## Keyboard shortcuts
| Keystroke | Action in browser mode | Action in editor mode |
| -- | -- | -- |
| NVDA+Alt+UpArrow or DownArrow | Jump to previous or next paragraph with the same offset. | Jump to previous or next line with the same indentation level within the current indetnation block. |
## Feedback
If you have any questions or comments, or if you find this addon useful, please don't hesitate to contact me at anton.malykh /at/ gmail.com.

# IndentNav-缩进导航 #

缩进导航插件。可以让 NVDA
用户通过行或段落的缩进级别或偏移量进行导航。在浏览器中，使用该插件可以快速导航距屏幕左边缘具有相同偏移量的段落，例如在具有层级结构的帖子评论区，您可以仅导航同级的评论。此外，在编程开发中，该插件可以用来快速在相同缩进级别的行之间跳转，以及快速跳转到具有更大或更小缩进级别的行。

请注意，树式图导航特性已移至 [TreeNav 插件](https://github.com/mltony/nvda-tree-nav)。

## 下载
请从 NVDA 插件商店安装最新版

## 与 VSCode 兼容的注意事项

VSCode 内置的辅助功能 API 仅能访问到500行代码。因此，在较大的文件中，IndentNav 则无法正常工作。

默认情况下本插件无法兼容 VSCode，如果您希望在 VSCode 中使用本插件，您需要从两个方案中做出选择：

* 安装 VSCode
  ([辅助功能扩展](https://marketplace.visualstudio.com/items?itemName=TonyMalykh.nvda-indent-nav-accessibility))
  ([源代码](https://github.com/mltony/
  vscode-nvda-indent-nav-accessibility))——这是推荐的方案。安装扩展后，无论文档有多大，NVDA
  都能够访问整个文档。
* 继续使用 VSCode 旧版模式——在 缩进导航的设置中启用此模式。不建议这样做，因为 NVDA 只能访问 500
  行文档，浙将导致缩进导航错误的识别兄弟/父子节点。

## 兼容性问题

缩进导航与[角色信息-charInfo插件](https://addons.nvda-project.org/addons/charInfo.en.html)
存在已知的兼容性问题。目前无法在启用该插件的情况下同时启用缩进导航的数字键盘布局。请卸载此插件，或在 IndentNav 中使用其他的按键布局。

## 按键布局

缩进导航提供了 3 种内置按键布局：

* 笔记本或旧版按键布局：该布局适用于习惯了缩进导航1.x且不想学习新布局的老用户，以及没有数字键盘的笔记本用户。
* Alt+数字键盘布局。
* 数字键盘按键布局。有两种处理与 NVDA 文本查看快捷键冲突的模式：

    * 数字键盘在可编辑区域作为缩进导航命令；在其他地方恢复对象文本查看命令。在编辑区域也可以按 NVDA+数字键盘锁定键临时开关缩进导航。
    * 将文本查看快捷键映射为 alt+数字键盘，从而避免与 NVDA 本身的快捷键冲突。

可以在缩进导航设置中选择适合您的按键布局。

## 快捷键

| 动作 | 传统布局 | `Alt+数字键盘` 布局 | 数字键盘布局 | 描述 |
| -- | -- | -- | -- | -- |
| 开关缩进导航 | `alt+numLock` | `alt+numLock` | `alt+numLock` | 若将缩进导航和文本查看手势同时分配给数字键盘时很有用。 |
| 跳转到上一个/下一个兄弟节点 | `NVDA+Alt+上/下箭头` | `alt+numPad8/numPad2` | `numPad8/numPad2` | 兄弟节点定义为具有相同缩进级别的行。该命令不会将光标移出当前代码块。 |
| 跳过若干杂项到上一个/下一个兄弟节点 | N/A | `control+alt+numPad8/numPad2` | `control+numPad8/numPad2` | 可以在设置中定义跳转的正则表达式。 |
| 跳转到第一个/最后一个兄弟节点 | `NVDA+Alt+shift+上/下箭头` | `alt+numPad4/numPad6` | `numPad4/numPad6` | 兄弟节点定义为具有相同缩进级别的行。该命令不会将光标移出当前代码块。 |
| 跳转到当前块之外的上一个/下一个兄弟节点 | `NVDA+control+Alt+上/下箭头` | `control+alt+numPad4/numPad6` | `control+numPad4/numPad6` | 此命令可以跳转到另一个块中的兄弟节点。 |
| 跳转到上一个/下一个父节点 | `NVDA+Alt+左箭头``NVDA+alt+control+左箭头` | `alt+numPad7/numPad1` | `numPad7/numPad1` | 父节点定义为具有更小缩进级别的行。 |
| 跳转到上一个/下一个子节点 | `NVDA+Alt+control+右箭头`,`NVDA+alt+右箭头` | `alt+numPad9/numPad3` | `numPad9/numPad3` | 子节点定义为具有更大缩进级别的行。此命令不会将光标移出当前代码块。 |
| 选中当前代码块 | `NVDA+control+i` | `control+alt+numPad7` | `control+numPad7` | 从当前行向后选择所有具有严格更大缩进级别的内容。重复按下可选择多个块。 |
| 选中当前代码块及其后续具有相同缩进级别的所有块 | `NVDA+alt+i` | `control+alt+numPad9` | `control+numPad9` | 选择当前行以及所有具有更大或相等缩进级别的后续行。 |
| 缩进粘贴 | `NVDA+v` | `NVDA+v` | `NVDA+v` | 在需要将代码块粘贴到不同缩进级别的位置时，该功能会调整缩进级别后再粘贴。 |
| 在历史记录中向前/向后跳转 | N/A | `control+alt+numPad1/numPad3` | `control+numPad1/numPad3` | IndentNav 保留通过缩进导航访问的行的历史记录。 |
| 朗读当前行 | N/A | `alt+numPad5` | `numPad5` | 这是为方便起见重新映射的对象查看光标命令。 |
| 朗读父行 | `NVDA+i` | N/A | N/A | |

## 其他功能

### 快捷书签

缩进导航支持添加任意数量的快捷书签，以便您轻松跳转到需要的位置。一个书签由书签匹配正则表达式和用于跳转的自定义快捷键组成。按“shift+”相应的自定义快捷键可跳转上一个匹配的位置。

### 缩进跳转提示音：

当一次性跳过了多行时，缩进导航会连续播放相应缩进级别的提示音。仅当在 NVDA
文档格式设置中将行缩进设置为提示音时，才会启用此功能。可以在缩进导航设置中调整或禁用缩进跳转时的提示音音量。

## 源代码

源代码可在 <http://github.com/mltony/nvda-indent-nav> 获取。

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=indentnav

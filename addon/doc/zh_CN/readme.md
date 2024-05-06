# IndentNav-缩进导航 #

* 作者: Tony Malykh
* 下载 [稳定版][1]

此插件允许NVDA用户按缩进级别或行或段落的偏移进行导航。在浏览器中，它允许快速查找与屏幕左边缘具有相同偏移量的段落，例如注释的分层树中的第一级注释。此外，在编辑许多编程语言的源代码时，它允许在相同缩进级别的行之间跳转，以及快速查找具有更大或更小缩进级别的行。

## 用于浏览器
IndentNav可用于从屏幕左边缘偏移导航。特别是，您可以按NVDA + Alt +
DownArrow或UpArrow跳转到具有相同偏移量的下一个或上一个段落。例如，当浏览评论的分层树（例如，在reddit.com上）以在第一级评论之间跳转并跳过所有更高级别的评论时，这可能是有用的。

严格地说，IndentNav可以在任何应用程序中使用，NVDA为其提供树拦截器对象。

快捷键：

* NVDA + Alt + UpArrow或DownArrow：使用相同的偏移量跳转到上一个或下一个段落。
* NVDA + alt + LeftArrow：跳转到上一段，偏移量较小。
* NVDA + Alt + RightArrow：跳转到下一段，偏移量更大。

## 在文本编辑器中的用法
IndentNav对于编辑许多编程语言的源代码也很有用。像Python这样的语言要求源代码正确缩进，而在许多其他编程语言中强烈建议使用。使用IndentNav，您可以按NVDA
+ Alt + DownArrow或UpArrow跳转到具有相同缩进级别的下一行或上一行。您也可以按NVDA + Alt +
LeftArrow跳转到父线，即具有较低缩进级别的上一行。在Python中，您可以轻松找到当前的函数定义或类定义。您也可以按NVDA + Alt +
RightArrow转到当前行的第一个子节点，即下一行具有更大的缩进级别。

如果您的NVDA设置为将音线缩进表示为音调，则IndentNav将快速播放所有跳过的音调。否则它只会大致表示跳过的行数。

快捷键：

* NVDA + Alt + UpArrow或DownArrow：跳转到当前不包含块内具有相同缩进级别的上一行或下一行。
* NVDA + Alt + Control +
  UpArrow或DownArrow：使用相同的缩进级别强制跳转到上一行或下一行。如有必要，此快捷键将跳转到其他缩进块（例如其他Python函数）。
* NVDA + alt + LeftArrow：跳转到父级 - 这是具有较小缩进级别的上一行。
* NVDA + Alt + RightArrow：跳转到第一个子节点 - 这是在同一缩进块内具有更大缩进级别的下一行。

## 发布历史记录
* [版本1.2](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.2.nvda-addon)
  * 增加了对国际化的支持.
  * 在源文件中添加了GPL许可证.
  * 小修正.
* [版本1.1](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.1.nvda-addon)
  * 发布初始版本.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=indentnav

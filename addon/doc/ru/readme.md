# IndentNav #

Это дополнение позволяет пользователям NVDA перемещаться по уровню отступа
строк.  При редактировании исходного кода во многих языках программирования
оно позволяет переключаться между строками с одинаковым уровнем отступа, а
также быстро находить строки с большим или меньшим уровнем отступа.  Оно
также обеспечивает аналогичные нажатия клавиш в древовидных представлениях.

Пожалуйста, обратите внимание, что команды древовидной навигации были
перенесены в [дополнение TreeNav](https://github.com/mltony/nvda-tree-nav).

## Загрузить
Пожалуйста, установите из магазина дополнений NVDA

## Примечание о совместимости с VSCode

Встроенная доступность VSCode очень ограничена: по состоянию на 2024 год она
предоставляет только 500 строк кода через accessibility API, что приводит к
неправильной работе IndentNav в VSCode.

По умолчанию IndentNav не будет работать с VSCode, и когда вы попытаетесь
его использовать, вам нужно будет выбрать один из двух вариантов:

* Установите расширение VSCode ([страница
  расширения](https://marketplace.visualstudio.com/items?itemName=TonyMalykh.nvda-indent-nav-accessibility))([исходный
  код](https://github.com/mltony/vscode-nvda-indent-nav-accessibility)) -
  рекомендуемый способ. После установки расширения NVDA сможет получить
  доступ ко всему документу, независимо от его размера.
* Продолжайте использовать VSCode в устаревшем режиме - включите этот режим
  в настройках IndentNav. Это не рекомендуется, поскольку NVDA увидит только
  500 строк документа и ошибочно сообщит о пропавших братьях и
  сестрах/родителях.

## Проблемы с совместимостью

Известны проблемы с совместимостью IndentNav с [дополнением информации о
символах](https://addons.nvda-project.org/addons/charInfo.ru.html). В
настоящее время невозможно настроить как IndentNav, так и просмотровый
курсор на цифровой клавиатуре во время работы этого дополнения. Пожалуйста,
либо удалите это дополнение, либо используйте альтернативную раскладку
комбинаций клавиш в IndentNav.

## Раскладки комбинаций клавиш

IndentNav предлагает 3 встроенных раскладки комбинаций клавиш:

* Устаревшая или раскладка для ноутбука: это для тех, кто использовал
  IndentNav v1.x и не хочет изучать новые раскладки, или для клавиатур
  ноутбуков, у которых нет цифровых блоков.
* Раскладка Alt+цифровая клавиатура.
* Раскладка клавиш цифровой клавиатуры. Существует два способа устранения
  конфликта при нажатии клавиш просмотрового курсора:

    * Используйте цифровую клавиатуру для ввода отступов в редактируемых
      файлах и просмотровый курсор в других местах. Если вам всё ещё нужно
      использовать просмотровый курсор в редактируемых файлах, вы можете
      временно отключить ввод отступов, нажав `alt+NumLock`.
    * Переназначьте команды просмотрового курсора на сочетание клавиш
      alt+numpad, чтобы избежать конфликт нажатий клавиш.

Раскладку комбинаций клавиш можно выбрать в настройках IndentNav.

## Комбинации клавиш

| Действие | Устаревшая раскладка | Раскладка `Alt+цифровая клавиатура` | Раскладка цифровой клавиатуры | Описание |
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

## Другие особенности

### Быстрый поиск закладок

IndentNav позволяет настроить любое количество закладок, к которым вы можете
легко перейти. Закладка определяется с помощью регулярного выражения и
пользовательского нажатия клавиши для перехода к совпадению. Нажмите клавишу
"shift", чтобы найти предыдущее появление.

### Потрескивание:

При переходе по нескольким строкам кода IndentNav попытается быстро
воспроизвести уровни отступов в виде тонов пропущенных строк. Эта функция
включена только в том случае, если в настройках NVDA включена функция
отображения отступов в виде тонов. Громкость треска можно регулировать или
отключать в настройках IndentNav.

## Исходный код

Исходный код доступен по адресу <http://github.com/mltony/nvda-indent-nav>.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=indentnav

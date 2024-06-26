# Навигация по отстъпи (IndentNav) #

Тази добавка позволява на потребителите на NVDA да навигират по ниво на
отстъп на редовете.   Докато редактирате изходния код на много езици за
програмиране, тя позволява прескачане между редовете с едно и също ниво на
отстъп, както и бързо намиране на редове с по-голямо или по-малко ниво на
отстъп.   Тя също така предоставя подобни клавишни команди за дървовидни
изгледи.

Моля, обърнете внимание, че командите за дървовидна навигация са преместени
в [добавката "TreeNav"](https://github.com/mltony/nvda-tree-nav).

## Изтегляне
Моля, инсталирайте от магазина за добавки на NVDA

## Забележка относно съвместимостта с VSCode

Вградената достъпност във VSCode е много ограничена: от 2024 г. той излага
само 500 реда код чрез ППИ за достъпност, което кара навигацията по отстъпи
да работи неправилно във VSCode.

По подразбиране навигацията по отстъпи няма да работи с VSCode и когато се
опитате да я използвате, ще трябва да изберете от две опции:

* Инсталиране на разширението за VSCode ([страница на
  разширението](https://marketplace.visualstudio.com/items?itemName=TonyMalykh.nvda-indent-nav-accessibility))
  ([изходен
  код](https://github.com/mltony/vscode-nvda-indent-nav-accessibility)) –
  препоръчителен начин. След инсталиране на разширението NVDA ще има достъп
  до целия документ, независимо колко голям е той.
* Продължаване на използването на VSCode в наследен режим – активирайте този
  режим в настройките за навигацията по отстъпи. Това не се препоръчва, тъй
  като NVDA ще вижда само 500 реда от документа и погрешно ще съобщава за
  липсващи свързани/родителски елементи.

## Проблеми със съвместимостта

Навигацията по отстъпи има известни проблеми със съвместимостта с [добавка
за информация за
знаците](https://addons.nvda-project.org/addons/charInfo.bg.html).
Понастоящем е невъзможно да конфигурирате както навигацията по отстъпи, така
и курсора за преглед на цифровата клавиатура, докато тази добавка
работи. Моля, или деинсталирайте тази добавка, или използвайте алтернативна
схема за клавишни команди за навигацията по отстъпи.

## Подредби с клавишни команди

Навигацията по отстъпи предлага 3 вградени схеми за клавишни команди:

* Наследена или лаптоп подредба: това е за хора, които са използвали версии
  1.x на навигацията по отстъпи и не искат да учат нови подредби или за
  клавиатури на лаптоп, които нямат цифров блок.
* Подредба с Alt+цифровия блок.
* Подредба с клавишите от цифровия блок. Има два режима за справяне с
  конфликти с клавишните команди на курсора за преглед:

    * Използване на цифровия блок за текстовите полета и за курсора за
      преглед навсякъде другаде. Ако се налага да се използва курсора за
      преглед в текстовите полета, може временно да се деактивира
      навигацията по отстъпи, като се натисне `Alt+Num Lock`.
    * Пренастройване на командите на курсора за преглед на Alt+цифровия
      блок, като по този начин се избягва конфликт при клавишните команди.

Подредбата на клавишните команди може да бъде избрана в настройките за
навигацията по отстъпи.

## Клавишни комбинации

| Действие | Наследена подредба | Подредба `Alt+цифров блок` | Подредба `цифров блок` | Описание |
| -- | -- | -- | -- | -- |
| Превключване на навигацията по отстъпи | `Alt+Num Lock` | `Alt+Num Lock` | `Alt+Num Lock` | Това е полезно, когато и NVDA, и жестовете на курсора за преглед са присвоени на цифровия блок. |
| Преминаване към предишен/следващ сроден елемент | `NVDA+Alt+Стрелка нагоре/Стрелка надолу` | `Alt+8 от цифровия блок/2 от цифровия блок` | `8 от цифровия блок/2 от цифровия блок` | Сродният елемент се дефинира като ред със същото ниво на отстъп.<br>Тази команда няма да изведе курсора отвъд текущия кодов блок. |
| Преминаване към предишен/следващ сроден елемент, прескачайки излишното | Не е указано | `Control+Alt+8 от цифровия блок/2 от цифровия блок` | `Control+8 от цифровия блок/2 от цифровия блок` | Регулярният израз за излишното може да бъде конфигуриран в настройките. |
| Преминаване към първия/последния сроден елемент | `NVDA+Alt+Shift+Стрелка нагоре/Стрелка надолу` | `Alt+4 от цифровия блок/6 от цифровия блок` | `4 от цифровия блок/6 от цифровия блок` | Сродният елемент се дефинира като ред със същото ниво на отстъп.<br>Тази команда няма да изведе курсора отвъд текущия кодов блок. |
| Преминаване към първия/последния сроден елемент потенциално извън текущия блок | `NVDA+Control+Alt+Стрелка нагоре/Стрелка надолу` | `Control+Alt+4 от цифровия блок/6 от цифровия блок` | `Control+4 от цифровия блок/6 от цифровия блок` | Тази команда позволява да се преминава към сроден елемент в друг блок. |
| Преминаване към предишен/следващ родителски елемент | `NVDA+Alt+Стрелка наляво`,<br>`NVDA+Alt+Control+Стрелка наляво` | `Alt+7 от цифровия блок/1 от цифровия блок` | `7 от цифровия блок/1 от цифровия блок` | Родителски елемент се определя като ред с по-ниско ниво на отстъп. |
| Преминаване към предишен/следващ дъщерен елемент | `NVDA+Alt+Control+Стрелка надясно`,<br>`NVDA+Alt+Стрелка надясно` | `Alt+9 от цифровия блок/3 от цифровия блок` | `9 от цифровия блок/3 от цифровия блок` | Дъщерният елемент се определя като ред с по-голямо ниво на отстъп.<br>Тази команда няма да изведе курсора отвъд текущия кодов блок. |
| Избиране на текущия блок | `NVDA+Control+I` | `Control+Alt+7 от цифровия блок` | `Control+7 от цифровия блок` | Избира текущия ред плюс всички следващи редове със строго по-високо ниво на отстъп.<br>Многократното натискане избира няколко блока. |
| Избиране на текущия блок и всички следващи блокове на същото ниво на отстъп | `NVDA+Alt+I` | `Control+Alt+9 от цифровия блок` | `Control+9 от цифровия блок` | Избира текущия ред плюс всички следващи редове с по-голямо или равно ниво на отстъп. |
| Поставяне с отстъп | `NVDA+V` | `NVDA+V` | `NVDA+V` | Когато трябва да се постави блок от код на място с различно ниво на отстъп, тази команда ще коригира нивото на отстъп преди поставяне. |
| Преминаване назад/напред в хронологията | Не е указано | `Control+Alt+1 от цифровия блок/3 от цифровия блок` | `Control+1 от цифровия блок/3 от цифровия блок` | Навигацията по отстъпи пази хронология на редовете, които са обхождани чрез командите за навигация по отстъпи. |
| Изговаряне на текущия ред | Не е указано | `Alt+5 от цифровия блок` | `5 от цифровия блок` | Това всъщност е команда на курсора за преглед, преназначена за удобство. |
| Изговаряне на родителския ред | `NVDA+I` | Не е указано | Не е указано | |

## Други функции

### Показалци за бързо намиране

Навигацията по отстъпи позволява да се конфигурират произволен брой
показалци, до които може лесно да се премине. Показалецът се определя от
регулярен израз и персонализирана клавишна команда за преминаване към
съвпадение. Натискането на `Shift+`, за преминаване към предишно съвпадение.

### Пукане

Когато прескача много редове код, навигацията по отстъпи ще се опита бързо
да възпроизведе нивата на отстъп като тонове на пропуснатите редове. Тази
функция е активирана само когато опцията за докладване на отстъп като тонове
е включена в настройките на NVDA. Силата на звука на пукането може да се
регулира или деактивира в настройките за навигация по отстъпи.

## Изходен код

Изходният код е наличен на адрес <http://github.com/mltony/nvda-indent-nav>.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=indentnav

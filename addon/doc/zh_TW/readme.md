# NVDA 的 IndentNav 附加元件
這個附加元件讓 NVDA 使用者能依照行的縮排層級來導覽。
在編輯多種程式語言的原始碼時，它可以讓您在縮排層級相同的行之間跳轉，也能快速找到縮排層級更大或更小的行。

請注意，樹狀導覽指令已移至 [TreeNav 附加元件](https://github.com/mltony/nvda-tree-nav)。

## 下載
請從 NVDA 附加元件商店安裝

## 與 VSCode 相容性的注意事項

VSCode 內建的無障礙功能非常有限：截至 2024 年，它只透過無障礙 API 提供 500 行程式碼，這會讓 IndentNav 在 VSCode 中無法正常運作。

IndentNav 預設不會在 VSCode 中運作，當您嘗試使用時，必須從以下兩個選項中擇一：

* 安裝 VSCode 延伸模組（[延伸模組頁面](https://marketplace.visualstudio.com/items?itemName=TonyMalykh.nvda-indent-nav-accessibility)）（[原始碼](https://github.com/mltony/vscode-nvda-indent-nav-accessibility)）－建議採用這個方式。安裝延伸模組後，無論文件有多大，NVDA 都能存取整份文件。
* 繼續以舊版模式使用 VSCode－請在 IndentNav 設定中啟用這個模式。不建議這樣做，因為 NVDA 只會看到文件的 500 行，並且會錯誤地回報找不到同層級的行或父行。

## 相容性問題

IndentNav 與[字元資訊 (Character Information) 附加元件](https://addons.nvda-project.org/addons/charInfo.en.html)有已知的相容性問題。在這個附加元件執行的情況下，目前無法同時把 IndentNav 與檢閱游標設定在數字鍵盤上。請您移除這個附加元件，或是在 IndentNav 中改用其他的按鍵配置。

## 按鍵配置

IndentNav 提供 3 種內建的按鍵配置：

* 舊版或筆記型電腦配置：適合原本使用 IndentNav 1.x 而不想學習新配置的使用者，或是沒有數字鍵盤的筆記型電腦。
* Alt+數字鍵盤配置。
* 數字鍵盤配置。處理與檢閱游標按鍵衝突的方式有兩種：
    * 在可編輯區域中數字鍵盤用於 IndentNav，在其他地方數字鍵盤則用於檢閱游標。如果您仍需要在可編輯區域中使用檢閱游標，可以按 `alt+numLock` 暫時停用 IndentNav。
    * 把檢閱游標指令改對應到 alt+數字鍵盤，藉此避免按鍵衝突。

按鍵配置可以在 IndentNav 設定中選擇。

## 按鍵

| 動作 | 舊版配置 | `Alt+數字鍵盤` 配置 | 數字鍵盤配置 | 說明 |
| -- | -- | -- | -- | -- |
| 切換 IndentNav 的開或關 | `alt+numLock` | `alt+numLock` | `alt+numLock` | 當 NVDA 與檢閱游標的手勢都指定給數字鍵盤時很有用。 |
| 跳到上一個/下一個同層行 | `NVDA+Alt+up/downArrow` | `alt+numPad8/numPad2` | `numPad8/numPad2` | 同層行是指縮排層級相同的行。<br>這個指令不會把游標帶出目前的程式區塊。 |
| 跳到上一個/下一個同層行並略過雜項 | 無 | `control+alt+numPad8/numPad2` | `control+numPad8/numPad2` | 您可以在設定中設定雜項的正規表達式。 |
| 跳到第一個/最後一個同層行 | `NVDA+Alt+shift+up/downArrow` | `alt+numPad4/numPad6` | `numPad4/numPad6` | 同層行是指縮排層級相同的行。<br>這個指令不會把游標帶出目前的程式區塊。 |
| 跳到上一個/最後一個同層行，可能位於目前區塊之外 | `NVDA+control+Alt+up/downArrow` | `control+alt+numPad4/numPad6` | `control+numPad4/numPad6` | 這個指令讓您跳到另一個區塊中的同層行。 |
| 跳到上一個/下一個父行 | `NVDA+Alt+leftArrow`,<br>`NVDA+alt+control+leftArrow` | `alt+numPad7/numPad1` | `numPad7/numPad1` | 父行是指縮排層級較小的行。 |
| 跳到上一個/下一個子行 | `NVDA+Alt+control+rightArrow`,<br>`NVDA+alt+rightArrow` | `alt+numPad9/numPad3` | `numPad9/numPad3` | 子行是指縮排層級較大的行。<br>這個指令不會把游標帶出目前的程式區塊。 |
| 選取目前的區塊 | `NVDA+control+i` | `control+alt+numPad7` | `control+numPad7` | 選取目前行以及後面所有縮排層級嚴格大於目前行的行。<br>重複按下可選取多個區塊。 |
| 選取目前的區塊以及後面所有相同縮排層級的區塊 | `NVDA+alt+i` | `control+alt+numPad9` | `control+numPad9` | 選取目前行以及後面所有縮排層級大於或等於目前行的行。 |
| 縮排貼上 | `NVDA+v` | `NVDA+v` | `NVDA+v` | 當您需要把一段程式碼貼到縮排層級不同的位置時，這個指令會先調整縮排層級再貼上。 |
| 在歷程記錄中往回/往前跳 | 無 | `control+alt+numPad1/numPad3` | `control+numPad1/numPad3` | IndentNav 會保留您透過 IndentNav 指令造訪過的行的歷程記錄。 |
| 讀出目前行 | 無 | `alt+numPad5` | `numPad5` | 這其實是為了方便而重新對應的檢閱游標指令。 |
| 讀出父行 | `NVDA+i` | 無 | 無 | |

## 其他功能

### 快速尋找書籤

IndentNav 讓您設定任意數量的書籤，方便您快速跳到指定位置。一個書籤由一個正規表達式以及一個自訂按鍵組成，按下該按鍵即可跳到相符之處。按 `shift+` 該按鍵可尋找上一個相符之處。

每個書籤還可以設定一個父書籤。這種情況下，當您搜尋子書籤時，游標永遠不會越過父書籤。舉例來說，把類別定義的書籤設為函式定義書籤的父書籤是合理的，這樣搜尋函式時就永遠不會跑到目前的類別之外。

### 縮排提示音：

當一次跳過許多行程式碼時，IndentNav 會快速播放所略過各行的縮排層級提示音。這個功能只有在 NVDA 設定中開啟「以音調提示縮排」時才會啟用。縮排提示音的音量可以在 IndentNav 設定中調整或停用。

## 原始碼

原始碼位於 <http://github.com/mltony/nvda-indent-nav>。

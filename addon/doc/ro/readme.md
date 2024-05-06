# IndentNav #
[[!meta title="IndentNav"]]

* Autor: Tony Malykh
* Descarcați versiunea [stabila][1]

Acest supliment permite utilizatorilor NVDA să navigheze prin nivelul de
indentare ori prin distanța de la marginea din stânga ecranului a rândurilor
sau paragrafelor. În browsere permite găsirea rapidă a paragrafelor cu
aceeași distanță de la marginea din stânga a ecranului, cum ar fi
comentariile de nivel 1 într-un arbore ierarhic de comentarii. De asemenea,
în timp ce editați codul sursă în multe limbi de programare, permite să
săriți între rândurile aceluiași nivel de indentare, precum și să găsiți
rapid rânduri cu nivel de indentare mai mare sau mai mic.

## Folosirea în browsere
IndentNav poate fi utilizat pentru a naviga prin distanța de la marginea din
stânga a ecranului. În special, puteți apăsa NVDA + Alt + săgeată jos sau
sus pentru a trece la paragraful următor sau anterior care are același
decalaj. De exemplu, acest mod de navigare poate fi util atunci când
răsfoiți arborii ierarhici de comentarii (de ex. Pe reddit.com). Cu acest
supliment puteți sări între comentariile de la primul nivel ignorând toate
comentariile cu nivel de indentare superior.

Strict vorbind, IndentNav poate fi folosit în orice aplicație pentru care
NVDA furnizează un obiect arbore interceptor.

comenzi de tastatură:

* NVDA+Alt+săgeată sus sau jos: Sare la paragraful anterior sau următor cu
  aceeași distanță de la marginea din stânga ecranului.
* NVDA+alt+Săgeată stânga: Sare la paragraful anterior cu distanță mai mică
  de la marginea din stânga ecranului.
* NVDA+alt+Săgeată dreapta: Sare la paragraful următor cu distanță mai mare
  de la marginea din stânga ecranului.

## Folosirea in editoare de text
IndentNav poate fi util și pentru editarea codului sursă în multe limbi de
programare. în limbi ca Python este necesară indentarea codului sursa, în
timp ce în multe alte limbi de programare indentarea este recomandată dar nu
necesară. Cu IndentNav puteți apăsa NVDA + Alt + săgeată jos sau sus pentru
a naviga la rândul urmator sau anterior cu același nivel de indentare. De
asemenea, puteți apăsa NVDA + Alt + săgeată stânga pentru a sări la un rând
parinte, adică un rând anterior cu un nivel inferior de indentare. În Python
puteți găsi în acest fel cu ușurință definiția funcției actuale sau
definiția clasei. Pe lânga asta, uteți apăsa NVDA + Alt + săgeată dreapta
pentru a naviga la primul copil al rândului actual, adica următorul rând cu
un nivel de indentare mai mare.

Dacă NVDA este setat să exprime indentarea rândului prin tonuri, atunci
IndentNav va reda rapid tonurile tuturor rândurilor ignorate. În caz
contrar, suplimentul va pâcâi doar pentru a indica aproximativ numărul de
rânduri excluse.

comenzi de tastatură:

* NVDA+Alt+săgeată sus sau jos: Sare la rândul anterior sau următor cu
  același nivel de indentare în cadrul blocului actual de indentare.
* NVDA+Alt+Control+săgeată sus sau jos: Forțeaza săritura la rândul anterior
  sau următor cu același nivel de indentare. Această comandă va naviga și la
  alte blocuri de indentare (cum ar fi alte funcții Python), dacă este
  necesar.
* NVDA+alt+săgeată stânga: Sare la rândul părinte - acesta este rândul
  anterioară cu nivel de indentare mai mic.
* NVDA+Alt+săgeată dreapta: Sare la primul rând copil - adica urmatorul rând
  cu nivel de indentare mai mare in același block de indentare.

## Istoria versiunilor
* [v1.2](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.2.nvda-addon)
  * A fost adaugata functia de traducere.
  * s-au adaugat datele GPL in header-ul fișierelor codului de sursă .
  * Corectări minore.
* [v1.1](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.1.nvda-addon)
  * Versiunea inițială.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=indentnav

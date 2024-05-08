# Navigácia po odsadeniach #

* Autor: Tony Malykh
* Stiahnuť [stabilnú verziu][1]

Umožňuje rýchlo nájsť odseky s rovnakým odsadením. V prehliadačoch umožňuje
vyhľadať odseky s rovnakým, prípadne menším alebo väčším odsadením. Takto je
možné rýchlo sa orientovať v strome s komentármi. Pri programovaní môže byť
doplnok užitočný pri hľadaní kódu s rovnakým, prípadne menším alebo väčším
odsadením.

## Použitie v režime prehliadania
Skratkou nvda+alt+šípka dole preskočíte na odsek s rovnakým odsadením, ako
má aktuálny odsek. NVDA+alt+šípka hore vyhľadá predchádzajúci odsek s
rovnakým odsadením. Takto môžere napríkald rýchlo vyhľadať kkomentáre prvej
úrovne (napríklad na reddit.com).

Jednoducho povedané, doplnok funguje všade tam, kde je dostupný objekt so
stromovou štruktúrou.

Klávesové skratky:

* NVDA+alt+šípky hore a dole: preskočí na predchádzajúci alebo nasledujúci
  odsek s rovnakým odsadením.
* NVDA+alt+ľavá šípka: Prejdi na predchádzajúci odsek s menším odsadením.
* NVDA+alt+pravá šípka: Prejdi na nasledujúci odsek s väčším odsadením.

## Použitie v textových editoroch
Doplnok môže byť užitočný pri programovaní. Jazyky ako napríklad Python
vyžadujú odsadenie kódu, mnohé ďalšie to tiež a odporúčajú. Nvda+alt+šípky
hore a dole prejdú na predchádzajúci alebo nasledujúci riadok s rovnakým
odsadením. Nvda+alt+ľavá šípka prejde na rodičovský riadok, teda
predchádzajúci riadok s menším odsadením. V Pythone takto môžete rýchlo
skočiť na definíciu funkcie alebo triedy. NVDA+alt+pravá šípka prejde na
potomka aktuálneho riadka, teda nasledujúci riadok s väčším odsadením.

Ak máte zapnuté oznamovanie odsadenia pípaním, NVDA pri preskakovaní zapípa
riadky, ktoré boli preskočené. Ak máte toto oznamovanie vypnuté, budete
počuť len prasknutie indikujúce, že boli preskočené riadky.

Klávesové skratky:

* Nvda+alt+šípky hore a dole: Prejde na predchádzajúci alebo nasledujúci
  riadok s tým istým odsadením, a,o má aktuálny riadok.
* NVDA+Alt+Ctrl+šípky hore a dole: Vynútiť skočenie na predchádzajúci alebo
  nasledujúci riadok s rovnakým odsadením. Ak je to potrebné, Skočí na iné
  bloky s rovnakým odsadením.
* NVDA+alt+ľavá šípka: Prejdi na rodiča: Predchádzajúci riadok s menším
  odsadením.
* NVDA+alt+pravá šípka: Prejdi na potomka - nasledujúci riadok s väčším
  odsadením.

## Zmeny
* [v1.2](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.2.nvda-addon)
  * Pridaná podpora lokalizácie do iných jazykov.
  * Do zdrojových súborov doplnená GPL hlavička.
  * Malé úpravy.
* [v1.1](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.1.nvda-addon)
  * Prvé vydadnie.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=indentnav

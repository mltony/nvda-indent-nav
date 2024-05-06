# Sisennysnavigointi #

* Tekijä: Tony Malykh
* Lataa [vakaa versio][1]

Tämän lisäosan avulla NVDA:n käyttäjät voivat siirtyä sisennystason,
rivipoikkeamien tai kappaleiden mukaan.  Selaimissa sen avulla on
mahdollista etsiä nopeasti kappaleita, jotka alkavat ruudun vasemmasta
reunasta katsottuna samasta kohdasta, kuten ensimmäisen tason kommentit
hierarkkisessa kommenttipuussa.  Lisäksi se mahdollistaa useiden
ohjelmointikielien lähdekoodia muokattaessa siirtymisen samalla
sisennystasolla olevien rivien välillä sekä sellaisten rivien nopean
etsimisen, joilla on suurempi tai pienempi sisennystaso.

## Käyttö selaimissa
Sisennysnavigointia voidaan käyttää poikkeaman mukaan siirtymiseen ruudun
vasemmasta reunasta katsottuna.  Paina NVDA+Alt+Nuoli alas/ylös siirtyäksesi
seuraavaan tai edelliseen kappaleeseen, jolla on sama rivipoikkeama.  Tästä
voi olla hyötyä esim. selattaessa hierarkkisia kommenttipuita
(esim. reddit.com-sivustolla) siirtymällä ensimmäisen tason kommenttien
välillä ja ohittamalla kaikki ylemmällä tasolla olevat.

Tarkkaan ottaen Sisennysnavigointia on mahdollista käyttää missä tahansa
sovelluksessa, jolle NVDA tarjoaa puumaisen objektirakenteen.

Näppäinkomennot:

* NVDA+Alt+Nuoli ylös/alas: Siirry edelliseen tai seuraavaan kappaleeseen,
  jolla on sama poikkeama.
* NVDA+Alt+Nuoli vasemmalle: Siirry edelliseen kappaleeseen, jolla on
  pienempi poikkeama.
* NVDA+Alt+Nuoli oikealle: Siirry seuraavaan kappaleeseen, jolla on suurempi
  poikkeama.

## Käyttö tekstieditoreissa
Sisennysnavigoinnista voi olla hyötyä myös tekstieditoreissa useiden
ohjelmointikielien lähdekoodia muokattaessa.  Sellaiset kielet, kuten Python
edellyttävät, että lähdekoodi on sisennetty asianmukaisesti, kun taas
monissa muissa kielissä sitä suositellaan.  Sisennysnavigointia käyttäessäsi
voit painaa NVDA+Alt+Nuoli alas/ylös siirtyäksesi seuraavalle tai
edelliselle saman sisennystason riville.  Voit myös painaa NVDA+Alt+Nuoli
vasemmalle siirtyäksesi ylemmän tason riville, toisin sanoen edelliselle
riville, jolla on pienempi sisennystaso.  Pythonissa löydät tällä tavalla
helposti nykyisen funktio- tai luokkamäärityksen.  Paina NVDA+Alt+Nuoli
oikealle siirtyäksesi ensimmäiselle, nykyistä riviä alemmalla tasolla
olevalle riville, toisin sanoen seuraavalle riville, jolla on suurempi
sisennystaso.

Mikäli NVDA on määritetty ilmaisemaan rivien sisennykset äänimerkkeinä,
Sisennysnavigointi toistaa nopeasti kaikki ohitettujen rivien äänet.
Muutoin se vain antaa äänimerkin ilmoittaakseen karkeasti ohitettujen rivien
määrän.

Näppäinkomennot:

* NVDA+Alt+Nuoli ylös/alas: Siirry edelliselle tai seuraavalle riville,
  jolla on sama sisennystaso nykyisessä sisennyslohkossa.
* NVDA+Alt+Ctrl+Nuoli ylös/alas: Siirry pakotetusti edelliselle tai
  seuraavalle riville, jolla on sama sisennystaso. Tämä komento siirtää
  muihin sisennyslohkoihin (kuten Python-funktioihin), mikäli se on tarpeen.
* NVDA+Alt+Nuoli vasemmalle: Siirry ylemmälle tasolle - toisin sanoen
  edelliselle riville, jolla on pienempi sisennystaso.
* NVDA+Alt+Nuoli oikealle: Siirry ensimmäiselle alemmalle tasolle - toisin
  sanoen seuraavalle riville, jolla on suurempi sisennystaso samassa
  sisennyslohkossa.

## Julkaisuhistoria
* [v1.2](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.2.nvda-addon)
  * Lisätty tuki käännöksille.
  * Lisätty GPL-otsakkeet lähdekooditiedostoihin.
  * Pieniä korjauksia.
* [v1.1](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.1.nvda-addon)
  * Ensimmäinen julkaisu.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=indentnav

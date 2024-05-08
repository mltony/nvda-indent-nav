# Kretanje po uvlakama (IndentNav) #

* Autor: Tony Malykh
* Preuzmi [stabilnu verziju][1]

Ovaj dodatak dozvoljava NVDA korisnicima kretanje po razinama uvlačenja
redaka ili po odmacima redaka ili po odlomcima. U preglednicima omogućuje
brzo pronalaženje odlomaka s istim odmakom od lijevog ruba ekrana, poput
komentara prve razine u hijerarhijskom stablu komentara. Također, tijekom
uređivanja izvornog koda programskih jezika, omogućuje kretanje između
redaka iste razine uvlačenja, kao i brzo pronalaženje redaka s većom ili
manjom uvlakom.

## Primjena u preglednicima
Kretanje po uvlakama se može koristiti za kretanje prema odmaku od lijevog
ruba ekrana. Tipkama NVDA+Alt+Strelica Gore ili Strelica Dolje se prelazi na
sljedeći ili prethodni odlomak koji ima isti odmak. Primjerice, to može biti
korisno prilikom pregledavanja hijerarhijskih stabala komentara (na primjer,
na reddit.com) za kretanje po komentarima prve razine, preskačući sve
komentare više razine.

Strogo rečeno, dodatak „Kretanje po uvlakama” se može koristiti u bilo kojoj
aplikaciji za koju NVDA pruža mogućnost prikaza stabla.

Tipkovni prečaci:

* NVDA+strelica gore ili strelica dolje: Skoči na prethodni ili sljedeći
  odlomak s istim odmakom.
* NVDA+Alt+strelica lijevo: Skoči na prethodni odlomak s manjim odmakom.
* NVDA+Alt+strelica desno: Skoči na sljedeći odlomak s većim odmakom.

## Primjena u programima za uređivanje teksta
Kretanje po uvlakama također može biti korisna za uređivanje izvornog koda u
mnogim programskim jezicima. Jezici poput Pythona zahtijevaju da izvorni kod
bude pravilno uvučen, dok se u mnogim drugim programskim jezicima to
preporučuje. Kretanje po uvlakama koristi tipke NVDA+Alt+strelica dolje ili
strelica gore za prelaženje na sljedeći ili prethodni redak s istom razinom
uvlačenja. Tipkama NVDA+Alt+strelica lijevo se prelazi na prethodni redak s
nižom razinom uvlačenja. U Pythonu se trenutačna definicija funkcije ili
klasa lako pronalaze. Tipkama NVDA+Alt+strelica desno se prelazi na prvi
podređeni redak, a to je sljedeći redak s većom uvlakom.

Ako je NVDA postavljen da pomoću zvukova izvještava o uvlačenju redaka,
Kretanje po uvlakama će brzo svirati zvukove svih preskočenih redaka. U
suprotnom će samo pucketati i brzo izgovarati broj preskočenih redaka.

Tipkovni prečaci:

* NVDA+Alt+strelica gore ili strelica dolje: Skoči na prethodni ili sljedeći
  redak s istom razinom uvlačenja unutar trenutnog bloka.
* NVDA+Alt+kontrol+strelica gore ili strelica dolje: Prisilno skoči na
  prethodni ili sljedeći redak s istom razinom uvlačenja. Ova naredba će
  skočiti na druge blokove (kao što su druge funkcije Pythona) ako je
  potrebno.
* NVDA+Alt+strelica lijevo: Skoči na prethodni redak s nižom razinom
  uvlačenja.
* NVDA+Alt+strelica desno: Skoči na prvi podređeni redak – to je sljedeći
  redak s većom uvlakom unutar istog bloka.

## Povijest izdanja
* [v1.2](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.2.nvda-addon)
  * Dodana je podrška za internacionalizaciju.
  * Dodana su zaglavlja za opću javnu licencu u izvornim datotekama.
  * Manji ispravci.
* [v1.1](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.1.nvda-addon)
  * Prvo izdanje.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=indentnav

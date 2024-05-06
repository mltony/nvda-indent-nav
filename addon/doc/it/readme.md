# IndentNav #

* Autore: Tony Malykh
* Scarica [versione stabile][1]

Questo add-on consente agli utenti di NVDA di navigare per livello di
indentazione o per rientro di linea o di paragrafo. Nei browser consente di
trovare rapidamente paragrafi con lo stesso rientro dal margine sinistro
dello schermo, come i commenti di primo livello in una gerarchia di
commenti. Inoltre, quando si scrivono programmi,  il componente permette di
spostarsi rapidamente tra le righe con lo stesso livello di indentazione e
trovare rapidamente linee con livello di indentazione maggiore o minore.

## Utilizzo nei browser
IndentNav può essere utilizzato per navigare per rientro dal margine
sinistro dello schermo. In particolare, si può premere NVDA+ALT+Freccia Giù
o Freccia Su per spostarsi al paragrafo precedente o successivo che abbia lo
stesso rientro sinistro. Ciò può essere utile, ad esempio, quando si leggono
commenti organizzati in conversazioni (ad es. in reddit.com), per saltare
rapidamente tra i commenti di primo livello, ignorando tutti i commenti di
livello superiore (ossia le risposte ai precedenti).

Per la precisione, IndentNav può essere utilizzato in tutte le applicazioni
per le quali NVDA fornisce un tree interceptor object.

Tasti di scelta rapida:

* NVDA+Alt+Freccia Su o Freccia Giù: salta al paragrafo precedente o
  sucessivo con lo stesso rientro.
* NVDA+Alt+Freccia Sinistra: salta al paragrafo precedente con rientro
  minore.
* NVDA+Alt+Freccia Destra: salta al paragrafo successivo con rientro
  maggiore.

## Utilizzo negli editor di testi
IndentNav può essere utile anche nella scrittura di programmi in molti
linguaggi di programmazione. Linguaggi come Python richiedono che il codice
sorgente sia correttamente indentato, mentre in molti altri linguaggi di
programmazione ciò è fortemente consigliato. Con IndentNav, si può premere
NVDA+Alt+Freccia Su o Freccia Giù  per spostarsi alla linea precedente o
successiva con lo stesso livello di indentazione. Si può inoltre premere
NVDA+Alt+Freccia Sinistra per spostarsi ad una linea padre, ossia a una
linea precedente con un livello di indentazione più basso. In questo modo,
in Python, si può risalire facilmente alla definizione della funzione o
della classe corrente (quella al cui interno della quale si trova il
cursore). Si può anche premere NVDA+Alt+Freccia Destra per andare al primo
figlio della linea attuale, ossia la linea successiva con un livello di
indentazione maggiore.

Se avete impostato NVDA per indicare con suoni l'indentazione delle linee,
IndentNav riprodurà rapidamente i suoni delle linee saltate ad ogni comando;
altrimenti emetterà un unico suono per indicare, più o meno, il numero di
linee saltate.

Tasti di scelta rapida:

* NVDA+Alt+Freccia Su o Freccia Giù: salta alla linea precedente o
  successiva con lo stesso livello di indentazione all'interno dello stesso
  blocco di indentazione.
* NVDA+Alt+Control+Freccia Su o Freccia Giù: forza il salto alla linea
  precedente o successiva con lo stesso livello di indentazione. questo
  comando porterà il cursore su altri blocchi di indentazione (come altre
  funzioni Python) se necessario.
* NVDA+alt+Freccia Sinistra: salta al padre, ossia a una linea precedente
  con livello di indentazione più basso.
* NVDA+alt+Freccia Destra: salta al primo figlio, ossia a una linea
  successiva con livello di indentazione più alto nello stesso blocco di
  indentazione.

## Cronologia revisioni
* [v1.2](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.2.nvda-addon)
* Aggiunto il supporto per l'internazionalizzazione.
* Aggiunte le intestazioni GPL nei file sorgente.
* Altre piccole migliorie.
* [v1.1](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.1.nvda-addon)
  * Versione iniziale.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=indentnav

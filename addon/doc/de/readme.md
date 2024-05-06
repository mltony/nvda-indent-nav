# IndentNav #

* Autor: Tony Malykh
* [Stabile Version herunterladen][1]

Diese Erweiterung ermöglicht die Navigation im Text nach der
Einrückungsebene oder dem Abstand von Zeilen und Absätzen.  In Browsern
ermöglicht diese Erweiterung das schnelle Auffinden von Absätzen mit
gleichem Abstand zum linken Bildschirmrand, wie z.B. Kommentare der ersten
Ebene in einem hierarchischen Kommentarbaum.  Auch beim Editieren von
Quellcode in vielen Programmiersprachen erlaubt Indentnav zwischen den
Zeilen der gleichen Einrückungsebene zu springen, sowie schnell Zeilen mit
niedrigerer oder höherer Einrückungsebene zu finden.

## Verwendung in Browsern
IndentNav kann verwendet werden, um zu einem bestimmten Abstand vom linken
Bildschirmrand zu navigieren.  Insbesondere können Sie NVDA+Alt+Pfeil ab und
auf drücken, um zum nächsten oder vorherigen Absatz mit dem gleichen Abstand
zu springen.  Dies kann z.B. nützlich sein, wenn Sie hierarchische Bäume von
Kommentaren durchsuchen (z.B. auf reddit.com). So können Sie zwischen
Kommentaren der ersten Ebene springen und alle Kommentare der höheren Ebene
überspringen.

Streng genommen kann IndentNav in jeder Anwendung verwendet werden, für
welche NVDA ein Tree-Interceptor-Objekt zur Verfügung stellt.

Tastenkürzel:

* NVDA+Alt+Pfeil aufwärts oder abwärts: Springt zum vorherigen oder nächsten
  Absatz mit dem gleichen Abstand vom linken Bildschirmrand.
* NVDA+alt+Linkspfeil: Springt zum vorherigen Absatz mit geringerem Abstand
  vom linken Bildschirmrand.
* NVDA+Alt+Rechtspfeil: Springt zum nächsten Absatz mit größerem Abstand vom
  linken Bildschirmrand.

## Einsatz in Text-Editoren
IndentNav kann auch nützlich sein, um Quellcode in vielen
Programmiersprachen zu bearbeiten.  Sprachen wie Python verlangen, dass der
Quellcode richtig eingerückt wird, während es in vielen anderen
Programmiersprachen dringend empfohlen wird.  Mit IndentNav können Sie
NVDA+Alt+Pfeil ab- und aufwärts drücken, um zur nächsten oder vorherigen
Zeile mit der gleichen Einrückungsebene zu springen.  Sie können auch
NVDA+Alt+Linkspfeil drücken, um zu einer übergeordneten Zeile zu springen,
d.h. zu einer vorherigen Zeile mit niedrigerer Einrückungsebene.  In Python
finden Sie somit leicht die aktuelle Funktionsdefinition oder
Klassendefinition.  Sie können NVDA+Alt+Rechtspfeil drücken, um zum ersten
Child der aktuellen Zeile zu gehen, d.h. zur nächsten Zeile mit größerer
Einrückungsebene.

Wenn NVDA so eingestellt ist, dass Zeileneinrückungen als Töne ausgedrückt
werden, wird IndentNav schnell die Töne aller übersprungenen Zeilen
wiedergeben.  Andernfalls wird es nur knacken, um die Anzahl der
übersprungenen Zeilen grob darzustellen.

Tastenkürzel:

* NVDA+Alt+Pfeil aufwärts oder abwärts: Springt zur vorherigen oder nächsten
  Zeile mit der gleichen Einrückung innerhalb des aktuellen
  Einrückungsblocks.
* NVDA+Alt+STRG+Pfeil aufwärts oder abwärts: Erzwingt den Sprung zur
  vorherigen oder nächsten Zeile mit der gleichen Einrückung. Dieser Befehl
  springt bei Bedarf zu anderen Einrückungsblöcken (z.B. anderen
  Python-Funktionen).
* NVDA+alt+Linkspfeil: Springt zur übergeordneten Zeile - das ist die
  vorherige Zeile mit der niedrigeren Einrückung.
* NVDA+Alt+Rechtspfeil: Springt zur ersten Zeile mit größerer Einrückung
  innerhalb desselben Einrückungsblocks.

## Versionsverlauf
* [v1.2](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.2.nvda-addon)
  * Unterstützung für Übersetzungen wurde hinzugefügt.
  * GPL-Kopfdaten wurden in den Quelldateien eingefügt.
  * Geringfügige Verbesserungen.
* [v1.1](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.1.nvda-addon)
  * Erste Version.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=indentnav

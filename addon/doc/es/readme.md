# IndentNav #

* Autor: Tony Malykh
* Descargar [versión estable][1]

Este complemento permite a los usuarios de NVDA navegar por nivel de sangría
o por intervalos de líneas o párrafos.  En navegadores permite encontrar
párrafos rápidamente con el mismo intervalo desde el margen izquierdo de la
pantalla, como por ejemplo los comentarios de primer nivel en un árbol
jerárquico de comentarios.  También mientras se edita código fuente en
muchos lenguajes de programación, permite saltar entre las líneas del mismo
nivel de sangría, así como encontrar rápidamente líneas con mayor o menor
nivel de sangría.

## Utilización en navegadores
IndentNav puede utilizarse para navegar por intervalos desde el margen
izquierdo de la pantalla.  En particular, puedes pulsar NVDA+Alt+Flecha
Abajo o Flecha Arriba para saltar al párrafo siguiente o anterior que tenga
el mismo intervalo.  Por ejemplo, esto puede ser útil al navegar por árboles
jerárquicos de comentarios (ej.: en reddit.com) para saltar entre
comentarios de primer nivel y omitir todos los comentarios de nivel
superior.

En sentido estricto, IndentNav puede utilizarse en cualquier aplicación,
para la que NVDA proporcione un interceptor del objeto árbol.

Teclas rápidas:

* NVDA+Alt+Flecha Arriba o abajo: Saltar a la siguiente línea con el mismo
  desplazamiento.
* NVDA+Alt+Flecha Izquierda: salta al anterior párrafo con menos
  desplazamiento.
* NVDA+Alt+Flecha Derecha: salta al siguiente párrafo con mayor
  desplazamiento.

## Utilización en editores de texto
IndentNav también puede ser útil para editar código fuente en muchos
lenguajes de programación.  Lenguajes como Python requieren que el código
fuente sea apropiadamente sangrado, mientras que en muchos otros lenguajes
de programación es altamente recomendado.  Con IndentNav puedes pulsar
NVDA+Alt+Flecha abajo o Flecha Arriba para saltar a la línea siguiente o
anterior con el mismo nivel de sangría.  También puedes pulsar
NVDA+Alt+Flecha izquierda para saltar a una línea padre, que es una línea
anterior con nivel de sangría menor.  En Python puedes encontrar fácilmente
la definición de la función o la definición de clase actual.  También puedes
pulsar NVDA+Alt+Flecha derecha para ir al primer hijo de la línea actual,
que es la siguiente línea con nivel de sangría mayor.

Si tu NVDA está configurado para expresar la sangría de la línea con tonos,
entonces IndentNav reproducirá rápidamente los tonos de todas las líneas
omitidas.  De lo contrario, solo cremitará para indicar aproximadamente el
número de líneas omitidas.

Teclas rápidas:

* NVDA+Alt+Flecha Arriba y Abajo: salta a la anterior o siguiente línea con
  el mismo nivel de indentación en el bloque de indentación.
* NVDA+Alt+Ctrl+Flecha Arriba o Abajo: Salto forzado a la línea anterior o
  posterior con la misma indentación. Este comando puede cambiar a
  diferentes bloques de indentación, por ejemplo, otras funciones Python.
* NVDA+Alt+Flecha izquierda: salta a la línea padre (es la línea anterior
  con menor nivel de indentación).
* NVDA*Alt+Flecha derecha: Salta a la primera línea hija (la siguiente línea
  con mayor nivel de indentación en el mismo bloque de indentación).

## Historial de liberaciones
* [v1.2](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.2.nvda-addon)
  * Añadido soporte para internacionalización.
  * Añadidos encabezados de la GPL en los archivos fuente.
  * Corecciones menores.
* [v1.1](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.1.nvda-addon)
  * Liberación inicial.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=indentnav

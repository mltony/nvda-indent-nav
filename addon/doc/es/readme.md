# IndentNav #

Este complemento permite a los usuarios de NVDA navegar por nivel de sangría
de líneas.  Mientras se edita código fuente en muchos lenguajes de
programación, permite saltar entre líneas con el mismo nivel de sangría, así
como encontrar líneas con mayor o menor nivel de sangría. También
proporciona atajos de teclado similares en las vistas en árbol.

Ten en cuenta que las órdenes de navegación por árboles se han movido al
[complemento TreeNav](https://github.com/mltony/nvda-tree-nav).

## Descarga
Instala desde la tienda de complementos de NVDA

## Nota sobre la compatibilidad con VSCode

La accesibilidad incorporada en VSCode está muy limitada: a fecha de 2024
expone sólo 500 líneas de código mediante la API de accesibilidad, lo que
provoca que IndentNav funcione en VSCode de manera incorrecta.

Por defecto, IndentNav no funcionará con VSCode. Cuando intentes usarlo,
deberás elegir entre dos opciones:

* Instalar extensión de VSCode ([página de la
  extensión](https://marketplace.visualstudio.com/items?itemName=TonyMalykh.nvda-indent-nav-accessibility))
  ([código
  fuente](https://github.com/mltony/vscode-nvda-indent-nav-accessibility)):
  la forma recomendada. Tras instalar la extensión, NVDA podrá acceder al
  documento completo, sin importar lo grande que sea.
* Continuar usando VSCode en modo heredado: activa este modo en las opciones
  de IndentNav. No se recomienda, ya que NVDA sólo verá 500 líneas del
  documento y e indicará erróneamente que faltan padres y hermanos.

## Problemas de compatibilidad

IndentNav tiene problemas de compatibilidad conocidos con el [complemento
Información del
carácter](https://addons.nvda-project.org/addons/charInfo.es.html). Es
imposible configurar IndentNav y el cursor de revisión con el bloque
numérico mientras este complemento está en ejecución. Desinstala este
complemento, o bien usa un mapa de atajos de teclado alternativo para
IndentNav.

## Disposiciones de atajos de teclado

IndentNav ofrece tres mapas de atajos de teclado incorporados:

* Disposición heredada o portátil: es para personas que usaban IndentNav
  v1.x y no quieren aprender nuevas disposiciones o para teclados de
  portátiles que no tienen bloque numérico.
* Disposición alt+bloque numérico.
* Disposición con teclas del bloque numérico. Hay dos modos de tratar con
  los conflictos con los atajos del cursor de revisión:

    * Usar el bloque numérico para IndentNav en campos editables y el cursor
      de revisión en todos los demás sitios. Si todavía necesitas usar el
      cursor de revisión en campos editables, se puede desactivar IndentNav
      temporalmente pulsando `alt+bloqueo numérico`.
    * Reasignar órdenes del cursor de revisión a alt+bloque numérico,
      evitando por tanto el conflicto de atajos.

Se puede seleccionar la disposición de atajos de teclado en las opciones de
IndentNav.

## Atajos de teclado

| Acción | Disposición heredada | Disposición de `alt+bloque numérico` | Disposición de bloque numérico | Descripción |
| -- | -- | -- | -- | -- |
| Conmutar IndentNav | `alt+bloqueo numérico` | `alt+bloqueo numérico` | `alt+bloqueo numérico` | Útil cuando tanto los gestos de IndentNav como los del cursor de revisión se asignan al bloque numérico. |
| Saltar al hermano anterior/siguiente | `NVDA+Alt+flechas arriba o abajo` | `alt+8 del teclado numérico/2 del teclado numérico` | `8 / 2 del teclado numérico` | Por hermano se entiende una línea con el mismo nivel de sangría.<br>Esta orden no llevará el cursor más allá del bloque de código actual. |
| Saltar al hermano anterior/siguiente evitando desorden | N/A | `control+alt+8 del teclado numérico/2 del teclado numérico` | `control+8 del teclado numérico/2 del teclado numérico` | Puedes configurar la expresión regular de desorden en las opciones. |
| Saltar al primer/último hermano | `NVDA+Alt+shift+flechas arriba y abajo` | `alt+4 del teclado numérico/6 del teclado numérico` | `4 del teclado numérico/6 del teclado numérico` | Por hermano se entiende una línea con el mismo nivel de sangría.<br>Esta orden no llevará el cursor más allá del bloque de código actual. |
| Saltar al anterior/último hermano potencialmente fuera del bloque actual | `NVDA+control+Alt+flechas arriba y abajo` | `control+alt+4 del teclado numérico/6 del teclado numérico` | `control+4 del teclado numérico/6 del teclado numérico` | Esta orden permite saltar a un hermano de otro bloque. |
| Saltar al padre anterior/siguiente | `NVDA+Alt+flecha izquierda`,<br>`NVDA+alt+control+flecha izquierda` | `alt+7 del teclado numérico/1 del teclado numérico` | `7 del teclado numérico/1 del teclado numérico` | Se entiende por padre una línea con nivel de sangría menor. |
| Saltar al hijo anterior/siguiente | `NVDA+Alt+control+flecha derecha`,<br>`NVDA+alt+flecha derecha` | `alt+9 del teclado numérico/3 del teclado numérico` | `9 del teclado numérico/3 del teclado numérico` | Por hijo se entiende una línea con mayor nivel de sangría.<br>Esta orden no llevará el cursor más allá del bloque de código actual. |
| Seleccionar bloque actual | `NVDA+control+i` | `control+alt+7 del teclado numérico` | `control+7 del teclado numérico` | Selecciona la línea actual, y todas las siguientes que tengan estrictamente mayor nivel de sangría.<br>Pulsa repetidamente para seleccionar varios bloques. |
| Seleccionar el bloque actual y todos los bloques siguientes con el mismo nivel de sangría | `NVDA+alt+i` | `control+alt+9 del teclado numérico` | `control+9 del teclado numérico` | Selecciona la línea actual y todas las líneas siguientes con el mismo nivel de sangría o uno superior. |
| Pegar con sangría | `NVDA+v` | `NVDA+v` | `NVDA+v` | Cuando necesites pegar un bloque de código en un lugar con nivel de sangría distinto, esta orden ajustará el nivel de sangría antes de pegar. |
| Retroceder/avanzar por el historial | N/A | `control+alt+1 del teclado numérico/3 del teclado numérico` | `control+1 del teclado numérico/3 del teclado numérico` | IndentNav conserva un historial de líneas visitadas mediante órdenes de IndentNav. |
| Verbalizar línea actual | N/A | `alt+5 del teclado numérico` | `5 del teclado numérico` | Realmente es una orden del cursor de revisión, reasignada por conveniencia. |
| Verbalizar línea padre | `NVDA+i` | N/A | N/A | |

## Otras características

### Marcadores de búsqueda rápida

IndentNav permite configurar cualquier cantidad de marcadores a los que se
puede saltar con facilidad. Un marcador se define con una expresión regular
y un atajo de teclado personalizado para saltar a una coincidencia. Pulsa
`sift+atajo` para saltar a la coincidencia anterior.

### Crepitación:

Al saltar por muchas líneas de código, IndentNav intentará reproducir
rápidamente los niveles de sangría como pitidos con las líneas
saltadas. Esta característica sólo está activada cuando se habilita indicar
sangría con tonos en las opciones de NVDA. Se puede ajustar o desactivar el
volumen de la crepitación en las opciones de IndentNav.

## Código fuente

El código fuente está disponible en
<http://github.com/mltony/nvda-indent-nav>.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=indentnav

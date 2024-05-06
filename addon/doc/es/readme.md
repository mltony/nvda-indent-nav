### IndentNav para NVDA

Este complemento permite a los usuarios de NVDA navegar por nivel de sangría de las líneas.
Mientras se edita código fuente en muchos lenguajes de programación, permite saltar entre las líneas del mismo nivel de sangría, así como encontrar rápidamente líneas con un nivel de sangría mayor o menor.
También proporciona pulsaciones de teclas similares en vistas de árbol.

## Descargar

Por favor, instala desde la tienda de complementos de NVDA.

## Nota sobre la compatibilidad con VSCode

La accesibilidad integrada en VSCode es muy limitada: a partir de 2024, solo expone 500 líneas de código a través de la API de accesibilidad, lo que hace que IndentNav funcione incorrectamente en VSCode.

De forma predeterminada, IndentNav no funcionará con VSCode y cuando intentes usarlo, tendrás que elegir entre dos opciones:

* Instalar la extensión de VSCode ([página de extensión](https://marketplace.visualstudio.com/items?itemName=TonyMalykh.nvda-indent-nav-accessibility))([código fuente](https://github.com/mltony/vscode-nvda-indent-nav-accessibility)) - método recomendado. Después de instalar la extensión, NVDA podrá acceder a todo el documento sin importar cuán grande sea.
* Continuar usando VSCode en modo heredado - habilita este modo en la configuración de IndentNav. Esto no se recomienda, ya que NVDA solo verá 500 líneas del documento y reportará erróneamente la falta de elementos hermanos/padres.

## Problemas de compatibilidad

IndentNav tiene problemas de compatibilidad conocidos con el complemento [Character Information](https://addons.nvda-project.org/addons/charInfo.en.html). Actualmente es imposible configurar tanto IndentNav como el cursor de revisión en el teclado numérico mientras se ejecuta este complemento. Por favor, desinstala este complemento o usa un mapa de teclas alternativo en IndentNav.

## Mapas de teclas

IndentNav ofrece 3 asignaciones de teclas integradas:

* Distribución heredada o para laptop: para las personas que usaban IndentNav v1.x y no quieren aprender nuevas distribuciones o para teclados de portátiles que no tienen teclado numérico.
* Distribución `Alt+numpad`.
* Distribución de teclas del teclado numérico. Hay dos modos de lidiar con el conflicto de teclas del cursor de revisión:
    * Usar el teclado numérico para IndentNav en editables y el cursor de revisión en otros lugares. Si aún necesitas usar el cursor de revisión en editables, puedes deshabilitar temporalmente IndentNav presionando `alt+numLock`.
    * Reasignar los comandos del cursor de revisión a `alt+numpad`, evitando así el conflicto de teclas.

La distribución de teclas se puede seleccionar en la configuración de IndentNav.

## Pulsaciones de teclas

| Acción | Distribución heredada | Distribución `Alt+numpad` | Distribución teclado numérico | Descripción |
| -- | -- | -- | -- | -- |
| Activar/desactivar IndentNav | `alt+numLock` | `alt+numLock` | `alt+numLock` | Útil cuando tanto NVDA como los gestos del cursor de revisión están asignados al teclado numérico. |
| Saltar al hermano anterior/siguiente | `NVDA+Alt+up/downArrow` | `alt+numPad8/numPad2` | `numPad8/numPad2` | Un hermano se define como una línea con el mismo nivel de sangría.<br>Este comando no llevará el cursor más allá del bloque de código actual. |
| Saltar al hermano anterior/siguiente, ignorando ruido | N/A | `control+alt+numPad8/numPad2` | `control+numPad8/numPad2` | Puedes configurar una expresión regular para el ruido en la configuración. |
| Saltar al primer/último hermano | `NVDA+Alt+shift+up/downArrow` | `alt+numPad4/numPad6` | `numPad4/numPad6` | Un hermano se define como una línea con el mismo nivel de sangría.<br>Este comando no llevará el cursor más allá del bloque de código actual. |
| Saltar al hermano anterior/siguiente potencialmente fuera del bloque actual | `NVDA+control+Alt+up/downArrow` | `control+alt+numPad4/numPad6` | `control+numPad4/numPad6` | Este comando te permite saltar a un hermano en otro bloque. |
| Saltar al padre anterior/siguiente | `NVDA+Alt+leftArrow`,<br>`NVDA+alt+control+leftArrow` | `alt+numPad7/numPad1` | `numPad7/numPad1` | Un padre se define como una línea con un menor nivel de sangría. |
| Saltar al hijo anterior/siguiente | `NVDA+Alt+control+rightArrow`,<br>`NVDA+alt+rightArrow` | `alt+numPad9/numPad3` | `numPad9/numPad3` | Un hijo se define como una línea con un mayor nivel de sangría.<br>Este comando no llevará el cursor más allá del bloque de código actual. |
| Seleccionar el bloque actual | `NVDA+control+i` | `control+alt+numPad7` | `control+numPad7` | Selecciona la línea actual más todas las líneas siguientes con un nivel de sangría estrictamente mayor.<br>Presiona repetidamente para seleccionar varios bloques. |
| Seleccionar el bloque actual y todos los bloques siguientes del mismo nivel de sangría | `NVDA+alt+i` | `control+alt+numPad9` | `control+numPad9` | Selecciona la línea actual más todas las líneas siguientes con un nivel de sangría mayor o igual. |
| Pegar con sangría | `NVDA+v` | `NVDA+v` | `NVDA+v` | Cuando necesites pegar un bloque de código en un lugar con un nivel de sangría diferente, este comando ajustará el nivel de sangría antes de pegar. |
| Retroceder/avanzar en el historial | N/A | `control+alt+numPad1/numPad3` | `control+numPad1/numPad3` | IndentNav mantiene un historial de líneas que visitaste a través de comandos de IndentNav. |
| Hablar la línea actual | N/A | `alt+numPad5` | `numPad5` | Esto es realmente un comando del cursor de revisión reasignado para mayor comodidad. |
| Hablar la línea padre | `NVDA+i` | N/A | N/A | |

## Otras características

### Marcadores de búsqueda rápida

IndentNav te permite configurar cualquier número de marcadores a los que puedes saltar fácilmente. Un marcador se define mediante una expresión regular y una tecla personalizada para saltar a una coincidencia. Presiona `shift+` tecla para encontrar la ocurrencia anterior.

### Sonido crepitante

Al saltar muchas líneas de código, IndentNav intentará reproducir rápidamente los niveles de sangría como tonos de las líneas omitidas. Esta función solo se habilita cuando se informa de la sangría como tonos en la configuración de NVDA. El volumen del sonido crepitante se puede ajustar o desactivar en la configuración de IndentNav.

## Código fuente

El código fuente está disponible en <http://github.com/mltony/nvda-indent-nav>.
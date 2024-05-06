# IndentNav #

* Autor: Tony Malykh
* Descargar [versión estable][1]

Este complemento permite aos usuarios do NVDA navegar por nivel de sangría
ou por intervalos de liñas ou parágrafos.  En navegadores permite atopar
parágrafos rápidamente co mesmo intervalo dende a marxe esquerda da
pantalla, como por exempro os comentarios de primeiro nivel nunha árbore
xerárquica de comentarios.  Tamén mentres se edita código fonte en moitas
linguaxes de programación, permite saltar entre as liñas do mesmo nivel de
sangría, así como atopar rápidamente liñas con maior ou menor nivel de
sangría.

## Uso en navegadores
IndentNav pode usarse para navegar por intervalos dende a marxe esquerda da
pantalla.  En particular, podes premer NVDA+Alt+Frecha Abaixo ou Frecha
Arriba para saltar ao parágrafo seguinte ou anterior que teña o mesmo
intervalo.  Por exempro, esto pode seren útil ao navegar por árbores
xerárquicas de comentarios (ex.: en reddit.com) para saltar entre
comentarios de primeiro nivel e omitir todos os comentarios de nivel
superior.

En senso estricto, IndentNav pode usarse en calquera aplicación, para a que
NVDA proporcione un interceptor do obxecto árbore.

Teclas rápidas:

* NVDA+Alt+Frecha Arriba ou Abaixo: Salta ao seguinte parágrafo co mesmo
  desprazamento.
* NVDA+Alt+Frecha Esquerda: Salta ao anterior parágrafo con menor
  desprazamento.
* NVDA+Alt+Frecha Dereita: Salta ao seguinte parágrafo con maior
  desprazamento.

## Uso en editores de texto
IndentNav tamén pode seren útil para editar código fonte en moitas linguaxes
de programación.  Linguaxes coma Python requiren que o código fonte sexa
apropiadamente sangrado, mentres que en moitas outras linguaxes de
programación é altamente recomendado.  Co IndentNav podes premer
NVDA+Alt+Frecha abaixo ou Frecha Arriba para saltar á liña seguinte ou
anterior co mesmo nivel de sangría.  Tamén podes premer NVDA+Alt+Frecha
esquerda para saltar a unha liña pai, que é unha liña anterior co nivel de
sangría menor.  En Python podes atopar sinxelamente a definición da función
ou da definición de clase actual.  Tamén podes premer NVDA+Alt+Frecha
dereita para ir ao primeiro fillo da liña actual, que é a seguinte liña co
nivel de sangría maior.

Se o teu NVDA está configurado para expresar a sangría da liña con tons,
entón IndentNav reproducirá rápidamente os tons de todas as liñas omitidas.
Pola contra, so cremitará para indicar aproximadamente o número de liñas
omitidas.

Teclas rápidas:

* NVDA+Alt+Frecha Arriba ou Abaixo: Salta á liña anterior ou posterior coa
  mesma indentación.
* NVDA+Alt+Ctrl+Frecha Arriba e Abaixo: Salto forzado á liña anterior ou
  posterior coa mesma indentación. Saltarase a outros bloques de
  indentación, como poden ser outras funcións Python, se é necesario.
* NVDA+Alt+Frecha esquerda: Salta á pai (ésta é a anterior liña con menor
  nivel de indentación).
* NVDA+Alt+Frecha dereita: Salta á primeira filla (ésta é a próxima liña con
  maior nivel de indentación).

## Historial de liberacións
* [v1.2](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.2.nvda-addon)
  * Engadido soporte para internacionalización.
  * Engadidos encabezados da GPL nos arquivos fonte.
  * Minor fixes.
* [v1.1](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.1.nvda-addon)
  * Initial release.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=indentnav

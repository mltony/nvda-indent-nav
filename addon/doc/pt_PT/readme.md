# IndentNav #

* Autor: Tony Malykh
* Baixar [versão estável][1]

Este extra permite aos utilizadores do NVDA navegar pelo nível de indentação
ou saltar entre linhas ou parágrafos. Nos navegadores, permite encontrar
rapidamente parágrafos com o mesmo deslocamento da borda esquerda do ecrã,
como comentários de primeiro nível em uma árvore hierárquica de
comentários. Além disso, ao editar o código-fonte em muitas linguagens de
programação, ele permite saltar entre as linhas do mesmo nível de
indentação, bem como encontrar rapidamente linhas com maior ou menor nível
de recuo.

## Uso em navegadores
IndentNav can be used to navigate by offset from the left edge of the
screen.  IN particular, you can press NVDA+Alt+DownArrow or UpArrow to jump
to the next or previous paragraph that has the same offset.  For example,
this can be useful when browsing hierarchical trees of comments (e.g. on
reddit.com) to jump between first level comments and skipping all the higher
level comments.

Estrictamente falando, o IndentNav pode ser usado em qualquer aplicação,
para a qual o NVDA forneça um objeto interceptor de árvore.

Teclas:

* NVDA+Alt+seta para cima ou seta para baixo: Ir para o parágrafo anterior
  ou seguinte com o mesmo deslocamento.
* NVDA+alt+seta esquerda: Salta para o parágrafo anterior com menor
  deslocamento.
* NVDA+Alt+ seta direita: vai para o próximo parágrafo com maior
  deslocamento.

## Uso em editores de texto:
O IndentNav também pode ser útil para explorar código fonte em muitas
linguagens de programação. Linguagens como o Python exigem que o
código-fonte seja correctamente indentado, enquanto em muitas outras
linguagens de programação é altamente recomendável. Com o IndentNav, pode
pressionar NVDA+Alt+seta para baixo ou seta para cima para ir para a linha
seguinte ou anterior com o mesmo nível de indentação. Também pode pressionar
NVDA+Alt+seta esquerda para ir para uma linha pai, que é uma linha anterior
com menor nível de indentação. Em Python, pode encontrar facilmente a
definição da função actual ou a definição da classe. Também pode pressionar
NVDA+Alt+seta direita para ir para o primeiro filho da linha actual, que é a
próxima linha com maior nível de indentação.

Se o seu NVDA estiver configurado para indicar a indentação de linha como
beeps, então o IndentNav reproduzirá rapidamente os beeps de todas as linhas
ignoradas. Caso contrário, ele só irá tentar denotar aproximadamente o
número de linhas ignoradas.

Teclas:

* NVDA+Alt+seta para cima ou seta para baixo: vai para a linha anterior ou
  seguinte com o mesmo nível de indentação dentro do bloco de indentação
  actual.
* NVDA+Alt+Control+seta para cima ou seta para baixo: Força-salto para a
  linha anterior ou seguinte com o mesmo nível de indentação. Este comando
  irá saltar para outros blocos de indentação (como outras funções do
  Python), se necessário.
* NVDA+alt+seta esquerda: vai para o pai: essa é a linha anterior com menor
  nível de indentação.
* NVDA+Alt+seta direita: vai para o primeiro filho - essa é a próxima linha
  com maior nível de indentação dentro do mesmo bloco de indentação.

## Histórico de lançamentos
* [v1.2] (https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.2.nvda-addon)
  * Adicionado suporte para internacionalização.
  * Adicionado cabeçalhos GPL nos ficheiros de origem.
  * Pequenas correcções.
* [v1.1] (https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.1.nvda-addon)
  * Lançamento inicial.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=indentnav

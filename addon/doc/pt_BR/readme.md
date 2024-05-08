# IndentNav #

* Autor: Tony Malykh
* Baixe a [versão estável][1]

Esse complemento permite que os usuários do NVDA naveguem por nível de recuo
(indentação) ou deslocamento de linhas ou parágrafos. Nos navegadores,
permite localizar rapidamente parágrafos com o mesmo deslocamento da borda
esquerda da tela, como comentários de primeiro nível em uma árvore
hierárquica de comentários. Além disso, ao editar código fonte em muitas
linguagens de programação, ele permite saltar entre as linhas do mesmo nível
de recuo (indentação), além de encontrar rapidamente linhas com maior ou
menor nível de recuo (endentação).

## Uso em navegadores
O IndentNav pode ser usado para navegar por deslocamento a partir da borda
esquerda da tela. Em particular, você pode pressionar NVDA+Alt+Seta Para
Baixo ou Seta Para Cima para pular para o parágrafo seguinte ou anterior que
possui o mesmo deslocamento. Por exemplo, isso pode ser útil ao navegar por
árvores hierárquicas de comentários (ex: no reddit.com) para alternar entre
comentários de primeiro nível e pular todos os comentários de nível
superior.

Estritamente falando, o IndentNav pode ser usado em qualquer aplicativo,
para o qual o NVDA forneça um objeto interceptador em árvore.

Teclas:

* NVDA+Alt+Seta Para Cima ou Seta Para Baixo: Pula para o parágrafo anterior
  ou seguinte com o mesmo deslocamento.
* NVDA+alt+Seta Esquerda: Pula para o parágrafo anterior com menor
  deslocamento.
* NVDA+Alt+Seta Direita: Pula para o próximo parágrafo com maior
  deslocamento.

## Uso em editores de texto
O IndentNav também pode ser útil para editar código fonte em muitas
linguagens de programação. Linguagens como o Python exigem que o
código-fonte seja recuado (indentado) adequadamente, enquanto em muitas
outras linguagens de programação é altamente recomendável. Com o IndentNav,
pode pressionar NVDA+Alt+Seta Para Baixo ou Seta Para Cima para pular para a
linha seguinte ou anterior com o mesmo nível de recuo. Também pode
pressionar NVDA+Alt+Seta Esquerda para pular para uma linha pai, que é uma
linha anterior com menor nível de recuo. Em Python, pode encontrar
facilmente a definição da função atual ou a definição da classe. Também pode
pressionar NVDA+Alt+Seta Direita para ir para o primeiro filho da linha
atual, que é a próxima linha com maior nível de recuo.

Se o seu NVDA estiver definido para expressar o recuo da linha como tons, o
IndentNav reproduzirá rapidamente os tons de todas as linhas puladas. Caso
contrário, Ele apenas estalará para indicar aproximadamente o número de
linhas puladas.

Teclas:

* NVDA+Alt+Seta Para Cima ou Seta Para Baixo: Pula para a linha anterior ou
  seguinte com o mesmo nível de recuo (endentação) no bloco de recuo atual.
* NVDA+Alt+Control+Seta Para Cima ou Seta Para Baixo: Pular à força para a
  linha anterior ou seguinte com o mesmo nível de recuo. Este comando irá
  pular para outros blocos de recuo (como outras funções do Python), se
  necessário.
* NVDA+alt+Seta Esquerda: Pula para pai - que é a linha anterior com menor
  nível de recuo.
* NVDA+Alt+Seta Direita: Pula para o primeiro filho - que é a próxima linha
  com maior nível de recuo dentro do mesmo bloco de recuo.

## Histórico de lançamentos
* [v1.2](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.2.nvda-addon)
  * Adicionado suporte para internacionalização.
  * Adicionado cabeçalhos GPL nos arquivos de origem.
  * Pequenas correções.
* [v1.1](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.1.nvda-addon)
  * Versão inicial.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=indentnav

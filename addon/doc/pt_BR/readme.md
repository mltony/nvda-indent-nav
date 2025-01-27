# IndentNav #

Esse complemento permite que os usuários do NVDA naveguem pelo nível de
recuo das linhas.  Ao editar o código-fonte em muitas linguagens de
programação, ele permite saltar entre as linhas do mesmo nível de recuo, bem
como localizar rapidamente linhas com nível de recuo maior ou menor.  Ele
também fornece pressionamentos de teclas semelhantes em exibições de árvore.
Esse complemento permite que os usuários do NVDA naveguem por nível de recuo
(indentação) ou deslocamento de linhas ou parágrafos. Nos navegadores,
permite localizar rapidamente parágrafos com o mesmo deslocamento da borda
esquerda da tela, como comentários de primeiro nível em uma árvore
hierárquica de comentários. Além disso, ao editar código fonte em muitas
linguagens de programação, ele permite saltar entre as linhas do mesmo nível
de recuo (indentação), além de encontrar rapidamente linhas com maior ou
menor nível de recuo (endentação).

Observe que os comandos de navegação em árvore foram movidos para [TreeNav
add-on] (https://github.com/mltony/nvda-tree-nav).

## Baixar
Instale a partir da loja de complementos do NVDA

## Observação sobre a compatibilidade com o VSCode

A acessibilidade integrada do VSCode é muito limitada: a partir de 2024, ela
expõe apenas 500 linhas de código por meio da API de acessibilidade, o que
faz com que o IndentNav funcione incorretamente no VSCode.

Por padrão, o IndentNav não funcionará com o VSCode e, quando você tentar
usá-lo, precisará selecionar entre duas opções:

* Instale a extensão VSCode ([página da
  extensão](https://marketplace.visualstudio.com/items?itemName=TonyMalykh.nvda-indent-nav-accessibility))([código-fonte](https://github.com/mltony/vscode-nvda-indent-nav-accessibility))
  - maneira recomendada. Depois de instalar a extensão, o NVDA poderá
  acessar o documento inteiro, independentemente do tamanho dele.
* Continue usando o VSCode no modo legado - ative esse modo nas
  configurações do IndentNav. Isso não é recomendado, pois o NVDA verá
  apenas 500 linhas do documento e informará erroneamente a falta de
  irmãos/pais.

## Problemas de compatibilidade

O IndentNav tem problemas de compatibilidade conhecidos com o [complemento
Character Information]
(https://addons.nvda-project.org/addons/charInfo.en.html). Atualmente, é
impossível configurar o IndentNav e o cursor de revisão no teclado numérico
enquanto esse complemento estiver em execução. Desinstale esse complemento
ou use um mapa de teclas alternativo no IndentNav.

## Layouts de teclas

O IndentNav oferece 3 mapeamentos de teclas incorporados:

* Layout legado ou de laptop: para pessoas que estavam usando o IndentNav
  v1.x e não querem aprender novos layouts ou para teclados de laptop que
  não têm numpads.
* Layout Alt+numpad.
* Layout das teclas do Numpad. Há dois modos de lidar com o conflito de
  pressionamento de tecla do cursor de revisão:

    * Use o teclado numérico para o IndentNav em editáveis e o cursor de
      revisão em todos os outros lugares. Se você ainda precisar usar o
      cursor de revisão em editáveis, poderá desativar temporariamente o
      IndentNav pressionando `alt+numLock`.
    * Remapear os comandos do cursor de revisão para alt+numpad, evitando
      assim conflitos de teclas.

O layout do pressionamento de tecla pode ser selecionado nas configurações
do IndentNav.

## Pressionamento de teclas

| Ação | Legado layout | `Alt+numpad` layout | Numpad layout | Descrição |
| -- | -- | -- | -- | -- |
| Alternar IndentNav | `alt+numLock` | `alt+numLock` | `alt+numLock` | Isso é útil quando ambos NVDA e os gestos de revisão do cursor são atribuídos ao numPad. |
| Ir para o anterior/irmão seguinte | `NVDA+Alt+cima/baixo` | `alt+numPad8/numPad2` | `numPad8/numPad2` | Irmão é definido como uma linha com o mesmo nível de recuo.<br>Esse comando não levará o cursor para além do bloco de código atual. |
| Ir para o anterior/irmão seguinte pulando a bagunça | N/A | `control+alt+numPad8/numPad2` | `control+numPad8/numPad2` | Você pode configurar a expressão regular de desordem nas configurações. |
| Ir para o primeiro/último irmão | `NVDA+Alt+shift+cima/baixo` | `alt+numPad4/numPad6` | `numPad4/numPad6` | Irmão é definido como uma linha com o mesmo nível de recuo.<br>Esse comando não levará o cursor para além do bloco de código atual. |
| Ir para o anterior/último irmão potencialmente fora do bloco atual | `NVDA+control+Alt+cima/baixo` | `control+alt+numPad4/numPad6` | `control+numPad4/numPad6` | Esse comando permite que você pule para um irmão em outro bloco. |
| Ir para o anterior/próximo pai | `NVDA+Alt+esquerda`,<br>`NVDA+alt+control+esquerda` | `alt+numPad7/numPad1` | `numPad7/numPad1` | O pai é definido como uma linha com nível de recuo inferior. |
| Pular para o filho anterior/seguinte | `NVDA+Alt+control+direita`,<br>`NVDA+alt+direita` | `alt+numPad9/numPad3` | `numPad9/numPad3` | A criança é definida como uma linha com grande

## Outros recursos

### Marcadores buscaRápida

O IndentNav permite configurar qualquer número de marcadores para os quais
você pode saltar facilmente. Um marcador é definido por uma expressão
regular e um pressionamento de tecla personalizado para saltar para uma
correspondência. Pressione a tecla `shift+` para localizar a ocorrência
anterior.

### Crackling:

Ao pular muitas linhas de código, o IndentNav tentará reproduzir rapidamente
os níveis de recuo como tons das linhas puladas. Esse recurso só é ativado
quando a indicação de recuo como tons está ativada nas configurações do
NVDA. O volume de crepitação pode ser ajustado ou desativado nas
configurações do IndentNav.

## Código-fonte

O código-fonte está disponível em
<http://github.com/mltony/nvda-indent-nav>.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=indentnav

# IndentNav #

Cette extension permet aux utilisateurs de NVDA de naviguer par niveau
d'indentation  des lignes. Lors de l'édition du code source dans de nombreux
langages de programmation, elle permet de sauter entre les lignes du même
niveau d'indentation, ainsi que de trouver rapidement des lignes avec un
niveau d'indentation plus ou moins élevé. Elle fournit également des touches
de commandes similaires dans les arborescences.

Veuillez noter que les commandes de navigation dans l'arborescence ont été
déplacées vers [l'extension
TreeNav](https://github.com/mltony/nvda-tree-nav).

## Télécharger
Veuillez installer à partir de l'add-on store de NVDA

## Remarque sur la compatibilité avec VSCode

L'accessibilité VSCode intégrée est très limitée : à partir de 2024, il
n'expose que 500 lignes de code via l'API d'accessibilité, ce qui fait
qu'IndentNav ne fonctionne pas correctement dans VSCode.

Par défaut, IndentNav ne fonctionnera pas avec VSCode et lorsque vous
essayez de l'utiliser, vous devrez choisir parmi deux options :

* Installez l'extension VSCode ([page de
  l'extension](https://marketplace.visualstudio.com/items?itemName=TonyMalykh.nvda-indent-nav-accessibility))([code
  source](https://github.com/mltony/vscode-nvda-indent-nav-accessibility)) -
  méthode recommandée. Après avoir installé l'extension, NVDA pourra accéder
  à l'intégralité du document, quelle que soit sa taille.
* Continuez à utiliser VSCode en mode hérité - activez ce mode dans les
  paramètres IndentNav. Ceci n'est pas recommandé puisque NVDA ne verra que
  500 lignes de document et signalera par erreur les enfants/parents
  manquants.

## Problèmes de compatibilité

IndentNav a des problèmes de compatibilité connus avec [l'extension
Information
caractère](https://addons.nvda-project.org/addons/charInfo.fr.html). Il est
actuellement impossible de configurer à la fois IndentNav et le curseur de
revue sur le pavé numérique pendant que cette extension est en cours
d'exécution. Veuillez soit désinstaller cette extension, soit utiliser une
autre carte de touche de commande dans IndentNav.

## Dispositions des touches de commandes

IndentNav propose 3 mappages de touches de commandes intégrés :

* Disposition héritée ou pour ordinateur portable : ceci est destiné aux
  personnes qui utilisaient IndentNav v1.x et ne souhaitent pas apprendre de
  nouvelles dispositions ou aux claviers d'ordinateurs portables qui n'ont
  pas de pavé numérique.
* Disposition Alt+pavé numérique.
* Disposition des touches du pavé numérique. Il existe deux modes de gérer
  le conflit de touche de commande du curseur de revue :

    * Utilisez le pavé numérique pour IndentNav dans les éléments
      modifiables et le curseur de revue partout ailleurs. Si vous devez
      toujours utiliser le curseur de revue dans les éléments modifiables,
      vous pouvez désactiver temporairement IndentNav en appuyant sur
      `alt+verrouillage numérique`.
    * Remappez les commandes du curseur de revue sur alt+pavé numérique,
      évitant ainsi les conflits de touche de commande.

La disposition des touches de commandes peut être sélectionnée dans les
paramètres d'IndentNav.

## Touches de commandes

| Actions | Disposition héritée | Disposition `Alt+pavé numérique` | Disposition du pavé numérique | Description |
| -- | -- | -- | -- | -- |
| Basculer IndentNav | `alt+verrouillage numérique` | `alt+verrouillage numérique` | `alt+verrouillage numérique` | Ceci est utile lorsque les gestes NVDA et du curseur de revue sont attribués au pavé numérique. |
| Aller à l'enfant précédent/suivant | `NVDA+Alt+flèche haut/bas` | `alt+PavNum8/PavNum2` | `PavNum8/PavNum2` | L'enfant est défini comme une ligne avec le même niveau d'indentation.<br>Cette commande ne déplacera pas le curseur au-delà du bloc de code actuel. |
| Aller à l'enfant précédent/suivant en ignorant le désordre | N/A | `contrôle+alt+PavNum8/PavNum2` | `contrôle+PavNum8/PavNum2` | Vous pouvez configurer l'expression régulière en désordre dans les paramètres. |
| Aller au premier/dernier enfant | `NVDA+Alt+maj+flèche haut/bas` | `alt+PavNum4/PavNum6` | `PavNum4/PavNum6` | L'enfant est défini comme une ligne avec le même niveau d'indentation.<br>Cette commande ne déplacera pas le curseur au-delà du bloc de code actuel. |
| Aller à l'enfant précédent/dernier potentiellement en dehors du bloc actuel | `NVDA+contrôle+Alt+flèche haut/bas` | `contrôle+alt+PavNum4/PaVNum6` | `contrôle+PaVNum4/PaVNum6` | Cette commande vous permet de Aller à un enfant dans un autre bloc. |
| Aller au parent précédent/suivant | `NVDA+Alt+Flèche gauche`,<br>`NVDA+alt+contrôle+Flèche gauche` | `alt+PavNum7/PavNum1` | `PavNum7/PavNum1` | Le parent est défini comme une ligne avec un niveau d'indentation inférieur. |
| Aller à l'enfant précédent/suivant | `NVDA+Alt+contrôle+Flèche droite`,<br>`NVDA+alt+Flèche droite` | `alt+PavNum9/PavNum3` | `PavNum9/PavNum3` | L'enfant est défini comme une ligne avec un niveau d'indentation plus élevé.<br>Cette commande ne déplacera pas le curseur au-delà du bloc de code actuel. |
| Sélectionner le bloc actuel | `NVDA+contrôle+i` | `contrôle+alt+PavNum7` | `contrôle+PavNum7` | Sélectionne la ligne actuelle ainsi que toutes les lignes suivantes ayant un niveau d'indentation strictement supérieur.<br>Appuyez à plusieurs reprises pour sélectionner plusieurs blocs. |
| Sélectionnez le bloc actuel et tous les blocs suivants sur le même niveau d'indentation | `NVDA+alt+i` | `contrôle+alt+PavNum9` | `contrôle+PavNum9` | Sélectionne la ligne actuelle ainsi que toutes les lignes suivantes ayant un niveau d'indentation supérieur ou égal. |
| Coller l'indentation | `NVDA+v` | `NVDA+v` | `NVDA+v` | Lorsque vous devez coller un bloc de code à un endroit avec un niveau d'indentation différent, cette commande ajustera le niveau d'indentation avant de le coller. |
| Aller en arrière/en avance dans l'historique | N/A | `contrôle+alt+PavNum1/PavNum3` | `contrôle+PavNum1/PavNum3` | IndentNav conserve un historique des lignes que vous avez visitées via les commandes IndentNav. |
| Annoncer la ligne actuelle | N/A | `alt+PavNum5` | `PavNum5` | Il s’agit en réalité d’une commande du curseur de revue remappée pour plus de commodité. |
| Annoncer la ligne parent | `NVDA+i` | N/A | N/A | |

## Autres caractéristiques

### Recherche rapide de signets

IndentNav vous permet de configurer n'importe quel nombre de signets
auxquels vous pouvez facilement accéder. Un signet est défini par une
expression régulière et une touche de commande personnalisée pour accéder à
une correspondance. Appuyez sur la touche de commande `maj+` pour rechercher
l'occurrence précédente.

### Crépitement :

Lorsque vous sautez sur plusieurs lignes de code, IndentNav essaiera de lire
rapidement les niveaux d'indentation au fur et à mesure des tonalités des
lignes sautées. Cette fonctionnalité n'est activée que lorsque l'annonce
d'indentation par des tonalités est activée dans les paramètres NVDA. Le
volume des crépitements peut être ajusté ou désactivé dans les paramètres
d'IndentNav.

## Code source

Le code source est disponible sur
<http://github.com/mltony/nvda-indent-nav>.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=indentnav

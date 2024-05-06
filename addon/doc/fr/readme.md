# IndentNav #

* Auteur : Tony Malykh
* Télécharger [version stable][1]

Cette extension permet aux utilisateurs de NVDA de naviguer par niveau
d'indentation ou par décalage de lignes ou de paragraphes. Dans les
navigateurs, elle permet de trouver rapidement des paragraphes ayant le même
décalage par rapport au bord gauche de l'écran, tels que des commentaires de
premier niveau dans un arbre hiérarchique de commentaires. Aussi lors de
l'édition du code source dans de nombreux langages de programmation, elle
permet de sauter entre les lignes du même niveau d'indentation, ainsi que de
trouver rapidement des lignes avec un niveau d'indentation plus ou moins
élevé.

## Utilisation dans les navigateurs
IndentNav peut être utilisé pour naviguer par décalage depuis le bord gauche
de l'écran. En particulier, vous pouvez appuyer sur NVDA+Alt+FlècheBas ou
FlècheHaut pour aller au paragraphe suivant ou précédent qui a le même
décalage. Par exemple, cela peut être utile lorsque vous parcourez des
arborescences hiérarchiques de commentaires (par exemple sur reddit.com)
pour sauter entre le premier niveau et ignorer tous les commentaires de
niveau supérieur.

Strictement parlant, IndentNav peut être utilisé dans n'importe quelle
application, pour laquelle NVDA fournit un objet d'intercepteur
d'arborescence.

Touches de commandes :

* NVDA+Alt+FlècheHaut ou FlècheBas : Aller au paragraphe précédent ou
  suivant avec le même décalage.
* NVDA+alt+FlècheGauche : Aller au paragraphe précédent avec un décalage
  inférieur.
* NVDA+Alt+FlècheDroite : Aller au paragraphe suivant avec un décalage
  supérieur.

## Utilisation dans les éditeurs de texte
IndentNav peut également être utile pour éditer le code source dans de
nombreux langages de programmation. Les langages comme Python nécessitent
que le code source soit correctement mis en retrait, alors que dans beaucoup
d'autres langages de programmation, c'est fortement recommandé. Avec
IndentNav vous pouvez appuyer sur NVDA+Alt+FlècheBas ou FlècheHaut pour
aller à la ligne suivante ou précédente avec le même niveau
d'indentation. Vous pouvez également appuyer sur NVDA+Alt+FlècheGauche pour
aller à une ligne parente, c'est-à-dire une ligne précédente avec un niveau
d'indentation inférieur. En Python, vous pouvez facilement trouver la
définition de la fonction en cours ou la définition de la classe. Vous
pouvez également appuyer sur NVDA+Alt+FlècheDroite pour aller au premier
enfant de la ligne en cours, c'est-à-dire la ligne suivante avec un niveau
d'indentation supérieur.

Si votre NVDA est configuré pour exprimer l'indentation de ligne comme des
tonalités, alors IndentNav jouera rapidement les tonalités de toutes les
lignes sautées. Sinon, il ne crépitera que pour indiquer approximativement
le nombre de lignes sautées.

Touches de commandes :

* NVDA+Alt+FlècheHaut ou FlècheBas : Aller à la ligne précédente ou suivante
  avec le même niveau d'indentation dans le bloc d'indétnation en cours.
* NVDA+Alt+Contrôle+FlècheHaut ou FlècheBas : Force-saute à la ligne
  précédente ou suivante avec le même niveau d'indentation. Cette commande
  va sauter vers d'autres blocs d'indentation (tels que d'autres fonctions
  Python) si nécessaire.
* NVDA+alt+FlècheGauche : Aller au parent - c'est la ligne précédente avec
  un niveau d'indentation moindre.
* NVDA+Alt+FlècheDroite : Aller au premier enfant - c'est la prochaine ligne
  avec un plus grand niveau d'indentation dans le même bloc d'indentation.

## Historique des versions
* [v1.2](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.2.nvda-addon)
  * Ajout du support pour l'internationalisation.
  * Ajout des en-têtes GPL dans les fichiers source.
  * Corrections mineures.
* [v1.1](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.1.nvda-addon)
  * Première version.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=indentnav

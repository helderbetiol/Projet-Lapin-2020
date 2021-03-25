# Projet Lapin - Traitement des données

## Comment utiliser nos fichiers ?

### Objectif
Ce projet implemente en langage Cpp, permet d’étudier un problème de simulation d’un écosystème composé de
bestioles. Vous trouverez une description détaillée de ce problème dans le fichier intitulé Simulation Ecosystème. À
partir du besoin exprimé dans ce document, nous avons réalisé une modélisation de la solution envisagée au travers
de designs patterns pour modéliser certains aspects statiques et dynamiques de la simulation demandée. L’analyse
du besoin peut être trouvée dans le document suivant Analyse Besoin.

## Fonctionnemment
Pour exécuter la programme vous devez télécharger le répertoire et exécuter la commande :

make clean
make exec

Cela va permettre de construire tout le répertoire et les différents fichiers binaires pour exécuter le programme, et
à la fin va exécuter le programme. Grâce à l’automatisation du Makefile, il n’est pas nécessaire de mettre tous
les arguments d’entrée à la main et les recopier à chaque fois que l’on veut exécuter le programme. C’est donc
recommandé d’utiliser le Makefile pour modifier les arguments d’entrée et exécuter le programme.
Les différents arguments sont détaillés plus en profondeur ci-dessous :

[0] nbBestioles : Nombre de bestioles totales. Nombre entier.
- x100Personnalites : Pourcentages de chaque type de Bestiole (selon son comportement). C’est un vecteur
de taille 5. Les valeurs sont données comme pourcentage (entre 0 et 100 par exemple) :


[1] %Population Grégaire.
[2] %Population Peureuse.
[3] %Population Kamikaze.
[4] %Population Prévoyante.
[5] %Population Personnalités Multiples.

Les suivantes sont couples de paramètres qui représentent les limites ([maximum] et [minimum]) des différentes
variables :

[6][7] : Champ anguler de détection pour les yeux. Valeurs en dégrées.
[8][9] : Distance de détection pour les yeux. Valeurs en nombre de pixels.
[10][11] : Capacité de détection pour les yeux. Valeurs entre 0 et 1.
[12][13] : Distance de perception pour les oreilles. Valeurs en nombre de pixels.
[14][15] : Capacité de perception pour les oreilles. Valeurs entre 0 et 1.
[16] : Coefficient d’augmentation maximum sur la vitesse pour les nageoires. Valeurs double avec un décimale
de précision.
[17][18] : Capacité de camouflage pour le camouflage. Valeurs entre 0 et 1.
[19] : Coefficient maximum de résistance aux collisions pour la carapace. Valeur double avec un décimale de précision.
[20] : Coefficient maximum de ralentissement de la vitesse pour la carapace. Valeur double avec un décimale de précision.
[21] : Probabilité de mort dans le cas de collision pour une bestiole. Probabilité donnée entre 0 et 1.
[22] : Distance à laquelle est considérée une collision entre deux bestioles. Valeur en nombre de pixels.
[23] : Valeur maximum pour la durée de vie d’une bestiole. Valeur entier qui représente nombre de pas de simulation.
[24] : Probabilité de qu'une bestiole fasse de clonage un cycle. Probabilité donnée entre 0 et 1.


Projet-Bestioles-Corrigés - Groupe2

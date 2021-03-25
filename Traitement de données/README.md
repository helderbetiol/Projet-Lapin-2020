# Projet Lapin - Traitement des données

## Comment utiliser nos livrables ?

Ce répertoire permet de traiter les données transmises par les étudiants de vétérinaire lors de ces TPs. Ce répertoire consiste en 5 fichiers : main.py, importationData.py, correction.py, affichageCourbes.py et csv2influx.py.

Pour l'exécuter nous vous suggérons d'abord créer un dossier avec toutes les fichiers .txt qui contiennent les différents fichiers à traiter. Nous vous recommandons aussi d'avoir un dossier à part où seront sauvegardés les fichiers traités.

Pour faire le traitement il suffit d'exécuter le fichier main.py. Les différents modes vont définir quel comportement va être exécuté. Les modes possibles sont : Imp, Correct et Affich.

## main.py

Voici la liste d'arguments d'entrée qui peuvent être utilisés pour exécuter le main.py:


### --mode (type=str, required=True)

Mode d'exécution du programme. Il y a 3 possibles valeurs: 
  - 'Imp' : Importe les données, les séparent par séquence, enlève les séquences illogiques (telles que plusieurs débuts), et finalement les transforme en fichiers .csv. Ce mode crée 3 types de fichiers, un fichier .csv avec toutes les séquences (son nom inclu le mot "complet"), un fichier .txt qui met en relation le nom d'une séquence avec l'ordre d'exécution (par exemple la séquence 0 généralement est "démarrage"), et finalement plusieurs fichiers .csv avec les différentes séquences, et només selon l'ordre d'apparition de la séquence (par exemple séquence0).
  - 'Correct' : Corrige les données dans un fichier .csv. Les intervalles pour les données ont été fournis par une experte et se trouvent à l'intérieur du code. Un point d'amélioration serait de les données comme paramètres d'entrée.
  - 'Affich' permet d'afficher une variable particulière d'un fichier .csv spécifique.

### --pathin (type=str, required=False)

Chemin où se trouvent les fichiers à traiter. Celui-ci peut-être un fichier ou un dossier en dépendant du mode choisi. Par défaut est "./data/Source"

### --pathout (type=str, required=False)

Chemin où se stockent les fichiers traités. Celui-ci est toujours un dossier. Par défaut est "./data/Sortie"

### --varex (type=str, required=False)

C'est la variable à éxaminer et être affichée. N'est applicable que dans le mode "Affich". Par défaut est "Frequence Respiratoire".

### --step (type=int, required=False)

Pas de réchantillonage pour l'affichée. N'est applicable que dans le mode "Affich". Par défaut est 0.1.

### --oristep (type=int, required=False)

Pas d'échantillonage des données, c'est-à-dire, la periode de temps entre chaque échantillon d'un fichier. N'est applicable que dans le mode "Affich". Par défaut est 0.001.

### --sommaire (type=str, required=False)

Nom de la colonne de sommaire des données pour l'affichée. N'est applicable que dans le mode "Affich". Par défaut est "Temps".

### -vars (type=int, required=False, nargs=7)

Nom des différentes variables qui se trouvent dans l'en-tête à générer. N'est applicable que dans le mode "Imp". By default it will be ['Temps', 'PressionArterielle', 'Spirometrie', 'PAmoyenne', 'FrequenceCardiaque', 'FrequenceRespiratoire', 'Remarque'].

## Fonctionnement des modes

### Importation ("Imp")

Pour ce mode vous devez fournir obligatoirement le paramètre --mode. Par contre, il est recommandé de fournir aussi le --pathin et le --pathout. --pathin fait référence à un dossier où se trouvent toutes les fichiers à traiter. --pathout doit être un dossier où se stockeront les fichiers traités en sous-dossieurs produits pour le programme même.

De plus, vous pouvez fournir le paramètre -vars pour spécifier les variables et leur ordre dans l'en-tête.

Ex : 

´python main.py --mode "Imp" --pathin "C:\Users\Projet\Data\Source" --pathout "C:\Users\Projet\Data\Sortie" -vars "Temps" "PressionArterielle" "Spirometrie" "PAmoyenne" "FrequenceCardiaque" "FrequenceRespiratoire" "Remarque"´

### Correction ("Correct")

Pour ce mode vous devez fournir obligatoirement le paramètre --mode. Par contre, il est recommandé de fournir aussi le --pathin. --pathin fait référence au dossier à un dossier où se trouvent les différents sous-dossiers qui stockent les données déjà importées préalablement par le mode "Imp".

De plus, vous pouvez changer directement dans le code les valeurs par défaut qui définiront la première valeur d'une séquence. Comme point d'amélioration, ces valeurs par défaut pourrient être données par l'utilisateur.

Ex : 

´python main.py --mode "Correct" --pathin "C:\Users\Projet\Data\Sortie" ´

### Affichage ("Affich")

Pour ce mode vous devez fournir obligatoirement le paramètre --mode. Par contre, il est recommandé de fournir aussi le --pathin, --sommaire et --varex. --pathin fait référence à un fichier .csv. --sommaire est le sommaire qui détermine la valeur de l'axe "x" dans la graphique. --varex détermine la variable à examiner et qui correspond à celle de l'axe "y".

Comme point d'amélioration, les autres valeurs peuvent être inclus dans l'algorithme d'affichage.

Ex : 

´python main.py --mode "Affiche" --pathin "C:\Users\Projet\Data\Sortie\data-groupe9\Corrigees\data-groupe9_Sequence6_Corrigee.csv" --sommaire "Temps" --varex "PAmoyenne"´


## csv2python

Ce fichier envoie les données en format .csv vers la base de données InfluxDB dans le format influx.

### --host (type=str, required=False)

Hostname de InfluxDB http API.

### --port (type=int, required=False)

Porte de InfluxDB http API.

### --user (type=str, required=False)

Utilisateur de InfluxDB.

### --password (type=str, required=False)

Mot de passe de InfluxDB.

### --dbname (type=str, required=False)

Base de données à utiliser ou créer.

### --file (type=str, required=False)

Fichier CSV à partir duquel les données seront lues.

### --path (type=str, required=False)

Dossier avec fichiers CSV à partir duquel les données seront lues.

### --measure (type=str, required=True)

Mesures : adrenaline, acetylcholine, rest, etc.

### --group (type=int, required=True)

ID de groupe qu'identifie un lapin unique.

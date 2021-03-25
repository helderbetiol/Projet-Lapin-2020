from time import time
import os
import json
import argparse
import pandas as pd
import importationData as imp_data
import matplotlib.pyplot as plt
import affichageCourbes as affichage
import correction

path_actuel_def = os.getcwd()
path_entree_def = path_actuel_def + "\\data\\Source"
path_sortie_def = path_actuel_def + "\\data"
variables = ['Temps', 
            'PressionArterielle', 
            'Spirometrie', 
            'PAmoyenne', 
            'FrequenceCardiaque', 
            'FrequenceRespiratoire', 
            'Remarque']

default_values = {'FrequenceCardiaque' : [180], 
                'FrequenceRespiratoire' : [40]}
"""
importation_donnees(path_entree, path_data_output, variables)

Inputs:     path_entree : Chemin où ils se trouvent les fichiers à traiter.
            path_data_output : Chemin où se stockeront les fichiers modifiés.
            variables : Différentes variables des en-têtes.

Cette méthode scanée tous les fichiers à l'intérieur de path_entree et les
prépare pour être traités en enlévant les lignes sans données, les essais qui ne
font pas partie de la séquence et divise aussi l'ensemblle de données en 
différentes fichiers sélon les injections apliquées. Finalement, tout est 
sauvegardé sur des fichiers .csv.
"""
def importation_donnees(path_entree, path_data_output, variables):
    if not(os.path.isdir(path_entree)):
        print(f"There is not folder {path_entree} with the files to process. \
The program will finish")
        exit()
    else:
         _, file_list = imp_data.scan_dir(path_entree)

    title = "\t".join(variables) + "\n"
    for element in file_list:
        file = open(f"{path_entree}\\{element}", 'r')
        file_name = element.rsplit(".", 1)[0]  # Nom du fichier sans l'extension (.txt, etc)
        path_sortie = imp_data.dir_exists(path_data_output, file_name)
        print(f"Fichier {file_name} en traitement")
        imp_data.import_data(file, path_sortie, title, file_name)


"""
correction_donnees(path_data)

Inputs:     path_data : Chemin où se trouvent les fichier à corriger.

Cette méthode corrige les valeurs exceptionnelles pour les variables 
Frequence cardiaque et fréquence respiratoire des fichier à l'intérieur de
path_data. 
"""
def correction_donnees(path_data, def_val):
    for chemin, dossier, fichier in os.walk(path_data):
        if (chemin!=path_data):
            time1 = time();
            correction.correction(chemin, fichier, def_val)
            print(f'Demoró proceso: {time() - time1}')


"""
affichage_donnees(path, sommaire, var_etudiee)

Inputs:     path : Chemin vers le fichier où se trouvent les données à afficher
            sommaire : Nom du champs qui indèxe les données (ex: temps, id, etc)
            var_etudiee : Nom du champ à afficher.

Cette méthode permet d'afficher une variable var_etudiee du fichier dans path
pour voir son commportement. La variable est graphiquée dans un plot de 
sommaire vs var_etudiee. De plus, il montre les points où il y a une remarque.
"""
def affichage_donnees(path, sommaire, var_etudiee):
    data = pd.read_csv(path)
    print("Données lues")
    z = []
    null_vec = data["Remarque"].isnull()
    z = [data[sommaire][i] for i in range(len(data["Remarque"])) if not(null_vec[i])]
    print("En train de graphiquer")
    fig, ax = plt.subplots()
    title = f"{var_etudiee} vs {sommaire}"
    affichage.afficher( ax, 
                        data[sommaire], 
                        data[var_etudiee], 
                        sommaire, 
                        var_etudiee, 
                        title)
    [ax.axvline(x=i, color='r') for i in z]
    plt.show()

"""
parse_args()

Cette fonction établisse les arguments d'entrée par console.
"""
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, required=True,
                        dest='mode',
                        help="Mode d'exécution du programme. 'Imp' importe les\
données et les séparent par séquence. 'Correct' Corrige les données dans un \
fichier .csv. 'Affich' permet d'afficher une donnée particulière d'une \
fichier spécifique.")
    parser.add_argument('--pathin', type=str, required=False,
                        default=path_entree_def,
                        dest='pathin',
                        help="Chemin où se trouvent les fichiers à traiter")
    parser.add_argument('--pathout', type=str, required=False, 
                        default=path_sortie_def,
                        dest='pathout',
                        help="Chemin où les données traitées seront déposées")
    parser.add_argument('--varex', type=str, required=False, 
                        default='FrequenceRespiratoire', 
                        dest='varex',
                        help="Variable pour éxaminer et être affichée")
    parser.add_argument('--step', type=int, required=False, default=0.1,
                        dest='step',
                        help="Pas de réchantillonage")
    parser.add_argument('--oristep', type=int, required=False, default=0.001,
                        dest='oristep',
                        help="Pas d'échantillonage des données")
    parser.add_argument('--sommaire', type=str, required=False, default="Temps",
                        dest='sommaire',
                        help="Nom de la colonne de sommaire des données")
    parser.add_argument('-vars',
                        metavar=("Variables de l'en-tête"),
                        type=str,
                        nargs=7,
                        default=variables,
                        dest='variables',
                        help=f"Nom des différentes variables qui se trouvent \
                        dans l'en-tête à générer. By default it will \
                        be {variables}.")
    """parser.add_argument('--defvals',
                        metavar=("Valeurs par défaut des variables"),
                        type=str,
                        dest='default_values',
                        help=f"Valeur par défaut des différentes variables qui \
                        seront corrigées. By default it will be {default_values}.")"""
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    path_entree = args.pathin + "\\"
    path_sortie = args.pathout + "\\"
    if args.pathout==path_sortie_def:
        path_sortie = imp_data.dir_exists(path_sortie_def, "Sortie")
    variables = args.variables
    def_val = default_values
    print(f'Valeurs par défaut: {def_val}')
    time0 = time();
    if args.mode == "Imp":
        importation_donnees(path_entree, path_sortie, variables)
    elif(args.mode == "Correct"):
        if args.pathin==path_entree_def:
            path_entree = imp_data.dir_exists(path_sortie_def, "Sortie")
        correction_donnees(path_entree, def_val)
    elif(args.mode == "Affich"):
        fichier = path_entree[:-1]
        sommaire = args.sommaire
        var_etudiee = args.varex
        affichage_donnees(fichier, sommaire, var_etudiee)
    else:
        print("Vous avez choisi un mode invalide. Vous pouvez utiliser --help \
si vous avez de questions et essayez à nouveau.")

    print(f'Cela a pris : {time() - time0}')

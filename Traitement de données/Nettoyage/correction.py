# coding: utf-8

import os
import pandas as pd
import numpy as np
import importationData as imp_data


"""
correction_valeurs_absurdes(db_entree, var_def)

Inputs:     db_entree : Base des données à corriger.
            var_def : Un dictionnaire avec les valeurs par défaut pour 
                      initialiser les séquences.
Outputs:    db_entree : Base des données corrigée.
            _last_values : Valeurs finales de la séquence.

Cette méthode corrige les valeurs de la fréquence cardiaque et respiratoir
pour les données en 'db_entree'. Il faut fournir 'var_def' pour initialiser les
premières valeurs de la séquence. À la fin, le programme retourne la base de 
données corrigée et les dernières valeurs de la séquence. De cette manière,
les valeurs pour la prochaine séquence seront accordes avec celles de la 
séquence précedante.
"""
def correction_valeurs_absurdes(db_entree, var_def):
    taille = db_entree['Temps'].size
    db_entree['FrequenceCardiaque'][0] = var_def['FrequenceCardiaque'][0]
    db_entree['FrequenceRespiratoire'][0] = var_def['FrequenceRespiratoire'][0]
    for i in range(1, taille):
        if (i == 10):
            print("Llegó a los 10")
        elif(i % 1000000 == 0):
            print("Vamos con un mega más")
        freq_card = db_entree['FrequenceCardiaque'][i]
        freq_resp = db_entree['FrequenceRespiratoire'][i]
        if ((freq_card < 30) or (freq_card > 300)):
            db_entree['FrequenceCardiaque'][i] = db_entree['FrequenceCardiaque'][i-1]
        if ((freq_resp < 10) or (freq_resp > 100)):
            db_entree['FrequenceRespiratoire'][i] = db_entree['FrequenceRespiratoire'][i-1]
    _last_values = [db_entree['FrequenceCardiaque'][i], db_entree['FrequenceRespiratoire'][i]]
    return db_entree, _last_values

"""
correction(path, file_list, var_def)

Inputs:     path : Chemin où se trouvent les séquence d'un même groupe.
            file_list : Une liste avec le nom de tous les fichiers.
            var_def : Un dictionnaire avec les valeurs par défaut pour 
                      initialiser les séquences.
Outputs:    Cette méthode ne retourne rien.

Cette méthode parcour la liste 'file_liste', charge les fichiers et les 
corrige. Comme c'est supposé que les fichiers font partie d'un même groupe,
il va remplacer les premières valeurs d'une séquence avec les dernières de la
séquence précédente. Pour le premier fichier de la liste, les premières valeurs
prennent la valeur de 'var_def'. Les fichiers corrigés seront mis sur le chemin
"'path'/Corrigées".
"""
def correction(path, file_list, var_def):
    # Initialisation
    nb_fichiers_totales = len(file_list)
    nb_fichiers_traitees = 1
    # Correction dataframe par dataframe

    for file in file_list:
        if (".csv" in file):
            path_sortie = imp_data.dir_exists(path+"\\", "Corrigées")
            df = pd.read_csv(f"{path}\\{file}", encoding='utf-8-sig')
            print(f"Fichier {file} en traitement")
            data_a_corriger = df
            _, last_values = correction_valeurs_absurdes(data_a_corriger, var_def)
            data_a_corriger.to_csv(f"{path_sortie}\\Corrigee-{file}", index=False)
            var_def['FrequenceCardiaque'][0] = last_values[0]
            var_def['FrequenceRespiratoire'][0] = last_values[1]

            # Affichage de l'avancement
            avancement = nb_fichiers_traitees / nb_fichiers_totales * 100
            print(f"Avancement actuel : {avancement}% effectué")
            nb_fichiers_traitees += 1



# coding: utf-8

import os
import io
import pandas as pd
import argparse
import importationData as imp_data
import affichageCourbes as affichage
import correction



path1 = os.getcwd()
path_entree = path1 + "\\data\\data-groupes\\"
path_data_output = path1 + "\\data\\"
var_etudiee = 'PressionArterielle'
pas = 0.1
pas_echantillonage = 0.001
sommaire = "Temps"

variables = ['Temps', 
            'PressionArterielle', 
            'Spirometrie', 
            'PAmoyenne', 
            'FrequenceCardiaque', 
            'FrequenceRespiratoire', 
            'Remarque']

# Récupère les données brutes et les sépare par groupe, séquence et injection.
imp_data.import_data(path_entree, path_data_output, variables)

# Affiche les données échantillonées "pas" fois de la variable "var_etudiee"

dir_list, file_list = imp_data.scan_dir(path_data_output)[0]

for chemin, dossier, fichier in os.walk(path_data_output):
    if (chemin!=path_data_output):
        donnees_corrigees = correction.correction(chemin, fichier)
        x, y = affichage.calculer(  donnees_corrigees, 
                                    var_etudiee, 
                                    pas, 
                                    sommaire=sommaire, 
                                    pas_echantillonage=pas_echantillonage)
        titre = file.split("_Seq")[1].split("_")[1]
            affichage.afficher(x, y, 'Temps en secondes', var_etudiee, titre)
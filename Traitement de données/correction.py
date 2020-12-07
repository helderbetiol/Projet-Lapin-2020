
# coding: utf-8

# # Fonction corrections

# A faire : réflexion sur quoi faire, fonction décaler l'injection

# Imports utiles 


import os
import pandas as pd
import numpy as np
import importationData as imp_data


# Fonction qui corrige les valeurs impossible pour une dataframe entiere : a accélérer si possible

def correction_valeurs_absurdes(new_df, old_df):

    # Correction de la première ligne
    
    if not old_df.empty :

        n_old = old_df['Temps'].size # longueur de la df précendentes

        # on enregistre les valeurs utiles
        new_freqCardiaque = new_df['FrequenceCardiaque'][0]
        old_freqCardiaque = old_df['FrequenceCardiaque'][n_old-1]
        new_freqRespiratoire = new_df['FrequenceRespiratoire'][0]
        old_freqRespiratoire = old_df['FrequenceRespiratoire'][n_old-1]

        # Freq Cardiaque

         #Cas ou bornes dépassées
        if new_freqCardiaque > 350 or new_freqCardiaque < 100:
            new_df['FrequenceCardiaque'][0] = old_freqCardiaque

        # Cas ou trop gros bon : enlevé pour l'instant car mauvais résultats

        # Freq respiratoire :
        if new_freqRespiratoire > 70 or new_freqRespiratoire < 20:
            new_df['FrequenceRespiratoire'][0] = old_freqRespiratoire
    
    else: # Cas ou c'est le premier fichier : si il est hors des bornes, on ne lui attribue pas de valeur
        new_freqCardiaque = new_df['FrequenceCardiaque'][0]
        new_freqRespiratoire = new_df['FrequenceRespiratoire'][0]
        if new_freqCardiaque > 350 or new_freqCardiaque < 100 :
            new_df['FrequenceCardiaque'][0] = np.nan


    # Correction des lignes suivantes  :

    n_new = new_df['Temps'].size

    for row in range(1, n_new):

        if row == 10:
            print("Llegó a los 10")
        elif(row == 100):
            print("Llegó a los 100")
        elif(row == 1000):
            print("Llegó a los 1000")
        elif(row%1000000 == 0):
            print("Vamos con un mega más")
        # Données utile
        old_freqCardiaque = new_freqCardiaque
        new_freqCardiaque = new_df['FrequenceCardiaque'][row]
        old_freqRespiratoire = new_freqRespiratoire
        new_freqRespiratoire = new_df['FrequenceRespiratoire'][row]

        # Freq Cardiaque

         #Cas ou bornes dépassées
        if new_freqCardiaque > 350 or new_freqCardiaque < 100:
            new_df['FrequenceCardiaque'][row] = old_freqCardiaque

        # Cas ou trop gros bon : enlevé pour l'instant car mauvais résultats

        # Freq respiratoire :

        if new_freqRespiratoire > 70 or new_freqRespiratoire < 20:
            new_df['FrequenceRespiratoire'][row] = old_freqRespiratoire
    return new_df


# Fonction qui prend un path et qui importe puis applique les fonctions

# ### Correction :

def correction(path, file_list):
    # Initialisation
    data_a_corriger = pd.DataFrame()
    nb_fichiers_totales = len(file_list)
    nb_fichiers_traitees = 1

    # Correction dataframe par dataframe

    for file in file_list:
        if (".csv" in file):
            path_sortie = imp_data.dir_exists(path, "Corrigées")
            df = pd.read_csv(f"{path}\\{file}", encoding='utf-8-sig')
            data_corrigee = data_a_corriger
            data_a_corriger = df
            correction_valeurs_absurdes(data_a_corriger, data_corrigee)
            data_a_corriger.to_csv(f"{path_sortie}\\Corrigee-{file}", index=False)

            # Affichage de l'avancement
            avancement = nb_fichiers_traitees / nb_fichiers_totales * 100
            print(f"Avancement actuel : {avancement}% effectué")
            nb_fichiers_traitees += 1


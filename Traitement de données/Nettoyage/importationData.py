import os
import io
import pandas as pd

"""
scan_dir(path)

Inputs:     path : Chemin à parcourir.
Outputs:    dir_list : Liste de dossiers dans path.
            file_list : Liste de fichiers dans path.

Examine tous les éléments dans path et retourne une liste avec les dossiers et
une autre avec les fichiers.
"""
def scan_dir(path):
    with os.scandir(path) as temp:
        file_list = []
        dir_list = []
        for element in temp:
            if os.path.isfile(element):
                file_list.append(element.name)
            if os.path.isdir(element):
                dir_list.append(element.name)
    return dir_list, file_list

"""
dir_exists(path, directory)

Inputs:     path : Chemin où on veut avoir un dossier.
            directory : Dossier d'intérêt.
Outputs:    path_sortie : Chemin avec le dossier d'intérêt.

Parcours le chemin path et vérifie l'existence du dossier directory. Si 
directory n'existe pas, il sera crée.
"""
def dir_exists(path, directory):
    dir_list, _ = scan_dir(path)
    path_sortie = path + directory + "\\"
    if not(directory in dir_list):
        os.mkdir(path_sortie)
    return path_sortie

"""
save_file(content, path, name)

Inputs:     content : Le contenu du fichier
            path : Chemin où se gardera le fichier.
            name : Le nom du fichier avec le format.

Sauvegarde le content dans un fichier csv, dans le dossier path et avec le nom
name. Name dois finir avec le format du fichier, i.e. ".csv".
"""
def save_file(content, path, name):
    new_file = io.StringIO(content)
    new_df = pd.read_table(new_file, decimal = ",")
    new_df.to_csv(path + name, index=False)


"""
import_data(file, path_sortie, title)

Inputs:     file : Fichier à parcourir.
            path_sortie : Le chemin où se stockeront les fichiers modifiés.
            title : Les en-têtes des fichiers.
            file_name : Nom base du fichier de sortie.

Parcour le fichier file en enlévant les lignes sans données, les essais qui ne
font pas partie de la séquence et divise aussi l'ensemblle de données en 
différentes fichiers sélon les injections apliquées. Finalement, tout est 
sauvegardé sur des fichiers .csv.
"""
def import_data(file, path_sortie, title, file_name):
    num_injection = 0
    new_string_seq = title
    new_string_comp = title
    injection_name = "Demarrage"
    sequence_file = ""
    finish_string = False   #Signale quand plusieurs lignes non numérqiues continues sont passées
    for ligne in file:
        if ligne[0].isalpha():            
            if finish_string:
                print("On a une nouvelle essai !")
                finish_string = False
        else:
            if "#" in ligne:                
                sequence_file += f"Seq {num_injection} = {injection_name}\n"
                new_path = f"{file_name}_Seq{num_injection}.csv"
                save_file(new_string_seq, path_sortie, new_path)

                injection = ligne.rpartition("#")[-1]  #On récupère le nom de l'injection après le #
                char_injection = [i for i in injection if i.isalpha()]  #On obtien le characters alphabetiques
                injection_name = injection[injection.find(char_injection[0]):len(injection)].rstrip(" \n")  #On récupère le nom de l'injection sans characters spécials
                print(f"On a une nouvelle injection: {injection_name} !")

                new_string_seq = title
                num_injection += 1
            new_string_seq += ligne
            new_string_comp += ligne
            finish_string = True 

    new_path = f"{file_name}_Complet.csv"
    save_file(new_string_comp, path_sortie, new_path)
    seq_file = open(f"{path_sortie}Nom_Sequences.txt", "w")
    seq_file.write(sequence_file)

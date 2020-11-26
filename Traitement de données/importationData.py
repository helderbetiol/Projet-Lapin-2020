
# coding: utf-8

# # Importation de la data et division par injection

# ### Fonction dir_exists
# 
# _dir_exists(path, directory)_
# 
# Définition d'une fonction pour créer automatiquement les dossier pour sauvegarder les données. Elle scane le directoire _path_ et récuper tous les dossiers. Après elle cherche le dossier _directory_ et s'il n'existe pas, elle le crée.


# Imports utiles 

import os
import io
import pandas as pd


def scan_dir(path):
    with os.scandir(path) as temp:    #Cherche tous les dossiers dans path
        dir_list = [direc.name for direc in temp if os.path.isdir(direc)]    #Crée une liste avec les dossiers
        file_list = [file.name for file in temp if os.path.isfile(file)]
    return dir_list, file_list

def dir_exists(path, directory):
    dir_list, _ = scan_dir(path)
    path_sortie = path + directory + "\\"    #Unifie le chemin path et directory
    if not(directory in dir_list):    #Si directory n'existe pas dans path il est créé
        os.mkdir(path_sortie)
    return path_sortie


# ### Function de sauvegardage de fichiers



def save_file(content, path, name):
    
    new_file = io.StringIO(content) # Transformation du string en IO
    new_df = pd.read_table(new_file, decimal = ",") # Création de la dataframe à partir de l'IO
    new_df.to_csv(path + name) # On enregistre la dataframe sous forme d'un fichier csv, dans le dossier de sortie


# ### Préparation
def import_data(path_entree, path_data_output, variables):
    title = "\t".join(variables) + "\n"
    if not(os.path.isdir(path_entree)):  #Si le dossier d'entrée n'existe pas, il ferme le program
        print(f"There is not folder {path_entree} with the files to process. The program will finish")
        exit()
    else:  #Sinon, l'algorithme récupère tous les fichiers à l'intérieur du dossier d'entrée
         _, file_list = scan_dir(path_entree)
            


    # ### On parcours le dossier et aussi chaque fichier, on le divise par injection (ou essaie dans le cas où il y aurait eu la nécessité de faire plusieurs essais) et on l'exporte dans le path_sortie

    # In[39]:


    # On ouvre le fichier d'entrée
    for element in file_list:
        file = open(path_entree + element, 'r')  #On ouvre un fichier à la fois, entre ceux qui se trouvent au path_entrée
        file_name = element.rsplit(".", 1)[0]  # On récupère le nom du fichier sans l'extension (.txt, etc)
        path_sortie = dir_exists(path_data_output, file_name)  #On crée un dossier pour mettre les fichiers de sortie
        num_essai = 0  #Nombre d'essais dans le cas où la pratique n'aurait pas commencé à la première fois
        num_injection = 0  
        new_string = title  #Initialization d'un nouveau fichier avec l'en-tête des variables (le titre)
        injection_name = "Début"  #La première injection s'appelle Début, mais ne répresente pas une injection réelle
        finish_string = False  #C'est un état pour savoir quand plusieurs lignes non numériques continues sont passées

        # On effectue une boucle sur les lignes du fichier ; on rajoute les lignes au fur et à mesure à new_string, et quand il y a un # on enregistre

        for ligne in file:
            
            if ligne[0].isalpha():  #Si le premier élément de la ligne n'est pas un character numérique, il ne faut pas que l'on prend ce ligne là
                
                if finish_string:   #Si la dernière ligne était numérique, ce paramètre est True, ce qui marque la fin d'un essai
                    
                    print("On a une nouvelle essai !")

                    new_path = f"{file_name}_Seq{num_injection}_{injection_name}_Essai{num_essai}.csv"  #C'est le nom du fichier
                    save_file(new_string, path_sortie, new_path)  #Cela permet de sauvegarder le fichier, qui dans ce cas ici c'est un essai de commencer le TP

                    #on réinitialise le string
                    new_string = title 
                    num_essai += 1  #On augmente le nombre d'essais pour savoir combien d'essais on a fait avant de faire le test complet
                    finish_string = False   #On remet l'état à False pour éviter que dans la prochaine ligne non numérique, l'algo sauvegarde la ligne

            else:

                if "#" in ligne: #Si nouvelle injection : on enregistre tout ce qu'il s'est passé depuis la dernière dans un nouveau fichier

                    
                    
                    injection = ligne.rpartition("#")[-1]  #On récupère le nom de l'injection après le #
                    char_injection = [i for i in injection if i.isalpha()]  #On obtien le characters alphabetiques
                    injection_name = injection[injection.find(char_injection[0]):len(injection)].rstrip(" \n")  #On récupère le nom de l'injection sans characters spécials
                    print(f"On a une nouvelle injection: {injection_name} !")
                    new_path = f"{file_name}_Seq{num_injection}_{injection_name}_Essai{num_essai}.csv"  #C'est le nom du fichier
                    save_file(new_string, path_sortie, new_path)  #On sauvegarde le fichier

                    #on réinitialise le string
                    new_string = title
                    num_injection += 1

                new_string += ligne # On ajoute la ligne au string
                finish_string = True  #On remet l'état à True pour assurer que dans la prochaine ligne non numérique, elle soit sauvegardé comme un essai


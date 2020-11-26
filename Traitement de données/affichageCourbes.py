import pandas as pd
import matplotlib.pyplot as plt 


def calculer(data, valeur_etudiee, pas, sommaire='Temps', pas_echantillonage=0.001):

    #On va étudier seulement un échantillon sinon trop long. Mais sur du long terme peut d'influence
    nb_donnees = int(data[sommaire].size/(pas/pas_echantillonage))
    indices = [i*(pas/pas_echantillonage) for i in range(nb_donnees)]
    x = []
    y = []
    for i in indices :
        x.append(data[sommaire][i])
        y.append(data[valeur_etudiee][i])
    return x, y

def afficher(x, y, label_x="", label_y="", title=""):
    # Création de la courbe
    plt.plot(x,y)
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.title(title)
    plt.show()
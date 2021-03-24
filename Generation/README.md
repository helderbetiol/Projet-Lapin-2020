
# LINKS IMPORTANTS :

# LoudML 
- Documentation : 
https://loudml.io/en/loudml/reference/current/getting-started.html
- Téléchargement (avec Docker) :
https://loudml.io/en/loudml/reference/current/docker.html 

# Chronograph
- Documentation : 
https://docs.influxdata.com/chronograf/v1.8/introduction/downloading/

COMMANDES TERMINAL LINUX :
 
# Importantion csv pour InfluxDB 
*CAS 1 - tous les données :
- Obtenir les fichiers corrects (pour le measure d'adrenaline pour tous les groups) :
$ python csv2influx.py --path /home/luana/loudin/adrenaline/ --measure adrenaline --group 1
Explication : python csv2influx.py --path [chemin avec les fichiers CSV] --measure [adrenaline ou acetylcholine ou autre] --group [n'importe quel numero]

*CAS 2 - sur une prévision de LoudML :
- Sur terminal entrez dans le repertoire où se trouve le fichier python:
$ cd [loudin/Projet-Lapin-2020/Traitement\ de\ données/]
- Dans cette fichier vous devez changer dans la ligne 105 les mesures que vous allez travaillez (dans ce cas par exemple je vas commenter les autres mesures et laisser que  la mesure que vous allez travaillez : FrequenceRespiratoire)
python csv2influx.py --file [/home/luana/loudin/a/Chronograf Adrenaline fc prevision] --measure prevision-adr-fc --group 0

# Ouverture InfluxDB / Voir données importées 
- Open influx db command  - Ouvrir le terminal:
$ influxd
$ influx
$ show databases
$ use [nom_database]
$ show series

# Ouverture du Docker pour LoudML
- Ouvrir d'autre terminal pour Loudml. Ouvrir le docker pour LoudML : 
$ sudo docker run -ti -p 8077:8077 -v /home/luana/loudin/etc/loudml/:/etc/loudml/:ro  -v /home/luana/loudin/var/lib/loudml:/var/lib/loudml:rw loudml/loudml
Explication : sudo docker run -ti -p [porte du LoudML:porte du LoudML] -v [chemin pour le fichier config.yml de loudml dans le PC de l'utilisateur]:[partie du chemin]:ro  -v [chemin pour le dossier avec les modeles dans le PC de l'utilisateur]:[partie du chemin]:rw loudml/loudml

# Ouverture LoudML
- Ouvrir d'autre terminal :
$ sudo docker container ls
- Prend à main le CONTAINER ID et changer dans le command :
$ sudo docker exec -it [CONTAINER ID] bash
% Problème d'adresse, tapez le commande : loudml --addr [172.17.0.1:8077] ( l'information sur le [] est dans le fichier <<confi.yml>> )
- Il va ouvrir le container où se trouve loudml, mais il a besoin que vous l'adresse le dossier où se trouve les modeles (leur chemin), dans notre cas avec le command :
$ cd [var/lib/loudml/models] 
- Puis, il aura besoin d'un command pour ouvrir loudml:
$ loudml
% Dans ce environement, si vous tapez <<help>> il va montrer des commandes plus importants de cette plateforme

# Utilisation LoudML / Faire des prévisions
- Creation du modèle par exemple pour la pression arterielle de l'injection d'adrenaline (utilise le fichier deja existante modelAdrPA.json):
$ create-model modelAdrPA.json
- Pour montrer le modele genere (nom_modele est ecrit dans le tag "name" du fichier .json), le command :
$ show-model nom_modele
- Entrainement du modele
$ train-model nom_modele --from 0000000000 --to 0000001000
- Faire la prévision
$ forecast-model nom_modele --from 0000000000 --to 0000001000 -s
% si vous avez un probleme au milieu du entrainement qui demande d'elargir l'interval de temps. Pour resoudre il va falloir changer (augmenter) le nombre mis pour le <<bucket_interval>>.

# Utilisation Chronograph
- Pour afficher les résultats. Il est necessaire entrer sur l'application chronograf sur l'internet, pour ouvrir Chronograph, sur votre navigateur écrire le lien <<http://localhost:8888/>> (8888 est la porte où se trouve Chronograph)
- Dans la partie explore vous aurez la base de données ou se trouvera la prevision faite. Il va falloir écrire ce query pour retrouver le fichier prévision :
$ SELECT "@FC" FROM "rabbit"."autogen"."ballon" WHERE "model"='modelBalFR'
Explication SELECT [nom database] FROM [nom database]."autogen".[nom injection] WHERE "model"=[nom_modele]
- Genere le .csv pour obtenir la prévision faite par LoudML et un nouveau donnée fiable pour utiliser sur arduino et l'interface. Le Chronograph affiche pas la serie temporelle prévue. Il y a un soucis, il va falloir changer dans le fichier prévision (retirer les " guillements du fichier texte des résultats), salvegarder le donnée sur la base a travers le fichier csv2influx.py (comme on a deja vu, dans la partie importantion) pour afficher sur chronograph.
- Pour voir un conjoint des points de la base étudié:
$ SELECT "FrequenceCardiaque" FROM "rabbit2"."autogen"."adrenaline" WHERE "group"='9'
Explication : SELECT [mesure] FROM [base_donnée]."autogen".[injection] WHERE "group"=[numero]

# Exportation / Importation base des données 
- Pour faire un backup creer fichier <<backup>>, et utiliser le command :
$ influxd backup -portable -database rabbit3 /home/luana/backup/
Explication : influxd backup -portable -database [nom_dataBase_pour_faire_backup] [chemin_dossier_backup]
- Pour reprendre les données:
$ influxd restore -portable -db rabbit3 -newdb rabbit4_restore /home/luana/backup/
Explication : influxd restore -portable -db [nom_dataBase_pour_prendre_donnees] -newdb [nom_donnee_aux_donnees_prises] [Chemin_dossier_avec_donnees_backup]

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# LINKS UTILES :
- Exemple de projet qui utilise LoudML ses prévision - pour avoir une base:
https://essay.utwente.nl/80409/1/Leemans_BA_BMS.pdf
- Explication comment faire un modele .json pour LoudML:
https://medium.com/@vova.sergeyev/understanding-loud-ml-model-settings-133b10998a67

# Arduino - Projet Lapin 2020

--- Code_complet_Lapin ---


Il s'agit du code permettant d'animer le lapin (gonfler le poumon en silicone et faire vibrer le moteur simulant le coeur du lapin).
Le lapin ne va s'animer qu'à partir du moment où l'arduino reçoit des données correctement formatées de fréquences respiratoires et cardiaques par le port série.

Le code python "Lapin_PC_Arduino_backend.py" permet d'envoyer ces données depuis la base de données des données générées.

___

--- Lapin_PC_Arduino_backend ---



Ce script python fait la liaison entre le PC et l'Arduino. Il permet d'envoyer les données de la base de données à l'Arduino par l'intermédiaire du port série.

Ce script télécharge directement des fichiers .csv de données générées préalablement et mises sur la base de données grâce à des requêtes http.

"Lapin_PC_Arduino.py" fonctionne avec des fichiers .csv stockés sur la machine qui l'exécute.

Le code "Code_complet_lapin.ino" doit avoir été téléversé sur l'arduino pour que ce code fonctionne. (Penser à vérifier dans le code python si le port COM indiqué est le bon.)

En cas de problème pour accéder au port COM pour le script python (ex: erreur "permission refusée"), penser à vérifier que le moniteur série Arduino est bien fermé, puis appuyer sur le bouton "reset" de l'Arduino.
Ce problème survient si le code python n'a pas pu s'exécuter jusqu'au bout et que le port COM n'a pas été fermé correctement.

# Variables du Template HTML

## Section Système
- {{timestamp}} : Date et heure de génération (format: DD/MM/YYYY HH:MM:SS)
- {{hostname}} : Nom de la machine
- {{os_name}} : Système d'exploitation et version
- {{uptime}} : Temps depuis le démarrage (format: X jours, Y heures)
- {{users_count}} : Nombre d'utilisateurs connectés

## Section CPU
- {{cpu_cores}} : Nombre de cœurs du processeur
- {{cpu_freq}} : Fréquence du CPU en MHz
- {{cpu_percent}} : Pourcentage d'utilisation du CPU

## Section Mémoire
- {{ram_total}} : RAM totale en GB
- {{ram_used}} : RAM utilisée en GB
- {{ram_percent}} : Pourcentage d'utilisation de la RAM

## Section Réseau
- {{ip_address}} : Adresse IP principale

## Section Processus
- {{top_processes}} : Code HTML des 3 processus (lignes <tr>)

## Section Fichiers
- {{analyzed_folder}} : Chemin du dossier analysé
- {{txt_count}}, {{txt_percent}} : Fichiers .txt
- {{py_count}}, {{py_percent}} : Fichiers .py
- {{pdf_count}}, {{pdf_percent}} : Fichiers .pdf
- {{jpg_count}}, {{jpg_percent}} : Fichiers .jpg
- {{total_files}} : Total de fichiers


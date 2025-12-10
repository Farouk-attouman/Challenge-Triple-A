<!-- # Projet AAA - Dashboard Monitoring Linux

Dashboard de monitoring en temps reel pour machine virtuelle Ubuntu, sans JavaScript.

## Description

Ce projet permet de surveiller les ressources systeme d'une VM Linux et d'afficher les informations dans un dashboard web statique qui se rafraichit automatiquement.

### Fonctionnalites

- **Systeme** : Hostname, OS, architecture, uptime
- **CPU** : Utilisation globale et par coeur, load average
- **Memoire** : RAM et Swap (utilisation, disponible)
- **Disque** : Espace utilise/libre
- **Reseau** : Donnees envoyees/recues, interfaces
- **Processus** : Top 3 CPU et memoire
- **Fichiers** : Analyse par extension, plus gros fichiers

## Prerequis

- Ubuntu Desktop 22.04 LTS (ou autre distribution Linux)
- Python 3.8+
- pip3

## Installation

bash
# 1. Cloner le projet
git clone <url-du-repo>
cd AAA

# 2. Creer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 3. Installer les dependances
pip install -r requirements.txt


## Utilisation

```bash
# Lancer le monitoring (genere index.html)
python monitor.py

# Options disponibles
python monitor.py --help
python monitor.py --directory /home/user/Documents
python monitor.py --output dashboard.html
python monitor.py --verbose
```

Ouvrir `index.html` dans un navigateur web. La page se rafraichit automatiquement toutes les 30 secondes.

## Architecture

Le projet suit une architecture en couches pour la modularite :

```
AAA/
├── src/
│   ├── api/                 # Couche API (generation HTML)
│   │   ├── __init__.py
│   │   └── html_generator.py
│   ├── core/                # Couche Core (logique metier)
│   │   ├── __init__.py
│   │   └── data_processor.py
│   └── data/                # Couche Data (acces systeme)
│       ├── __init__.py
│       └── system_collector.py
├── monitor.py               # Script principal
├── template.html            # Template HTML avec variables
├── template.css             # Styles CSS avec gauges
├── index.html               # Dashboard genere (gitignore)
├── requirements.txt         # Dependances Python
├── .gitignore
└── README.md
```

### Couches

| Couche | Role | Module |
|--------|------|--------|
| **Data** | Collecte des donnees via psutil | `system_collector.py` |
| **Core** | Traitement et formatage des donnees | `data_processor.py` |
| **API** | Substitution des variables dans le template | `html_generator.py` |

## Indicateurs Colores

Les gauges utilisent un code couleur selon les seuils :

| Couleur | Plage | Signification |
|---------|-------|---------------|
| Vert | 0-50% | Normal |
| Orange | 51-80% | Attention |
| Rouge | 81-100% | Critique |

## Captures d'ecran

*A ajouter dans le dossier `screenshots/`*

- `terminal.png` : Execution du script dans le terminal
- `index.png` : Dashboard dans le navigateur

## Difficultes Rencontrees

- Configuration de l'environnement virtuel Python sur Ubuntu
- Gestion des permissions pour acceder aux informations systeme
- Analyse recursive des fichiers avec gestion des erreurs d'acces

## Ameliorations Possibles

- Historique des metriques avec graphiques
- Alertes par email en cas de seuils depasses
- Interface d'administration pour configurer les parametres
- Support multi-machines avec aggregation des donnees
- Export des donnees en JSON/CSV

## Technologies

- **Python 3** : Langage principal
- **psutil** : Bibliotheque de collecte systeme
- **HTML5** : Structure semantique
- **CSS3** : Styles avec Flexbox/Grid, gauges animees

## Licence

Projet educatif - Libre d'utilisation -->

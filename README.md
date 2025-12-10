# Projet AAA - Dashboard Monitoring Linux

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Dashboard de monitoring en temps réel pour machine virtuelle Ubuntu.

## Description

Ce projet permet de surveiller les ressources système d'une VM Linux et d'afficher les informations dans un dashboard web statique qui se rafraîchit automatiquement.

### Fonctionnalités

- **Système** : Hostname, OS, architecture, uptime
- **CPU** : Utilisation globale et par cœur, load average
- **Mémoire** : RAM et Swap (utilisation, disponible)
- **Disque** : Espace utilisé/libre
- **Réseau** : Données envoyées/reçues, interfaces
- **Processus** : Top 3 CPU et mémoire
- **Fichiers** : Analyse par extension, plus gros fichiers

## Prérequis

- Ubuntu Desktop 22.04 LTS (ou autre distribution Linux)
- Python 3.8+
- pip3

## Installation

```bash
# 1. Cloner le projet
git clone <url-du-repo>
cd AAA

# 2. Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt
```

## Utilisation

```bash
# Lancer le monitoring (génère index.html)
python monitor.py

# Options disponibles
python monitor.py --help
python monitor.py --directory /home/user/Documents
python monitor.py --output dashboard.html
python monitor.py --verbose
```

Ouvrir `index.html` dans un navigateur web. La page se rafraîchit automatiquement toutes les 30 secondes.

## Architecture

Le projet suit une architecture en couches pour la modularité :

```
AAA/
├── src/
│   ├── api/                 # Couche API (génération HTML)
│   │   ├── __init__.py
│   │   └── html_generator.py
│   ├── core/                # Couche Core (logique métier)
│   │   ├── __init__.py
│   │   └── data_processor.py
│   └── data/                # Couche Data (accès système)
│       ├── __init__.py
│       └── system_collector.py
├── monitor.py               # Script principal
├── template.html            # Template HTML avec variables
├── template.css             # Styles CSS avec gauges
├── index.html               # Dashboard généré (gitignore)
├── requirements.txt         # Dépendances Python
├── .gitignore
└── README.md
```

### Couches

| Couche | Rôle | Module |
|--------|------|--------|
| **Data** | Collecte des données via psutil | `system_collector.py` |
| **Core** | Traitement et formatage des données | `data_processor.py` |
| **API** | Substitution des variables dans le template | `html_generator.py` |

## Indicateurs Colorés

Les gauges utilisent un code couleur selon les seuils :

| Couleur | Plage | Signification |
|---------|-------|---------------|
| 🟢 Vert | 0-50% | Normal |
| 🟠 Orange | 51-80% | Attention |
| 🔴 Rouge | 81-100% | Critique |

## Technologies

- **Python 3** : Langage principal
- **psutil** : Bibliothèque de collecte système
- **HTML5** : Structure sémantique
- **CSS3** : Styles avec Flexbox/Grid, gauges animées

## Contribuer

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## Licence

Projet éducatif - Libre d'utilisation

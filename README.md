# 🖥️ Challenge Triple A - Dashboard de Monitoring

## 📋 Description

Dashboard web de monitoring système en temps réel développé dans le cadre du Challenge Triple A. Cette application collecte et affiche les statistiques d'une machine virtuelle Linux (CPU, RAM, processus, réseau, fichiers) via une interface web élégante et responsive.

**Challenge Triple A** = **Administration** + **Algorithmique** + **Affichage**

## ✨ Fonctionnalités

### Monitoring Système
- 📊 **Informations système** : Hostname, OS, uptime, utilisateurs connectés
- ⚙️ **CPU** : Nombre de cœurs, fréquence, pourcentage d'utilisation
- 💾 **Mémoire** : RAM totale/utilisée avec barres de progression
- 🌐 **Réseau** : Adresse IP principale
- ⚡ **Processus** : Top 3 des processus les plus gourmands en ressources
- 📁 **Fichiers** : Analyse et statistiques par type de fichiers (.txt, .py, .pdf, .jpg)

### Interface Web
- Design moderne et responsive
- Barres de progression animées
- Code couleur par section
- Mise à jour manuelle des données

## 🔧 Prérequis

### Machine Virtuelle
- **OS** : Ubuntu Desktop 22.04 LTS ou supérieur
- **RAM** : 2 GB minimum
- **Disque** : 15 GB
- **Réseau** : Accès internet

### Logiciels
- Python 3.10+
- pip3
- Navigateur web (Firefox, Chrome, etc.)

## 📥 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-nom/AAA.git
cd AAA
2. Installer les dépendances Python
# Mettre à jour pip
pip3 install --upgrade pip

# Installer psutil (obligatoire)
pip3 install psutil

# Installer distro (optionnel, pour info OS détaillées)
pip3 install distro
3. Vérifier l'installation
python3 -c "import psutil; print('✅ psutil OK')"

🚀 Utilisation
Générer le dashboard
# Dans le dossier du projet
python3 monitor.py
Le script va :
    1. Collecter toutes les données système
    2. Générer le fichier index.html
    3. Afficher un message de confirmation
Visualiser le dashboard
# Ouvrir avec le navigateur par défaut
xdg-open index.html

# Ou avec Firefox
firefox index.html

# Ou avec Chrome
google-chrome index.html
Actualiser les données
Pour mettre à jour le dashboard avec de nouvelles données :
python3 monitor.py
# Puis rafraîchir la page dans le navigateur (F5)

📁 Structure du Projet
AAA/
├── README.md              # Documentation du projet
├── monitor.py             # Script Python de collecte
├── template.html          # Template HTML avec variables
├── template.css           # Feuille de style
├── index.html             # HTML généré (exemple)
├── screenshots/           # Captures d'écran
│   ├── terminal.png      # Exécution du script
│   └── index.png         # Dashboard final
└── .gitignore            # Fichiers à ignorer
📸 Captures d'Écran
Terminal

Dashboard

🛠️ Technologies Utilisées
    • Python 3 : Langage de programmation
    • psutil : Bibliothèque de monitoring système
    • HTML5 : Structure sémantique
    • CSS3 : Styles et animations
    • Ubuntu Linux : Système d'exploitation
    
🐛 Difficultés Rencontrées
1. Récupération de l'adresse IP
Problème : Difficulté à identifier l'IP principale parmi plusieurs interfaces réseau.
Solution : Utilisation d'une connexion socket vers un DNS public (8.8.8.8) pour déterminer l'interface active.
2. Pourcentage CPU des processus
Problème : Beaucoup de processus affichaient 0.0% de CPU.
Solution : Ajout d'un intervalle de mesure avec cpu_percent(interval=0.1).
3. Permissions sur certains fichiers
Problème : Erreurs PermissionDenied lors de l'analyse de fichiers.
Solution : Gestion des exceptions avec try/except pour ignorer les fichiers inaccessibles.
4. Conversion des unités de mémoire
Problème : Affichage de la RAM en octets (illisible).
Solution : Conversion en GB avec total / (1024**3) et arrondi à 2 décimales.

🚀 Améliorations Possibles
Court terme
    • [ ] Ajouter un rafraîchissement automatique toutes les 30 secondes
    • [ ] Implémenter un code couleur (vert/orange/rouge) selon les seuils d'utilisation
    • [ ] Ajouter des graphiques avec Chart.js ou Plotly
    • [ ] Afficher l'utilisation par cœur CPU
Moyen terme
    • [ ] Analyse récursive des sous-dossiers
    • [ ] Support de plus d'extensions de fichiers (10+)
    • [ ] Calcul de l'espace disque par type de fichier
    • [ ] Historique des mesures sur 24h
Long terme
    • [ ] Mode serveur avec Flask pour accès distant
    • [ ] Authentification utilisateur
    • [ ] Base de données pour stocker l'historique
    • [ ] Alertes email/SMS en cas de dépassement de seuils
    • [ ] Dashboard responsive avec graphiques interactifs
👥 Auteurs
    • Farouk - Administration & Python
    • Claude - Python & HTML
    • Lamali - Design & CSS
📝 Licence
Projet académique réalisé dans le cadre du Challenge Triple A.
🙏 Remerciements
    • L'équipe pédagogique pour le sujet du Challenge
    • La documentation de psutil
    • La communauté Ubuntu

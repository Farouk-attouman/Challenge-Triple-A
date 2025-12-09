#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Challenge Triple A - Script de Monitoring Système
Collecte les données système et génère un dashboard HTML
"""

import psutil
import platform
from datetime import datetime
import socket
import os
import time

# ===== FONCTION : Collecte des données CPU =====
def get_cpu_info():
    """Récupère les informations du processeur"""
    cpu_data = {}
    
    # Nombre de cœurs
    cpu_data['cpu_cores'] = psutil.cpu_count(logical=True)
    
    # Fréquence du CPU
    cpu_freq = psutil.cpu_freq()
    cpu_data['cpu_freq'] = round(cpu_freq.current, 1) if cpu_freq else 0
    
    # Pourcentage d'utilisation (moyenne sur 1 seconde)
    cpu_data['cpu_percent'] = round(psutil.cpu_percent(interval=1), 1)
    
    return cpu_data

# ===== FONCTION : Collecte des données Mémoire =====
def get_memory_info():
    """Récupère les informations de la RAM"""
    mem = psutil.virtual_memory()
    
    memory_data = {}
    memory_data['ram_total'] = round(mem.total / (1024**3), 2)  # Convertir en GB
    memory_data['ram_used'] = round(mem.used / (1024**3), 2)
    memory_data['ram_percent'] = round(mem.percent, 1)
    
    return memory_data

# ===== FONCTION : Collecte des données Système =====
def get_system_info():
    """Récupère les informations système générales"""
    system_data = {}
    
    # Nom de la machine
    system_data['hostname'] = socket.gethostname()
    
    # Système d'exploitation
    system_data['os_name'] = f"{platform.system()} {platform.release()}"
    if platform.system() == "Linux":
        try:
            import distro
            system_data['os_name'] = f"{distro.name()} {distro.version()}"
        except:
            pass
    
    # Uptime
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime_seconds = (datetime.now() - boot_time).total_seconds()
    days = int(uptime_seconds // 86400)
    hours = int((uptime_seconds % 86400) // 3600)
    system_data['uptime'] = f"{days} jours, {hours} heures"
    
    # Nombre d'utilisateurs connectés
    system_data['users_count'] = len(psutil.users())
    
    # Adresse IP principale
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        system_data['ip_address'] = s.getsockname()[0]
        s.close()
    except:
        system_data['ip_address'] = "Non disponible"
    
    # Timestamp actuel
    system_data['timestamp'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    return system_data

# ===== FONCTION : Top processus =====
def get_top_processes(n=3):
    """Récupère les N processus les plus gourmands"""
    processes = []
    
    # Première passe : initialiser les mesures CPU
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            proc.cpu_percent(interval=None)
        except:
            pass
    
    # Attendre pour avoir des mesures valides
    time.sleep(1)
    
    # Deuxième passe : collecter les vraies mesures
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            cpu = proc.cpu_percent(interval=None)
            mem = proc.memory_percent()
            name = proc.name()
            
            # Garder les processus avec activité
            if cpu > 0 or mem > 0.5:
                processes.append({
                    'name': name,
                    'cpu': round(cpu, 1),
                    'ram': round(mem, 1)
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Trier par CPU décroissant
    processes.sort(key=lambda x: x['cpu'], reverse=True)
    
    # Garder les N premiers
    top_processes = processes[:n]
    
    # Si pas assez, trier par RAM
    if len(top_processes) < n:
        processes.sort(key=lambda x: x['ram'], reverse=True)
        top_processes = processes[:n]
    
    # Générer le HTML
    html_rows = ""
    for proc in top_processes:
        html_rows += f"""
                    <tr>
                        <td>{proc['name']}</td>
                        <td>{proc['cpu']}%</td>
                        <td>{proc['ram']}%</td>
                    </tr>"""
    
    return html_rows

# ===== FONCTION : Analyse des fichiers =====
def analyze_files(directory=None):
    """Analyse les fichiers d'un dossier"""
    
    # Définir le dossier par défaut
    if directory is None:
        directory = os.path.expanduser("~/Documents")
    
    # Vérifier que le dossier existe
    if not os.path.exists(directory):
        directory = os.path.expanduser("~")
    
    # Compteurs par extension
    extensions = {'.txt': 0, '.py': 0, '.pdf': 0, '.jpg': 0}
    
    # Parcourir les fichiers
    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                _, ext = os.path.splitext(item)
                ext = ext.lower()
                if ext in extensions:
                    extensions[ext] += 1
    except PermissionError:
        pass
    
    # Calculer le total
    total = sum(extensions.values())
    
    # Préparer les données
    files_data = {
        'analyzed_folder': directory,
        'txt_count': extensions['.txt'],
        'py_count': extensions['.py'],
        'pdf_count': extensions['.pdf'],
        'jpg_count': extensions['.jpg'],
        'total_files': total
    }
    
    # Calculer les pourcentages
    if total > 0:
        files_data['txt_percent'] = round((extensions['.txt'] / total) * 100, 1)
        files_data['py_percent'] = round((extensions['.py'] / total) * 100, 1)
        files_data['pdf_percent'] = round((extensions['.pdf'] / total) * 100, 1)
        files_data['jpg_percent'] = round((extensions['.jpg'] / total) * 100, 1)
    else:
        files_data['txt_percent'] = 0
        files_data['py_percent'] = 0
        files_data['pdf_percent'] = 0
        files_data['jpg_percent'] = 0
    
    return files_data

# ===== FONCTION : Génération HTML =====
def generate_html():
    """Collecte toutes les données et génère le fichier HTML"""
    
    print("📊 Collecte des données système...")
    
    # Collecter toutes les données
    all_data = {}
    all_data.update(get_system_info())
    all_data.update(get_cpu_info())
    all_data.update(get_memory_info())
    all_data['top_processes'] = get_top_processes(3)
    all_data.update(analyze_files())
    
    print("✅ Données collectées")
    
    # Lire le template HTML
    print("📄 Lecture du template...")
    try:
        with open('template.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print("❌ Erreur : template.html introuvable")
        return False
    
    # Remplacer les variables
    print("🔄 Génération du HTML...")
    for key, value in all_data.items():
        placeholder = "{{" + key + "}}"
        html_content = html_content.replace(placeholder, str(value))
    
    # Écrire le fichier final
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ index.html généré avec succès!")
    return True

# ===== PROGRAMME PRINCIPAL =====
def main():
    """Point d'entrée principal du script"""
    print("=" * 50)
    print("  Challenge Triple A - Dashboard Monitoring")
    print("=" * 50)
    
    if generate_html():
        print("\n🎉 Dashboard généré! Ouvrez index.html dans votre navigateur.")
    else:
        print("\n❌ Erreur lors de la génération")

if __name__ == "__main__":
    main()
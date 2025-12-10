#!/usr/bin/env python3
"""
Monitor.py - Script principal de monitoring système.

Ce script collecte les informations système d'une VM Linux
et génère un dashboard HTML statique.

Usage:
    python monitor.py [--directory /chemin] [--output index.html]

Auteur: Projet AAA
"""

import argparse
import sys
from pathlib import Path

# Ajout du chemin src pour les imports
sys.path.insert(0, str(Path(__file__).parent))

from src.data.system_collector import SystemCollector
from src.core.data_processor import DataProcessor
from src.api.html_generator import HTMLGenerator


def parse_arguments() -> argparse.Namespace:
    """Parse les arguments de la ligne de commande."""
    parser = argparse.ArgumentParser(
        description="Monitoring système avec génération de dashboard HTML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
    python monitor.py
    python monitor.py --directory /home/user/Documents
    python monitor.py --output dashboard.html
    python monitor.py -d /var/log -o rapport.html
        """
    )

    parser.add_argument(
        "-d", "--directory",
        type=str,
        default="/home",
        help="Répertoire à analyser pour les fichiers (défaut: /home)"
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        default="index.html",
        help="Fichier HTML de sortie (défaut: index.html)"
    )

    parser.add_argument(
        "-t", "--template",
        type=str,
        default="template.html",
        help="Fichier template HTML (défaut: template.html)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Mode verbeux avec affichage des détails"
    )

    return parser.parse_args()


def main() -> int:
    """
    Fonction principale du script de monitoring.

    Returns:
        Code de retour (0 = succès, 1 = erreur).
    """
    args = parse_arguments()

    print("=" * 50)
    print("  DASHBOARD MONITORING - Projet AAA")
    print("=" * 50)
    print()

    # Étape 1: Collecte des données (Data Layer)
    print("[1/3] Collecte des données système...")
    try:
        collector = SystemCollector(files_directory=args.directory)
        raw_data = collector.collect_all()

        if args.verbose:
            print(f"      - Hostname: {raw_data['system']['hostname']}")
            print(f"      - OS: {raw_data['system']['os']} {raw_data['system']['os_version']}")
            print(f"      - CPU: {raw_data['cpu']['cpu_percent']}%")
            print(f"      - RAM: {raw_data['memory']['percent']}%")
            print(f"      - Disque: {raw_data['disk']['percent']}%")
            print(f"      - Processus: {raw_data['processes']['total_count']}")
            print(f"      - Fichiers analysés: {raw_data['files']['total_files']}")

        print("      Collecte terminée avec succès!")
    except Exception as e:
        print(f"      ERREUR: {e}")
        return 1

    # Étape 2: Traitement des données (Core Layer)
    print("[2/3] Traitement des données...")
    try:
        processor = DataProcessor(raw_data)
        template_vars = processor.get_template_variables()
        print(f"      {len(template_vars)} variables générées")
    except Exception as e:
        print(f"      ERREUR: {e}")
        return 1

    # Étape 3: Génération HTML (API Layer)
    print("[3/3] Génération du dashboard HTML...")
    try:
        # Déterminer le chemin du template
        script_dir = Path(__file__).parent
        template_path = script_dir / args.template

        if not template_path.exists():
            print(f"      ERREUR: Template non trouvé: {template_path}")
            return 1

        generator = HTMLGenerator(str(template_path))
        output_path = script_dir / args.output

        if generator.generate_file(template_vars, str(output_path)):
            print(f"      Dashboard généré: {output_path}")
        else:
            print("      ERREUR: Échec de la génération")
            return 1
    except Exception as e:
        print(f"      ERREUR: {e}")
        return 1

    print()
    print("=" * 50)
    print("  MONITORING TERMINÉ AVEC SUCCÈS")
    print("=" * 50)
    print()
    print(f"Dashboard disponible: {output_path}")
    print(f"Ouvrez ce fichier dans un navigateur web.")
    print()
    print("Le dashboard se rafraîchit automatiquement toutes les 30 secondes.")
    print("Pour mettre à jour les données, relancez ce script.")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())

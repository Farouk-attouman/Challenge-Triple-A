#!/usr/bin/env python3
"""
API Layer - Génération HTML à partir des templates.
Ce module gère la substitution des variables dans le template HTML.
"""

import re
from pathlib import Path


def load_template(template_path):
    """
    Charge le template depuis le fichier.

    Args:
        template_path: Chemin vers le fichier template HTML.

    Returns:
        Contenu du template ou chaîne vide en cas d'erreur.
    """
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Erreur: Template non trouvé: {template_path}")
        return ""
    except IOError as e:
        print(f"Erreur de lecture du template: {e}")
        return ""


def render(template_content, variables):
    """
    Génère le HTML en remplaçant les variables.

    Args:
        template_content: Contenu du template HTML.
        variables: Dictionnaire des variables à substituer.

    Returns:
        Contenu HTML avec les variables substituées.
    """
    if not template_content:
        return ""

    html = template_content

    # Remplacement des variables {{variable}}
    for key, value in variables.items():
        pattern = r"\{\{\s*" + re.escape(key) + r"\s*\}\}"
        html = re.sub(pattern, str(value), html)

    # Avertissement pour les variables non remplacées
    remaining = re.findall(r"\{\{[^}]+\}\}", html)
    if remaining:
        print(f"Attention: Variables non substituées: {remaining}")

    return html


def generate_file(template_path, variables, output_path):
    """
    Génère le fichier HTML de sortie.

    Args:
        template_path: Chemin vers le fichier template HTML.
        variables: Dictionnaire des variables à substituer.
        output_path: Chemin du fichier HTML de sortie.

    Returns:
        True si la génération a réussi, False sinon.
    """
    template_content = load_template(template_path)
    if not template_content:
        return False

    html = render(template_content, variables)
    if not html:
        return False

    try:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        with open(output, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"Dashboard généré: {output_path}")
        return True
    except IOError as e:
        print(f"Erreur d'écriture: {e}")
        return False


if __name__ == "__main__":
    # Test du module
    test_vars = {
        "timestamp": "2024-01-15 10:30:00",
        "system_hostname": "ubuntu-vm",
        "cpu_percent": 45.5,
    }

    template_content = load_template("template.html")
    html = render(template_content, test_vars)
    print(html[:500] if html else "Erreur de génération")

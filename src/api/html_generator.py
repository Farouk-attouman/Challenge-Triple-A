#!/usr/bin/env python3
"""
API Layer - Génération HTML à partir des templates.
Ce module gère la substitution des variables dans le template HTML.
"""

import re
from pathlib import Path
from typing import Dict, Any


class HTMLGenerator:
    """Générateur HTML utilisant des templates avec variables."""

    def __init__(self, template_path: str):
        """
        Initialise le générateur.

        Args:
            template_path: Chemin vers le fichier template HTML.
        """
        self.template_path = Path(template_path)
        self.template_content = ""

    def load_template(self) -> bool:
        """
        Charge le template depuis le fichier.

        Returns:
            True si le chargement a réussi, False sinon.
        """
        try:
            with open(self.template_path, "r", encoding="utf-8") as f:
                self.template_content = f.read()
            return True
        except FileNotFoundError:
            print(f"Erreur: Template non trouvé: {self.template_path}")
            return False
        except IOError as e:
            print(f"Erreur de lecture du template: {e}")
            return False

    def render(self, variables: Dict[str, Any]) -> str:
        """
        Génère le HTML en remplaçant les variables.

        Args:
            variables: Dictionnaire des variables à substituer.

        Returns:
            Contenu HTML avec les variables substituées.
        """
        if not self.template_content:
            if not self.load_template():
                return ""

        html = self.template_content

        # Remplacement des variables {{variable}}
        for key, value in variables.items():
            pattern = r"\{\{\s*" + re.escape(key) + r"\s*\}\}"
            html = re.sub(pattern, str(value), html)

        # Avertissement pour les variables non remplacées
        remaining = re.findall(r"\{\{[^}]+\}\}", html)
        if remaining:
            print(f"Attention: Variables non substituées: {remaining}")

        return html

    def generate_file(self, variables: Dict[str, Any], output_path: str) -> bool:
        """
        Génère le fichier HTML de sortie.

        Args:
            variables: Dictionnaire des variables à substituer.
            output_path: Chemin du fichier HTML de sortie.

        Returns:
            True si la génération a réussi, False sinon.
        """
        html = self.render(variables)
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
    generator = HTMLGenerator("template.html")

    test_vars = {
        "timestamp": "2024-01-15 10:30:00",
        "system_hostname": "ubuntu-vm",
        "cpu_percent": 45.5,
    }

    html = generator.render(test_vars)
    print(html[:500] if html else "Erreur de génération")

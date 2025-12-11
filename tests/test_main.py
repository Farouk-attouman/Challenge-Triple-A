#!/usr/bin/env python3
"""
Triple A Project - Tests basiques
"""

from src.data.system_collector import collect_all, format_bytes
from src.core.data_processor import get_color_class, get_template_variables
from src.api.html_generator import load_template


# --- Tests du collecteur ---

def test_collecteur_fonctionne():
    """Le collecteur récupère des données."""
    donnees = collect_all()

    # On vérifie qu'on a bien des données
    assert "cpu" in donnees
    assert "memory" in donnees


def test_format_bytes():
    """Le formatage des octets fonctionne."""
    assert format_bytes(1024) == "1.00 KB"
    assert format_bytes(1048576) == "1.00 MB"


# --- Tests du processeur ---

def test_couleurs():
    """Les couleurs sont correctes selon le pourcentage."""
    # Vert = OK (0-50%)
    assert get_color_class(30) == "gauge-green"

    # Orange = Attention (51-80%)
    assert get_color_class(70) == "gauge-orange"

    # Rouge = Critique (81-100%)
    assert get_color_class(90) == "gauge-red"


# --- Tests du générateur HTML ---

def test_generateur_fichier_inexistant():
    """Le générateur gère les fichiers manquants."""
    contenu = load_template("fichier_inexistant.html")

    assert contenu == ""


# --- Test complet ---

def test_pipeline():
    """Le pipeline complet fonctionne."""
    # Étape 1 : Collecter les données
    donnees = collect_all()

    # Étape 2 : Traiter les données
    variables = get_template_variables(donnees)

    # Étape 3 : Vérifier qu'on a les variables pour le HTML
    assert "cpu_percent" in variables
    assert "memory_percent" in variables

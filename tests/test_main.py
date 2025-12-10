#!/usr/bin/env python3
"""
Triple A Project - Tests basiques
"""

from src.data.system_collector import SystemCollector
from src.core.data_processor import DataProcessor
from src.api.html_generator import HTMLGenerator


# --- Tests du collecteur ---

def test_collecteur_fonctionne():
    """Le collecteur récupère des données."""
    collecteur = SystemCollector()
    donnees = collecteur.collect_all()

    # On vérifie qu'on a bien des données
    assert "cpu" in donnees
    assert "memory" in donnees


def test_format_bytes():
    """Le formatage des octets fonctionne."""
    collecteur = SystemCollector()

    assert collecteur._format_bytes(1024) == "1.00 KB"
    assert collecteur._format_bytes(1048576) == "1.00 MB"


# --- Tests du processeur ---

def test_couleurs():
    """Les couleurs sont correctes selon le pourcentage."""
    processeur = DataProcessor({})

    # Vert = OK (0-50%)
    assert processeur.get_color_class(30) == "gauge-green"

    # Orange = Attention (51-80%)
    assert processeur.get_color_class(70) == "gauge-orange"

    # Rouge = Critique (81-100%)
    assert processeur.get_color_class(90) == "gauge-red"


# --- Tests du générateur HTML ---

def test_generateur_fichier_inexistant():
    """Le générateur gère les fichiers manquants."""
    generateur = HTMLGenerator("fichier_inexistant.html")

    assert generateur.load_template() == False


# --- Test complet ---

def test_pipeline():
    """Le pipeline complet fonctionne."""
    # Étape 1 : Collecter les données
    collecteur = SystemCollector()
    donnees = collecteur.collect_all()

    # Étape 2 : Traiter les données
    processeur = DataProcessor(donnees)
    variables = processeur.get_template_variables()

    # Étape 3 : Vérifier qu'on a les variables pour le HTML
    assert "cpu_percent" in variables
    assert "memory_percent" in variables

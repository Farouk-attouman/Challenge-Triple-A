#!/usr/bin/env python3
"""
Triple A Project - Basic tests
"""

from src.data.system_collector import collect_all, format_bytes
from src.core.data_processor import get_color_class, get_template_variables
from src.api.html_generator import load_template


# --- Collector tests ---

def test_collector_works():
    """The collector retrieves data."""
    data = collect_all()

    # Verify we have data
    assert "cpu" in data
    assert "memory" in data


def test_format_bytes():
    """Byte formatting works correctly."""
    assert format_bytes(1024) == "1.00 KB"
    assert format_bytes(1048576) == "1.00 MB"


# --- Processor tests ---

def test_colors():
    """Colors are correct based on percentage."""
    # Green = OK (0-50%)
    assert get_color_class(30) == "gauge-green"

    # Orange = Warning (51-80%)
    assert get_color_class(70) == "gauge-orange"

    # Red = Critical (81-100%)
    assert get_color_class(90) == "gauge-red"


# --- HTML generator tests ---

def test_generator_missing_file():
    """The generator handles missing files."""
    content = load_template("nonexistent_file.html")

    assert content == ""


# --- Full pipeline test ---

def test_pipeline():
    """The complete pipeline works."""
    # Step 1: Collect data
    data = collect_all()

    # Step 2: Process data
    variables = get_template_variables(data)

    # Step 3: Verify we have variables for HTML
    assert "cpu_percent" in variables
    assert "memory_percent" in variables

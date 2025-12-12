#!/usr/bin/env python3
"""
API Layer - HTML generation from templates.
This module handles variable substitution in the HTML template.
"""

import re
from pathlib import Path


def load_template(template_path):
    """
    Load the template from file.

    Args:
        template_path: Path to the HTML template file.

    Returns:
        Template content or empty string on error.
    """
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Template not found: {template_path}")
        return ""
    except IOError as e:
        print(f"Error reading template: {e}")
        return ""


def render(template_content, variables):
    """
    Generate HTML by replacing variables.

    Args:
        template_content: HTML template content.
        variables: Dictionary of variables to substitute.

    Returns:
        HTML content with substituted variables.
    """
    # Return empty string if template is empty
    if not template_content:
        return ""

    html = template_content

    # Replace {{variable}} patterns
    for key, value in variables.items():
        pattern = r"\{\{\s*" + re.escape(key) + r"\s*\}\}"
        html = re.sub(pattern, str(value), html)

    # Warning for unsubstituted variables
    remaining = re.findall(r"\{\{[^}]+\}\}", html)
    if remaining:
        print(f"Warning: Unsubstituted variables: {remaining}")

    return html


def generate_file(template_path, variables, output_path):
    """
    Generate the output HTML file.

    Args:
        template_path: Path to the HTML template file.
        variables: Dictionary of variables to substitute.
        output_path: Path for the output HTML file.

    Returns:
        True if generation succeeded, False otherwise.
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

        print(f"Dashboard generated: {output_path}")
        return True
    except IOError as e:
        print(f"Write error: {e}")
        return False


if __name__ == "__main__":
    # Module test
    test_vars = {
        "timestamp": "2024-01-15 10:30:00",
        "system_hostname": "ubuntu-vm",
        "cpu_percent": 45.5,
    }

    template_content = load_template("template.html")
    html = render(template_content, test_vars)
    print(html[:500] if html else "Generation error")

#!/usr/bin/env python3
"""
Monitor.py - Main system monitoring script.

This script collects system information from a Linux VM
and generates a static HTML dashboard.

Usage:
    python monitor.py [--directory /path] [--output index.html]

Author: AAA Project
"""

import argparse
import sys
from pathlib import Path

# Add src path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.data.system_collector import collect_all
from src.core.data_processor import get_template_variables
from src.api.html_generator import generate_file


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="System monitoring with HTML dashboard generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python monitor.py
    python monitor.py --directory /home/user/Documents
    python monitor.py --output dashboard.html
    python monitor.py -d /var/log -o report.html
        """
    )

    parser.add_argument(
        "-d", "--directory",
        type=str,
        default="/home",
        help="Directory to analyze for files (default: /home)"
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        default="index.html",
        help="Output HTML file (default: index.html)"
    )

    parser.add_argument(
        "-t", "--template",
        type=str,
        default="template.html",
        help="HTML template file (default: template.html)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose mode with detailed output"
    )

    return parser.parse_args()


def main():
    """
    Main function of the monitoring script.

    Returns:
        Return code (0 = success, 1 = error).
    """
    args = parse_arguments()

    print("=" * 50)
    print("  MONITORING DASHBOARD - AAA Project")
    print("=" * 50)
    print()

    # Step 1: Data collection (Data Layer)
    print("[1/3] Collecting system data...")
    try:
        raw_data = collect_all(files_directory=args.directory)

        if args.verbose:
            print(f"      - Hostname: {raw_data['system']['hostname']}")
            print(f"      - OS: {raw_data['system']['os']} {raw_data['system']['os_version']}")
            print(f"      - CPU: {raw_data['cpu']['cpu_percent']}%")
            print(f"      - RAM: {raw_data['memory']['percent']}%")
            print(f"      - Disk: {raw_data['disk']['percent']}%")
            print(f"      - Processes: {raw_data['processes']['total_count']}")
            print(f"      - Files analyzed: {raw_data['files']['total_files']}")

        print("      Collection completed successfully!")
    except Exception as e:
        print(f"      ERROR: {e}")
        return 1

    # Step 2: Data processing (Core Layer)
    print("[2/3] Processing data...")
    try:
        template_vars = get_template_variables(raw_data)
        print(f"      {len(template_vars)} variables generated")
    except Exception as e:
        print(f"      ERROR: {e}")
        return 1

    # Step 3: HTML generation (API Layer)
    print("[3/3] Generating HTML dashboard...")
    try:
        # Determine template path
        script_dir = Path(__file__).parent
        template_path = script_dir / args.template

        if not template_path.exists():
            print(f"      ERROR: Template not found: {template_path}")
            return 1

        output_path = script_dir / args.output

        if generate_file(str(template_path), template_vars, str(output_path)):
            print(f"      Dashboard generated: {output_path}")
        else:
            print("      ERROR: Generation failed")
            return 1
    except Exception as e:
        print(f"      ERROR: {e}")
        return 1

    print()
    print("=" * 50)
    print("  MONITORING COMPLETED SUCCESSFULLY")
    print("=" * 50)
    print()
    print(f"Dashboard available: {output_path}")
    print(f"Open this file in a web browser.")
    print()
    print("The dashboard auto-refreshes every 30 seconds.")
    print("To update data, run this script again.")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())

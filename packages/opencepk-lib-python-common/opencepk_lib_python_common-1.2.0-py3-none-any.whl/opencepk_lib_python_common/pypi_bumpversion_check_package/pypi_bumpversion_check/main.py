#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import toml
import sys
import requests
import subprocess
import logging

def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    # Setup argument parser with usage examples in the epilog
    parser = argparse.ArgumentParser(
        description='Check if the current version is published on PyPI.',
        epilog='''Usage example:
        python main.py pyproject.toml -- Check if the version specified in pyproject.toml is published on PyPI.
        python main.py --usage -- Show this usage example.''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('toml_path', nargs='?', help='Path to the pyproject.toml file')  # Make toml_path optional
    parser.add_argument('--usage', action='store_true', help='Show usage example and exit')

    args = parser.parse_args()

    # If --usage is specified, print the epilog (usage examples) and exit
    if args.usage:
        print(parser.epilog)
        sys.exit(0)

    # Check if toml_path is provided
    if not args.toml_path:
        parser.print_help()
        sys.exit(1)

    logging.info("Loading pyproject.toml from %s", args.toml_path)
    # Load the pyproject.toml file
    with open(args.toml_path) as toml_file:
        data = toml.load(toml_file)

    # Get the current version
    current_version = data["project"]["version"]
    logging.info("Current version: %s", current_version)

    # Get the package name
    package_name = data["project"]["name"]
    logging.info("Package name: %s", package_name)

    # Check if the version is already published
    logging.info("Checking if version %s of %s is already published on PyPI", current_version, package_name)
    response = requests.get(f"https://pypi.org/pypi/{package_name}/{current_version}/json")

    if response.status_code == 200:
        logging.error("This version is already published. Please bump the version in pyproject.toml.")
        sys.exit(1)

    # Check if pyproject.toml has been modified but not committed
    logging.info("Checking if pyproject.toml has been modified but not committed")
    modified_files = subprocess.check_output(["git", "diff", "--name-only"]).decode().splitlines()

    if "pyproject.toml" in modified_files:
        logging.error("The version in pyproject.toml has been changed but not committed. Please commit your changes.")
        sys.exit(1)

if __name__ == "__main__":
    main()

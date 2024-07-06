#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import fileinput
import json
import sys
import logging


def replace_in_file(filename, search, replacement, dry_run=False):
    logging.info(f"Replacing {search} with {replacement} in {filename}")
    with fileinput.FileInput(filename, inplace=not dry_run) as file:
        for line in file:
            if search in line and dry_run:
                logging.info(f"{search} would be replaced with {replacement} in {filename}")
            elif not dry_run:
                print(line.replace(rf"{search}", rf"{replacement}"), end='')


def print_usage():
    print("Example usages:")
    print("python -m find_and_replace_strings --config e2e/.find-and-replace.json e2e/precommit-e2e.test --dry-run --verbose")
    print("python -m find_and_replace_strings --config e2e/.find-and-replace.json e2e/precommit-e2e.test --dry-run --log-level=DEBUG")
    print("python -m find_and_replace_strings --find 'old_string' --replacement 'new_string' example.txt --verbose")
    print("python -m find_and_replace_strings --find 'old_string' --replacement 'new_string' example1.txt example2.txt --verbose")
    print("python -m find_and_replace_strings --config my_config.json example.txt --dry-run --verbose")
    print("python -m find_and_replace_strings --config e2e/.find-and-replace.json e2e/precommit-e2e.test --dry-run --log-level=INFO")


def main():
    parser = argparse.ArgumentParser(
        description="""Perform find and replace operations on one or more target files.
                    By default, the script reads the search and replacement entries (strings) from a JSON file.
                    You can also specify the search and replacement strings directly as command line args by setting the
                    --find "search_string" and --replacement "replacement_string" argument options."""
    )
    parser.add_argument(
        '--config', default='.find-and-replace.json',
        help='PATH to JSON config file containing find and replacement entries'
    )
    parser.add_argument(
        '--find', dest='direct_mode', action='store_true', help='String to find in files'
    )
    parser.add_argument(
        '--replacement', dest='direct_mode', action='store_true', help='String to replace with in files'
    )
    parser.add_argument(
        'files', nargs='*', help='File(s) on which to perform search and replace'
    )
    parser.add_argument(
        '--dry-run', action='store_true', help='Perform a dry run without making any changes'
    )
    parser.add_argument(
        '--log-level', default='WARNING', help='Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)'
    )
    parser.add_argument(
        '--verbose', action='store_true', help='Print debug and info messages'
    )
    parser.add_argument(
        '--usage', action='store_true', help='Print example usages'
    )
    args = parser.parse_args()

    if args.usage:
        print_usage()
        sys.exit(0)

    levels = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO, 'WARNING': logging.WARNING, 'ERROR': logging.ERROR, 'CRITICAL': logging.CRITICAL}
    level = levels.get(args.log_level.upper(), logging.WARNING)
    if args.verbose:
        level = logging.DEBUG
    logging.basicConfig(level=level)

    config_path = os.path.abspath(args.config)

    if args.direct_mode:
        logging.info("Running in direct mode")
        for filename in args.files:
            file_path = os.path.abspath(filename)
            if file_path == config_path:
                logging.info(f"Skipping config file: {filename}")
                continue
            replace_in_file(filename, args.find, args.replacement, args.dry_run)
    else:
        logging.info("Running in default config file mode")
        try:
            with open(config_path, 'r') as f:
                replacements = json.load(f)
        except FileNotFoundError:
            logging.error(f"Error: {args.config} file not found.")
            logging.error(f'''Error: If your repo contains a {args.config}.template file -
                          update the values inside the template file and then rename {args.config}.template to {args.config}''')
            sys.exit(1)
        except json.JSONDecodeError:
            logging.error(f"Error: {args.config} is not a valid JSON file.")
            sys.exit(1)

        for filename in args.files:
            file_path = os.path.abspath(filename)
            if file_path == config_path:
                logging.info(f"Skipping config file: {filename}")
                continue
            for replacement in replacements:
                replace_in_file(filename, replacement['search'], replacement['replacement'], args.dry_run)

if __name__ == "__main__":
    main()

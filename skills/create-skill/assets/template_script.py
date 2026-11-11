#!/usr/bin/env python3
"""
Template script for an Agent Skill helper script.
"""

import argparse
import sys


def parse_arguments():
    parser = argparse.ArgumentParser(description="Helper script description")
    parser.add_argument("--input", required=True, help="Path to input data")
    parser.add_argument("--output", help="Path to output data (optional)")
    return parser.parse_args()


def main():
    args = parse_arguments()
    print(f"Processing {args.input}...")
    # Add business logic here
    print("Done successfully.")
    sys.exit(0)


if __name__ == "__main__":
    main()

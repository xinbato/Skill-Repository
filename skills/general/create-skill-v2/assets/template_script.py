#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
Helper script for {{SKILL_NAME}}.
Adheres to the agentskills.io standard for non-interactive execution.
"""

import argparse
import json
import sys


def parse_args():
    parser = argparse.ArgumentParser(description="Helper script for {{SKILL_NAME}}")
    parser.add_argument("--input", "-i", required=True, help="Path to input file")
    parser.add_argument("--output", "-o", help="Optional path to output file")
    parser.add_argument("--format", choices=["json", "text"], default="json", help="Output format")
    return parser.parse_args()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    args = parse_args()

    # Diagnostics and logs go to stderr to keep stdout clean for structured data
    print(f"[INFO] Processing {args.input}...", file=sys.stderr)

    # Core logic here
    result = {
        "status": "success",
        "skill": "{{SKILL_NAME}}",
        "input": args.input,
        "processed": True
    }

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"[SUCCESS] Output written to {args.output}", file=sys.stderr)
    else:
        # Structured data output to stdout
        print(json.dumps(result, indent=2, ensure_ascii=False))

    sys.exit(0)


if __name__ == "__main__":
    main()

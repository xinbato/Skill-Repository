#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
Generates an interactive, standalone HTML evaluation report from grading.json.
"""

import argparse
import json
import sys
from pathlib import Path


def generate_html_report(grading_file: Path, output_html: Path):
    if not grading_file.exists():
        raise FileNotFoundError(f"Grading file not found: {grading_file}")

    data = json.loads(grading_file.read_text(encoding="utf-8"))
    template_path = Path(__file__).resolve().parent.parent / "assets" / "eval_report_template.html"

    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    template = template_path.read_text(encoding="utf-8")

    # Build eval items HTML
    cases_html = []
    for case in data.get("cases", []):
        badge_class = "pass" if case.get("passed", True) else "fail"
        badge_text = "PASS" if case.get("passed", True) else "FAIL"

        assertions_html = "".join(
            f"<li>[{'OK' if a['passed'] else 'FAIL'}] {a['assertion']} <em>({a.get('evidence', '')})</em></li>"
            for a in case.get("assertions", [])
        )

        cases_html.append(f"""
        <div class="test-case">
          <div class="test-header">
            <strong>Case #{case.get('id')}: {case.get('prompt', '')[:80]}...</strong>
            <span class="badge {badge_class}">{badge_text}</span>
          </div>
          <div class="prompt">{case.get('prompt')}</div>
          <ul class="assertions">
            {assertions_html if assertions_html else "<li>No specific assertions declared.</li>"}
          </ul>
        </div>
        """)

    total_evals = data.get("total_cases", 0)
    pass_rate = data.get("pass_rate_percent", 0.0)
    passed = sum(1 for c in data.get("cases", []) if c.get("passed", True))
    failed = total_evals - passed

    html_content = template.replace("{{SKILL_NAME}}", data.get("skill_name", "unknown"))
    html_content = html_content.replace("{{TIMESTAMP}}", data.get("timestamp", ""))
    html_content = html_content.replace("{{TOTAL_EVALS}}", str(total_evals))
    html_content = html_content.replace("{{PASS_RATE}}", str(pass_rate))
    html_content = html_content.replace("{{PASSED}}", str(passed))
    html_content = html_content.replace("{{FAILED}}", str(failed))
    html_content = html_content.replace("{{EVAL_ITEMS}}", "\n".join(cases_html))

    output_html.parent.mkdir(parents=True, exist_ok=True)
    output_html.write_text(html_content, encoding="utf-8")
    print(f"[SUCCESS] HTML evaluation report generated: {output_html}", file=sys.stderr)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Generate HTML visual report from grading.json.")
    parser.add_argument("--grading-file", "-i", default="evals/output/grading.json", help="Path to grading.json")
    parser.add_argument("--output", "-o", default="evals/output/report.html", help="Path to output HTML report")

    args = parser.parse_args()

    try:
        generate_html_report(Path(args.grading_file).resolve(), Path(args.output).resolve())
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] Failed to generate HTML report: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

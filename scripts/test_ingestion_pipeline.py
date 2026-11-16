#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
Unit test suite for the Skill Ingestion & Automation Pipeline.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add scripts directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from ingest.dedup import (
    ExistingSkill,
    check_candidate_overlap,
    cosine_similarity,
    tokenize,
)
from ingest.normalizer import (
    normalize_skill_directory,
    parse_frontmatter,
    sanitize_skill_name,
)
from ingest.security import scan_markdown_content, scan_skill_directory


class TestIngestionPipeline(unittest.TestCase):
    def test_dedup_exact_name(self):
        mock_existing = [
            ExistingSkill(
                category="anthropic",
                name="pdf",
                path=Path("dummy"),
                description="PDF manipulation",
                tokens=["pdf", "manipulation"]
            )
        ]
        rep = check_candidate_overlap("pdf", "PDF extractor", "Extracts PDF", mock_existing)
        self.assertEqual(rep.verdict, "EXACT_NAME")
        self.assertEqual(rep.similarity_score, 1.0)

    def test_dedup_unique_skill(self):
        mock_existing = [
            ExistingSkill(
                category="general",
                name="git-workflow",
                path=Path("dummy"),
                description="Git commits and branching",
                tokens=["git", "commits", "branching"]
            )
        ]
        rep = check_candidate_overlap("quantum-computing", "Quantum circuits and Qiskit", "Run quantum code", mock_existing)
        self.assertEqual(rep.verdict, "UNIQUE")
        self.assertLess(rep.similarity_score, 0.5)

    def test_security_hidden_unicode(self):
        malicious_prompt = "Normal text \u200b Hidden injection"
        crits, warns = scan_markdown_content(malicious_prompt)
        self.assertTrue(any("Zero-width" in c for c in crits))

    def test_security_dangerous_eval(self):
        with tempfile.TemporaryDirectory() as td:
            skill_dir = Path(td) / "test-skill"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text("---\nname: test-skill\ndescription: test\n---\n# Test", encoding="utf-8")
            s_dir = skill_dir / "scripts"
            s_dir.mkdir()
            (s_dir / "bad.py").write_text("x = eval('1+1')", encoding="utf-8")

            rep = scan_skill_directory(skill_dir)
            self.assertFalse(rep.is_safe)
            self.assertTrue(any("eval()" in err for err in rep.critical_errors))

    def test_normalizer_fixes_frontmatter_and_evals(self):
        with tempfile.TemporaryDirectory() as td:
            skill_dir = Path(td) / "my-skill"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text("---\nname: wrong-name\n---\n# My Skill", encoding="utf-8")

            success, changes = normalize_skill_directory(skill_dir, expected_name="my-skill")
            self.assertTrue(success)

            # Check frontmatter name fixed
            updated_content = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            fm, _ = parse_frontmatter(updated_content)
            self.assertEqual(fm.get("name"), "my-skill")
            self.assertEqual(fm.get("license"), "MIT")

            # Check evals scaffolded
            self.assertTrue((skill_dir / "evals" / "evals.json").exists())


if __name__ == "__main__":
    unittest.main()

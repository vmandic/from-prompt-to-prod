"""Smoke tests for GitHub Pages build (requires: pip install -r requirements.txt)."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUILD = REPO / "scripts" / "build_ghpages.py"
VERIFY_HTML = REPO / "docs" / "verify" / "index.html"


class TestGhpagesBuild(unittest.TestCase):
    def test_build_exits_zero(self) -> None:
        r = subprocess.run(
            [sys.executable, str(BUILD)],
            cwd=str(REPO),
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 0, msg=r.stderr or r.stdout or "build failed")

    def test_verify_page_markers(self) -> None:
        text = VERIFY_HTML.read_text(encoding="utf-8")
        self.assertIn("verify-toc.js", text)
        self.assertIn("site-shell--with-toc", text)
        self.assertIn('id="main"', text)


if __name__ == "__main__":
    unittest.main()

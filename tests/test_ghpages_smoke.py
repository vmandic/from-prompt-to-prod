"""Smoke tests for GitHub Pages build (requires: pip install -r requirements.txt)."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUILD = REPO / "scripts" / "build_ghpages.py"
AUDIT_HTML = REPO / "docs" / "self-audit" / "index.html"
LEGACY_VERIFY_REDIRECT = REPO / "docs" / "verify" / "index.html"


class TestGhpagesBuild(unittest.TestCase):
    """Build runs once in setUpClass; unittest orders test_* alphabetically, so do not rely on method order."""

    @classmethod
    def setUpClass(cls) -> None:
        r = subprocess.run(
            [sys.executable, str(BUILD)],
            cwd=str(REPO),
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            raise AssertionError(
                "build_ghpages.py failed:\n" + (r.stderr or r.stdout or "(no output)")
            )

    def test_audit_page_markers(self) -> None:
        text = AUDIT_HTML.read_text(encoding="utf-8")
        self.assertIn("site-tracking-control.js?v=", text)
        self.assertIn("site-cookie-notice.js?v=", text)
        self.assertIn("site-analytics.js?v=", text)
        self.assertIn("verify-toc.js?v=", text)
        self.assertIn("base.css?v=", text)
        self.assertIn("site-toc-scroll", text)
        self.assertIn("site-shell--with-toc", text)
        self.assertIn('id="main"', text)
        self.assertIn("/self-audit/", text)
        # Rubric file links must stay absolute GitHub URLs for copy-paste from the page into agents.
        self.assertIn(
            "https://github.com/vmandic/from-prompt-to-prod/blob/main/README.md",
            text,
        )
        self.assertIn('class="copy-block"', text)
        self.assertIn("prompt-wizard.js?v=", text)
        self.assertIn('id="prompt-wizard"', text)
        self.assertIn('id="prompt-wizard-data"', text)

    def test_legacy_verify_redirect_page(self) -> None:
        text = LEGACY_VERIFY_REDIRECT.read_text(encoding="utf-8")
        self.assertIn("self-audit", text.lower())
        self.assertIn("http-equiv", text.lower())
        self.assertIn("refresh", text.lower())
        self.assertIn("noindex", text.lower())


if __name__ == "__main__":
    unittest.main()

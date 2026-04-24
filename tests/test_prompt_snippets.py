"""Golden checks for self-audit starter prompt composition."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from prompt_snippets import (  # noqa: E402
    OPENING_COMPUTER_WIDE,
    OPENING_PROJECT,
    PROMPT_COMPUTER_WIDE,
    PROMPT_PROJECT,
    compose_starter_body,
    wizard_config_json_for_html,
)


class TestPromptSnippets(unittest.TestCase):
    def test_bracket_examples_match_compose(self) -> None:
        body = compose_starter_body(
            "[$HOME/dir]",
            "[claude, cursor, copilot]",
            "[N] years",
            "[skills/MCP usage]",
        )
        self.assertEqual(OPENING_COMPUTER_WIDE + body, PROMPT_COMPUTER_WIDE)
        self.assertEqual(OPENING_PROJECT + body, PROMPT_PROJECT)

    def test_wizard_json_parseable(self) -> None:
        data = json.loads(wizard_config_json_for_html())
        self.assertIn("openingComputerWide", data)
        self.assertIn("bodyTemplate", data)
        self.assertIn("__DIR__", data["bodyTemplate"])
        self.assertTrue(data.get("tools"))
        self.assertEqual(len(data.get("years", [])), 4)
        ids = [t["id"] for t in data["tools"]]
        self.assertIn("openclaw", ids)
        self.assertNotIn("other", ids)

"""Starter prompts for the self-audit rubric.

Used by scripts/build_ghpages.py for the self-audit page. Keep the same wording in sync
with docs/index.html (copy blocks) and README.md (fenced examples).
"""

from __future__ import annotations

import html
import json
import re
from typing import Any

RUBRIC_RAW_URL = (
    "https://raw.githubusercontent.com/vmandic/from-prompt-to-prod/main/"
    "src/verify-your-agentic-workflows.md"
)

OPENING_COMPUTER_WIDE = (
    'This is an agentic workflows and daily use auditing task based on presentation '
    '"From prompt to prod". '
    "Audit me computer-wide. "
)
OPENING_PROJECT = (
    'This is an agentic workflows and daily use auditing task based on presentation '
    '"From prompt to prod". '
    "In project mode only. "
)

# Shared body: {dir} {tools} {n_years} {skills_mcp} are filled by the site wizard or examples.
_BODY_CORE = (
    "My code lives under {dir}. I use {tools} daily for {n_years}. "
    "Agent skills / MCPs: {skills_mcp}. Paste the full rubric from "
    f"{RUBRIC_RAW_URL} as your user message (or fetch that URL), then follow it: "
    "plan T1+T2 first, bounded scans only, structured A–K report, no secret values "
    "in the output."
)


def compose_starter_body(
    dir_value: str,
    tools: str,
    n_years: str,
    skills_mcp: str,
) -> str:
    return _BODY_CORE.format(
        dir=dir_value,
        tools=tools,
        n_years=n_years,
        skills_mcp=skills_mcp,
    )


PROMPT_COMPUTER_WIDE = OPENING_COMPUTER_WIDE + compose_starter_body(
    "[$HOME/dir]",
    "[claude, cursor, copilot]",
    "[N] years",
    "[skills/MCP usage]",
)

PROMPT_PROJECT = OPENING_PROJECT + compose_starter_body(
    "[$HOME/dir]",
    "[claude, cursor, copilot]",
    "[N] years",
    "[skills/MCP usage]",
)

COPY_BTN_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>"""


def copy_block_html(code: str, code_id: str | None = None) -> str:
    """Wrap escaped code in a copy-to-clipboard block (matches docs/assets/copy-blocks.js)."""
    safe = html.escape(code, quote=True)
    id_attr = ""
    if code_id and re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", code_id):
        id_attr = f' id="{html.escape(code_id, quote=True)}"'
    return (
        '<div class="copy-block">\n'
        '  <button type="button" class="copy-block__btn" aria-label="Copy to clipboard" title="Copy">\n'
        f"    {COPY_BTN_SVG}\n"
        "  </button>\n"
        f"  <pre><code{id_attr}>{safe}</code></pre>\n"
        "</div>\n"
    )


# Wizard: tool ids (order preserved when joining selected). "Other" is a free-text field; UI may combine it with checked tools.
WIZARD_TOOLS: list[dict[str, str]] = [
    {"id": "claude", "label": "Claude Code"},
    {"id": "cursor", "label": "Cursor"},
    {"id": "copilot", "label": "GitHub Copilot"},
    {"id": "codex", "label": "OpenAI Codex / ChatGPT coding"},
    {"id": "openclaw", "label": "OpenClaw"},
    {"id": "windsurf", "label": "Windsurf"},
]

# Wizard years: four bands (radio group). "Total newbie" is not the same as "< 1 year" on the job.
WIZARD_YEARS: list[dict[str, str]] = [
    {
        "value": "newbie",
        "label": "Total newbie",
        "phrase": "only days or weeks so far (total newbie)",
    },
    {"value": "lt1", "label": "Less than 1 year", "phrase": "less than 1 year"},
    {"value": "gt1", "label": "More than 1 year", "phrase": "over 1 year"},
    {"value": "gt3", "label": "More than 3 years", "phrase": "more than 3 years"},
]

WIZARD_SKILLS_PRESETS: list[dict[str, str]] = [
    {
        "id": "heavy",
        "label": "Heavy",
        "text": "heavy daily use; many packaged agent skills and several MCP integrations",
    },
    {
        "id": "moderate",
        "label": "Moderate",
        "text": "moderate use; some skills and a few MCP tools when tasks need them",
    },
    {
        "id": "light",
        "label": "Light",
        "text": "light use; occasional skills, rarely MCPs",
    },
    {
        "id": "minimal",
        "label": "Minimal",
        "text": "minimal; mostly defaults, almost no MCPs",
    },
    {
        "id": "none",
        "label": "None / unsure",
        "text": "none or not sure yet",
    },
]


def wizard_config() -> dict[str, Any]:
    """Data for docs/assets/prompt-wizard.js (embedded as JSON in self-audit page)."""
    return {
        "openingComputerWide": OPENING_COMPUTER_WIDE,
        "openingProject": OPENING_PROJECT,
        "rubricRawUrl": RUBRIC_RAW_URL,
        "bodyTemplate": (
            "My code lives under __DIR__. I use __TOOLS__ daily for __N_YEARS__. "
            "Agent skills / MCPs: __SKILLS_MCP__. Paste the full rubric from __RUBRIC_URL__ "
            "as your user message (or fetch that URL), then follow it: "
            "plan T1+T2 first, bounded scans only, structured A–K report, no secret values "
            "in the output."
        ),
        "tools": WIZARD_TOOLS,
        "years": WIZARD_YEARS,
        "skillsPresets": WIZARD_SKILLS_PRESETS,
    }


def wizard_config_json_for_html() -> str:
    """JSON string safe to embed inside <script type=\"application/json\">."""
    return json.dumps(wizard_config(), ensure_ascii=True)

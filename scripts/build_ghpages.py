#!/usr/bin/env python3
"""Build GitHub Pages output: docs/self-audit/index.html from verify-your-agentic-workflows.md."""

from __future__ import annotations

import html
import json
import os
import re
import sys
from pathlib import Path

import markdown
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.nl2br import Nl2BrExtension
from markdown.extensions.sane_lists import SaneListExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension

ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from prompt_snippets import (  # noqa: E402
    PROMPT_COMPUTER_WIDE,
    PROMPT_PROJECT,
    copy_block_html,
    wizard_config_json_for_html,
)

MD_PATH = ROOT / "src" / "verify-your-agentic-workflows.md"


def _audit_url_segment(raw: str, default: str = "self-audit") -> str:
    """Single path segment for /docs/<seg>/; rejects traversal and odd characters."""
    seg = raw.strip().strip("/")
    if not seg or ".." in seg or "/" in seg or "\\" in seg:
        return default
    if not re.fullmatch(r"[A-Za-z0-9_-]+", seg):
        return default
    return seg


# URL path /self-audit/ (legacy /verify/ is a small redirect HTML in docs/verify/).
AUDIT_SEG = _audit_url_segment(os.environ.get("AUDIT_PATH", "self-audit"))
OUT_PATH = ROOT / "docs" / AUDIT_SEG / "index.html"

SITE_URL = os.environ.get(
    "SITE_URL", "https://vmandic.github.io/from-prompt-to-prod"
).rstrip("/")
# Project Pages base path (leading slash) — use for in-site links so /repo vs /repo/ does not break relatives
SITE_BASE = os.environ.get("SITE_BASE", "/from-prompt-to-prod").rstrip("/") or "/from-prompt-to-prod"
if not SITE_BASE.startswith("/"):
    SITE_BASE = "/" + SITE_BASE

# Query string so GitHub Pages / browsers pick up new base.css + verify-toc.js after deploy
ASSET_QUERY = os.environ.get("ASSET_QUERY", "25")

TITLE = "Verify your agentic workflows"
FULL_TITLE = f"{TITLE} — From prompt to prod"
DESCRIPTION = (
    "Rubric and process: compare your Cursor and agentic setup to the "
    "From prompt to prod talk (A–K dimensions). For use as an agent prompt; "
    "bounded scans, no secret paste."
)

CANONICAL = f"{SITE_URL}/{AUDIT_SEG}/"
OG_IMAGE = f"{SITE_URL}/assets/photos/croai-title-qr.png"
# Slides file lives at repo root; /docs is the Pages root, so we link to the file on main.
PDF_URL = os.environ.get(
    "PDF_URL",
    "https://raw.githubusercontent.com/vmandic/from-prompt-to-prod/main/from-promt-to-prod-v2.pdf",
)
# Stable file URLs for the rubric body so copy-paste from the self-audit page keeps working in chat (not site-relative).
GITHUB_REPO = os.environ.get(
    "GITHUB_REPO", "https://github.com/vmandic/from-prompt-to-prod"
).rstrip("/")
README_BLOB_URL = os.environ.get(
    "README_BLOB_URL",
    f"{GITHUB_REPO}/blob/main/README.md",
)

MD_EXTENSIONS = [
    TableExtension(),
    FencedCodeExtension(),
    Nl2BrExtension(),
    SaneListExtension(),
    TocExtension(
        permalink=False,
        baselevel=1,
    ),
]


def attr(s: str) -> str:
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def esc_html(s: str) -> str:
    return html.escape(s, quote=True)


def extract_toc(body: str) -> list[tuple[int, str, str]]:
    items: list[tuple[int, str, str]] = []
    re_h = re.compile(
        r'<h([23]) id="([^"]+)"[^>]*>([\s\S]*?)</h\1>', re.IGNORECASE
    )
    for m in re_h.finditer(body):
        level = int(m.group(1))
        hid = m.group(2)
        inner = m.group(3)
        text = re.sub(r"<a\b[^>]*>[\s\S]*?</a>", "", inner, flags=re.IGNORECASE)
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        text = html.unescape(text)
        if text:
            items.append((level, hid, text))
    return items


def build_toc_nav(toc: list[tuple[int, str, str]]) -> str:
    if not toc:
        return ""
    # Use a paragraph for the label so the first heading in <main> remains <h1>
    lines = [
        '<nav class="on-this-page" aria-labelledby="on-this-page-label">',
        '  <p class="on-this-page__title" id="on-this-page-label">On this page</p>',
        "  <ol>",
    ]
    for level, hid, text in toc:
        # id="..." in body comes from the same build; only reject pathological ids
        if '"' in hid or "<" in hid or ">" in hid or not hid.strip():
            continue
        lines.append(
            f'    <li class="on-this-page__item on-this-page__item--h{level}">'
            f'<a href="#{hid}">{esc_html(text)}</a></li>'
        )
    lines.append("  </ol>")
    lines.append("</nav>")
    return "\n".join(lines)


def preface() -> str:
    wizard_json = wizard_config_json_for_html()
    # Fail build if snippets produce invalid JSON (do not HTML-escape JSON inside script).
    json.loads(wizard_json)
    empty_copy = copy_block_html("", code_id="prompt-wizard-output-code")
    ex_cw = copy_block_html(PROMPT_COMPUTER_WIDE)
    ex_proj = copy_block_html(PROMPT_PROJECT)
    return f"""<section class="callout callout--cta" aria-labelledby="self-audit-heading">
  <h2 id="self-audit-heading">How to self-audit yourself</h2>
  <p class="callout__lede">
    Use the <strong>prompt builder</strong> below to generate a starter message (click choices; type only your path), then paste that starter and the
    <a href="https://raw.githubusercontent.com/vmandic/from-prompt-to-prod/main/src/verify-your-agentic-workflows.md">full rubric</a>
    into <strong>your preferred coding agent</strong> (Cursor, Claude Code, Copilot in the editor, or similar) <strong>that can read your files on disk</strong>. The rubric expects bounded scans of real paths; a session with no filesystem access cannot follow it. If your client did not already load the rubric, send it as the next user message after the starter. The rubric tells the agent how to plan, scan, and report A–K.
  </p>
  <div id="prompt-wizard" class="prompt-wizard" role="group" aria-labelledby="prompt-wizard-title">
    <h3 id="prompt-wizard-title" class="prompt-wizard__title">Build your starter prompt</h3>
    <p class="prompt-wizard__intro">Choose computer-wide or one project, pick tools and presets, type your source path, then generate and copy.</p>
    <button type="button" class="prompt-wizard__start" id="prompt-wizard-start">Start</button>
    <div class="prompt-wizard__panel" id="prompt-wizard-panel" hidden>
      <fieldset class="prompt-wizard__fieldset">
        <legend class="prompt-wizard__legend">Mode</legend>
        <div class="prompt-wizard__mode" role="group" aria-label="Audit mode">
          <button type="button" class="prompt-wizard__mode-btn prompt-wizard__mode-btn--active" id="prompt-wizard-mode-cw" data-mode="computer" aria-pressed="true">Computer-wide</button>
          <button type="button" class="prompt-wizard__mode-btn" id="prompt-wizard-mode-proj" data-mode="project" aria-pressed="false">Project only</button>
        </div>
        <p class="prompt-wizard__mode-hint" id="prompt-wizard-mode-hint">Audit across your machine; put your usual source root (e.g. <code>$HOME/work</code>) in the path field.</p>
      </fieldset>
      <fieldset class="prompt-wizard__fieldset">
        <legend class="prompt-wizard__legend" id="prompt-wizard-path-label">Source(s) path</legend>
        <input type="text" class="prompt-wizard__path" id="prompt-wizard-path" autocomplete="off" placeholder="$HOME/work, or several roots (spaces or commas)" aria-labelledby="prompt-wizard-path-label" />
      </fieldset>
      <fieldset class="prompt-wizard__fieldset">
        <legend class="prompt-wizard__legend">Daily tools</legend>
        <div class="prompt-wizard__tools" id="prompt-wizard-tools"></div>
        <p class="prompt-wizard__other-tools-wrap">
          <label class="prompt-wizard__other-tools-label" for="prompt-wizard-other-tools">Other tools</label>
          <span class="prompt-wizard__other-tools-hint"> (optional; you can use this together with the checkboxes)</span>
        </p>
        <input type="text" class="prompt-wizard__other-tools" id="prompt-wizard-other-tools" autocomplete="off" placeholder="e.g. JetBrains AI Assistant, custom CLI agent" aria-label="Other daily tools (optional; works alongside checkboxes)" />
      </fieldset>
      <fieldset class="prompt-wizard__fieldset">
        <legend class="prompt-wizard__legend" id="prompt-wizard-years-label">How long do you use agents?</legend>
        <div class="prompt-wizard__years prompt-wizard__years--radios" id="prompt-wizard-years" role="radiogroup" aria-labelledby="prompt-wizard-years-label"></div>
      </fieldset>
      <fieldset class="prompt-wizard__fieldset">
        <legend class="prompt-wizard__legend">Agent skills and MCPs</legend>
        <div class="prompt-wizard__presets" id="prompt-wizard-skills"></div>
      </fieldset>
      <p class="prompt-wizard__err" id="prompt-wizard-err" role="alert" hidden></p>
      <button type="button" class="prompt-wizard__generate" id="prompt-wizard-generate">Generate prompt</button>
      <div class="prompt-wizard__postgen">
        <p class="prompt-wizard__disclaimer">
          <strong>Privacy:</strong> this is a client-side prompt generator. Nothing you type or select is sent anywhere; it only builds text in your browser.
        </p>
        <p class="prompt-wizard__disclaimer">
          If you want a ready-made example instead, expand <strong>Example prompts</strong> and copy a template, then edit it to match your setup (computer-wide vs project-only).
        </p>
        <details class="prompt-wizard__examples-details">
          <summary class="prompt-wizard__examples-summary">Example prompts</summary>
          <div class="prompt-wizard__examples-inner">
            <p class="prompt-wizard__examples-h"><strong>Computer-wide</strong> (bracketed placeholders)</p>
{ex_cw}
            <p class="prompt-wizard__examples-h"><strong>Project only</strong> (same body; set the path to your checkout)</p>
{ex_proj}
          </div>
        </details>
      </div>
    </div>
    <div class="prompt-wizard__result" id="prompt-wizard-result" hidden>
      <p class="prompt-wizard__result-label">Your starter message</p>
      {empty_copy}
    </div>
    <p class="prompt-wizard__live" id="prompt-wizard-live" aria-live="polite"></p>
  </div>
  <script type="application/json" id="prompt-wizard-data">{wizard_json}</script>
</section>
<section class="callout" aria-label="How to use this page">
  <h2>How to use this page</h2>
  <ol>
    <li><strong>Paste</strong> the <a href="https://raw.githubusercontent.com/vmandic/from-prompt-to-prod/main/src/verify-your-agentic-workflows.md">source markdown</a> (or the file from this repo) as a <strong>user message</strong> in your AI coding agent.</li>
    <li><strong>Choose</strong> <em>computer-wide</em> or <em>project</em> mode and answer the mandatory questions (source roots for machine-wide runs).</li>
    <li><strong>Get</strong> a structured A–K report with anchors, evidence, and concrete next steps—no secret values in the output.</li>
  </ol>
</section>
"""


def main() -> int:
    if not MD_PATH.is_file():
        print("Missing:", MD_PATH, file=sys.stderr)
        return 1

    raw = MD_PATH.read_text(encoding="utf-8")
    md = markdown.Markdown(extensions=MD_EXTENSIONS)
    body = md.convert(raw)

    # Drop source h1; page template has its own title.
    body = re.sub(
        r"^<h1[^>]*>[\s\S]*?</h1>\s*",
        "",
        body,
        count=1,
        flags=re.MULTILINE,
    )
    readme_href = attr(README_BLOB_URL)
    body = body.replace('href="../README.md"', f'href="{readme_href}"')
    body = body.replace('href="../index.html"', f'href="{readme_href}"')
    body = body.replace('href="../from-promt-to-prod-v2.pdf"', f'href="{PDF_URL}"')
    # Source links use "a–K" (en dash); ToC extension slug ends with "ak"
    body = re.sub(
        r'href="#best-practice-anchors-mandatory-injection-a[\u2013\-]k"',
        'href="#best-practice-anchors-mandatory-injection-ak"',
        body,
    )

    toc = extract_toc(body)
    toc_nav = build_toc_nav(toc)

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc_html(FULL_TITLE)}</title>
  <meta name="description" content="{attr(DESCRIPTION)}" />
  <link rel="canonical" href="{esc_html(CANONICAL)}" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{attr(FULL_TITLE)}" />
  <meta property="og:description" content="{attr(DESCRIPTION)}" />
  <meta property="og:url" content="{esc_html(CANONICAL)}" />
  <meta property="og:image" content="{esc_html(OG_IMAGE)}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{attr(FULL_TITLE)}" />
  <meta name="twitter:description" content="{attr(DESCRIPTION)}" />
  <meta name="twitter:image" content="{esc_html(OG_IMAGE)}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{SITE_BASE}/assets/base.css?v={ASSET_QUERY}" />
  <link rel="icon" href="{SITE_BASE}/favicon.svg" type="image/svg+xml" />
  <script src="{SITE_BASE}/assets/verify-toc.js?v={ASSET_QUERY}" defer></script>
  <script src="{SITE_BASE}/assets/copy-blocks.js?v={ASSET_QUERY}" defer></script>
  <script src="{SITE_BASE}/assets/prompt-wizard.js?v={ASSET_QUERY}" defer></script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <div class="site-shell site-shell--with-toc">
    <header class="site-header">
      <nav class="site-nav" aria-label="Site">
        <a href="{SITE_BASE}/" class="site-nav__brand">From prompt to prod</a>
        <a href="{SITE_BASE}/{AUDIT_SEG}/" class="site-nav__link" aria-current="page">Self-audit</a>
        <a href="{esc_html(PDF_URL)}" class="site-nav__link">Slides (PDF)</a>
        <a href="https://github.com/vmandic/from-prompt-to-prod" class="site-nav__link">Source</a>
      </nav>
    </header>
    <aside class="site-toc-wrap" id="site-toc">
      <div class="site-toc-scroll">
        {toc_nav}
      </div>
    </aside>
    <main id="main" class="site-main site-main--audit">
      <article class="prose">
        <h1 class="prose__title">{esc_html(TITLE)}</h1>
        <p class="lede">Self-audit against the talk. Compare what an agent can observe to these practices: context, agent loop, tooling, and safety.</p>
        {preface()}
        <div class="md-body">
{body}
        </div>
      </article>
    </main>
  </div>
</body>
</html>
"""

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(page, encoding="utf-8")
    rel = OUT_PATH.relative_to(ROOT)
    print("Wrote", rel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

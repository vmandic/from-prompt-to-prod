#!/usr/bin/env python3
"""Build GitHub Pages output: docs/verify/index.html from verify-your-agentic-workflows.md."""

from __future__ import annotations

import html
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
MD_PATH = ROOT / "src" / "verify-your-agentic-workflows.md"
OUT_PATH = ROOT / "docs" / "verify" / "index.html"

SITE_URL = os.environ.get(
    "SITE_URL", "https://vmandic.github.io/from-prompt-to-prod"
).rstrip("/")
# Project Pages base path (leading slash) — use for in-site links so /repo vs /repo/ does not break relatives
SITE_BASE = os.environ.get("SITE_BASE", "/from-prompt-to-prod").rstrip("/") or "/from-prompt-to-prod"
if not SITE_BASE.startswith("/"):
    SITE_BASE = "/" + SITE_BASE

# Query string so GitHub Pages / browsers pick up new base.css + verify-toc.js after deploy
ASSET_QUERY = os.environ.get("ASSET_QUERY", "4")

TITLE = "Verify your agentic workflows"
FULL_TITLE = f"{TITLE} — From prompt to prod"
DESCRIPTION = (
    "Rubric and process: compare your Cursor and agentic setup to the "
    "From prompt to prod talk (A–K dimensions). For use as an agent prompt; "
    "bounded scans, no secret paste."
)

CANONICAL = f"{SITE_URL}/verify/"
OG_IMAGE = f"{SITE_URL}/assets/photos/croai-title-qr.png"
# Slides file lives at repo root; /docs is the Pages root, so we link to the file on main.
PDF_URL = os.environ.get(
    "PDF_URL",
    "https://raw.githubusercontent.com/vmandic/from-prompt-to-prod/main/from-promt-to-prod-v2.pdf",
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
    return """<section class="callout" aria-label="How to use this page">
  <h2>How to use this</h2>
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
    body = body.replace('href="../README.md"', f'href="{SITE_BASE}/"')
    body = body.replace('href="../index.html"', f'href="{SITE_BASE}/"')
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
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <div class="site-shell site-shell--with-toc">
    <header class="site-header">
      <nav class="site-nav" aria-label="Site">
        <a href="{SITE_BASE}/" class="site-nav__brand">From prompt to prod</a>
        <a href="{SITE_BASE}/verify/" class="site-nav__link" aria-current="page">Self-check</a>
        <a href="{esc_html(PDF_URL)}" class="site-nav__link">Slides (PDF)</a>
        <a href="https://github.com/vmandic/from-prompt-to-prod" class="site-nav__link">Source</a>
      </nav>
    </header>
    <aside class="site-toc-wrap" id="site-toc">
      <div class="site-toc-scroll">
        {toc_nav}
      </div>
    </aside>
    <main id="main" class="site-main site-main--verify">
      <article class="prose">
        <h1 class="prose__title">{esc_html(TITLE)}</h1>
        <p class="lede">Self-check against the talk. Compare what an agent can observe to these practices: context, agent loop, tooling, and safety.</p>
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

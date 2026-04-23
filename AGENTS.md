# AGENTS.md — from-prompt-to-prod (rudimentary)

## What this repo is

- **Talk materials:** PDF + Keynote at repo root; outline and links in [`README.md`](README.md).
- **Self-check rubric (agent prompt):** [`src/verify-your-agentic-workflows.md`](src/verify-your-agentic-workflows.md) — A–K dimensions vs the talk; materials-only repos may show N/A for some file-based rows.
- **Static site (GitHub Pages):** source lives in **`docs/`**. With Pages set to publish from **`/docs` on `main`**, the **public site root** is `https://vmandic.github.io/from-prompt-to-prod/` — there is **no** `/docs` segment in the URL.

## Conventions we settled on in repo work

- **Do not** add a top-level folder named `writing-plans` for the site — that was a **planning-skill** label, not a product path. The published site is **`docs/`**.
- **Regenerate** [`docs/verify/index.html`](docs/verify/index.html) from the markdown: `python3 build_writing_plans.py` (needs `pip install -r requirements.txt`), or `npm run build:site`. Commit the HTML if you change the `.md` source and want the live site to match.
- **Slides on the site:** PDF is linked via **raw** `main` on GitHub (repo root is not inside `docs/`-only deploy).
- **README:** keep it for **readers** of the talk; avoid long “how to build the site” blocks unless the owner asks.
- Shields / badges: the owner preferred a **single website** badge; keep README minimal unless told otherwise.

## If you are unsure

- Read [`README.md`](README.md) and the first section of `src/verify-your-agentic-workflows.md` before big edits.

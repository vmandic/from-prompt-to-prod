# AGENTS.md — from-prompt-to-prod (rudimentary)

## What this repo is

- **Talk materials:** PDF + Keynote at repo root; outline and links in [`README.md`](README.md).
- **Self-audit rubric (agent prompt):** [`src/verify-your-agentic-workflows.md`](src/verify-your-agentic-workflows.md) — A–K dimensions vs the talk; materials-only repos may show N/A for some file-based rows.
- **Static site (GitHub Pages):** source lives in **`docs/`**. With Pages set to publish from **`/docs` on `main`**, the **public site root** is `https://vmandic.github.io/from-prompt-to-prod/` — there is **no** `/docs` segment in the URL. **Internal links use root-relative paths** (`/from-prompt-to-prod/...`) so nav and CSS work whether or not the URL has a trailing slash (GitHub project Pages quirk); local `file://` or a bare `http.server` at repo root will not match that base unless you fake the path.

## Conventions we settled on in repo work

- **Do not** add a top-level folder named `writing-plans` for the site — that was a **planning-skill** label, not a product path. The published site is **`docs/`**.
- **Regenerate** [`docs/self-audit/index.html`](docs/self-audit/index.html) from the markdown: `python3 scripts/build_ghpages.py` (needs `pip install -r requirements.txt`, or a project **`.venv`** with `markdown` installed), or `npm run build:site`. Commit the HTML if you change the `.md` source and want the live site to match. Legacy URL **`/verify/`** serves a short redirect to **`/self-audit/`**. **Smoke test:** `python3 -m unittest discover -s tests -v` (same Python as the build).
- **Self-audit prompt wizard:** the interactive UI on the self-audit page is built from [`scripts/prompt_snippets.py`](scripts/prompt_snippets.py) (JSON embedded in HTML) plus [`docs/assets/prompt-wizard.js`](docs/assets/prompt-wizard.js). After changing that JS or wizard-related CSS, bump `ASSET_QUERY` in `scripts/build_ghpages.py` so browsers pick up new assets.
- **Run the site locally:** from repo root, `python3 scripts/serve_site.py` — **reads `docs/` live** (not a one-time copy); save HTML/CSS/JS in `docs/` and **refresh the browser** to see changes (no server restart; optional `Cache-Control: no-store` on responses). Use `PORT=9000` if the default (`8765`) is taken. For **layout/DOM checks**, use that origin (e.g. `http://127.0.0.1:8765/from-prompt-to-prod/self-audit/`) when the user provides it.
- **Slides on the site:** PDF is linked via **raw** `main` on GitHub (repo root is not inside `docs/`-only deploy).
- **README:** keep it for **readers** of the talk; avoid long “how to build the site” blocks unless the owner asks.
- Shields / badges: the owner preferred a **single website** badge; keep README minimal unless told otherwise.

## Cross-OS (Unix vs Windows)

Commands and path examples in this file default to **macOS / Linux** and a Unix-style shell (`python3`, `export` / `PORT=...`, `~` for home, forward slashes).

- **On native Windows (cmd, PowerShell):** Adapt paths, quoting, and **`py` / `python` / `python3`** to whatever is on `PATH`. For home, prefer **`%USERPROFILE%`**, `C:\...`, or well-known user folders over `~` in these shells. Use **NTFS**-safe names and path lengths; do not copy-paste long Unix one-liners without checking.
- **Env vars** depend on the shell, for example: `$env:PORT=9000; python scripts\serve_site.py` in **PowerShell**; `set PORT=9000` then run Python in **cmd**.
- **Git Bash** / **MSYS2** often support `~` and POSIX-style paths like a Linux session; still be careful when passing paths to **native** Windows tools (`.exe` outside the MSYS environment may need Windows-style or translated paths).
- **WSL** is usually like Linux for patterns in this file, unless the task is about the Windows host or interop across `/mnt/...` and the host.

## If you are unsure

- Read [`README.md`](README.md) and the first section of `src/verify-your-agentic-workflows.md` before big edits.

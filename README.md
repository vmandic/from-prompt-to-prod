# From prompt to prod

[![Live site](https://img.shields.io/badge/live%20site-github.io-1e4d36?style=for-the-badge&logo=google-chrome)](https://vmandic.github.io/from-prompt-to-prod/) [![Self-check (A–K)](https://img.shields.io/badge/self--check-A%E2%80%93K-c9a227?style=for-the-badge)](https://vmandic.github.io/from-prompt-to-prod/verify/) [![GitHub Pages](https://img.shields.io/badge/Pages-%2Fdocs%20on%20main-222?logo=githubpages&logoColor=white)](https://github.com/vmandic/from-prompt-to-prod/deployments)

Materials for a short talk about **Cursor** and **agent-style development**: how to go from an idea in the chat to something you can ship, without losing your mind along the way.

**Speaker:** Vedran Mandić  
**Context:** Backend engineer at Similarweb, shared at CroAI on 21 April 2026.

**Web (GitHub Pages)** — static site: **[vmandic.github.io/from-prompt-to-prod](https://vmandic.github.io/from-prompt-to-prod/)** (home) · **[…/verify/](https://vmandic.github.io/from-prompt-to-prod/verify/)** (A–K self-check). The HTML lives in [`docs/`](docs/); in **Settings → Pages**, use **Deploy from a branch** → `main` → **`/docs`** (that folder is the site root, so the URL has no `/docs` segment). [Deployments and Pages runs →](https://github.com/vmandic/from-prompt-to-prod/deployments)

This repo holds the **slides** so you can read them at your own pace:

- [`from-promt-to-prod-v2.pdf`](from-promt-to-prod-v2.pdf) — PDF export (easy to skim and search)
- [`from-promt-to-prod-v2.key`](from-promt-to-prod-v2.key) — Keynote source (if you use Keynote)

**Regenerate the verify HTML** after editing [`src/verify-your-agentic-workflows.md`](src/verify-your-agentic-workflows.md): with Python 3 and deps (`pip install -r requirements.txt` in a venv), run `python3 build_writing_plans.py` or `npm run build:site`.

---

## What the talk covers

1. **Cursor in context** — AI-native editor on a familiar VS Code base, agents in the UI (and CLI), diffs, indexing, and team-oriented features.
2. **How LLMs actually show up in the editor** — tokens, system prompts, tools, history, and your messages. Why “big context” on the label is not the same as comfortable room left for your work.
3. **Project setup** — `AGENTS.md`, scoped rules, skills, commands, hooks, and MCP configuration. Rules for steady conventions, skills for repeatable workflows.
4. **The agentic loop** — plan before you generate, review like you would a junior’s PR, then verify with tests and your own eyes.
5. **Prompting** — be precise when you know the outcome; stay a bit open when you are exploring. Use paths, symbols, and docs the editor can see.
6. **Parallel work** — subagents, worktrees, and cloud agents when they fit the problem (without forcing complexity).
7. **Extend the toolkit** — MCPs, small CLIs wrapped as skills, team skill repos, and a few ecosystem ideas worth knowing.
8. **Trust but verify** — least privilege, branch hygiene, and keeping secrets out of plain text the model can read.

The deck is an honest personal take, not a product pitch. If something sparks an idea, try it on a small real task first.

---

## Takeaways (short version)

- Spend real time on **context**: globs for rules, lean skills, fresh threads for unrelated work.
- Treat **plan and review** as first-class steps; execution is cheaper when the plan is right.
- Prefer **scoped automation** (skills, MCPs, scripts you own) over giant always-on rule packs.
- **Verify** everything that touches production paths, credentials, or customer data.

---

## Check your setup against the talk (agent prompt)

This is how you can **see whether your project and workflow line up** with the practices from the presentation Vedran shares—**context**, **agent loop**, **tooling**, and **safety**—in a way any AI assistant can run.

- **File:** [`src/verify-your-agentic-workflows.md`](src/verify-your-agentic-workflows.md) — copy or `@`-reference it in chat. The agent must (1) ask **computer-wide** vs **project**, (2) ask **where you keep source code** (one or more directories) for machine-wide runs so it can **sample** real repos—not just `~`—and (3) **plan** the work and use **subagents** (or serial “tracks”) to split **home/global** config (Cursor, Claude, Copilot, Codex, …) from **project** evidence. Every section A–K includes a **best-practice line from the talk** plus your evidence, so a run is never an empty “not observable” list. Front-load to skip questions, e.g. `computer-wide, source roots ~/dev ~/work, home scan OK`.  
  **Note:** *This* repo is mostly **talk materials** (PDF, README). Project-mode here still yields lots of **“N/A to files”** for D–F; the prompt says how to treat **slide-only** vs **application** repos. For a rich check, use **project** on a repo you ship and/or **computer-wide** with **source roots** you actually use.
- **What you get back:** a **research plan**, `T1`/`T2` scan notes, per-dimension **anchors + evidence**, crosswalk, caveats, and an **open** closing—still **no** secret values in the output.

---

## Links mentioned in the slides

- [Addy Osmani — agent skills](https://github.com/addyosmani/agent-skills) — collection and patterns for **packaging** reusable agent “skills” (workflows, scripts, instructions); the deck uses his **treat the model like a junior** quote and the **full loop** (plan → act → review) framing.
- [Cursor “doctor” (community)](https://github.com/nedcodes-ok/cursor-doctor) — community **diagnostics** / health checks for a Cursor install (useful for debugging odd editor or agent behavior; **not** official Cursor support).
- [Notes on Cursor Auto mode and model choice](https://github.com/nedcodes/i-tested-whether-cursors-auto-mode-actually-picks-the-right-model-20ml) — **empirical** write-up on whether **Auto** mode picks a sensible model; supports the talk’s point that you should still **understand** model / cost / task fit instead of assuming the label is magic.
- [Claude Code best practices (community collection)](https://github.com/shanraisshan/claude-code-best-practice) — **curated** tips and links for **Claude Code** (and adjacent agent workflows): prompts, context, skills, and team habits; community-maintained, not an Anthropic official doc.
- [Superpowers (Obra)](https://github.com/obra/superpowers) — a **library of skills** and workflows (TDD, planning, verification, etc.) designed to be loaded by agentic tools; fits the “skills + process discipline” thread in the talk.
- [MemPalace](https://github.com/MemPalace/mempalace) — long-term **memory** for coding agents (MCP tools, wings / rooms / drawers, optional knowledge graph; see also the [MCP integration guide](https://mempalace.github.io/mempalace/guide/mcp-integration.html)).
- [Skillshare (runkids)](https://github.com/runkids/skillshare) — **distribute and sync** a team’s **skills** (and related rules) via **git** so everyone’s agents share the same behaviors; pairs with a shared `skills` repo in your org.

---

## Contact

- **GitHub:** [github.com/vmandic](https://github.com/vmandic) — this repo: [github.com/vmandic/from-prompt-to-prod](https://github.com/vmandic/from-prompt-to-prod)  
- **Handles:** @vekzdran, @vmandic  
- **Email:** mandic.vedran@gmail.com  

If something in the deck is unclear or dated, open an issue or reach out. Happy building.

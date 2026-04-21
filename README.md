# From prompt to prod

Materials for a short talk about **Cursor** and **agent-style development**: how to go from an idea in the chat to something you can ship, without losing your mind along the way.

**Speaker:** Vedran Mandić  
**Context:** Backend engineer at Similarweb, shared at CroAI on 21 April 2026.

This repo holds the **slides** so you can read them at your own pace:

- [`from-promt-to-prod-v2.pdf`](from-promt-to-prod-v2.pdf) — PDF export (easy to skim and search)
- [`from-promt-to-prod-v2.key`](from-promt-to-prod-v2.key) — Keynote source (if you use Keynote)

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

## Links mentioned in the slides

- [Addy Osmani — agent skills](https://github.com/addyosmani/agent-skills) (quote and “full loop” reference)
- [Cursor “doctor” style diagnostics (community)](https://github.com/nedcodes-ok/cursor-doctor)
- [Notes on Cursor Auto mode and model choice](https://github.com/nedcodes/i-tested-whether-cursors-auto-mode-actually-picks-the-right-model-20ml)
- [Claude Code best practices (community collection)](https://github.com/shanraisshan/claude-code-best-practice)
- [Superpowers (Obra)](https://github.com/obra/superpowers)
- [Skillshare (runkids) — share team skills via git](https://github.com/runkids/skillshare)

---

## Contact

- **GitHub:** [github.com/vmandic](https://github.com/vmandic) — this repo: [github.com/vmandic/from-prompt-to-prod](https://github.com/vmandic/from-prompt-to-prod)  
- **Handles:** @vekzdran, @vmandic  
- **Email:** mandic.vedran@gmail.com  

If something in the deck is unclear or dated, open an issue or reach out. Happy building.

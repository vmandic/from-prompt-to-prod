# Verify your agentic workflows (self-check against *From prompt to prod*)

## Overview

Use this file as a **user message** or **system add-on** for any AI coding agent. The analysis can be **computer-wide** (how you use AI across your machine) or **project-scoped** (one tree). The agent compares what it can observe to *From prompt to prod* (Cursor, LLM context, agentic loops, tooling, and safety).

**Non-negotiable:** A **computer-wide** run must **not** be a list of “not observable” for every row. The agent must **(1)** [plan and parallelize research](#plan-then-research-chief-coordinator) (subagents or clustered passes), **(2)** [scan agreed locations](#where-do-you-keep-source-code) including **user source roots** and **standard** editor/agent config dirs, and **(3)** for **every** dimension A–K, output a **[best practice from the talk](#best-practice-anchors-mandatory-injection-a–k)** line plus your evidence—so the user always gets **actionable** steering.

**Two modes (pick one per run):**

| Mode | What it emphasizes |
|------|--------------------|
| **Computer-wide** | Fingerprint of **how you work machine-wide**: home-level configs (Cursor, Claude, Copilot, Codex, …) **and** a **sample** of your real projects (from paths **you** give). Rubric A–K each get **evidence** or a **caveat**, never a blank. |
| **Project** | D–F, G–K grounded in a **concrete** project path (or **this workspace**). |

**Authoritative material in this repo (read order):**

1. [`from-promt-to-prod-v2.pdf`](../from-promt-to-prod-v2.pdf) — full deck.  
2. [README.md](../README.md) — outline, takeaways, links.  

This file is a **rubric and process**, not a replacement for the deck. When the rubric and the PDF differ, the **PDF and README win**.

---

## Mandatory user questions (ask if not already answered)

| # | Question | If user already said it in the first message |
|---|-----------|-----------------------------------------------|
| **1** | **Computer-wide** or **project** analysis? | Record verbatim. |
| **2** | **Where do you keep your source code?** (one or more directories: e.g. `~/dev`, `~/repos`, `~/work`). *These are the roots for **sampling** real repos—`AGENTS.md`, `.cursor/`, `package.json`, etc. Not optional for computer-wide unless the user explicitly refuses paths and accepts a weaker, home-only pass—then [Caveat] must say so.* | Record paths. |
| **3** (optional) | Which **editors/CLI agents** do you use daily? (Cursor, Claude Code, Copilot, Codex, …) | Merge with [what you find on disk](#default-home--global-locations-to-check). |

**Project mode:** still ask **(2)** only if you need **one** more repo for comparison; otherwise the **project root** from the user **is** the tree.

**Front-loading (skip questions):** e.g. *“Computer-wide, source roots: `~/a` `~/b`, home scan OK, project sample `~/a/foo`”*.

---

## Plan, then research (chief coordinator)

**The agent running this prompt must not improvise a single long grep.** Before touching files, **write a short plan** with **research tracks** and **subagent boundaries** (or, if the product has no subagents, **sequential** batches with the same split):

| Track | Scope | What to return |
|-------|--------|----------------|
| **T1: Home & global** | [Default home locations](#default-home--global-locations-to-check) | **Which** products appear installed, **list** of config files *opened or listed* (not secret contents), **MCP** / hooks pointers if in scope |
| **T2: Source roots** | User’s `AGENTS.md`, `.cursor/`, `.vscode/`, `.claude/`, `pubspec.yaml`, `package.json`, `go.mod`, `pyproject.toml`, `Makefile`, `CI` dirs—**bounded** (see [Bounded scanning](#bounded-scanning)) | **Per-repo** or **per subfolder** evidence for D, E, F, G, K patterns |
| **T3: Synthesis** | None | Map findings into A–K using [best practice anchors](#best-practice-anchors-mandatory-injection-a–k); fill the [template](#response-template-mandatory-structure) |

- **With subagents:** dispatch **T1** and **T2** in **parallel** (independent), then merge.  
- **Without subagents:** run **T1** then **T2**; do **T3** last. **Never** skip T1 for computer-wide.

If any track returns empty, **widen** once (e.g. one more subfolder) before declaring “not found”—**then** state **what you tried** under **Caveats**, not a lazy “n/a.”

---

## Default home & global locations to check

Run **`test -d` / `list_dir` on these first** (OS varies; use the rows that exist). **Read** only *non-secret* config: JSON/YAML structure for keys like `mcp`, `model`, `rules`, not tokens.

### Cross-platform (typical)

| Product / use | Paths (check which exist) | What to look for (non-secret) |
|---------------|----------------------------|---------------------------------|
| **Cursor (user config)** | `~/.cursor/` | `mcp.json`, `argv.json`, `ide_state.json` names; `extensions/`; **do not** dump OAuth/session blobs |
| **Claude (Code / app)** | `~/.claude/`, on macOS also `~/Library/Application Support/Claude/` (if present) | `config.json` / `settings` **keys** only, `projects/` or cache **names** only |
| **VS Code + Copilot** | `~/.vscode/` **or** `~/.config/Code/` **or** macOS `~/Library/Application Support/Code/User/` | `settings.json` — grep for `github.copilot`, `chat`, `agent`; `extensions/**/package.json` **names** for `copilot` |
| **Cursor (macOS app data)** | `~/Library/Application Support/Cursor/User/` (if present) | `settings.json` similarly; `globalStorage` **directory names** only if listing helps |
| **OpenAI / Codex / “Codex” CLI** | `~/.config/opencode*`, `~/.codex`, `~/.openai` (if any) | `*.json` / `*.yaml` top-level keys; **if** unknown, **list** directory and stop |
| **Windsurf / other** | user may name; add only if they consent | same discipline |

**Rule:** If a file likely contains **refresh tokens** or long base64, **list path + “present”** and **do not** paste the value.

### Why this is here

A **machine-wide** analysis that never opens **any** of these is **incomplete** unless the user **denied** home access. You must still deliver **D–E** from **user source roots** (T2) so the run is never “empty.”

---

## Where do you keep source code?

- **User answers** with 1+ directories (e.g. `~/source/vmandic`, `~/dev`). You **scan T2** there with [bounded rules](#bounded-scanning).  
- If the user has **no** code outside the current project, they may name **one** project path; treat as **T2 = that tree only** + T1 = home.  
- **Refusal:** If they refuse to name paths, T2 is **weaker**; state under **Caveats**: *“No source roots: only T1 and user interview.”*

---

## Bounded scanning (source roots)

To avoid exfiltrating the whole machine:

- **Depth:** default **4** from each source root; stop early if a large monorepo appears—ask user.  
- **Width:** at least **2** and up to **6** “project” candidates: prefer dirs that contain `package.json` **or** `pubspec.yaml` **or** `go.mod` **or** `.git` at depth ≤2, or the **most recently modified** subdirs the tools expose.  
- **Always look for** in each candidate: `AGENTS.md`, `.cursor/`, `.cursor/mcp.json`, `.cursorrules`, `CLAUDE.md`, `.llm/`, `mcp.json`, `.vscode/`, `.github/workflows/`, `.env.example`, `.gitignore` patterns for env files.  
- **Never** `find` the entire `$HOME` without a **stated** root and depth cap.

---

## When to use (and not)

| Situation | Use this prompt? |
|-----------|------------------|
| **Gap analysis** of an app repo | **Project** + path, or *this workspace* |
| **Machine-level** + **fingerprint of real projects** | **Computer-wide** + **source roots** + T1+T2 |
| **Security / compliance** sign-off | **No** |

**Success looks like:** every A–K row has a **best practice** line + your evidence, subagent-style research done, unknowns in **Caveats**, and an **open** closing.

---

## Assessing “slide- or doc-only” repositories

Materials-only repo: D–E may be N/A to **files**, but the **best practice** lines still print; *practice* = “N/A: deck repo, principles in README.”

---

## Workflow for the agent (phases, updated)

| Phase | Goal | Key actions |
|-------|------|-------------|
| **0. Questions** | Mode + **source root(s)** + tools | [Mandatory user questions](#mandatory-user-questions-ask-if-not-already-answered) |
| **0b. Plan** | Parallel research | [Plan, then research](#plan-then-research-chief-coordinator) — **write the plan in chat (brief)** then execute T1, T2 |
| **1. Orient** | Rubric A–K + [anchors](#best-practice-anchors-mandatory-injection-a–k) | Have the map in context |
| **2. T1** | Home/global | [Default home & global locations](#default-home--global-locations-to-check) |
| **3. T2** | Source roots | [Bounded scanning](#bounded-scanning) |
| **4. Synthesize** | A–K + template | For **each** row: anchor + evidence + [match verdict](#per-dimension-block-all-of-a–k) |
| **5. Safety pass** | [Security](#security-and-secrets-strict) | No secret bodies |
| **6. Close** | [Template](#response-template-mandatory-structure) | Open **How do you want to proceed?** |

---

## Best practice anchors (mandatory injection, A–K)

**Every** dimension in the final report must include the **short “From the talk”** line below (you may rephrase slightly, same meaning), then the **user’s** situation.

| ID | **Best practice (from the talk) — use as fixed anchor** |
|----|--------------------------------------------------------|
| **A** | **Deliberately** use the AI editor’s workflow: plan mode, diffs, review, optional CLI; be aware of **model choice and cost** (e.g. fast default vs “frontier” planning). |
| **B** | Build a mental model: context = system + **tools** + **history** + you; **advertised** context ≠ comfortable **headroom**; **pick models for the job**. |
| **C** | **Scope** rules; avoid **always-on** bloat; **separate** unrelated work; **track** the window; treat **compaction** as a nudge to **split the thread** or work, not to ignore. |
| **D** | Short **`AGENTS.md`**-style **hub**; **rules** = stable conventions, **skills** = repeatable **actions**; keep **MCP and hooks** **lean**; monorepos: nested **`.cursor`** only **on purpose**. |
| **E** | **Scope** with globs; default **`alwaysApply: false`** unless you mean it; **scripts** in `scripts/`, not giant inline shell in skills; **tighten** skills with test-like iteration when useful. |
| **F** | **MCP** and **hooks** for real integrations; subagents, worktrees, cloud agents, CLIs as skills—**only** when the leverage is clear. |
| **G** | **Plan** before **big** gen; **review** like a **junior’s PR**; **execute** in steps; **verify** (tests, tools, your eyes). |
| **H** | **Precise** when the outcome is known; **a bit open** for exploration; use **@ paths**, symbols, indexed docs. |
| **I** | **Parallel** (subagents, worktrees) to **go faster** or **split** context; **do not** force parallel theater. |
| **J** | Optional: **shared** team skills, **memory** tools (e.g. long-term RAG) where they **earn** their keep. |
| **K** | **Least privilege**; no prod **secrets** in text the model **reads**; **read-only** where possible; **human** in the loop; **branches** / not agents alone on production. |

### References (README)

- [Addy Osmani — agent skills](https://github.com/addyosmani/agent-skills)  
- [Cursor “doctor” (community)](https://github.com/nedcodes-ok/cursor-doctor)  
- [Auto mode & model (nedcodes)](https://github.com/nedcodes/i-tested-whether-cursors-auto-mode-actually-picks-the-right-model-20ml)  
- [Claude Code best practices (community)](https://github.com/shanraisshan/claude-code-best-practice)  
- [Superpowers (Obra)](https://github.com/obra/superpowers)  
- [Skillshare (runkids)](https://github.com/runkids/skillshare)  

---

## Map: talk outline → rubric rows

| Talk section | Primary IDs |
|--------------|------------|
| Cursor in context | A |
| LLMs in the editor | B, C |
| Project setup | D, E, F |
| Agentic loop | G |
| Prompting | H |
| Parallel work | I, (F) |
| Extend toolkit | F, J |
| Trust | K |

---

## Per-dimension block (all of A–K)

For each row, output in **this order**:

1. **`Best practice (from the talk):`** — copy/paraphrase from the [table](#best-practice-anchors-mandatory-injection-a–k) (required).  
2. **`Your setup (evidence):`** — **Awareness** / **practice** / **tools** in one tight paragraph or sub-bullets, with **paths** from T1/T2 or “searched [paths], not found.” **Forbidden:** leaving this blank because “not observable” without also stating **where you looked** (T1/T2 or user quote).  
3. **`How this matches the talk`:** **align** / **partial** / **misaligned** + one **concrete** reason.  
4. **`Gap after search` (if any):** *what* was still unknown or not found after T1/T2, or **“none”** if the evidence was enough for this row. **Always** one line minimum (even “N/A: fully covered”).  
5. **`Suggested resolution or improvement` (required every row):** If **align** and no real gap, write **“None needed for visible scope”** or at most one **optional** polish. If **partial** or **misaligned** or a **gap** line exists, give **1–3 concrete** next steps: things to add/change/try (e.g. “add a one-line `AGENTS.md` pointer to `.llm/rules`,” “tighten `alwaysApply` on rule X,” “turn on branch protection for `main`,” “add `.env` to globalcursorignore,” “pilot one worktree for hotfixes,” “document model choice in team README”)—**grounded in the [anchors](#best-practice-anchors-mandatory-injection-a–k)**, not generic life advice. **Never** a single forced prescription; this is a **menu** of small fixes. **Forbidden:** “be more careful” with no file or habit. **Security (K):** never suggest pasting secrets to “verify.”

*Terminology:* do not duplicate “Reflection” as a different concept—**match** and **evidence** are enough.

**Hints (still not new requirements):** **A** from T1 + user; **B–C** from rules count in T2, settings keys; **D–E** from `AGENTS.md`, `.llm/`, glob rules; **F** from mcp, hooks, mempalace files; **G** from `plans/`, `test/`, CI; **H** from `.llm/prompts` or similar; **I** user-asked; **J** from mempalace, skill links; **K** from `.gitignore`, `*.example`, **no** secret paste.

---

## Security and secrets (strict)

- **Not** print **`.env`**, keys, tokens, long session material.  
- **May** name paths, `git` tracked vs ignored, **file exists**.  
- **T1** config files: **structural** flags OK (e.g. `mcpServers` key exists); not values of secrets.  
- **Computer-wide:** T1+T2 are **allowed**; not “inventory entire `Downloads`” without user.

---

## Anti-patterns (for the responding agent)

| If you do this | Do this instead |
|----------------|------------------|
| A–K all “not observable” in computer-wide | Run **T1+T2**; print **anchors** + **“searched `path`, found|not”** |  
| No **plan** before file reads | [Plan, then research](#plan-then-research-chief-coordinator) in chat first |
| Skip **ask for source roots** in computer-wide | [Mandatory questions](#mandatory-user-questions-ask-if-not-already-answered) |
| Pasting **secrets** to prove K | [Security](#security-and-secrets-strict) |
| “Best practice” from your head, not the table | Use [anchors table](#best-practice-anchors-mandatory-injection-a–k) only |
| One next step | [Template](#response-template-mandatory-structure) closing: **3–5 options** + question |
| **Partial/misalign** with **no** “Suggested resolution or improvement” | Every row [requires](#per-dimension-block-all-of-a–k) a suggestion block — use **“None needed”** only when **align** + no gap |  

---

## Response template (mandatory structure)

```text
## Research plan (brief)
- **Mode:** [computer-wide | project]
- **T1 (home/global):** [paths checked, in 1-3 lines]
- **T2 (source root(s)):** [paths checked, depth, how many project candidates]
- **Parallelism:** [subagents: yes/no — which track each | serial: T1 then T2]

## Summary
[3-5 sentences: mode, what was scanned, overall alignment, biggest gap, limits]

## Scope and mode
- **Analysis mode:** [computer-wide | project]
- **Source root(s) (T2) or "none / refused":** […]
- **Project root (if project only):** […]
- **AI tools (from T1 + user):** […]
- **Note:** [e.g. "home-only" caveat]

## Orientation
- **Focus type:** […]
- **User context:** [… or none]

## A–K: Dimension notes

For **each** A–K, use **exactly** this sub-structure:

### [ID] [Topic name]
- **Best practice (from the talk):** [one line from anchor table]
- **Your setup (evidence):** [paths, configs, what you read—must cite T1/T2 or "searched X, Y not found"]
- **How this matches the talk:** [align | partial | misaligned] — [one concrete reason]
- **Gap after search (if any):** [what was still unknown, or "none"]
- **Suggested resolution or improvement:** [1–3 concrete, deck-tied actions; or "None needed for visible scope" / one optional polish when align]

## Tools and practices from the deck (crosswalk)
- **Found on disk (paths):** […]
- **Not found or N/A after search:** [… with what was tried]

## Strengths
[…]

## Gaps and risks
[… — K without values]

## Caveats
[refusals, unread sensitive files, depth limits, user didn’t name roots]

## How do you want to proceed?
[3-5 open options; ask user priority]
```

---

## Scope: what this is and is not

**Personal** talk, not product docs. Stay descriptive, kind, and **evidence-bounded**. If ambiguous, **cite the PDF / README** and the **anchor** row.

When in doubt, stay **boring, precise, and kind**.

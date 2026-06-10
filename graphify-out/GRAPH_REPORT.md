# Graph Report - from-prompt-to-prod  (2026-06-10)

## Corpus Check
- 16 files · ~41,187 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 121 nodes · 139 edges · 15 communities (13 shown, 2 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 4 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8bd069c5`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]

## God Nodes (most connected - your core abstractions)
1. `Verify your agentic workflows (self-audit against *From prompt to prod*)` - 17 edges
2. `Self-audit interactive prompt wizard` - 9 edges
3. `computeActiveFromScroll()` - 6 edges
4. `applyHash()` - 6 edges
5. `bindToc()` - 6 edges
6. `main()` - 6 edges
7. `From prompt to prod` - 6 edges
8. `wizard_config_json_for_html()` - 5 edges
9. `TestGhpagesBuild` - 5 edges
10. `AGENTS.md — from-prompt-to-prod (rudimentary)` - 5 edges

## Surprising Connections (you probably didn't know these)
- `preface()` --calls--> `copy_block_html()`  [INFERRED]
  scripts/build_ghpages.py → scripts/prompt_snippets.py
- `preface()` --calls--> `wizard_config_json_for_html()`  [INFERRED]
  scripts/build_ghpages.py → scripts/prompt_snippets.py

## Import Cycles
- None detected.

## Communities (15 total, 2 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.10
Nodes (20): Anti-patterns (for the responding agent), Assessing “slide- or doc-only” repositories, Best practice anchors (mandatory injection, A–K), Bounded scanning (source roots), Cross-platform (typical), Default home & global locations to check, Mandatory user questions (ask if not already answered), Map: talk outline → rubric rows (+12 more)

### Community 1 - "Community 1"
Cohesion: 0.15
Nodes (11): Any, compose_starter_body(), copy_block_html(), Starter prompts for the self-audit rubric.  Used by scripts/build_ghpages.py for, Data for docs/assets/prompt-wizard.js (embedded as JSON in self-audit page)., JSON string safe to embed inside <script type=\"application/json\">., Wrap escaped code in a copy-to-clipboard block (matches docs/assets/copy-blocks., wizard_config() (+3 more)

### Community 2 - "Community 2"
Cohesion: 0.31
Nodes (12): applyHash(), applyMql(), bindToc(), buildSections(), computeActiveFromScroll(), onHash(), onResize(), onScroll() (+4 more)

### Community 3 - "Community 3"
Cohesion: 0.20
Nodes (9): Architecture, Copy and docs, Goal, New / changed front-end files, Scope (per your choice), Self-audit interactive prompt wizard, Tests, Verification (+1 more)

### Community 4 - "Community 4"
Cohesion: 0.39
Nodes (8): attr(), _audit_url_segment(), build_toc_nav(), esc_html(), extract_toc(), main(), preface(), Single path segment for /docs/<seg>/; rejects traversal and odd characters.

### Community 5 - "Community 5"
Cohesion: 0.25
Nodes (7): Contact, From prompt to prod, How to self-audit yourself (copy into your agent), Links mentioned in the slides, Self-audit your setup against the talk (agent prompt), Takeaways (short version), What the talk covers

### Community 6 - "Community 6"
Cohesion: 0.29
Nodes (3): Smoke tests for GitHub Pages build (requires: pip install -r requirements.txt)., Build runs once in setUpClass; unittest orders test_* alphabetically, so do not, TestGhpagesBuild

### Community 7 - "Community 7"
Cohesion: 0.33
Nodes (5): AGENTS.md — from-prompt-to-prod (rudimentary), Conventions we settled on in repo work, Cross-OS (Unix vs Windows), If you are unsure, What this repo is

### Community 8 - "Community 8"
Cohesion: 0.70
Nodes (4): boot(), initAuditScrollEnd(), initNavTracking(), track()

### Community 10 - "Community 10"
Cohesion: 0.40
Nodes (4): name, private, scripts, build:site

### Community 11 - "Community 11"
Cohesion: 0.50
Nodes (4): Path, main(), make_handler(), SimpleHTTPRequestHandler

### Community 13 - "Community 13"
Cohesion: 0.83
Nodes (3): init(), show(), text()

## Knowledge Gaps
- **40 isolated node(s):** `name`, `private`, `build:site`, `Any`, `Path` (+35 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `wizard_config_json_for_html()` connect `Community 1` to `Community 4`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Why does `preface()` connect `Community 4` to `Community 1`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **What connects `name`, `private`, `build:site` to the rest of the system?**
  _48 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.09523809523809523 - nodes in this community are weakly interconnected._
# RAG Builder — Governance Framework

A versioned, rules-driven knowledge base for designing retrieval-augmented generation (RAG)
systems, operated with an AI assistant (Claude Code) under strict human approval gates.

## What it does
- Separates **Source Truth** (authoritative RAG techniques, preserved verbatim) from
  **Custom Design** (my own strategies, freely revisable) — custom never overrides source.
- Treats the AI as the **hands, not the decision-maker**: every create, revise, rollback,
  rename, or delete requires explicit, per-action approval.
- Protects critical elements (version IDs, verbatim source text, titles, deletions) as
  **protected nodes** that need express permission to change.
- Versions every document with **Semantic Versioning** and an immutable archive.

## Repository layout
| Path | Contents |
|---|---|
| `governance/` | The active versions of the three governance documents |
| `custom-design/` | My own designs, including `.yaml` data documents (e.g., the Variable Catalog) |
| `tools/` | Small scripts (the quote checker) |
| `tests/` | Automated tests for the tools |
| `requirements.txt` | Python packages the tools need |
| `templates/` | The empty build-workspace skeleton copied by `New Build` |
| `.githooks/` | Git hooks that block build data from being committed |
| `archive/` | Every superseded version, kept for history and rollback |
| `CHANGELOG.md` | What changed in each release |
| `CLAUDE.md` | Operating instructions loaded by Claude Code at session start |

## Knowledge base contents
| Document | What it is |
|---|---|
| `custom-design/Custom__RAG_Variable_Catalog__v1.1.0.yaml` | 81 variables that must be answered before a RAG architecture is chosen, with plain-language questions, where to find answers, who can confirm them, defaults, analysis depth and hard-to-undo flags, plus authority and fallback rules. The Build commands run on it. |
| `custom-design/Custom__Role_Map__v1.0.0.yaml` | The 13 roles behind the catalog: who each is, what they approve, which variables they confirm or inform, and who to go to when they're unavailable. |

## Setup
After cloning, run these once from the project folder:
```
git config core.hooksPath .githooks
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```
The first line turns on the commit guard. The other two create a private Python environment
(`.venv/`, never committed) for the tools.

## Tools
| Command | What it does |
|---|---|
| `.venv/bin/python tools/quote_check.py <build-folder>` | Checks every evidence quote in a build appears word for word in its source document or logged reply, and that no source changed after intake. Read-only. |
| `.venv/bin/python -m unittest discover -s tests -v` | Runs the automated tests for the tools. |

## Build workflow
This repository is the **tool**. Each company engagement is a **build**, which holds that
company's confidential data and lives in a private workspace **outside this repo**
(`~/Documents/rag-builds/<name>/`, never with a git remote). Build chats are opened from the
build's folder.

`New Build` → `Ingest` → `Gap Report` → `Draft Emails` → `Log Response` → `Signoff Packet` →
`Record Signoff` → `Close Build`

Every answer cites a verbatim quote from a document or a named person. The result is a
plain-language sign-off packet a non-technical manager can verify. See Command Reference §18–§26.

**Builds hold confidential company data and never live in this repo.**

## The governance documents
- **Operating Charter** — how the assistant behaves: processing modes, document classes, selection, conflict handling.
- **Command Reference** — every command, with quick reference and deep dives.
- **Organizational Rules** — naming, versioning model, protected nodes, folder ontology, security guardrail.

## Commands at a glance
| Command | Purpose |
|---|---|
| `Doc It` | Format pasted source material verbatim into a structured Source Truth document |
| `Revise 'X'` | Make a described change; approve the before/after; saved as a new version |
| `Update 'X' Source` / `Custom` | Web-search for newer sources or better architectures; approve what to integrate |
| `Rollback` / `Update` (by steps, to a version, or `Full`) | Move a document's active version along its history |
| `List` / `Get 'X'` | Read-only overview, or one document's full version history |
| `New Build` … `Close Build` | Build intake: gather, cite and sign off a company's architecture variables |

See the Command Reference for exact rules.

## Versioning
`vMAJOR.MINOR.PATCH` — MAJOR = breaking, MINOR = addition, PATCH = correction.
Unreleased drafts that are superseded before commit are kept as `-rc.N`.
Current versions and history: see [CHANGELOG.md](CHANGELOG.md).

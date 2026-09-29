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
| `tools/` | Small scripts (quote checker, report generator) |
| `templates/` | The empty build-workspace skeleton copied by `New Build` |
| `.githooks/` | Git hooks that block build data from being committed |
| `archive/` | Every superseded version, kept for history and rollback |
| `CHANGELOG.md` | What changed in each release |
| `CLAUDE.md` | Operating instructions loaded by Claude Code at session start |

## Setup
After cloning, turn on the commit guard once:
```
git config core.hooksPath .githooks
```

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

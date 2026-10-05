# Changelog

All released versions of the RAG Builder's documents (governance and knowledge base) are recorded here, newest first.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Version IDs follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html), adapted for documents — see
*Organizational Rules §2*. Each document is versioned independently; a release may cover several.

## 2026-10-05 — Variable Catalog v1.0.0

### RAG Variable Catalog → v1.0.0 (new, `custom-design/`)
- **Added** the first Custom document: 81 variables in 9 groups (O, A, B, I, C, D, E, F, G) that must be answered before a RAG architecture is chosen.
- Each variable carries a technical question, a plain-language question for emails, a plain-language explanation and "why it matters" for the sign-off glossary, where to find the answer, typical authority and informant roles, what counts as a sufficient answer, a default, a 0–10 analysis-depth level, and a one-way (hard-to-undo) flag.
- Group O (organization & governance) comes first; O4 defines the dispute escalation path and its named exceptions.

### Repository
- **Changed** `CHANGELOG.md` header to cover all documents, not only governance.
- **Added** a "Knowledge base contents" section to `README.md`.

## 2026-09-29 — Build intake update

### Organizational Rules → v1.2.0
- **Added** §8 Build Workspaces: private location, layout, evidence rules, enforcement layers, close-out.
- **Added** YAML data documents (§1); `tools/`, `templates/`, `.githooks/` folders (§5).
- **Added** guardrail triggers 5–7 (§6); protected nodes 5–6: sign-off packets and evidence quotes (§3).
- **Changed** version IDs and titles protect existing versions; a clean new version needs no separate approval (§2, §3).

### Operating Charter → v1.2.0
- **Added** the Gather job (§1), Mode 3 Build Intake (§4), and build records outside the knowledge base (§3).
- **Added** build dependency flags (§10) and build gates (§13).
- **Changed** §8 selection now uses the build's confirmed answers; §12 aligned with the new version-ID scope.

### Command Reference → v1.2.0
- **Added** build intake commands §18–§26 and their Quick Reference table.
- **Added** knowledge-base-vs-build and missing-tool-piece rules (§2).
- **Changed** §15 step 4 to match the new version-ID scope.

### Repository
- **Added** `.githooks/pre-commit` build-data guard, `.gitignore` build patterns, and README build-workflow and setup sections.
- **Changed** `CLAUDE.md`: build-data rule, build workspace location, protected-node scope, three modes.

## 2026-09-25 — Commands tool expansion update

### Command Reference → v1.1.0
- **Added** `Revise 'X'` (§15): human-directed revisions, saved as a new version with before/after approval.
- **Added** `List` (§16) and `Get 'X'` (§17): read-only overview and per-document detail with integrity checks.
- **Added** bump-level proposal to `Update … Source`, `Update … Custom`, and `Revise`.
- **Added** bump-level labels on dependency flags (MAJOR = review required).
- **Changed** version examples to the `vMAJOR.MINOR.PATCH` format; §13 scoped to commands that take a target.

### Organizational Rules → v1.1.0
- **Added** Semantic Versioning model (§2): bump levels, highest-version rule, release candidates, numeric ordering, Version note, changelog.
- **Added** rule for where the active version lives on disk (§5); `governance/` holds active versions only.
- **Changed** Version ID format to `vMAJOR.MINOR.PATCH` for all Types, including variants (§1).
- **Migrated** existing versions: `v1` → `v1.0.0`; unreleased `v2` → `v1.1.0-rc.1`.

### Operating Charter → v1.1.0
- **Added** `Revise` to the class table (§3), Mode 1 (§4), and change gating (§13).
- **Added** bump-level labels on dependency flags (§10).
- **Changed** §9 versioning summary; §14 companion references are now version-free.

### Repository
- **Added** root `README.md` (project overview, layout, commands, versioning).

*Release candidates `v1.1.0-rc.1` (all three documents) were created during this update and archived unreleased.*

## 2026-09-25 — Initial release

### Command Reference, Operating Charter, Organizational Rules → v1.0.0
- Initial public release of the governance framework (originally labeled `v1`).

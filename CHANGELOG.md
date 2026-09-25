# Changelog

All released versions of the RAG Builder governance documents are recorded here, newest first.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Version IDs follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html), adapted for documents — see
*Organizational Rules §2*. Each document is versioned independently; a release may cover several.

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

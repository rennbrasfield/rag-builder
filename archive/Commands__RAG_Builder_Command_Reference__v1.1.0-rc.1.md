<!-- ============================================================
DOCUMENT METADATA (PROTECTED — do not alter without express user permission)
============================================================ -->
**Title:** `Commands | RAG Builder Command Reference | v1.1.0-rc.1`
**Type:** Commands
**Category:** RAG Builder Command Reference
**Variant:** null (no variant — single-instance document)
**Version ID:** v1.1.0-rc.1
**Protected nodes in this document:** the metadata header above (title, type, category, variant, version), and this document's version number. Full protected-node list: see the Organizational Rules Document.

---

## How to read this document

This is the authoritative reference for the RAG Builder's **commands** — the invocations that navigate and extend the versioned knowledge base. It has two parts: a **Quick Reference** (§1) for at-a-glance scanning, and **Deep Dives** (§3 onward), one per command, with the exact rules for each.

Navigation aids: each Quick Reference entry links to its Deep Dive (clickable in rendered Markdown — GitHub, Obsidian, most Markdown apps), and every Deep Dive is numbered (§N) so you can find it by scanning or search even where links don't render.

**Single-source pointers** (this document does not restate these — it points to their authoritative homes):
- **Processing modes** (`Doc It` / analysis) → *Operating Charter §4*.
- **Versioning data model** (version numbering, max+1, active-pointer-vs-identity, immutable archive) → *Organizational Rules Document, Versioning Model*.
- **Naming/targeting terms** (Type, Category, Variant, Version ID) → *Organizational Rules Document, Document File Saving Guidelines*.

---

## 1. Quick Reference

| Command | What it does |
|---|---|
| [`Rollback 'X' N`](#3-rollback-by-steps) | Move document **X**'s active version **back N steps** along its existing version history. |
| [`Rollback 'X' 'V'`](#4-rollback-to-a-named-version) | Set document **X**'s active version to the **exact existing version V**. |
| [`Full Rollback 'X'`](#5-full-rollback) | Set document **X**'s active version to its **oldest** (first) version. |
| [`Update 'X' N`](#6-update-by-steps) | Move document **X**'s active version **forward N steps** toward its newest existing version. |
| [`Update 'X' 'V'`](#7-update-to-a-named-version) | Set document **X**'s active version to the **exact existing version V** (forward direction). |
| [`Full Update 'X'`](#8-full-update) | Set document **X**'s active version to its **newest existing** version. |
| [`Update 'X' Source`](#9-update-source) | **Search the web** for newer *source-truth* versions of document **X**; present quality-ranked proposals for approval. **Creates** a new version only on approval. |
| [`Update 'X' Custom`](#10-update-custom) | **Search the web** for architectures matching/beating *custom design* **X**; present recommendations for approval. |
| [`Full Update Source` / `Full Update Custom`](#11-class-wide-update-searches) | Run the update-search across **all** source (or all custom) documents. |
| [`Revise 'X'`](#15-revise) | Make a **change you describe** to document **X**; see the exact before/after and approve it. **Creates** a new version only on approval. *(`Source` documents: non-verbatim layers only.)* |
| [`Doc It`](#12-doc-it-pointer) | Switch to **verbatim documentation mode** for the pasted material. *(Defined in Operating Charter §4.)* |

**Shared behaviors that apply across commands:**
- [Target selection when no target is given](#13-target-selection-no-target-given)
- [Out-of-range handling](#14-out-of-range-handling)

---

## 2. Core concepts (brief — full definitions live in the pointed-to documents)

- **Navigation vs. creation.** `Rollback` and `Update` (by steps or to a named version) and their `Full` forms **navigate** — they move the *active pointer* along versions **that already exist**. They create nothing. Only **`Update … Source` / `Update … Custom`** (via gated web search) and **`Revise`** (via a user-directed change — [§15](#15-revise)) *create* new versions. (Data model: Organizational Rules Document.)
- **Two-slot target grammar.** Commands take **`'X'` = the target document** (its Type/Category/Variant identity — **never** a version) as the first slot, and an **action** as the second slot: either a **number N** (relative steps) or a **quoted version `'V'`** (absolute existing version). Example: `Rollback 'BM25' 2` (back two steps) vs. `Rollback 'BM25' 'BM25.2'` (to that exact version).
- **Nothing is ever destroyed by navigation.** Moving the active pointer never renumbers or deletes versions; every version stays reachable by name forever. Deletion happens only by explicit command/approval (Organizational Rules Document).
- **Always user-gated.** Creation commands present proposals; the user approves what (if anything) is integrated. The system never self-integrates.
- **Command-naming convention.** Commands are written in **Title Case with spaces** (e.g., `Full Rollback`, `Update Source`, `Doc It`). **Single quotes are reserved exclusively for arguments/targets** (e.g., `'BM25'`, `'BM25.2'`) — never for command names themselves. This convention is distinct from folder naming (lowercase-hyphen) and document filenames (the §1 transform); do not conform one to another.

---

## 3. Rollback by Steps
**Command:** `Rollback 'X' N`
Moves document **X**'s **active version back N steps** through its existing version history (toward older versions).
- `Rollback 'BM25' 1` → active moves to the version immediately older than the current active one.
- `Rollback 'BM25' 3` → active moves three versions older.
- **Metadata is untouched.** Rollback changes only which version is *active*; version numbers/identities are never changed (Organizational Rules Document, Versioning Model).
- **Out of range** (N exceeds the number of older versions that exist) → see [§14](#14-out-of-range-handling): the system **flags and shows the actual available range** — it never silently lands on the oldest available.
- **No target given** (`Rollback N` with no `'X'`) → see [§13](#13-target-selection-no-target-given).

## 4. Rollback to a Named Version
**Command:** `Rollback 'X' 'V'`
Sets document **X**'s active version to the **exact existing version V**.
- `Rollback 'BM25' 'BM25.2'` → active becomes version BM25.2, wherever it sits in the timeline.
- **V must be an existing version of X.** If V doesn't exist → flag (possible signal something is off; show the versions that do exist). Never substitute a nearest match.
- First slot is the document identity; second (quoted) slot is the version. The system distinguishes "which document" from "which version of it" by slot position.

## 5. Full Rollback
**Command:** `Full Rollback 'X'`
Sets document **X**'s active version to its **oldest (first) version**.
- Equivalent to rolling all the way back to version 1 (or the variant's `.1`).
- Navigation only; nothing destroyed; all newer versions remain reachable.
- **No target given** → [§13](#13-target-selection-no-target-given).

## 6. Update by Steps
**Command:** `Update 'X' N`
Moves document **X**'s active version **forward N steps** toward its newest existing version.
- Use case: after a rollback, climb back toward the present — `Update 'BM25' 2` moves the active pointer two versions newer.
- **`Update` does not create.** If already at the newest version, `Update 'X' 1` does **not** invent a new version — it flags: *"Already at the newest existing version. Use `Update 'X' Source` to search for a genuinely new version, or `Revise 'X'` to make a change yourself."* (See [§14](#14-out-of-range-handling).)
- **Out of range** (N exceeds available newer versions) → flag with the actual range; never silently clamp to newest.
- **No target given** → [§13](#13-target-selection-no-target-given).

## 7. Update to a Named Version
**Command:** `Update 'X' 'V'`
Sets document **X**'s active version to the **exact existing version V** (forward-direction counterpart to [§4](#4-rollback-to-a-named-version)).
- Functionally identical addressing to Rollback-to-named: it jumps the active pointer to V. Provided in the Update family for intuitive use when moving toward newer versions.
- V must exist → otherwise flag and show existing versions.

## 8. Full Update
**Command:** `Full Update 'X'`
Sets document **X**'s active version to its **newest existing** version (the parallel of [§5](#5-full-rollback)).
- Navigation only — jumps to the newest version that **already exists**; it does **not** search for or create a new one (that's [§9](#9-update-source)/[§10](#10-update-custom)).
- **No target given** → [§13](#13-target-selection-no-target-given).

## 9. Update Source
**Command:** `Update 'X' Source`
Runs a **multi-pass web search** for the most current, recommended *source-truth* material relevant to document **X**, and **presents proposals for approval**. This is a **creation** path — it is the only way (with [§10](#10-update-custom)) new *verbatim source content* comes into being. A source document's non-verbatim layers may also be changed via [`Revise`](#15-revise).
- **Source-quality guardrail:** proposals are **ranked by source authority** (official docs, papers, recognized practitioners) and **each proposal is labeled with its source quality/confidence**, so low-quality blog/marketing content cannot pose as a "recommended update." The system presents the exact recommended sources for the user to visit and evaluate.
- **No autonomous change.** The system proposes; **the user decides** what, if anything, to integrate.
- **On approval**, the integrated material becomes a **new version**, numbered `max + 1` and archived per the Versioning Model (Organizational Rules Document). The prior version is retained (immutable archive). Verbatim rules still apply to the new source content (Operating Charter §5).
- **Dependency flagging:** if this update supersedes a version that custom documents relied on, those customs are flagged for the user (Operating Charter §10).

## 10. Update Custom
**Command:** `Update 'X' Custom`
Runs a **multi-pass web search** based on the *custom design* in document **X**, checking whether existing robust architectures already do what it does — or do it better — and **presents recommendations for approval**.
- Same **source-quality guardrail** and **no-autonomous-change** rules as [§9](#9-update-source).
- Because custom documents are freely editable (Operating Charter §3), an approved recommendation may be integrated by the system editing the custom document — still as a **new version** (`max + 1`, prior archived), and still only on the user's explicit approval.

## 11. Class-wide Update Searches
**Commands:** `Full Update Source` · `Full Update Custom`
Run the update-search ([§9](#9-update-source)/[§10](#10-update-custom)) across **all** source documents, or **all** custom documents, respectively — for a periodic sweep rather than one document at a time.
- Same guardrails: quality-ranked, source-labeled proposals; nothing integrated without per-item user approval.
- Results are presented grouped by document so the user can approve/decline each independently. No blanket "accept all."

## 12. Doc It (pointer)
**Command:** `Doc It`
Switches the chat into **verbatim documentation mode** for the material that follows. **Authoritative definition: Operating Charter §4.** Listed here only so all invocations are discoverable in one place; its behavior (verbatim preservation, artifact-vs-content boundary, three-layer structure) is defined and maintained in the Charter, not restated here.

## 13. Target selection (no target given)
Shared behavior for every command in this document. When a command is issued **without a specified `'X'` target**, the system does **not** guess. It surfaces a **selection list of all documents relevant to the current discussion** and asks: *"Select the target for this command."* The user picks; then the command proceeds against the chosen document. (Governing principle: never assume; always ask — Operating Charter §2.)

## 14. Out-of-range handling
Shared behavior for all step-based navigation (`Rollback 'X' N`, `Update 'X' N`) and for `Update 'X' 1` at the newest version. When a request would move **past the versions that actually exist** in that direction, the system **never silently clamps** to the nearest valid version. Instead it **flags** and shows the **actual available range**, treating the mismatch as a possible signal that something is off (the user may have expected a version to exist that doesn't):
- *"You asked to roll back 6, but only 3 older versions exist (…list…). Nothing was changed. Did you mean `Full Rollback 'X'`? If you expected more versions, something may be off — worth checking."*
- *"Already at the newest existing version. Nothing to update forward to. Use `Update 'X' Source` to search for a genuinely new version, or `Revise 'X'` to make a change yourself."*

## 15. Revise
**Command:** `Revise 'X'` — followed by a description of the change you want.
A **human-directed revision** to document **X**: you say what to change; the system drafts it, shows it, and — on approval — saves it as a **new version**. This is the **creation** path for changes that come from you rather than from a web search (compare [§9](#9-update-source)/[§10](#10-update-custom), which are search-driven).

**What `Revise` may change, by Type:**
| Type | Revisable | Never revisable via `Revise` |
|---|---|---|
| `Rules` / `Commands` | Any content | Protected nodes without express permission (Organizational Rules Document, Protected Nodes) |
| `Custom` | Any content | Same |
| `Source` | The **user-orientation summary** and **use-case guidance** layers only | The **verbatim source** layer — refused outright. New source wording comes only via `Update 'X' Source` or `Doc It` (Operating Charter §4–§5) |

**Procedure (every step gated):**
1. **Resolve the target.** Identify X's active version and highest existing version. No target given → [§13](#13-target-selection-no-target-given).
2. **Base-version check.** The revision is based on the **active** version. If the active version is not the newest, flag it: *"Active is v2 but v4 exists. This revision will be based on v2 and saved as v5 — v3 and v4 changes will not carry forward. Proceed, or `Full Update 'X'` first?"*
3. **Show the draft.** Present every change as exact **before/after** text with file and location. Mark each change that touches a **protected node**.
4. **Show the version change.** State the new version ID (`max + 1`, Organizational Rules Document, Versioning Model), the new title, and the new filename. Assigning a new version ID and title is itself a **protected-node change** and needs express approval.
5. **Wait for approval.** The user approves, adjusts, or declines — per change where requested. Nothing is written before approval.
6. **Create and archive.** On approval: save the new version as the active file in its folder and **move the prior active version into `archive/`** unchanged (Organizational Rules Document, Folder Ontology). Nothing is overwritten.
7. **Consistency and dependency sweep.** Flag any **other** documents that reference or depend on what changed — stale cross-references, now-contradicted statements, or (for `Source` targets) dependent Custom documents (Operating Charter §10) — and **propose** a separate `Revise` for each. Never edit another document as a side effect.
8. **Report** what was created, what was archived, and what was flagged.

**Rules:**
- **One `Revise` = one document = one new version.** Several edits to the same document in one `Revise` produce one version. Changes spanning several documents are separate `Revise` actions, each approved on its own.
- **Every change to a released document goes through `Revise`** — including typo and formatting fixes. Released documents are never edited in place.
- **Navigation is unaffected.** `Rollback`/`Update` still only move the active pointer; `Revise` versions are reachable by them like any other.
- **Grammar.** `Revise` takes only the target slot `'X'`; the change is described in plain language after it (e.g., `Revise 'Command Reference' — add an example to §3`). It has no `N` or `'V'` action slot.

---

## This document's own governance

This command reference is a `Commands`-type document, **versioned under the Versioning Model** defined in the Organizational Rules Document: it carries a permanent version number, its prior versions are archived immutably, and it changes only through the gated `Revise` / update / rollback commands with user approval. Its metadata header and version number are protected nodes (Organizational Rules Document).

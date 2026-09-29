<!-- ============================================================
DOCUMENT METADATA (PROTECTED — do not alter without express user permission)
============================================================ -->
**Title:** `Rules | RAG Builder Organizational Rules | v1.2.0`
**Type:** Rules
**Category:** RAG Builder Organizational Rules
**Variant:** null (no variant — single-instance document)
**Version ID:** v1.2.0
**Version note:** Build workspaces and data documents
**Protected nodes in this document:** the metadata header above, this document's version number, and the Protected Nodes list defined in §3 (which is itself the authoritative list).

---

## How to read this document

This is the **authoritative home** for the RAG Builder's structural rules. Under the single-source principle, the definitions below live **only here**; the Operating Charter and Command Reference *point* to them rather than restating them. This document is written to be usable as instructions **both** to the Project chat (the "brain") **and** to Claude Code (the "hands" that actually files, versions, and manages the folder — see §5).

Sections: §1 Document File Saving Guidelines (naming) · §2 Versioning Model · §3 Protected Nodes · §4 Variant Metadata Tracking · §5 Folder Ontology & Claude Code Filing Protocol · §6 Security Hygiene Coaching Guardrail · §7 Automation Options · §8 Build Workspaces.

---

## §1. Document File Saving Guidelines (the naming convention)

Every document's **title** is composed of up to four fields, in order, separated by a spaced pipe ` | `:

```
[Type] | [Category] | [Variant] | [Version ID]
```

- **Type** — one of: `Source`, `Custom`, `Rules`, `Commands` (capitalized exactly as shown).
  - `Source` = externally authoritative, verbatim RAG technique/standard material.
  - `Custom` = the user's own designs and strategies (freely editable).
  - `Rules` = governance/operating documents (e.g., the Operating Charter, this document).
  - `Commands` = command-reference documents (e.g., the Command Reference).
- **Category** — the RAG slot/function the document belongs to (e.g., `First-Pass Filtering`, `Metadata Filtering`, `Prompt Augmentation Protocol`). For `Rules`/`Commands` documents, the Category is the document's own name/role.
- **Variant** — the specific option within a Category where multiple exist (e.g., `BM25` vs. `TF-IDF` within a keyword-retrieval Category). **Omitted from the title when the document has no variant** — but still tracked internally (see §4).
- **Version ID** — the permanent version identifier (see §2 for format).

**Examples:**
- `Source | Keyword Retrieval | BM25 | v1.2.0`
- `Source | Prompt Augmentation Protocol | (single option) | v1.0.0` → written without the variant field: `Source | Prompt Augmentation Protocol | v1.0.0`
- `Rules | RAG Builder Operating Charter | v1.0.0`
- `Commands | RAG Builder Command Reference | v1.0.0`

**Version ID format (all Types):** `v[MAJOR].[MINOR].[PATCH]` — always three parts, e.g., `v1.0.0`, `v1.0.1`, `v1.1.0`, `v2.0.0`. An unreleased version may carry a release-candidate suffix, `-rc.[N]` — e.g., `v1.1.0-rc.1` (see §2). Variant documents use the same format; the variant is identified by the **Variant** field, never by the Version ID.

**Filesystem-safe filename mapping.** The ` | `-delimited title is the canonical identity and lives in the document's metadata header. The **actual saved filename** uses a filesystem-safe transform of that title:
- ` | ` (spaced pipe) → `__` (double underscore)
- remaining spaces → `_` (single underscore)
- append `.md` (or `.yaml` for a data document — see below)

Example: title `Source | Keyword Retrieval | BM25 | v1.2.0` → filename `Source__Keyword_Retrieval__BM25__v1.2.0.md`. The `|`-delimited human-readable form stays in the metadata; the filename stays safe. Both encode the same fields, so either can be parsed to identify a document.

**Data documents (`.yaml`).** A document whose content is structured data (e.g., the Variable Catalog) is saved as YAML. It follows every rule in this section: the same title, the same Type/Category/Variant/Version fields and the same filename transform, ending in `.yaml`. Its metadata lives in a top-level `metadata:` block with the fields `title`, `type`, `category`, `variant`, `version`, `version_note`. That block is its metadata header, and it is protected the same way (§3). Example: `Custom | RAG Variable Catalog | v1.0.0` → `Custom__RAG_Variable_Catalog__v1.0.0.yaml`.

---

## §2. Versioning Model (authoritative)

*(Operating Charter §9 and the Command Reference point here.)*

- **Semantic versioning.** Every version carries a permanent **Version ID** of the form `vMAJOR.MINOR.PATCH` (Semantic Versioning, adapted for documents). The first saved version of any document is `v1.0.0`.
- **What each part means:**

  | Bump | Use when | Examples |
  |---|---|---|
  | **MAJOR** (`v2.0.0`) | **Breaking:** following the previous version would now produce wrong results for existing documents or workflows | a command removed or renamed; a rule reversed; a `Source` document's verbatim content replaced (new edition or standard) |
  | **MINOR** (`v1.1.0`) | **Addition:** new capability; nothing previously valid becomes invalid | a new command or section; a new rule that contradicts nothing; a `Source` document's use-case guidance substantively rewritten |
  | **PATCH** (`v1.0.1`) | **Correction:** meaning unchanged | typo, formatting, clearer wording, a fixed cross-reference; repairing a formatting artifact |

  A MINOR bump resets PATCH to 0 (`v1.3.7` → `v1.4.0`); a MAJOR bump resets both (`v1.4.2` → `v2.0.0`). If one change mixes levels, the highest level applies.
- **The system proposes the level; the user decides.** Every version-creating command proposes the bump level with its reasoning. The user's approval of the change and its bump level also covers assigning the new version's Version ID and title; no separate protected-node approval is needed for a genuinely new version (see §3, *Scope of items 1 and 3*).
- **New versions bump the highest existing version — never the active one.** The system scans all of the document's versions (active and archived), takes the **highest**, and bumps it at the approved level. This prevents collisions when an older version is active (e.g., active is `v1.1.0` but `v1.3.2` exists → a PATCH produces `v1.3.3`, not `v1.1.1`).
- **Release candidates.** A version is **released** once it is committed. If a version has been created but **not yet committed**, and more changes **of the same bump level** are added to that update, the uncommitted version is relabeled with the next unused release-candidate suffix — `vX.Y.Z-rc.1`, `-rc.2`, … — and moved to `archive/`, and the combined changes are saved as `vX.Y.Z`. Nothing is deleted. If the added changes would **raise** the bump level, the system flags it and asks the user how to proceed. Relabeling is a protected-node change and needs express approval.
- **Version IDs are permanent and never reused.** A version *is* its ID, for life (Protected — §3). The only relabeling ever permitted is the release-candidate rule above, with express approval.
- **Ordering.** Versions are ordered by Semantic Versioning precedence: MAJOR, then MINOR, then PATCH, compared **numerically** (so `v1.10.0` is newer than `v1.9.0`); a release candidate sorts before its release (`v1.1.0-rc.1` < `v1.1.0`). Gaps are normal (`v1.0.3` → `v1.1.0`); IDs only ever increase.
- **Active pointer vs. version identity are separate.** "Which version is active" is a movable label; "which ID a version has" is fixed identity. `v1.3.2` being newest while `v1.1.0` is active is normal and non-contradictory.
- **Version note and changelog.** Every new version's metadata header carries a **`Version note:`** field — a short label for the change (e.g., `Commands tool expansion update`), approved with the version. Every **released** version is also recorded in `CHANGELOG.md` at the project root.
- **The archive is immutable.** Every version ever created remains reachable by name forever (a release-candidate relabel changes its ID, never its content). **Nothing is destroyed except by the user's explicit deletion command, or the user's approval of a recommended deletion.** Mistaken updates may persist in the archive; the system never prunes or "tidies" versions on its own.
- **Navigation vs. creation.** `Rollback`/`Update` (and their `Full` forms) move the *active pointer* along existing versions and create nothing. Only `Update … Source` / `Update … Custom` / `Revise` create new versions (Command Reference §9–§11, §15).

---

## §3. Protected Nodes (authoritative list)

*(Operating Charter §12 points here.)*

The following are **never altered by the system without the user's express, per-instance permission** (a standing/blanket permission does not count as express permission for a specific change):

1. **Version numbers in metadata** — the monotonic identity IDs (§2). Never renumbered or reassigned.
2. **Source Text on `Source` documents** — the verbatim body (Operating Charter §5). Never edited word-for-word.
3. **Document titles** — they carry baked-in Type/Category/Variant/Version metadata; altering a title corrupts the addressing system.
4. **Deletion of any version or document** — nothing is deleted without an **explicit deletion command** or the user's **approval of a recommended deletion** (§2).
5. **Issued sign-off packets and recorded sign-offs** — a build's sign-off packet is never edited once issued. Any change produces a new numbered packet that needs its own sign-off (§8).
6. **Verbatim evidence quotes** — a quote in a build's evidence ledger is never altered. A wrong or outdated quote is handled by adding a new evidence entry and marking the old one superseded (§8).

**Scope of items 1 and 3 (version IDs and titles).** These protect **existing** versions: a version that already exists never has its ID or title changed. Creating a **genuinely new** version is not a change to a protected node, *provided* it comes from a version-creating command (`Update … Source` / `Update … Custom` / `Revise`) that follows §2 exactly and raises no flag or error. In that case, approving the command, including its bump level, covers the new ID and title. Any flag or error needs express approval: a collision, an ID that isn't the highest existing version bumped, a release-candidate relabel (which renames an existing version), or a non-standard ID.

**Rules about this list:**
- The list is **extensible only by the user.** The user may add protected nodes; the system may **never remove** an entry.
- "Express permission" = the user explicitly approves *that specific* change to *that specific* node. The system does not generalize one approval to future changes.
- When the system needs to touch a protected node, it **stops, states exactly what it wants to change and why, and waits for approval** before proceeding.

---

## §4. Variant Metadata Tracking

- **Every document tracks a Variant metadata field, even when it has no variant** — recorded as `null` (or `-`). A variant-less document simply omits the field from its *title* (§1) but still carries `Variant: null` in its metadata header, so its variant status is always known.
- **Introducing a variant to a previously variant-less Category** triggers a required consistency update: when a second option is added to a Category that had only one (previously unnotated) option, **all documents in that Category must be updated to carry an explicit Variant notation** in their titles and metadata. This keeps every document in a multi-option Category consistently addressable. (User-gated like any title change — titles are protected nodes, §3.)

---

## §5. Folder Ontology & Claude Code Filing Protocol

**The split of responsibilities (capability-honest):**
- **The Project chat is the brain.** It analyzes, drafts, decides naming and placement per this ontology, manages versioning *logic*, and — because it cannot touch the filesystem — **states the exact filename and folder path** for every document it produces so it can be filed.
- **Claude Code is the hands.** It has filesystem/git access and **executes** the actual filing, folder creation, versioned archiving, and renaming, following this ontology. It is **not** a silent always-on daemon — it acts on the user's direction within a session, not unattended. This document is written so Claude Code can follow it directly.

**The folder structure:**
```
rag-builder/
├── governance/            (all three governance docs live here together:
│                           the Operating Charter, the Command Reference,
│                           and this Organizational Rules document)
├── source-truth/          (source docs, organized by slot)
│   ├── first-pass-filtering/
│   ├── metadata-filtering/
│   ├── prompt-augmentation/
│   └── …                  (one folder per slot; variants + active versions inside)
├── custom-design/         (custom docs, including .yaml data documents)
├── tools/                 (small scripts: quote checker, report generator)
├── templates/
│   └── build-workspace/   (empty skeleton copied by `New Build`)
├── .githooks/             (git hooks that block build data from commits — §8)
└── archive/               (superseded versions of any document)
```

**Folder naming (rule, not just the examples above):**
- **All folder names are lowercase, hyphenated, no spaces** — e.g., `source-truth/`, `first-pass-filtering/`, `custom-design/`. This applies to **every new slot folder** created over time, so new slots are named consistently by rule rather than by inference.
- This is the standard repo convention (cross-platform safe, no space-escaping, git-friendly).
- **Folder naming intentionally differs from document filenames.** Folders use lowercase-hyphen; **document filenames** use the `Type__Category__Variant__Version` transform (§1) with meaningful capitals and underscores. **Do not conform one convention to the other** — a document filename is not "fixed" by lowercasing it to match a folder, and a folder is not renamed to match a filename.

**Filing rules:**
- The three **governance documents** (`Rules` Operating Charter, `Commands` Command Reference, `Rules` Organizational Rules) all live together in **`governance/`** — they are read and managed as a set. Only their **active** versions live there; superseded versions move to `archive/` like any other document.
- Every other document is filed by its **Type/class**: a `Source` document goes into its **slot subfolder** under `source-truth/` (slot = its Category); a `Custom` document goes into `custom-design/`.
- **Filenames use the filesystem-safe transform** (§1).
- **Versioned archiving on a new version:** when `Update … Source`/`Update … Custom`/`Revise` creates a new version (§2), Claude Code saves the new version as the active file in the slot/class folder and **moves the prior active version into `archive/`, preserving its version-ID filename.** Nothing is overwritten; the archive copy remains reachable by name for rollback (Command Reference §3–§8).
- **Where the active version lives.** A document's **active** version is the one file in its home folder (`governance/`, its slot folder, or `custom-design/`); every other version of it lives in `archive/`. Navigation (`Rollback`/`Update`) moves the newly active version's file into the home folder and the previously active one into `archive/` — files are moved, never edited. A home folder holding zero, or more than one, version of the same document is an integrity problem, reported by `List`/`Get` (Command Reference §16–§17).
- **Tools, templates and hooks are code, not documents.** They are versioned by git and release tags, not by §1 naming or §2 Version IDs.
- **Build workspaces never live in this tree.** See §8.
- **Slot folders are created as slots are defined** (adding a slot is user-gated — Operating Charter §7).
- **Protected nodes (§3) are never touched** by Claude Code without express permission — including never renaming a title or deleting a version without the user's explicit say-so.

**One-time manual setup** (the user creates the project root folder once, in any location; everything after is Claude-Code-managed). All paths in this document are relative to that project root. From inside the project root, run:
```
mkdir -p governance source-truth custom-design archive tools templates/build-workspace .githooks
git config core.hooksPath .githooks
```
*(The second line turns on the §8 commit guard. It must be run once in every clone of the tool.)*

---

## §6. Security Hygiene Coaching Guardrail

A standing guardrail that **catches secret/security-hygiene mistakes as they happen, explains them, and recommends the fix** — so the discipline is learned over time rather than assumed. Enforced by **Claude Code** (the surface with filesystem/git access); surfaced as **reminders** by the Project chat whenever these topics arise.

**Trigger moments:**
1. **A secret is about to enter a file** — an API key, credential, token, or connection string is pasted into any document or code file.
2. **A project lacks basic protections** — no `.gitignore`, or `.env` not ignored.
3. **Pre-publish check** — before any push/publish/make-public action: **scan the files *and* the git history** for secrets, and **confirm the material is intended to be public** (not a private/proprietary build, client data, or ambiguous content).
4. **Other recognized risky actions** — committing a `.env`, hardcoding credentials, making a private-looking project public.
5. **Build data is about to enter the tool repo, or any location with a git remote.** Build data means company documents, contact details, answers, evidence, correspondence and sign-off packets (§8).
6. **A build is requested at an unsafe location** (inside the tool repo, or anywhere with a git remote). The request is **refused**, not just flagged.
7. **Company information is about to be written into the assistant's memory.** Memory may hold working preferences, never company facts.

**Flag format (every trigger):** *what it noticed → why it's a risk → the recommended fix → a yes/no to the user.* The system halts the risky action and proceeds only on the user's explicit choice.

**Remediation guidance the flag provides:**
- Move any secret into an environment variable (Claude Code's local-environment store) or a `.env` file, and confirm `.env` is in `.gitignore`.
- Check git **history**, not just current files — a secret committed earlier and later "deleted" still lives in history and must be scrubbed (or the repo re-created clean).
- For private/proprietary material: keep the repo **private**, or publish only a sanitized/example version.
- Treat anything published as **permanently public** (scraped, cached, forked) — which is why the check runs *before* the push.
- Move build data to its workspace under `~/Documents/rag-builds/`. If it was ever committed, treat it as published: scrub the history and tell the company (trigger 3 logic).

**Honesty clause (must remain in this section):** This guardrail is a **backstop, not a guarantee.** It only catches risks that pass **through a Claude session** — a secret pasted into a file entirely outside of Claude is not seen and not flagged — and AI recognition of secrets is strong but not perfect. It **does not replace** the primary discipline (never put secrets in code/files; `.env` + `.gitignore` from the first commit). Do not over-trust it: it is the net under the habit, and over-trusting a net lowers the vigilance that actually keeps you safe.

---

## §7. Automation Options (reference)

For reducing the manual filing step beyond in-session Claude Code management:
- **Claude Code** — the primary file-managing surface (§5): understands this ontology, files/versions/archives per the rules, reasons about placement. Acts in-session on direction.
- **Folder-action script / n8n auto-sort** — a no-AI, hands-off option: save documents to a single inbox folder, and a script (macOS Folder Actions/Automator, or an n8n workflow) **parses the filename and auto-files** it into the correct slot/class folder. This is possible **because the naming convention (§1) encodes Type/Category/Variant/Version in the filename** — the automation just reads the fields. Simpler and always-on, but "dumb": it sorts by name and does not reason, version, or apply protected-node rules. Best as a convenience layer under Claude-Code-managed versioning, not a replacement for it.

---

## §8. Build Workspaces

**Tool vs. builds.** This repository is the **tool**: governance, catalogs, templates and scripts. It is company-neutral and may be public. A **build** is one engagement with one company. It holds that company's confidential material and lives in a **build workspace**, entirely outside this repository.

**Location.**
- The default is `~/Documents/rag-builds/<build-name>/`, where the folder name is lowercase and hyphenated (§5).
- A build workspace is **never** inside the tool repo, and **never** has a git remote.
- Local git with no remote is allowed, and recommended as an audit trail.
- `New Build` checks the location and refuses it otherwise.
- **Company machines:** copy the tool as a ZIP download, or clone it and immediately run `git remote remove origin`. Confirm that `git remote -v` prints nothing.

**Layout.**
```
<build-name>/
├── CLAUDE.md          loads the tool's governance by path; build chats are opened here
├── build.yaml         status, stage, dates, tool version, catalog version, AI-processing approval
├── inputs/            documents as received; never modified; fingerprinted on intake
├── contacts.yaml      role → person → email; supplied only by the user
├── evidence.yaml      evidence ledger: source, location, verbatim quote, variables supported
├── answers.yaml       one entry per variable: value, status, confidence, evidence IDs
├── correspondence/    drafted emails and logged responses
├── reports/           gap reports; numbered sign-off packets (signoff-packet-v1.md, …)
└── decisions/         sign-off records; later, architecture decision records
```

**Rules.**
1. **Work from the build folder.** Build chats are opened in the build workspace, not in the tool repo. The build's `CLAUDE.md` loads the tool's governance by path, so the same rules apply there.
2. **Record the versions.** `build.yaml` records the tool version (release tag or commit) and the Variable Catalog version the build used.
3. **AI-processing approval comes first.** Before any input is accepted, `build.yaml` must record whether the company permits its documents to be processed by the AI provider, who approved it, and when. If the answer is no, or isn't recorded, no inputs are accepted.
4. **Inputs are immutable.** Files in `inputs/` are never modified. A SHA-256 fingerprint is recorded when each file is received.
5. **Every answer cites evidence.** Each filled variable points to one or more evidence entries. An entry gives the source (a file plus page or section, or a person plus date) and a **verbatim quote**. A tool script checks that every quote appears word for word in its source. A value with no evidence is labeled **Assumed** and is disclosed as such in the sign-off packet.
6. **Build records are not knowledge-base documents.** They don't use §1 titles or §2 Version IDs. Snapshots such as sign-off packets are numbered `v1`, `v2`, … and are immutable once issued (§3 item 5).
7. **No crossing.** Build data is never copied into the tool repo or into the assistant's memory. A lesson a build teaches (a missing variable, a better question) returns to the tool only as a **company-neutral** `Revise`.
8. **Close-out.** When an engagement ends, `Close Build` archives or deletes the workspace according to the company's retention requirements. Deletion needs the user's explicit approval (§3 item 4).

**Enforcement layers.** No single layer is trusted on its own:
- **Location:** builds happen outside the tool repo (rule 1).
- **Mechanism:** a pre-commit hook in `.githooks/`, plus `.gitignore` patterns, block commits that contain build files (`inputs/`, `build.yaml`, `evidence.yaml`, `answers.yaml`, `contacts.yaml`, `correspondence/`). This works whoever makes the commit.
- **Rules:** this section and §6.

*Honesty clause:* the hook runs only after the `git config core.hooksPath .githooks` setup step (§5), and `git commit --no-verify` can bypass it. The layers reduce the risk; they don't remove it.

---

## This document's own governance

This Organizational Rules document is a `Rules`-type document, **versioned under the Versioning Model it defines** (§2): permanent version number, immutable archive of prior versions, changed only through gated `Revise` / update / rollback commands with user approval. Its metadata header, version number, and the Protected Nodes list (§3) are protected nodes.

# Catalyst Invariants

The non-negotiable rules of the catalyst framework, extracted into one lean file
so they can be re-read cheaply and survive context compaction. This is the
**canonical** copy; `BOOTSTRAP.md §0` mirrors it and `INSTANTIATION-GUIDE.md §1`
is the prose origin. If those disagree with this file, this file wins and the
others should be corrected.

Keep this file short. Anything that needs explanation, examples, or rationale
belongs in the guide it came from — not here. A bloated invariants file decays
faster and is the first thing a summarizer mangles.

## Behavioural

- **INV-1 — Repo-scoped references.** Never mention a local drive, folder, or
  path when referring to catalyst. Only the git repository and repository name.
- **INV-2 — Install on first load.** First load into a project ⇒ install
  immediately via the instantiation procedure.
- **INV-3 — Name it "catalyst".** Always "catalyst" / "catalyst framework"
  thereafter, in guidance, memory, and discussion.
- **INV-4 — Assent before push.** Never push anything (project or catalyst)
  without the user's explicit assent. No target-repo commit without assent.

## Structural

- **INV-5 — Chain invariant.** No work without a traceable link down to a
  documented rule: epic → story → task → REQ/BUG/HK → rule → domain. Every
  document, domain, and rule has a stable, permanent, never-reused ID.
- **INV-6 — Fixed deploy dir.** The deployment directory is `.catalyst-proj/`.
  No exception.
- **INV-7 — Descriptive naming.** Every rule, dev-artifact, and domain file is
  `<id>-<short-summary>.md` (sub-domain: `<prefix>-<PARENT>.<SUB>-<summary>.md`).
  Bare-ID filenames are invalid.
- **INV-8 — No orphan rules.** Every rule lives in its type directory, appears in
  its local type index, and appears in the global `rules.md`. Exactly one
  `TEMPLATE-RULE.md`, in the `rules/` root.
- **INV-9 — Requirements, not bugs, for new work.** `FEAT-` entries are
  non-rule-linked roadmap. When work on one starts it becomes a `REQ-` (never a
  `BUG-`), which is vetted against every rule, assigned a domain, and measured.
- **INV-14 — Persisted backlog.** `development/BACKLOG.md` always exists,
  seeded from `templates/backlog.template.md`. It is never hand-edited —
  `/show-backlog` overwrites it in full every run, so it can't drift from
  the real indexes.
- **INV-15 — Machine-maintained roadmap tracking.** `development/roadmaps/`
  and its `roadmaps.md` index always exist (empty is fine); individual named
  roadmaps are created only via `/roadmap-add`. In every
  `development/roadmaps/<name>.md`, the Status/Linked columns are set only
  by the `/roadmap-*` commands and `/show-backlog` — never hand-edited.
  `/roadmap-remove` never deletes a roadmap with linked items; it retires
  it in place.
- **INV-16 — At least one active user; advisory role signing.**
  `development/users.json` and `development/roles.json` always exist, and
  `users.json` must contain **at least one user with `"active": true`** —
  a hard requirement, not optional-if-empty like `roadmaps.md`. Every
  dev-artifact, feature, roadmap item, and work item carries a
  `Signed-off-by` field. Role checks against `roles.json` are advisory — a
  mismatch prompts for confirmation, never a hard block, since catalyst
  cannot verify who is actually typing. `/user-remove` never deletes a
  user's entry; it sets `"active": false`, and refuses (or warns) if doing
  so would leave zero active users.
- **INV-17 — Append-only, replayable journal.** `development/journal.jsonl`
  always exists (empty is fine). Every command that creates, modifies,
  closes, or retires a rule-linked artifact, rule, domain, or work item, or
  changes a `Status` field, appends exactly one entry — timestamp, actor,
  command, action, artifact ID, `targets` (rule IDs, when applicable), one
  or more `intent` statements (the goal driving the change, not just a
  label), and, per touched file, its content hash immediately before and
  immediately after (`git hash-object -w`, written to the object store so
  it's retrievable independent of any commit; `null` for create/delete).
  This makes the journal transaction-log-grade: replaying entries up to
  any timestamp and materializing each file's last `after` hash as of
  that point reconstructs the exact tree state then, via `/journal-restore`
  into a side directory — never overwriting the live tree outright.
  Entries are immutable once written: never edited, deleted, or reordered.
  Complements — does not duplicate — the `catalyst-git` plugin's
  continuous compliance auditing of a *deployed project*; this journal is
  core, applies to catalyst's own deployment too, and records history
  rather than flagging violations.

## Plugins

- **INV-10 — Activation gate.** A plugin is not loaded unless activated via
  `/catalyzer`, and only if it carries `README.md` + `working-contract.md`.
- **INV-11 — Plugin provenance.** Every plugin has its own repository; no plugin
  is sourced from the framework repository.
- **INV-12 — Contract is canonical + stable.** Every plugin's
  `working-contract.md` carries the six metadata fields (Name, Description,
  UUID, Version, Active, Type). The UUID is generated once and never changes.
  `Version` matches the plugin's own `version.txt` and its catalog pin. The
  framework reads `Active` at startup to decide what loads.
- **INV-13 — Operate on the deployment, not on catalyst.** A plugin's runtime
  target (monitoring, auditing, mutation) is the *deployed project's* repository,
  resolved at activation time — never the catalyst framework's own repository and
  never the plugin's own installation directory under `plugins/<type>/<name>/`.

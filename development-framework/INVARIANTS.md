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

# Catalyst Framework

A project-agnostic, portable specification for how any codebase organizes
its rules, its development work, its agile process, its roadmap, its
accountability, and its own change history — extrapolated from the
concrete system built in this repo's own [`.criterion/`](../.criterion/)
deployment. That folder is **one instantiation** of this framework, for
this project, built via the retrofit path (§4 below); this folder is the
generic template for standing the same system up in any project so it
can create rules that fit that project's reality.

(`criterion` is a different thing entirely as of INV-18 — the
canonical branch name in a *repoed* deployment's dedicated sync
repository, not a folder. See §13 of `rules-of-rules.template.md`.)

## What this framework is

A four-layer chain, each layer subordinate to the one below it:

```
Work items    EPIC ─▶ STORY ─▶ TASK / SPIKE / SPRINT   (agile process layer)
                        │
                        ▼
Dev artifacts        REQ- / BUG- / HK- / TAG-         (rule-linked work and lightweight annotations)
                        │
                        ▼
Rules            (prefix)-(DOMAIN)-(NNN)               (documented behavior)
                        │
                        ▼
Rules of rules   the meta-rules governing all of the above
```

The chain's invariant, at every layer: **no work happens without a
traceable link down to a documented rule.** A story targets a requirement or
bug doc; a requirement doc targets (or proposes) a rule; a rule belongs to a
domain; a domain belongs to a document; every document, domain, and rule has a
stable, permanent, never-reused ID. This is what makes "why does this code
do X" and "what rule does this ticket satisfy" both answerable by
following IDs, in either direction, indefinitely.

Sitting above all of this, `FEAT-NNNNNN` feature entries (`features/`) are a
separate, optional, **non-rule-linked** layer — a place to write down new or
future app functionality as an idea or roadmap item, before it's ready to be
measured. A feature is never itself implemented and never breaks the chain's
invariant: when work on one actually starts, that work is tracked as a
`REQ-NNNNNN` requirement (never a `BUG-NNNNNN`), which is what gets vetted
against every existing rule document, assigned a domain, and measured for
completion. See `Rules-of-Rules.md` §9.

`FEAT-` entries can themselves be bulk-populated: named roadmaps
(`development/roadmaps/<name>.md`, one file per external source ingested
via `/roadmap-add`/`-update`/`-merge`) hold `RM-NNNNNN` items with their own
Status, triaged into a `FEAT-` when a human decides one's worth tracking.
See `Rules-of-Rules.md` §10.

Every artifact this framework creates — dev-artifact, feature, roadmap
item, or work item — carries a `Signed-off-by` field, resolved against
`IAM/users/users.json` (managed by `/user-add`/`-remove`/`-modify`/
`-assign-role`) and `IAM/roles/roles.json` (the role → typical-action
mapping, `/role-add`/`-modify`). A deployment must always have at least
one active user; beyond that, role checks are advisory, not access
control — see `Rules-of-Rules.md` §11.

Every artifact-type directory follows the same shape — a versioned,
catalogued `templates/` subdirectory and its own `README.md`
(`INVARIANTS.md` INV-20, `Rules-of-Rules.md` §15) — including `boards/`
and `workflows/` (optional, per agile flavor) and a `tickets/` slot
reserved for plugin population rather than a core-defined type.

Every rule-linked change also appends one entry to
`development/journal.jsonl`, an append-only, transaction-log-grade
record: exact git content hashes before/after per touched file, the
rule(s) it served, and the actual intent behind it. Precise enough that
`/journal-restore <timestamp>` can materialize the tree as it stood at
any point into a side directory — real reconstruction, not narrative.
See `Rules-of-Rules.md` §12.

A deployment can additionally opt into being **repoed**: `.criterion/`
mirrored through a dedicated repository so multiple contributors converge
on one agreed-upon state instead of silently diverging.
`/criterion create`/`get`/`push` manage it; every push is vetted against
the framework's own rules (`/check-rules` plus a four-eyes drift check)
before an AI-assisted merge lands it on the canonical `criterion`
branch. `/dogfood` runs that same vetting procedure standalone, but only
against catalyst's own repository — it's never part of what a deployed
project carries. See `Rules-of-Rules.md` §13.

## Files in this folder

| File | Purpose |
|---|---|
| [`rules-of-rules.template.md`](rules-of-rules.template.md) | Generic meta-rules: conflict-checking, done-bar, ID scheme, domain standard, retirement. Copy to `<project>/rules/Rules-of-Rules.md` and fill in placeholders. |
| [`rules-of-development.template.md`](rules-of-development.template.md) | Generic standards for bug/requirement/house-keeping/meta-tag artifacts. Copy to `<project>/CODE-OF-CONDUCT.md`. |
| [`rules-of-work-items.template.md`](rules-of-work-items.template.md) | Generic Scrum/agile process layer sitting above dev artifacts. Copy to `<project>/<work-items-dir>/rules-of-work-items.md`. |
| [`templates/`](templates/) | Generic per-item-type document templates (bug, requirement, feature, house-keeping, meta-tag, epic, story, task, spike, sprint, domain, slash-command, backlog, roadmap, roles, users, journal). |
| [`SYNCHRONIZE.md`](SYNCHRONIZE.md) | Rules for synchronizing this framework with deployed projects when versions are missing or outdated. |
| [`version.txt`](version.txt) | Current framework version. |
| [`INSTANTIATION-GUIDE.md`](INSTANTIATION-GUIDE.md) | Step-by-step: how to stand this framework up in a new (or existing) project. |
| [`ARTIFACT-LAYOUT.md`](ARTIFACT-LAYOUT.md) | Clean, standalone reference tree for the deployed uniform artifact-type layout (`Rules-of-Rules.md` §15, INV-20) — the shape alone, without the deploy-procedure prose. |
| [`migrations/`](migrations/) | One-time migration plans for bringing an existing deployment up to a framework version that changed the deployed shape. |

## Folder guides

- [`templates/README.md`](templates/README.md) — explains the purpose of the reusable template library and how the templates map to the framework's artifact and workflow layers.

## Agile-methodology agnostic

The work-items layer defaults to Scrum vocabulary (epic/story/task/spike/
sprint) because it's the most widely recognized, but nothing below the
work-items layer cares which agile flavor sits on top of it:

- **Scrum**: use `SPRINT-NNN` as written — time-boxed, committed items,
  retro.
- **Kanban**: drop `sprints/` entirely; treat `STORY-`/`TASK-` as
  continuous-flow cards, add a `Status` value for each WIP-limited column
  instead of sprint membership.
- **Scrumban / any hybrid**: keep `epics/`/`stories/`/`tasks/`/`spikes/`,
  make `sprints/` optional per team.

The rules layer and the dev-artifacts layer never change based on this
choice — "no development without a targeted rule" is a project-wide
invariant regardless of how work is scheduled above it.

## Greenfield projects (no code yet)

See [`INSTANTIATION-GUIDE.md`](INSTANTIATION-GUIDE.md) §3. The mirror
image of retrofitting: instead of extracting rules from existing code,
this path establishes the stack, tooling, and dev-environment decisions
— language/runtime, package manager, linter/formatter, test framework,
CI, local dev setup, repo layout — as the first rule document, before
any application code exists, so the project is born governed rather than
governed after the fact.

## Retrofitting an existing project

See [`INSTANTIATION-GUIDE.md`](INSTANTIATION-GUIDE.md) §4. This repo's own
[`.criterion/`](../.criterion/) was retrofitted this way — its
`Rules-of-Rules.md`, `CODE-OF-CONDUCT.md`, and `rules-of-work-items.md`
each carry a header noting they are this project's instantiation of the
corresponding template here, so the two stay traceable to each other as
this framework evolves. Its one rule document
(`rules/framework/fw-framework-rules.md`) retrofits every entry in
`INVARIANTS.md` into a real, ID'd rule, honestly marked ✅ where a
`scripts/check_*.py` function and test actually enforce it and ⚠️ where
it's behavioural (agent conduct during a session) rather than
machine-checkable from a tree snapshot.

The instantiation guide also now includes a persistent-memory step so the
project path and `.criterion/` location used for deployment are
remembered across sessions.

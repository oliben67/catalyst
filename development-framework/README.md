# Catalyst Framework

A project-agnostic, portable specification for how any codebase organizes
its rules, its development work, and its agile process — extrapolated
from the concrete system built in this repo's
[`.thingamabob/`](../.thingamabob/) folder. That folder is
**one instantiation** of this framework, for this project; this folder is
the generic template for standing the same system up in any project so it
can create rules that fit that project's reality.

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

Sitting above all of this, `FEAT-NNNN` feature entries (`features/`) are a
separate, optional, **non-rule-linked** layer — a place to write down new or
future app functionality as an idea or roadmap item, before it's ready to be
measured. A feature is never itself implemented and never breaks the chain's
invariant: when work on one actually starts, that work is tracked as a
`REQ-NNNN` requirement (never a `BUG-NNNN`), which is what gets vetted
against every existing rule document, assigned a domain, and measured for
completion. See `Rules-of-Rules.md` §9.

## Files in this folder

| File | Purpose |
|---|---|
| [`rules-of-rules.template.md`](rules-of-rules.template.md) | Generic meta-rules: conflict-checking, done-bar, ID scheme, domain standard, retirement. Copy to `<project>/rules/Rules-of-Rules.md` and fill in placeholders. |
| [`rules-of-development.template.md`](rules-of-development.template.md) | Generic standards for bug/requirement/house-keeping/meta-tag artifacts. Copy to `<project>/CODE-OF-CONDUCT.md`. |
| [`rules-of-work-items.template.md`](rules-of-work-items.template.md) | Generic Scrum/agile process layer sitting above dev artifacts. Copy to `<project>/<work-items-dir>/rules-of-work-items.md`. |
| [`templates/`](templates/) | Generic per-item-type document templates (bug, requirement, feature, house-keeping, meta-tag, epic, story, task, spike, sprint, domain, slash-command, backlog, roadmap, roles, users). |
| [`SYNCHRONIZE.md`](SYNCHRONIZE.md) | Rules for synchronizing this framework with deployed projects when versions are missing or outdated. |
| [`version.txt`](version.txt) | Current framework version (`0.1.10`). |
| [`INSTANTIATION-GUIDE.md`](INSTANTIATION-GUIDE.md) | Step-by-step: how to stand this framework up in a new (or existing) project. |

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
`.thingamabob/` folder was retrofitted this way — its
`Rules-of-Rules.md`, `CODE-OF-CONDUCT.md`, and
`rules-of-work-items.md` each carry a header noting they are this
project's instantiation of the corresponding template here, so the two
stay traceable to each other as this framework evolves.

The instantiation guide also now includes a persistent-memory step so the
project path and `.thingamabob/` location used for deployment are remembered
across sessions.

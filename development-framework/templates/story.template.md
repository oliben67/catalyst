# `STORY-NNNN` — short title

| Field | Value |
|---|---|
| **ID** | `STORY-NNNN` |
| **Status** | backlog / ready / in-progress / review / done |
| **Epic** | `EPIC-NNNN` (or "none") |
| **Targets** | rule ID(s) this story implements/extends — required per `rules-of-development.md` §1; if none exist yet, see Feature doc below |
| **Feature doc** | `FEAT-NNNN` — the corresponding entry, which owns rule-compliance bookkeeping. Create it first if it doesn't exist |
| **Points** | story-point estimate |
| **Section** | `SECTION` code(s), from the linked feature/rule IDs |

## Story

As a **\<role\>**, I want **\<capability\>**, so that **\<benefit\>**.

## Acceptance criteria

Given/When/Then, one block per criterion — should mirror the acceptance
criteria already in the linked `FEAT-NNNN` doc, not diverge from them.

- **Given** … **When** … **Then** …

## Tasks

| Task | Title | Status |
|---|---|---|
| `TASK-NNNN` | … | … |

## Related

Other `STORY-`/`TASK-`/`SPIKE-` IDs, or rule IDs.

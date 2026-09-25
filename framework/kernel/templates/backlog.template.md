# Backlog — template

> Copy this file to `development/BACKLOG.md` on first deploy. Unlike every
> other template here, this is not a fill-in-once document: `/show-backlog`
> **overwrites it in full** every time it runs, regenerating each section
> from the real indexes. Hand-editing it is pointless — the next
> `/show-backlog` run replaces whatever you wrote. See
> [`../rules-of-development.template.md`](../rules-of-development.template.md)
> §2 and `INVARIANTS.md` INV-14.

**Last refreshed:** {{DATE}} by `/show-backlog`.

## Open bugs

{{BUG-NNNNNN items grouped by Severity (Critical/High/Medium/Low), or "*(none)*" if empty}}

## In-progress / proposed requirements

{{REQ-NNNNNN items with Status proposed/approved/in-progress, or "*(none)*"}}

## Work items missing links

{{if a project-management-type plugin is active: any STORY-/TASK- with no linked REQ-/BUG- doc, per that plugin's rules-of-work-items.md §1 — a real violation to flag, not routine backlog; otherwise "*(no work-items layer active)*"}}

## Rules with no open work

{{any ⚠️ or ❌ rule with no BUG-/REQ- currently targeting it, or "*(none)*"}}

## Feature ideas with no requirement yet

{{FEAT-NNNNNN entries with an empty Requirement(s) field, or "*(none)*"}}

## Roadmap

{{RM-NNNNNN rows from every non-retired development/roadmaps/<name>.md, grouped by roadmap name then Status (Not triaged / Triaged / In progress), or "*(none)*" if every row is Done or no named roadmap has been added yet}}

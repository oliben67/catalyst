---
description: Create a new epic work item and register it in epics/epics.md
argument-hint: <goal> [--domains <CODE>...]
---

> **Prototype — not implemented.** Part of the agile schema at
> `plugins/_prototyping/project-management/agile/`, not a deployed
> command. No concrete project-management plugin exists yet to activate
> this; kept here as the spec a future one implements against.

Create a new epic work item. Full spec: this plugin's schema, `rules-of-work-items.template.md`
(this directory), template:
`templates/TEMPLATE-EPIC-v1.md` (this directory).
Input: $ARGUMENTS

1. Resolve the next `EPIC-NNNNNN` ID from `epics/epics.md` + a
   directory listing of `epics/`.
2. Names the `DOMAIN` code(s) it spans; never targets a rule directly
   (`rules-of-work-items.md` §4).
3. Resolve who is signing this per CODE-OF-CONDUCT.md §2 and fill
   `Signed-off-by`.
4. Copy the current `TEMPLATE-EPIC-vN.md`, fill every field, save as
   `epics/EPIC-NNNNNN-<short-summary>.md`.
5. Register it in `epics/epics.md`.
6. Report the result. Do not commit or push — leave changes unstaged
   unless the user asks otherwise.

---
description: Create a new sprint container and register it in sprints/sprints.md
argument-hint: <sprint-goal> --dates <start>..<end>
---

> **Prototype — not implemented.** Part of the agile schema at
> `plugins/_prototyping/project-management/agile/`, not a deployed
> command. No concrete project-management plugin exists yet to activate
> this; kept here as the spec a future one implements against.

Create a new sprint container. Full spec: this plugin's schema, `rules-of-work-items.template.md`
(this directory), template:
`templates/TEMPLATE-SPRINT-v1.md` (this directory).
Input: $ARGUMENTS

1. Resolve the next `SPRINT-NNN` ID (3 digits) from
   `sprints/sprints.md` + a directory listing of `sprints/`.
2. Holds `STORY-`/`TASK-`/`SPIKE-` IDs as-is — never restates acceptance
   criteria or rule targets (`rules-of-work-items.md` §5).
3. Resolve who is signing this per CODE-OF-CONDUCT.md §2 and fill
   `Signed-off-by`.
4. Copy the current `TEMPLATE-SPRINT-vN.md`, fill every field, save as
   `sprints/SPRINT-NNN-<short-summary>.md`.
5. Register it in `sprints/sprints.md`.
6. Report the result. Do not commit or push — leave changes unstaged
   unless the user asks otherwise.

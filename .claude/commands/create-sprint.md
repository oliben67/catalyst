---
description: Create a new sprint container and register it in work-items/sprints.md
argument-hint: <sprint-goal> --dates <start>..<end>
---

Create a new sprint container. Full spec:
`.catalyst-proj/CODE-OF-CONDUCT.md` §4,
`.catalyst-proj/work-items/rules-of-work-items.md`, template:
`.catalyst-proj/work-items/TEMPLATE-SPRINT.md`.
Input: $ARGUMENTS

1. Resolve the next `SPRINT-NNN` ID (3 digits) from
   `work-items/sprints.md` + a directory listing of `work-items/sprints/`.
2. Holds `STORY-`/`TASK-`/`SPIKE-` IDs as-is — never restates acceptance
   criteria or rule targets (`rules-of-work-items.md` §5).
3. Resolve who is signing this per CODE-OF-CONDUCT.md §2 and fill
   `Signed-off-by`.
4. Copy `TEMPLATE-SPRINT.md`, fill every field, save as
   `work-items/sprints/SPRINT-NNN-<short-summary>.md`.
5. Register it in `work-items/sprints.md`.
6. Report the result. Do not commit or push — leave changes unstaged
   unless the user asks otherwise.

---
description: Create a new epic work item and register it in work-items/epics.md
argument-hint: <goal> [--domains <CODE>...]
---

Create a new epic work item. Full spec:
`.catalyst-proj/CODE-OF-CONDUCT.md` §4,
`.catalyst-proj/work-items/rules-of-work-items.md`, template:
`.catalyst-proj/work-items/TEMPLATE-EPIC.md`.
Input: $ARGUMENTS

1. Resolve the next `EPIC-NNNN` ID from `work-items/epics.md` + a
   directory listing of `work-items/epics/`.
2. Names the `DOMAIN` code(s) it spans; never targets a rule directly
   (`rules-of-work-items.md` §4).
3. Resolve who is signing this per CODE-OF-CONDUCT.md §2 and fill
   `Signed-off-by`.
4. Copy `TEMPLATE-EPIC.md`, fill every field, save as
   `work-items/epics/EPIC-NNNN-<short-summary>.md`.
5. Register it in `work-items/epics.md`.
6. Report the result. Do not commit or push — leave changes unstaged
   unless the user asks otherwise.

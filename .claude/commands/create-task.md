---
description: Create a new task work item under a parent story and register it in work-items/tasks.md
argument-hint: <task> --story <STORY-NNNN>
---

Create a new task work item. Full spec:
`.catalyst-proj/CODE-OF-CONDUCT.md` §4,
`.catalyst-proj/work-items/rules-of-work-items.md`, template:
`.catalyst-proj/work-items/TEMPLATE-TASK.md`.
Input: $ARGUMENTS

1. Resolve the next `TASK-NNNN` ID from `work-items/tasks.md` + a
   directory listing of `work-items/tasks/`.
2. A task never gets its own rule target — it inherits its parent story's
   (`rules-of-work-items.md` §2). If it needs a rule the story doesn't
   cover, fix the story/requirement first.
3. Resolve who is signing this per CODE-OF-CONDUCT.md §2 and fill
   `Signed-off-by`.
4. Copy `TEMPLATE-TASK.md`, fill every field, save as
   `work-items/tasks/TASK-NNNN-<short-summary>.md`.
5. Register it in `work-items/tasks.md`.
6. Report the result. Do not commit or push — leave changes unstaged
   unless the user asks otherwise.

---
description: Create a new story work item, linked to a REQ-/BUG- doc, and register it in work-items/stories.md
argument-hint: <story> --req <REQ-NNNN|BUG-NNNN> [--epic <EPIC-NNNN>]
---

Create a new story work item. Full spec:
`.catalyst-proj/CODE-OF-CONDUCT.md` §4,
`.catalyst-proj/work-items/rules-of-work-items.md`, template:
`.catalyst-proj/work-items/TEMPLATE-STORY.md`.
Input: $ARGUMENTS

1. Resolve the next `STORY-NNNN` ID from `work-items/stories.md` + a
   directory listing of `work-items/stories/`.
2. Must link to exactly one `REQ-NNNN` or `BUG-NNNN` — never a substitute
   for one (`rules-of-work-items.md` §1). If none exists yet, create it
   first via `/create-req`/`/create-bug`.
3. Resolve who is signing this per CODE-OF-CONDUCT.md §2 and fill
   `Signed-off-by`.
4. Copy `TEMPLATE-STORY.md`, fill every field, save as
   `work-items/stories/STORY-NNNN-<short-summary>.md`.
5. Register it in `work-items/stories.md`.
6. Report the result. Do not commit or push — leave changes unstaged
   unless the user asks otherwise.

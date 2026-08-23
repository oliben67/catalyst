---
description: Create a new time-boxed spike work item and register it in work-items/spikes.md
argument-hint: <question> --timebox <duration> [--parent <STORY-NNNN|EPIC-NNNN>]
---

Create a new spike work item. Full spec:
`.catalyst-proj/CODE-OF-CONDUCT.md` §4,
`.catalyst-proj/work-items/rules-of-work-items.md`, template:
`.catalyst-proj/work-items/TEMPLATE-SPIKE.md`.
Input: $ARGUMENTS

1. Resolve the next `SPIKE-NNNN` ID from `work-items/spikes.md` + a
   directory listing of `work-items/spikes/`.
2. Time-boxed, never itself "implements" anything
   (`rules-of-work-items.md` §3) — phrase the Question so
   "answered: yes/no/X" is unambiguous.
3. Resolve who is signing this per CODE-OF-CONDUCT.md §2 and fill
   `Signed-off-by`.
4. Copy `TEMPLATE-SPIKE.md`, fill every field, save as
   `work-items/spikes/SPIKE-NNNN-<short-summary>.md`.
5. Register it in `work-items/spikes.md`.
6. Report the result. Do not commit or push — leave changes unstaged
   unless the user asks otherwise.

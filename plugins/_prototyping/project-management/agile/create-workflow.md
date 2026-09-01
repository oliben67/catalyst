---
description: Create a new process-definition document and register it in workflows/workflows.md
argument-hint: <process-name>
---

> **Prototype — not implemented.** Part of the agile schema at
> `plugins/_prototyping/project-management/agile/`, not a deployed
> command. No concrete project-management plugin exists yet to activate
> this; kept here as the spec a future one implements against.

Create a new process-definition document. Full spec: this plugin's schema, `rules-of-work-items.template.md`
(this directory), template:
`templates/TEMPLATE-WORKFLOW-v1.md` (this directory).
Input: $ARGUMENTS

**Not a unit of work** — no parent epic/story link, never itself "done."
Documents how a category of work moves through its steps.

1. Resolve the next `WORKFLOW-NNNNNN` ID (6 digits) from
   `workflows/workflows.md` + a directory listing of
   `workflows/`.
2. `Status: Active` (only ever `Active` or `Deprecated` — never a
   work-tracking lifecycle).
3. Resolve who is signing this per CODE-OF-CONDUCT.md §2 and fill
   `Signed-off-by`.
4. Copy the current `TEMPLATE-WORKFLOW-vN.md`, fill every field, save as
   `workflows/WORKFLOW-NNNNNN-<short-summary>.md`.
5. Register it in `workflows/workflows.md`.
6. Report the result. Do not commit or push — leave changes unstaged
   unless the user asks otherwise.

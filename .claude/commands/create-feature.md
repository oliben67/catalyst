---
description: Create a new feature entry and register it in features/features.md (non-rule-linked)
argument-hint: <description> [--roadmap <RM-NNNN>]
---

Create a new feature entry. Full spec: `.catalyst-proj/CODE-OF-CONDUCT.md`
§3/§4, template: `.catalyst-proj/features/TEMPLATE-FEATURE.md`.
Input: $ARGUMENTS

1. Resolve the next `FEAT-NNNN` ID from `features/features.md` + a
   directory listing of `features/` — never guess or reuse a number.
2. Do not prompt for a domain or rule target — neither field exists on
   this artifact type (`Rules-of-Rules.md` §9).
3. If this formalizes an existing roadmap row (any
   `development/roadmaps/<name>.md`), cite that row's `RM-NNNN` ID in the
   `Roadmap` field and set the row's `Status` to `Triaged`, `Linked` to
   this new `FEAT-NNNN`.
4. Resolve who is signing this per §2 and fill `Signed-off-by`.
5. Copy `TEMPLATE-FEATURE.md`, fill every field, save as
   `features/FEAT-NNNN-<short-summary>.md`.
6. Register it in `features/features.md`.
7. Report the result. Do not commit or push — leave changes unstaged
   unless the user asks otherwise.

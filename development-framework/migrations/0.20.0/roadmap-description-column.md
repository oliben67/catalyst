# Migration: roadmap items gain a `Description` column

> Target version: `0.20.0` — this is the migration that produces the
> shape `0.20.0` introduced. Triggered by `SYNCHRONIZE.md`'s
> "Version-specific one-time migrations" (`From 0.19.0`). Applies once,
> the first time a deployment's `version.txt` advances past `0.19.0` to
> `0.20.0` or later. Never re-run on a later sync once applied.

## What changed

Every `RM-NNNNNN` roadmap row (`development/roadmaps/<name>.md`) gains a
`Description` column, between `Title` and `Status` — a sentence or two
summarizing the item, distinct from `Title`'s short label. `/roadmap-add`,
`/roadmap-update`, and `/roadmap-merge` now populate it the same way they
already populate `Title`, drawn from the ingested source file.

| Old | New |
|---|---|
| `\| ID \| Title \| Status \| Linked \| Signed-off-by \| Notes \|` | `\| ID \| Title \| Description \| Status \| Linked \| Signed-off-by \| Notes \|` |

If you're running the `catalyst-ui` VS Code extension against this
deployment: versions of that extension before its own `Description`-aware
release parse this table **positionally** — inserting a column in the
middle would shift `Status`/`Linked`/`Signed-off-by` for any row created
under the new shape. Upgrade `catalyst-ui` alongside this migration, not
after it, if you use it.

## Steps

1. For each existing `development/roadmaps/<name>.md`, insert a
   `Description` column into the `## Items` table header and separator
   row, between `Title` and `Status`.
2. For each existing `RM-NNNNNN` row, fill in its new `Description` cell:
   re-derive it from whatever source file `/roadmap-add`/`-update` last
   ingested for that roadmap (`Source` field in the file's own header) if
   still available; otherwise ask the user for a one-line summary per
   row rather than leaving it blank or guessing from `Title` alone.
3. Leave every other column (`ID`, `Title`, `Status`, `Linked`,
   `Signed-off-by`, `Notes`) exactly as they are — this migration only
   adds a column, it never changes `RM-NNNNNN` IDs or existing field
   values.
4. Verify: `/show-backlog`'s Roadmap section still renders correctly
   (it reads `Status`/`Linked` by name from the table, not position, so
   this migration doesn't require touching it — but confirm after, since
   this is the first migration to reshape this specific table).
5. Journal the migration (`action: "update"`, `intent` describing the
   column addition, one entry per roadmap file actually touched) — never
   rewrite the journal itself (INV-17).
6. Report the result.

Past migration docs and their rows in `migrations.md` describe shapes as
they were named at the time and are not rewritten by this migration.

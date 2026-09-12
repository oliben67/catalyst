# Migration: add `ACCESS-CONTROL.md`

> Target version: `0.25.0` — this is the migration that produces the shape
> `0.25.0` introduces. Triggered by `SYNCHRONIZE.md`'s "Version-specific
> one-time migrations" (`From 0.24.0`). Applies once, the first time a
> deployment's `version.txt` advances past `0.24.0` to `0.25.0` or later.
> Never re-run on a later sync once applied.

## What changed

New root-level governing reference document, `ACCESS-CONTROL.md` — per-role
read/write rights (read is universal; write is advisory except
reconciliation, INV-21, and the INV-16 active-user floor) and the
conditions under which the agent may sign a write as the `*.catalyst`
pointer's `created_by` identity without asking. Same treatment as
`CODE-OF-CONDUCT.md`/`Rules-of-Rules.md`: copied verbatim (no
project-specific customization), created if missing, refreshed on
`/sync-framework` whenever this framework version actually changes its
content.

## Steps

1. Copy `development-framework/ACCESS-CONTROL.md` to
   `.criterion/ACCESS-CONTROL.md` if it doesn't already exist.
2. Link it from the deployed root `README.md`'s discoverability section,
   alongside `CODE-OF-CONDUCT.md`.
3. Journal the migration (`action: "create"`, `intent` describing the new
   doc, `files` covering the created path by content hash) — never rewrite
   the journal itself (INV-17).
4. Report the result.

Past migration docs and their rows in `migrations.md` describe shapes as
they were named at the time and are not rewritten by this migration.

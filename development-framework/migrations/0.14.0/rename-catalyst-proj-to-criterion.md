# Migration: `.catalyst-proj/` and the repoed-sync mechanism renamed to "criterion"

> Target version: `0.14.0` — this is the migration that produces the
> shape `0.14.0` introduced. Triggered by `SYNCHRONIZE.md`'s
> "Version-specific one-time migrations" (`From 0.13.0`). Applies once,
> the first time a deployment's `version.txt` advances past `0.13.0` to
> `0.14.0` or later. Never re-run on a later sync once applied.

## What changed

The working-copy directory name and the whole repoed-sync mechanism
around it (previously codenamed `thingamabob`) are renamed to
"criterion" — the framework's permanent name for this concept, and the
source of truth for any project sharing a catalyst deployment across
contributors. The full mechanism is unchanged; only the names are:

| Old | New |
|---|---|
| `.catalyst-proj/` (working-copy directory, and as a branch suffix `<name>.catalyst-proj`) | `.criterion/` |
| `<project-name>-catalyst-proj` (backing-repo naming convention) | `<project-name>-criterion` |
| `/thingamabob` command | `/criterion` |
| `thingamabob` (canonical branch) | `criterion` |
| `thingamabob_branch` field | `criterion_branch` |

`<app-name>.catalyst`'s own filename/extension, and the `catalyst_repo`/
`catalyst_repo_url`/`repoed`/`created_by` field names, are unaffected.

## Steps

1. Rename the working-copy directory in place, wherever it's rooted
   (agent-owned space, or the in-project fallback) — `.catalyst-proj/` →
   `.criterion/`. A plain directory move; its own `.git` history (if
   repoed) is preserved.
2. Rewrite `<app-name>.catalyst` at the project root: `agent-source` to
   the new path, `thingamabob_branch` → `criterion_branch` (same value).
   If `repoed: true`, also update `catalyst_repo`/`catalyst_repo_url` to
   the renamed backing repo once it's renamed (step 4 below) — until
   then these keep their old values, since the actual repo hasn't moved
   yet.
3. Inside the working copy, `DEPLOYMENT.md`: same field rename
   (`thingamabob_branch` → `criterion_branch`), plus append one new
   dated history bullet noting the rename — never edit or remove the
   existing history bullets.
4. If `repoed: true`: rename the backing repository and its canonical
   branch to match (`<name>` → `criterion`-based naming per the table
   above) — externally-visible and hard-to-reverse, so confirm with the
   user before doing it, same tier of confirmation `/criterion create`'s
   own repo-creation step already requires. Update the contributor's
   local remote/branch tracking to match once done.
5. Journal the migration (`action: "update"`, `intent` describing the
   rename, one entry covering every file actually rewritten) — never
   rewrite the journal itself (INV-17).
6. Report the result.

Past migration docs (`0.11.0/`, `0.12.0/`, `0.13.0/`) and their rows in
`migrations.md` describe shapes as they were named at the time and are
not rewritten by this migration — they remain accurate historical
record of what each prior version changed.

# Migration: `TEST-` entity

> Target version: `0.30.0` — this is the migration that produces the
> shape `0.30.0` introduces. Triggered by `SYNCHRONIZE.md`'s
> "Version-specific one-time migrations" (`From 0.29.0`). Applies once,
> the first time a deployment's `version.txt` advances past `0.29.0` to
> `0.30.0` or later. Never re-run on a later sync once applied.

## What changed

New core entity, `TEST-NNNNNN` (`templates/test.template.md`,
`Rules-of-Rules.md` §22, `INVARIANTS.md` INV-28): a fourth member of the
`(BUG|REQ|HK|TEST)` development-artifact format — unlike `STEP-`/`FEAT-`/
`RM-`, **not** exempt from `rules-of-development.md` §1 ("no development
without a targeted rule"): a test always carries its own `Targets`/
`Domain`, vetted the same way a bug or requirement is. On top of that, a
test may independently name `(0,n)` requirements and `(0,n)` steps it
verifies — both optional, neither implying the other; a test naming
neither is valid as long as it still carries `Targets`/`Domain`. Own
top-level `tests/` folder, full INV-20 treatment. New command,
`/create-test`.

Every requirement and every step also gains a **`Tests`** field: the
list of `TEST-NNNNNN` that name it, in creation order — the mirror image
of a requirement's existing `Steps` field. `/create-test` populates both
sides in one action.

| Old | New |
|---|---|
| Development-artifact format: `(BUG\|REQ\|HK)-(NNNNNN)`. | `(BUG\|REQ\|HK\|TEST)-(NNNNNN)`. |
| No `tests/` folder. | `tests/<TEST-NNNNNN>-<summary>.md`, one file per test, indexed in `tests/tests.md`. |
| Requirement field table: `ID`/`Name`/`Filename`/`Status`/`Opened`/`Targets`/`Domain`/`Feature`/`Steps`/`Signed-off-by`. | Same, plus `Tests` (between `Steps` and `Signed-off-by`). |
| Step field table: `ID`/`Name`/`Filename`/`Requirement`/`Status`/`Opened`/`Closed`/`Signed-off-by`. | Same, plus `Tests` (between `Closed` and `Signed-off-by`). |

## Steps

1. **Deploy the `tests/` folder** if it doesn't already exist: `templates/`
   (`README.md`, `templates-test.md` seeded with a `v1` row,
   `TEMPLATE-TEST-v1.md` copied from this framework's
   `templates/test.template.md`), the folder's own `README.md`, and an
   empty `tests.md` index (empty is fine — no deployment has real test
   coverage retroactively reconstructable as `TEST-` records).
2. **Create `.criterion/definitions/test.md`** if missing, from this
   framework's current latest `definitions/test/DEFINITION-TEST-v1.md`
   (INV-23's "create if missing" logic, applied to a type introduced
   after the project's last sync).
3. **Add the `Tests` field to every existing requirement and every
   existing step.** For each file under `requirements/`, insert a
   `**Tests**` row into its field table, immediately after `**Steps**`.
   For each file under `steps/`, insert a `**Tests**` row immediately
   after `**Closed**`. Leave both empty (`*(none yet)*`) — **do not
   retroactively invent `TEST-NNNNNN` records for verification already
   done before this migration ran.** The field simply starts empty and
   gets populated going forward, the same posture the `0.29.0` migration
   took for a requirement's `Steps` field.
4. **Refresh the requirement and step template(s)**
   (`requirements/templates/`, `steps/templates/`) to the current
   `templates/requirements.template.md`/`templates/step.template.md`
   shape (new version, per `Rules-of-Rules.md` §15 — never edit a
   superseded template file in place) if this deployment's templates
   predate the `Tests` field.
5. **Add `/create-test`** to the deployed command set: create
   `.claude/commands/create-test.md` (following
   `templates/slash-command.template.md`) and the matching task in
   `.criterion/Taskfile.common.yml`, same as any other missing §4 command.
6. Journal the migration (`action: "create"`, `intent` describing the new
   entity type and the `Tests` back-reference field, `files` covering
   every path actually touched by content hash) — never rewrite the
   journal itself (INV-17).
7. Report the result.

## Rollback

Steps 1–2 and 5 are pure additions (new folder, new definition, new
command) — safe to delete if this needs undoing, since nothing
pre-existing was touched. Step 3 only adds a field to existing
requirements/steps (their other content is untouched) — safe to remove
the added `Tests` rows.

Past migration docs and their rows in `migrations.md` describe shapes as
they were named at the time and are not rewritten by this migration.

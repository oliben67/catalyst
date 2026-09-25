# Migration: a step's parent widens to requirement or bug

> Target version: `0.31.0` — this is the migration that produces the
> shape `0.31.0` introduces. Triggered by `SYNCHRONIZE.md`'s
> "Version-specific one-time migrations" (`From 0.30.0`). Applies once,
> the first time a deployment's `version.txt` advances past `0.30.0` to
> `0.31.0` or later. Never re-run on a later sync once applied.

## What changed

A `STEP-NNNNNN`'s single required parent field is renamed `Requirement`
→ `Parent`, and its accepted value widens from "exactly one
`REQ-NNNNNN`" to "exactly one `REQ-NNNNNN` **or** `BUG-NNNNNN`" — a unit
of implementation work can now be recorded against a bug fix the same
way it already could against a requirement. The bug template
(`templates/bug.template.md`) gains its own `Steps` field, the same
back-reference list a requirement already carries, and a bug is now
subject to the same "not closeable until every listed step is `done`/
`abandoned`" gate a requirement already had (`rules-of-development.md`
§7). `/create-step` accepts either kind of id.

| Old | New |
|---|---|
| Step field table: `ID`/`Name`/`Filename`/`Requirement`/`Status`/`Opened`/`Closed`/`Tests`/`Signed-off-by`. `Requirement` names exactly one `REQ-NNNNNN`. | Same, `Requirement` renamed `Parent`, naming exactly one `REQ-NNNNNN` **or** `BUG-NNNNNN`. |
| Bug field table: no `Steps` field. | Bug field table gains `Steps` (same position/semantics as the requirement's). |
| `/create-step <REQ-id>` — refuses unless `<REQ-id>` resolves under `requirements/`. | `/create-step <REQ-id\|BUG-id>` — refuses unless it resolves under `requirements/` or `development/bugs/`. |

## Steps

1. **Rename the field on every existing step file.** For each file under
   `steps/`, rename its `**Requirement**` row to `**Parent**` — the
   value (a `REQ-NNNNNN`) doesn't change; only the label does, since
   every step that already exists targets a requirement (this migration
   doesn't retroactively invent a bug parent for anything).
2. **Add the `Steps` field to every existing bug.** For each file under
   `development/bugs/`, insert a `**Steps**` row into its field table,
   immediately after `**Area**`. Leave it empty (`*(none yet)*`) —
   **do not retroactively invent `STEP-NNNNNN` records for work already
   done before this migration ran.**
3. **Refresh the step and bug template(s)** (`steps/templates/`,
   `development/bugs/templates/`) to the current
   `templates/step.template.md`/`templates/bug.template.md` shape (new
   version, per `Rules-of-Rules.md` §15 — never edit a superseded
   template file in place) if this deployment's templates predate this
   change.
4. **Update `/create-step`'s deployed command file**
   (`.claude/commands/create-step.md`) and its Taskfile task to the new
   `<REQ-id|BUG-id>` argument shape and the widened resolution check.
5. **Re-sync `CODE-OF-CONDUCT.md`/`Rules-of-Rules.md`** (the ordinary
   template-refresh path) so their own copies of the `Requirement` →
   `Parent` rename and the "steps sit below a requirement or a bug"
   framing match the current templates.
6. Journal the migration (`action: "update"`, `intent` describing the
   field rename and the bug-parent widening, `files` covering every path
   actually touched by content hash) — never rewrite the journal itself
   (INV-17).
7. Report the result.

## Rollback

Step 1 only renames a field label on existing files (the value is
untouched) — safe to rename back. Step 2 only adds a field to existing
bugs (their other content is untouched) — safe to remove the added
`Steps` rows. Steps 3–5 are template/command refreshes — safe to revert
to the prior version file/command content.

Past migration docs and their rows in `migrations.md` describe shapes as
they were named at the time and are not rewritten by this migration.

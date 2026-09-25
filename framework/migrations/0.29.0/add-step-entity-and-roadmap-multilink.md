# Migration: `STEP-` entity + roadmap multi-link

> Target version: `0.29.0` — this is the migration that produces the
> shape `0.29.0` introduces. Triggered by `SYNCHRONIZE.md`'s
> "Version-specific one-time migrations" (`From 0.28.0`). Applies once,
> the first time a deployment's `version.txt` advances past `0.28.0` to
> `0.29.0` or later. Never re-run on a later sync once applied.

## What changed

- New core entity, `STEP-NNNNNN` (`templates/step.template.md`,
  `Rules-of-Rules.md` §21, `INVARIANTS.md` INV-27): records one concrete
  unit of implementation work performed toward a specific `REQ-NNNNNN` —
  files touched, commands run, how it was verified. Always names exactly
  one parent requirement. Exempt from the rule-targeting/conflict-check
  gate the same way `FEAT-`/`RM-` are — it inherits its parent
  requirement's already-vetted rule target. Own top-level `steps/` folder,
  full INV-20 treatment. New command, `/create-step <REQ-id>`.
- Every requirement template/instance gains a **Steps** field: the list
  of `STEP-NNNNNN` ids opened against it, in creation order. A requirement
  isn't closeable as `done` until every listed step is `done` or
  `abandoned`.
- A roadmap row's **`Linked` field generalizes from an implicit single ID
  to an explicit, comma-separated list**: every `FEAT-`/`REQ-NNNNNN`
  currently associated with that row, not just one. `Status` computation
  changes to match: `Done` only once *every* linked `REQ-NNNNNN` is
  `done`; `In progress` once at least one linked `REQ-` isn't yet `done`.

| Old | New |
|---|---|
| No `steps/` folder; a requirement's implementation history lived only in its own prose (`## Design / implementation plan`) or the journal's free-text `intent`. | `steps/<STEP-NNNNNN>-<summary>.md`, one file per unit of work, cross-referenced from its parent requirement's `Steps` field. |
| Requirement field table: `ID`/`Name`/`Filename`/`Status`/`Opened`/`Targets`/`Domain`/`Feature`/`Signed-off-by`. | Same, plus `Steps` (between `Feature` and `Signed-off-by`). |
| Roadmap row `Linked`: implicitly one `FEAT-`/`REQ-NNNNNN`. | Roadmap row `Linked`: comma-separated list of every currently-associated `FEAT-`/`REQ-NNNNNN`. |

## Steps

1. **Deploy the `steps/` folder** if it doesn't already exist: `templates/`
   (`README.md`, `templates-step.md` seeded with a `v1` row,
   `TEMPLATE-STEP-v1.md` copied from this framework's
   `templates/step.template.md`), the folder's own `README.md`, and an
   empty `steps.md` index (empty is fine — no deployment has real
   implementation work retroactively reconstructable as steps).
2. **Create `.criterion/definitions/step.md`** if missing, from this
   framework's current latest `definitions/step/DEFINITION-STEP-v1.md`
   (INV-23's "create if missing" logic, applied to a type introduced
   after the project's last sync).
3. **Add the `Steps` field to every existing requirement.** For each file
   under `requirements/`, insert a `**Steps**` row into its field table,
   immediately after `**Feature**` (or after `**Domain**` if no `Feature`
   row exists). Leave it empty (`*(none yet)*`) — **do not retroactively
   invent `STEP-NNNNNN` records for work already done before this
   migration ran.** A requirement whose implementation predates this
   migration is not required to backfill steps for history it doesn't
   have; the field simply starts empty and gets populated going forward.
4. **Refresh the requirement template(s)** (`requirements/templates/`) to
   the current `templates/requirements.template.md` shape (new version,
   per `Rules-of-Rules.md` §15 — never edit a superseded template file in
   place) if this deployment's template predates the `Steps` field.
5. **Generalize every roadmap file's `Linked` column semantics.** No
   table shape changes (the column already exists) — this is a
   documentation/behavior change, not a structural one. Re-read every
   `development/roadmaps/<name>.md`'s existing `Linked` values: a single
   `FEAT-`/`REQ-NNNNNN` already there is already valid list syntax (a
   one-element list), so **no existing row's data needs rewriting** —
   only future `/show-backlog`/`/create-feature`/`/create-req` runs need
   to know `Linked` can grow past one entry. Refresh the deployed
   `development/roadmaps/templates/TEMPLATE-ROADMAP-vN.md` (new version)
   and this deployment's `CODE-OF-CONDUCT.md`/`Rules-of-Rules.md` (re-sync
   per the ordinary template-refresh path) so `/show-backlog`'s own
   spec reflects the new multi-link `Status` computation.
6. **Add `/create-step`** to the deployed command set: create
   `.claude/commands/create-step.md` (following
   `templates/slash-command.template.md`) and the matching task in
   `.criterion/Taskfile.common.yml`, same as any other missing §4 command.
7. Journal the migration (`action: "create"`, `intent` describing the new
   entity type and the roadmap `Linked` generalization, `files` covering
   every path actually touched by content hash) — never rewrite the
   journal itself (INV-17).
8. Report the result.

## Rollback

Steps 1–2 and 6 are pure additions (new folder, new definition, new
command) — safe to delete if this needs undoing, since nothing
pre-existing was touched. Step 3 only adds a field to existing
requirements (their other content is untouched) — safe to remove the
added `Steps` rows. Step 5 changes no data, only documentation/behavior —
nothing to roll back there beyond reverting the refreshed template/
governing-doc content.

Past migration docs and their rows in `migrations.md` describe shapes as
they were named at the time and are not rewritten by this migration.

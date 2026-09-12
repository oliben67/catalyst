# Migration: role-gated reconciliation

> Target version: `0.22.0` — this is the migration that produces the
> shape `0.22.0` introduced. Triggered by `SYNCHRONIZE.md`'s
> "Version-specific one-time migrations" (`From 0.21.0`). Applies once,
> the first time a deployment's `version.txt` advances past `0.21.0` to
> `0.22.0` or later. Never re-run on a later sync once applied.

## What changed

Every role in `IAM/roles/roles.json` gains a `reconciliation` field:
`full` / `propose` / `none`. `/reconcile` now genuinely enforces it — the
one deliberate exception to `Rules-of-Rules.md` §11's "advisory, not
access control" principle (`INVARIANTS.md` INV-21, §16). A new `propose
<text>` verb lets a `propose`-level actor move a case to `Under Review`
without resolving it.

| Old | New |
|---|---|
| `{"name": ..., "actions": [...]}` | `{"name": ..., "actions": [...], "reconciliation": "full"\|"propose"\|"none"}` |

## Steps

1. For each existing role entry in `IAM/roles/roles.json` with no
   `reconciliation` field, add one:
   - If the role's `name` matches one of this framework's default roles
     (`templates/roles.template.json`), use that role's default:
     `Admin`/`Tech Lead / Architect`/`Release Manager` → `full`;
     `Product Owner`/`Developer`/`Scrum Master / Delivery Lead`/
     `QA / Tester` → `propose`; `Stakeholder` → `none`.
   - Otherwise (a custom, project-added role) — default to `propose`,
     never silently `full`. Ask the user to confirm or adjust it rather
     than guessing for a role this framework doesn't recognize.
2. Leave every other field (`name`, `actions`) exactly as they are —
   this migration only adds the new field.
3. Verify: any currently-`Open`/`Under Review` `RECON-` case is
   unaffected by this migration — the new gating only applies to future
   `/reconcile` invocations, not retroactively to cases already in
   flight.
4. Journal the migration (`action: "update"`, `intent` describing the
   field addition, `files` covering `IAM/roles/roles.json`'s real
   before/after hash) — never rewrite the journal itself (INV-17).
5. Report the result.

Past migration docs and their rows in `migrations.md` describe shapes as
they were named at the time and are not rewritten by this migration.

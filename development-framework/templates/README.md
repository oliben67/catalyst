# Templates

This folder contains the reusable document templates that seed the deployed catalyst framework.

## What lives here

- Artifact templates such as bugs, requirements, house-keeping, and meta-tags
  — these are the rule-linked development-artifact types governed by
  `CODE-OF-CONDUCT.md`.
- [`features.template.md`](features.template.md) — a related but separate,
  **non-rule-linked** template for documenting new/future app functionality
  as an idea or roadmap item. Not measured against a rule; see
  `Rules-of-Rules.md` §9. Opening actual development work for a feature
  still means opening a requirement (`requirements.template.md`), not
  editing the feature entry.
- Work-item templates for epics, stories, tasks, spikes, sprints,
  [`board.template.md`](board.template.md) (Kanban/Scrumban's counterpart
  to sprints — `BOARD-NNNNNN`), and
  [`workflow.template.md`](workflow.template.md) (a process-definition
  document, not a unit of work — `WORKFLOW-NNNNNN`). No `ticket.template.md`
  exists: `tickets/` is a reserved slot a project-management-type plugin
  populates, not a core template — see `Rules-of-Rules.md` §8.
- Rule and domain scaffolding templates used when a project is instantiated
  — `domain.template.md` deploys nested under `rules/domains/`, not as a
  top-level sibling (domains exist only to group rules).
- [`templates-catalog.template.md`](templates-catalog.template.md) — the
  generic catalog every artifact type's `templates/templates-<type>.md`
  is seeded from (`INVARIANTS.md` INV-20): Version | File | Timestamp |
  Notes, one row per template version. This is where the hard rule's
  "timestamped" requirement is actually satisfied — the template files
  themselves carry no date, this table does.
- [`slash-command.template.md`](slash-command.template.md) — the shape
  every deployed `.claude/commands/<name>.md` file follows, one per
  command in `../rules-of-development.template.md` §4. See `CLAUDE.md`'s
  "Slash commands" entry and `INSTANTIATION-GUIDE.md` §1 step 5 — this is
  required as part of instantiation, not an optional extra.
- [`backlog.template.md`](backlog.template.md) — copy to
  `development/BACKLOG.md` on first deploy (`INVARIANTS.md` INV-14). Unlike
  every other template here, never hand-edited afterward — `/show-backlog`
  overwrites it in full on every run.
- [`roadmap.template.md`](roadmap.template.md) — copy to
  `development/roadmaps/templates/TEMPLATE-ROADMAP-v1.md` on first deploy
  (`INVARIANTS.md` INV-15, INV-20), then to `development/roadmaps/<name>.md`
  per named roadmap by `/roadmap-add`. `/roadmap-add`/`-update`/`-merge` add
  or update a roadmap's `RM-NNNNNN` rows from an external file, `/roadmap-
  remove` deletes or retires one, and `/show-backlog` refreshes their
  Status/Linked columns — see `Rules-of-Rules.md` §10.
- [`roles.template.json`](roles.template.json) — copy to
  `IAM/roles/roles.json` on first deploy (`INVARIANTS.md` INV-16), filled
  in with its default agile-role mapping. JSON, not markdown, because it's
  managed by `/role-add`/`/role-modify` rather than hand-edited.
- [`users.template.json`](users.template.json) — copy to
  `IAM/users/users.json` on first deploy (`INVARIANTS.md` INV-16), empty
  array. Managed only by
  `/user-add`/`/user-remove`/`/user-modify`/`/user-assign-role`/`/user-list`
  — see `Rules-of-Rules.md` §11. **Hard requirement:** deployment isn't
  complete until `/user-add` has registered at least one active user.
  `IAM/users/` and `IAM/roles/` each get the same `templates/` treatment
  as every other artifact type (`INVARIANTS.md` INV-20).
- [`journal.template.jsonl`](journal.template.jsonl) — an empty file,
  copied to `development/journal.jsonl` on first deploy (`INVARIANTS.md`
  INV-17). Append-only, one JSON object per line, transaction-log-grade
  (exact before/after `git hash-object -w` content pointers per touched
  file, not just prose) — see `Rules-of-Rules.md` §12 for the full schema
  and the `/journal-restore` point-in-time reconstruction mechanism.
- [`catalyst-pointer.template.json`](catalyst-pointer.template.json) —
  copy to `<app-name>.catalyst` **at the target project's own root**
  (`INVARIANTS.md` INV-6), the one exception to "everything else deploys
  under `.criterion/`": this file is the only catalyst artifact the
  target project's own repo ever tracks. Its `agent-source` field names
  where the real working copy actually lives — agent-owned space if the
  running agent has one, the in-project `.criterion/` (gitignored)
  otherwise. Managed by `/project create`/`remove`/`export`/`import` and
  kept in sync with `.criterion/DEPLOYMENT.md`'s `repoed`/
  `catalyst_repo`/`catalyst_repo_url`/`created_by` — see
  `Rules-of-Rules.md` §14. `criterion_branch` names the current actor's
  chosen push branch once `/criterion create`/`get` asks for one (§13)
  — `null` until then, or once repoed again after `/project remove`.

## How to use this folder

Copy the appropriate template into the matching deployed folder and rename it to the project-specific filename convention used by the framework.

## Related docs

- [../README.md](../README.md)
- [../INSTANTIATION-GUIDE.md](../INSTANTIATION-GUIDE.md)

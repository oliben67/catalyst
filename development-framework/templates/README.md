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
- Workflow templates for epics, stories, tasks, spikes, and sprints.
- Rule and domain scaffolding templates used when a project is instantiated.
- [`slash-command.template.md`](slash-command.template.md) — the shape
  every deployed `.claude/commands/<name>.md` file follows, one per
  command in `../rules-of-development.template.md` §3. See `CLAUDE.md`'s
  "Slash commands" entry and `INSTANTIATION-GUIDE.md` §1 step 5 — this is
  required as part of instantiation, not an optional extra.

## How to use this folder

Copy the appropriate template into the matching deployed folder and rename it to the project-specific filename convention used by the framework.

## Related docs

- [../README.md](../README.md)
- [../INSTANTIATION-GUIDE.md](../INSTANTIATION-GUIDE.md)

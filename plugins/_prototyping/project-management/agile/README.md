# Agile — schema

The artifact-type schema for Scrum/Kanban-style work-item tracking
(`EPIC-`/`STORY-`/`TASK-`/`SPIKE-`/`SPRINT-`/`BOARD-`/`WORKFLOW-`, their
fields, lifecycle, and ID scheme in
[`rules-of-work-items.template.md`](rules-of-work-items.template.md),
seed templates in [`templates/`](templates/)). Not itself deployed or
activated — a `work-items/` folder only ever materializes into a
project when a concrete project-management plugin extends this schema
and is activated.

**No concrete plugin exists yet.** This is schema plus stub commands —
`create-epic.md`, `create-story.md`, `create-task.md`, `create-spike.md`,
`create-sprint.md`, `create-board.md`, `create-workflow.md` — kept here
as the spec a future plugin implements against, not deployed anywhere
(no `.claude/commands/` copy exists). See [`../../README.md`](../../README.md)
for what extending this schema into a real, activatable plugin means.

## Related docs

- `development-framework/INVARIANTS.md` INV-22 (content-contributing
  plugins) — the mechanism a future plugin here would use.

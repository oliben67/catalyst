# Project-management plugins

The plugin type for content-contributing plugins that add work-item
tracking to a deployment (INV-22) — the counterpart to
[`../repository/`](../repository/), matching its shape once a plugin
graduates here. Empty for now: nothing has graduated out of
[`../_prototyping/README.md`](../_prototyping/README.md) yet.

## Where the actual work is happening

[`../_prototyping/project-management/agile/`](../_prototyping/project-management/agile/)
defines the agile artifact-type schema (`EPIC-`/`STORY-`/`TASK-`/etc.) a
future plugin here would extend. No concrete plugin exists yet — this
directory is the reserved slot for when one does, the same way
`repository/catalyst-git` occupies its own type's slot today.

## Rule

Same activation gate as every plugin (`../README.md`): not loaded unless
explicitly activated via `/catalyzer`, requires `README.md` +
`working-contract.md` in its root, and — once something lives here —
its own repository (INV-11), unlike its `_prototyping/` counterpart.

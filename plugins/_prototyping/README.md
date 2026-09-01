# Prototyping

Plugin work that isn't spun out into its own repository yet — both the
shared schema a category of plugin extends, and the concrete,
activatable plugins built against it, while they're still maturing here
together. `INV-11`'s "every plugin has its own repository" doesn't apply
to anything under this directory: a plugin only needs its own repository
once it graduates out of `_prototyping/` into a top-level plugin-type
directory (e.g. `repository/`, the way `catalyst-git` already has).
Until then, everything here — schema and concrete plugin alike — lives
in catalyst's own repository.

## What lives here

One directory per plugin-type category (e.g. `project-management/`).
Inside it, the shared artifact-type schema (ID scheme, fields, lifecycle
rules, seed templates) sits alongside the concrete plugin(s) extending
it, so a plugin can literally be "more pieces of code than anything
else" — schema and implementation developed together — before it's
mature enough to move out on its own.

## How a plugin extends a prototype's schema

A concrete plugin's `working-contract.md` `## Contributes` section names
the prototype schema path(s) it extends. Activation (`/catalyzer
activate`) resolves the artifact-type templates and rule documents
directly from there, not from a copy vendored into the plugin's own
directory — so the schema never drifts between the prototype and a
stale per-plugin copy, even while both still live in this same
repository.

## Categories

- [`project-management/agile/`](project-management/agile/) — Scrum/
  Kanban-style work-item tracking. Schema only for now (ID scheme,
  fields, lifecycle, seed templates) — no concrete, activatable plugin
  exists yet. `work-items/` doesn't deploy into any project until one is
  built here and activated.

## Related docs

- `development-framework/INVARIANTS.md` INV-22 (content-contributing
  plugins) — the activation mechanism this folder feeds.
- [`../README.md`](../README.md), [`../TEMPLATE-WORKING-CONTRACT.md`](../TEMPLATE-WORKING-CONTRACT.md)

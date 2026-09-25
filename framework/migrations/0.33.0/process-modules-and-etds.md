# Migration 0.33.0: Process Modules & Entity Type Definitions (ETDs)

> Apply this migration when synchronizing a deployed framework whose
> `version.txt` is being advanced to `0.33.0` or later. See
> `SYNCHRONIZE.md` for the full synchronization procedure.

This migration introduces **Catalyst Process Modules** and **Entity Type Definitions (ETDs)**, splitting framework core engine mechanics from specific domain concepts.

## What changed

1. **Module Architecture (`MODULE-SPECIFICATION.md`):** Process workflows are now encapsulated into pluggable modules residing under `modules/<module-id>/`.
2. **Default Bundled Module (`software-engineering`):** All existing entity types (`BUG`, `REQ`, `HK`, `TEST`, `STEP`, `FEAT`, `RM`, `WORKFLOW`, `RECON`), document templates, and slash commands are packaged into the default `software-engineering` process module.
3. **Project Pointer (`*.catalyst`):** Added optional `"module": "software-engineering"` field to project pointers. If omitted, the engine defaults to `software-engineering` with complete backward compatibility.

## Steps for deployed projects

1. **Copy Module Specifications:** Seed `.criterion/modules/software-engineering/` from `framework/modules/software-engineering/`.
2. **Update Project Pointer:** Add `"module": "software-engineering"` to `<app-name>.catalyst`.
3. **Update Version File:** Update `.criterion/version.txt` to `0.33.0`.

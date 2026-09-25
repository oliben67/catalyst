# `reconciliation` — entity definition (v1)

| Field | Value |
|---|---|
| **Entity type** | `reconciliation` |
| **Version** | 1 |

## Description

A `RECON-NNNNNN` case records two diverging versions of an existing entity that
need resolving — never a unit of work with its own acceptance criteria. Opened
automatically when `/criterion push`'s vet+merge step can't cleanly reconcile
two versions of the same artifact (a git-level conflict, a vetting-flagged
semantic clash, or a rights mismatch), or manually, and closed via `/reconcile`
(accept / accept with edits / reject). Lives in `reconciliations/`.

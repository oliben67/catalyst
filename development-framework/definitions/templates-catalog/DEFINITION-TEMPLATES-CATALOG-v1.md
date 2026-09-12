# `templates-catalog` — entity definition (v1)

| Field | Value |
|---|---|
| **Entity type** | `templates-catalog` |
| **Version** | 1 |

## Description

A templates catalog (`<type-dir>/templates/templates-<type>.md`) is the
versioned index of one artifact type's own instance template — a table of every
`TEMPLATE-<TYPE>-vN.md` that has ever existed for that type, each row
timestamped and append-only. It's how INV-20's "versioned, catalogued
templates/ subdirectory" requirement is satisfied for every artifact type.

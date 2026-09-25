# `meta-tag` — entity definition (v1)

| Field | Value |
|---|---|
| **Entity type** | `meta-tag` |
| **Version** | 1 |

## Description

A meta-tag is a lightweight, standalone annotation attached to an existing
artifact without editing that artifact's own file — a comment, a version
marker, or a link-to reference, stored as `tag-<key>-<artefact-id>` under
`development/meta-tags/`. Created via `/meta-tag`, it records one key/value
pair plus a short description of why the tag was added.

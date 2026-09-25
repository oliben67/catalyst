# `roadmap` — entity definition (v1)

| Field | Value |
|---|---|
| **Entity type** | `roadmap` |
| **Version** | 1 |

## Description

A named roadmap file (`development/roadmaps/<name>.md`) holds a table of `RM-
NNNNNN` rows — externally-sourced product ideas ingested via `/roadmap-add`,
kept current via `/roadmap-update`/`/roadmap-merge`, with `Status`/`Linked`
columns refreshed by `/show-backlog` as rows get triaged into real
`FEAT-`/`REQ-` work. Unlike every other artifact type, a roadmap file isn't
filled in once by hand — it's a living, externally-fed table, registered in
`development/roadmaps/roadmaps.md`.

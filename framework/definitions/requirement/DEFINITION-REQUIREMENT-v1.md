# `requirement` — entity definition (v1)

| Field | Value |
|---|---|
| **Entity type** | `requirement` |
| **Version** | 1 |

## Description

A `REQ-NNNNNN` document captures a concrete, application-bound requirement
derived from the project's rule documents, or opened to introduce a new
feature. It is vetted against every existing rule before being opened, always
carries a Domain, and always targets or proposes one or more rules — the main
input for tests and acceptance criteria. Lives in the `requirements/` root
folder, registered in `requirements.md`.

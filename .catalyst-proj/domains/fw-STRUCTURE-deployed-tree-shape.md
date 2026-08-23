# `STRUCTURE` — Structural invariants

**Document:** rules/framework/fw-framework-rules.md
**Defined:** 2026-08-23
**Parent:** none
**Sub-domains:** none

Rules in this domain do not supersede, amend, or contradict any rule in
another domain unless explicitly stated below against that rule's ID.

## Scope

The shape a deployed `.catalyst-proj/` tree must have: the chain
invariant, the fixed deploy directory, descriptive naming, no-orphan
indexing, the requirement-vs-bug distinction for new work, and the
persisted backlog/roadmap/user-registry artifacts. Unlike `BEHAVIOR`,
most of this domain is machine-checkable from a tree snapshot —
`scripts/check_deployment.py` is the enforcement layer.

## Relationship to other domains

None.

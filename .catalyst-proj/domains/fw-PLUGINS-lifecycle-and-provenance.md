# `PLUGINS` — Plugin system invariants

**Document:** rules/framework/fw-framework-rules.md
**Defined:** 2026-08-23
**Parent:** none
**Sub-domains:** none

Rules in this domain do not supersede, amend, or contradict any rule in
another domain unless explicitly stated below against that rule's ID.

## Scope

The plugin lifecycle: activation gating, per-plugin repository
provenance, working-contract stability, and the boundary between a
plugin's runtime target (the deployed project) and catalyst's own
repository or a plugin's installation directory.
`scripts/check_plugins.py` and `scripts/check_plugin_contracts.py` are
the enforcement layer for the structural pieces of this domain; full
activation-gating and the deployment-vs-framework operating boundary are
behavioural and not machine-checked from a tree snapshot.

## Relationship to other domains

None.

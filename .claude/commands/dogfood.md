---
description: Vet the current deployment against its own rules (check-rules + a four-eyes drift check); reports, never fixes
argument-hint: (no arguments)
---

Dogfood the current instance. Full spec:
`.catalyst-proj/CODE-OF-CONDUCT.md` §4.
Input: $ARGUMENTS

1. Run `/check-rules` against the current `.catalyst-proj/` state.
2. Spawn two independent four-eyes sub-agents (no shared context) that
   each separately evaluate whether the deployment's actual state (code,
   tests, docs) still matches what its own rules claim: for a ✅ rule,
   does the cited `file:line` still hold with real test coverage; for a
   ⚠️/❌ rule, is that status still accurate rather than stale.
3. Reconcile the two passes. Where they disagree, surface the
   disagreement rather than silently picking one.
4. Report every drift found. Never fix anything automatically — that's
   the user's or a follow-up command's call.

This is the exact check `/thingamabob push` runs against an incoming
branch before merging (`.catalyst-proj/rules/Rules-of-Rules.md` §13).
Running it here standalone never touches `thingamabob` or any branch.

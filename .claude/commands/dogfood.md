---
description: Vet catalyst's own repository against its own rules (check-rules + a four-eyes drift check); reports, never fixes. Catalyst-development-only.
argument-hint: (no arguments)
---

Dogfood catalyst's own repository. Full spec:
`development-framework/rules-of-rules.template.md` §13 ("`/dogfood` is
catalyst-development-only").
Input: $ARGUMENTS

**This command is not part of the catalyst framework's deployed command
set** — it's never listed in `CODE-OF-CONDUCT.md` §4, and
`INSTANTIATION-GUIDE.md`/`SYNCHRONIZE.md` never materialize it into a
deployed project. It exists only here, in catalyst's own repository, for
verifying catalyst's own rules against catalyst's own actual state.

1. Run `scripts/check_deployment.py`/`scripts/check_plugins.py`/
   `scripts/check_plugin_contracts.py` and the pytest suite against
   `.catalyst-proj/` — the structural half of `/check-rules`.
2. Spawn two independent four-eyes sub-agents (no shared context) that
   each separately evaluate whether catalyst's actual state (code, tests,
   docs) still matches what `.catalyst-proj/rules/framework/fw-framework-rules.md`
   claims: for a ✅ rule, does the cited `file:line` still hold with real
   test coverage; for a ⚠️/❌ rule, is that status still accurate rather
   than stale.
3. Reconcile the two passes. Where they disagree, surface the
   disagreement rather than silently picking one.
4. Report every drift found. Never fix anything automatically — that's
   the user's or a follow-up command's call.
5. If this run ends clean, or ends with fixes applied and reverified,
   **offer** to sync — `/thingamabob push` if this deployment is already
   repoed, `/thingamabob create` otherwise. Never run either
   automatically; offer it and proceed only once the user says to.

This is the same procedure `/thingamabob push` runs inline against an
incoming branch before merging, in any repoed deployment
(`development-framework/rules-of-rules.template.md` §13) — described
there directly rather than depending on this command, since this command
doesn't exist outside catalyst's own repo. Running `/dogfood` here
standalone never touches `thingamabob` or any branch on its own — step 5
above only ever *offers* that as a next step, never triggers it.

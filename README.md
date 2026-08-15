# catalyst

**catalyst is a portable, model-agnostic development framework that a coding
agent installs into a project and then works within.** It gives any codebase a
single, traceable structure for its rules, its development work, and its agile
process — so every change traces down to a documented rule, and every rule back
up to the work that exercises it.

At its center is a four-layer chain, each layer subordinate to the one below it:

```
Work items    EPIC ─▶ STORY ─▶ TASK / SPIKE / SPRINT   (agile process layer)
                        ▼
Dev artifacts        REQ- / BUG- / HK- / TAG-          (rule-linked work)
                        ▼
Rules            (prefix)-(DOMAIN)-(NNN)                (documented behavior)
                        ▼
Rules of rules   the meta-rules governing all of the above
```

The chain's one invariant: **no work happens without a traceable link down to a
documented rule**, and every document, domain, and rule carries a stable,
permanent, never-reused ID. That is what makes both "why does this code do X"
and "what rule does this ticket satisfy" answerable by following IDs in either
direction, indefinitely.

catalyst is built to run under **any** capable coding agent — Claude Code, a
generic tool-using agent, or a system-prompted model — by detecting what the
running agent can do and falling back when a capability is absent. It installs
itself into a fixed deploy target (`.catalyst-proj/`) on first load, and stays
grounded across long runs through explicit anti-drift mechanisms (an invariants
file, deployment ledgers, and a re-ground cadence) rather than trusting the
agent to simply remember.

`BOOTSTRAP.md` is the single source of truth. Everything else here either points
at it or extends it.

## Which prompt to load

Choose the prompt file that matches the agent you are running, and load only
that file.

- `CLAUDE.md` — running Claude Code.
- `AGENT.md` — running a generic agent workflow.
- `SYSTEM.md` — running the system-level prompt.

All three load `BOOTSTRAP.md`, the single portable install core. Open the
selected file and follow its instructions from top to bottom.

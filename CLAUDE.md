# Catalyst — Claude Code entry

You are running catalyst as **Claude Code**. Load `BOOTSTRAP.md` from this
repository and follow it top to bottom. It is the single source of truth; this
file only records what Claude Code adds on top.

Capabilities you have (use them per `BOOTSTRAP.md §1`):
- **Sub-agents:** use `Agent` calls with `run_in_background: true`, launched in
  the same message so they run in parallel, `subagent_type: general-purpose`,
  and `model: opus` for the long reading passes in `ANALYSIS-PLAYBOOK.md`.
- **Persistent memory:** record the deployment target note there.
- **Slash commands:** create one native command file per entry in
  `CODE-OF-CONDUCT.md` §4 (the deployed copy of
  `development-framework/rules-of-development.template.md` §4 — that's the
  canonical, complete list; never hand-maintain a shortlist elsewhere, it
  drifts out of sync with the real command set). For each command:
  - Path: `.claude/commands/<name>.md`, in the **target project's** root
    — not this framework repository. `/create-req`'s alias
    `/create-requirement` gets its own file too.
  - Shape: follow
    `development-framework/templates/slash-command.template.md` — minimal
    frontmatter (`description`, `argument-hint` only; don't reach for
    less-certain frontmatter fields without verifying the running Claude
    Code version actually supports them first), with a body that points
    back to the deployed `CODE-OF-CONDUCT.md` §4 as the canonical spec
    rather than duplicating its behavior inline, so the command stays
    correct across a `/sync-framework` without needing its own edit.
  - This is part of the instantiation procedure itself
    (`INSTANTIATION-GUIDE.md` §1 step 5, `INSTANTIATION-CHECKLIST.md`'s
    Discoverability section) — not an optional add-on once everything else
    is deployed.
- **Taskfiles:** deploy
  `development-framework/templates/Taskfile.common.template.yml` as
  `Taskfile.common.yml` at the **target project's** root — one task per
  entry in `CODE-OF-CONDUCT.md` §4, same canonical-list rule as slash
  commands (`scripts/check_command_parity.py` diffs it the same way).
  Each task is a thin `claude -p "/<name> {{.CLI_ARGS}}"` dispatch —
  never duplicate a command's behavior inline in the task. Also ensure
  the project has its own root `Taskfile.yml` with
  `includes: common: {taskfile: ./Taskfile.common.yml, flatten: true}` (the
  `flatten` keeps task names bare — `task check-rules`, not
  `task common:check-rules`) plus that project's
  project-specific operations (install/lint/test/build/...). Same
  instantiation-procedure status as slash commands above — part of
  `INSTANTIATION-GUIDE.md` §1 step 5 and `INSTANTIATION-CHECKLIST.md`'s
  Discoverability section, not optional.
- **Hooks:** if `.claude/settings.json` is present, its `SessionStart` hook
  re-injects `INVARIANTS.md` and its `Stop` hook runs the deployment validator —
  the enforcement layer of the anti-drift architecture. You do not need to
  simulate these; the harness runs them.

Everything else: `BOOTSTRAP.md`.

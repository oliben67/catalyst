# Deployment Ledger: deploy-catalyst-self   (updated: 2026-08-23)

State file for a catalyst install/analysis run. The agent reads this before each
unit of work and writes it after, so progress survives context loss and any
drift is visible against a written record. Deployed to
`.catalyst-proj/.ledger/deploy-catalyst-self.todo.md` in this repo.

## Resolved mode (from BOOTSTRAP.md §1)
- Sub-agents: sequential-fallback (mechanical deploy, not an analysis pass)
- Memory: memory-tool
- Slash commands: native (.claude/commands/*.md files)

## Items
- [x] done — INVARIANTS.md, INSTANTIATION-GUIDE.md, INSTANTIATION-CHECKLIST.md re-read this session
- [x] done — Path chosen: retrofit (existing scripts/tests/process to extract rules from), not greenfield
- [x] done — Project name resolved: "catalyst" (repo name, no dev-instructions.yaml present)
- [x] done — Rule document(s)/prefixes chosen: one doc, prefix `fw` (framework), seam = the whole framework repo
- [x] done — Skeleton directories created under `.catalyst-proj/`
- [x] done — `CODE-OF-CONDUCT.md` created from rules-of-development.template.md, placeholders resolved
- [x] done — `rules/Rules-of-Rules.md` created from rules-of-rules.template.md, placeholders resolved
- [x] done — Exactly one `rules/TEMPLATE-RULE.md` created
- [x] done — `work-items/rules-of-work-items.md` created from its template
- [x] done — Per-type templates copied and renamed `TEMPLATE-<TYPE>.md` (13 files)
- [x] done — Per-type index files created (bugs.md, requirements.md, features.md, house-keeping.md, meta-tags.md, epics.md, stories.md, tasks.md, spikes.md, sprints.md)
- [x] done — `domains/` populated with fw-BEHAVIOR/fw-STRUCTURE/fw-PLUGINS domain files + domains.md index
- [x] done — `features/` created (empty index)
- [x] done — `development/BACKLOG.md` created, real content (not placeholder) via /show-backlog logic
- [x] done — `development/roadmaps/TEMPLATE-ROADMAP.md` + empty `roadmaps.md` index created (INV-15)
- [x] done — `development/users.json` + `development/roles.json` migrated from repo-root sandbox (INV-16), sandbox removed
- [x] done — First rule document `rules/framework/fw-framework-rules.md` seeded with `## Contents` + `## Known Bugs — Quick Index`, 16 rules retrofitted from INV-1..16 (fw-BEHAVIOR-001..004, fw-STRUCTURE-001..008, fw-PLUGINS-001..004)
- [x] done — Root `README.md` + 5 per-folder READMEs written, linked from root
- [x] done — `version.txt` written to match framework version.txt (0.7.1)
- [x] done — Every documented slash command has a `.claude/commands/<name>.md` file (31 files: 30 documented commands + `create-requirement` alias)
- [x] done — `/show-backlog` run once to populate `development/BACKLOG.md` for real (8 ⚠️ rules surfaced under "Rules with no open work")
- [x] done — `scripts/check_deployment.py` passes against `.catalyst-proj/` (also check_plugins.py, check_plugin_contracts.py, full pytest suite: 61/61)
- [x] done — Deployed tree presented to user; no commit/push yet (INV-4)

## Legend
- [x] done      — completed and verified
- [!] blocked   — cannot proceed; reason follows the em dash; MUST be surfaced
- [ ] pending   — not started

## Re-ground log
- 2026-08-23 — re-read INVARIANTS.md + INSTANTIATION-CHECKLIST.md before starting this deploy

# Instantiation Checklist

The tickable derivative of `INSTANTIATION-GUIDE.md`. Execute catalyst installs by
working *this* list against a deployment ledger (see
`templates/ledger.template.md`), re-reading `INVARIANTS.md` every 5 items. Each
item is atomic and independently verifiable — that is what stops a long install
from drifting. The guide holds the rationale; this holds the checks.

## Preconditions
- [ ] `INVARIANTS.md` read this session
- [ ] Capabilities resolved and fallbacks chosen (`BOOTSTRAP.md §1`); mode stated
- [ ] Confirmed this is a first load ⇒ install now (INV-2)
- [ ] Path chosen: greenfield — no code yet (`INSTANTIATION-GUIDE.md §3`) /
      retrofit — existing code, no rules yet (`§4`) / neither, skeleton only

## Greenfield path (only if chosen above, `INSTANTIATION-GUIDE.md §3`)
- [ ] Dedicated dev-environment rule document + prefix picked (e.g. `env`),
      added to the rule document list
- [ ] Decision areas worked with the user: runtime/language, dependency
      policy, code style, testing, CI/CD, local dev environment, repo layout
      (skip/add per project)
- [ ] Each area's `domains/<prefix>-<CODE>-<short-description>.md` created
      before its rule bullets (per `Rules-of-Rules.md` §7)
- [ ] Each rule implemented in the same pass (real config files created:
      package manifest, linter config, CI workflow, devcontainer, etc.)
- [ ] Each rule's "tested" bar met — tool/CI runs clean against the scaffold
- [ ] `{{TEST_LOCATIONS}}` for `Rules-of-Rules.md` §2 resolved from the
      testing decision

## Discover
- [ ] `dev-instructions.yaml` located, or user asked for the project name
- [ ] Project `name` resolved (defaults to target repo name)
- [ ] Optional `layout` override read, or default layout selected
- [ ] Rule document(s) and short lowercase prefixes chosen per project seams

## Deploy skeleton (into `.catalyst-proj/`, INV-6)
- [ ] `CODE-OF-CONDUCT.md` created from `rules-of-development.template.md`
- [ ] `rules/Rules-of-Rules.md` created from `rules-of-rules.template.md`
- [ ] Exactly one `rules/TEMPLATE-RULE.md` created; none in rule-type dirs (INV-8)
- [ ] `work-items/rules-of-work-items.md` created from its template
- [ ] Per-type templates copied and renamed `TEMPLATE-<TYPE>.md`
- [ ] Per-type index files created (`bugs.md`, `requirements.md`, `features.md`,
      `house-keeping.md`, `meta-tags.md`, `epics.md`, `stories.md`, `tasks.md`,
      `spikes.md`, `sprints.md`)
- [ ] `domains/` created at root (empty index allowed)
- [ ] `features/` created at root, alongside `requirements/`
- [ ] `development/BACKLOG.md` created from `templates/backlog.template.md`
      (INV-14) — a hard requirement, not one of the optional-per-project
      artifact templates above
- [ ] `development/roadmaps/TEMPLATE-ROADMAP.md` created from
      `templates/roadmap.template.md`, and an empty
      `development/roadmaps/roadmaps.md` index created (INV-15) — the
      folder/index are a hard requirement, same tier as `features/`;
      individual named roadmaps are created later via `/roadmap-add`
- [ ] `development/roles.json` created from `templates/roles.template.json`,
      filled in with its default agile-role mapping (INV-16)
- [ ] `development/users.json` created from `templates/users.template.json`,
      empty array (INV-16)
- [ ] `/user-add` run for at least one person — deployment is not
      complete with zero active users (INV-16, hard rule, stricter than
      every other on-demand artifact)

## Seed content
- [ ] First rule document(s) created with `## Contents` + `## Known Bugs — Quick
      Index` headings (INV-8)
- [ ] Starter requirement doc created, tied to concrete screens/flows/components
      — on the greenfield path, the dev-environment rule document stands in for
      this since there is no product behavior yet
- [ ] Every seeded rule/domain file follows `<id>-<short-summary>.md` (INV-7)

## Discoverability
- [ ] Root `README.md` written (structure, deploy path, artifact folders)
- [ ] Per-folder `README.md` written for `rules/`, `requirements/`, `features/`,
      `development/`, `work-items/`, and `templates/` where present, linked from root
- [ ] One `.claude/commands/<name>.md` created per command in
      `rules-of-development.template.md` §4 (Claude Code), each following
      `templates/slash-command.template.md` — or the documented fallback
      applied and noted in the deployed `README.md` (other agents), per
      `BOOTSTRAP.md §1`

## Finalize
- [ ] `dev-instructions.yaml` deleted after successful deploy
- [ ] Deployment target recorded (memory tool or `.catalyst-proj/DEPLOYMENT.md`)
- [ ] `version.txt` written to match framework `version.txt`

## Definition of done
- [ ] Every item above `[x]` in the ledger; no silent skips
- [ ] `scripts/check_deployment.py` passes against `.catalyst-proj/`
- [ ] Deployed tree presented to user; **no commit/push yet** (INV-4)
- [ ] On the retrofit path, if no work items exist yet, offered to run
      `ANALYSIS-PLAYBOOK.md` (not applicable on the greenfield path — it reads
      an existing codebase)

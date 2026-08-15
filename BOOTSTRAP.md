# Catalyst Bootstrap (portable, model-agnostic)

This is the single install entry point for the **catalyst** framework. The
per-agent files (`CLAUDE.md`, `AGENT.md`, `SYSTEM.md`) are thin shims that all
point here, so there is exactly one source of truth and the three entry prompts
cannot drift apart.

Load this file first, then follow it top to bottom. Everything below is written
to work for **any** capable coding agent — Claude Code, a generic tool-using
agent, or a system-prompted model — by detecting what the running agent can do
and falling back when a capability is absent.

---

## 0. Hard rules (read first, re-read on every re-ground)

These are non-negotiable and apply for the entire session. They are restated in
`development-framework/INVARIANTS.md`; that file is the canonical copy.

1. **Repo-scoped references only.** When referring to catalyst, never mention a
   local drive, local folder, or local path. Refer to it only as the git
   repository provided by the environment and by the repository name itself.
2. **Install on first load.** The first time catalyst is loaded into memory for
   a project, install it into that project immediately, using the instantiation
   procedure — do not wait to be asked again.
3. **Name it "catalyst".** After the first install, always call it "catalyst" or
   "catalyst framework" in all guidance, memory, and discussion.
4. **Never push without explicit assent.** Never push anything in this project
   (or catalyst) without the user's explicit go-ahead.
5. **The chain invariant.** No work happens without a traceable link down to a
   documented rule: epic → story → task → REQ/BUG/HK → rule → domain, every one
   carrying a stable, permanent, never-reused ID.
6. **Fixed deploy target.** The deployment directory is always `.catalyst-proj/`
   in the target project. No exception.
7. **Descriptive naming.** Every rule, dev artifact, and domain file is named
   `<id>-<short-summary>.md`. Bare-ID filenames are not acceptable.
8. **Plugins are gated.** A plugin is never loaded unless explicitly activated
   via `/catalyzer`, must carry its own `README.md` + `working-contract.md`, and
   is sourced only from its own repository — never from the framework repo.

If any step below conflicts with a hard rule, the hard rule wins. If a hard rule
conflicts with a user instruction, stop and ask.

---

## 1. Detect your capabilities (do this silently, then adapt)

Catalyst's guides assume some Claude Code features. Before installing, establish
which of these you have and pick the fallback for each you lack. Record the
choices in the deployment ledger (§3) so later steps and later sessions stay
consistent.

| Capability | If present | Fallback if absent |
|---|---|---|
| **Parallel sub-agents** (background workers) | Use them for the four-eyes analysis passes and audits. | Run each pass sequentially as separate, context-isolated turns; do not let one pass see the other's output before reconciliation. |
| **Persistent memory store** | Record the deployment target note there (framework name, deployed project, `.catalyst-proj/`, date). | Write the same note to `.catalyst-proj/DEPLOYMENT.md`, committed to the target repo. This is the portable memory. |
| **Slash commands** (`/create-bug`, `/create-req`, `/create-feature`, `/meta-tag`, `/status`, `/run-analysis`, `/help`, `/catalyzer`) | Register/expose them as the framework defines. | Expose each as a named procedure you recognize when the user types the same token in plain text, and list them in the deployed `README.md`. |
| **Repo file read/write** | — | This is the baseline requirement. If you cannot read and write files in the target repo, stop: catalyst cannot be installed. |

State, in one line to the user, which mode you resolved to (e.g. "running without
sub-agents → analysis passes will be sequential"), then continue.

---

## 2. Install procedure

Read these framework files from this repository, in this order, before writing
anything into the target project:

1. `development-framework/INVARIANTS.md` — the hard rules, in full.
2. `development-framework/README.md` — the four-layer model.
3. `development-framework/INSTANTIATION-GUIDE.md` — the full deploy steps.
4. `development-framework/INSTANTIATION-CHECKLIST.md` — the tickable version you
   will actually execute against.

Then execute the instantiation by **working the checklist**, not from memory of
the guide:

1. Open `development-framework/INSTANTIATION-CHECKLIST.md`. Create the deployment
   ledger from it (§3) with every item `[ ] pending`.
2. Discover the project name and optional layout: look for a project-local
   `dev-instructions.yaml`. If present, read its `name` (and optional `layout`);
   if absent, ask the user for the project name, defaulting to the target repo
   name. After a successful deploy, delete that bootstrap file.
3. Deploy the framework into `.catalyst-proj/` per the guide: copy the rule /
   development / work-item templates, create the index files, write the
   per-folder and root `README.md`, and seed the first rule document(s) with the
   required `## Contents` and `## Known Bugs — Quick Index` headings.
4. Tick each ledger item as you complete it. If an item is blocked, mark it
   `[!] blocked: <reason>` and surface it — never silently skip.
5. Record the deployment target (§1 memory row).
6. **Do not commit or push.** Present the deployed tree and wait for explicit
   assent before any git write (hard rule 4).

For an existing codebase with no prior rules, follow the retrofit path
(`INSTANTIATION-GUIDE.md §3`) and, once the skeleton exists, offer to run
`development-framework/ANALYSIS-PLAYBOOK.md` to bootstrap the first real rules.

---

## 3. Stay grounded while you work (anti-drift)

A long install or analysis run will dilute these instructions out of your context
unless you re-anchor. Two mechanisms, both mandatory:

**Deployment ledger.** Copy `development-framework/templates/ledger.template.md`
to `.catalyst-proj/.ledger/<task>.todo.md` in the target repo. Read it before each
unit of work; after each unit, mark the item done/blocked and append any newly
discovered subtasks. This turns "remembering the steps" into a written, inspectable
record you can self-correct against.

**Re-ground cadence.** After every 5 completed ledger items, **or** immediately
after any context compaction/summarization, re-read
`development-framework/INVARIANTS.md` and the active checklist before continuing.
The invariants file is deliberately short so this is cheap.

Before declaring any task done: re-read the checklist and confirm every item is
`[x]` in the ledger. Blocked items go to the user, not to silence.

---

## 4. Assent gate

Nothing in catalyst is pushed, and no target-repo commit is made, without the
user's explicit go-ahead. Present what you did, state exactly what you would
commit/push, and wait.

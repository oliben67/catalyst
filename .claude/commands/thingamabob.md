---
description: Bootstrap/branch (create), join (get), or sync (push) a repoed .catalyst-proj/ deployment through a dedicated repository
argument-hint: create <name> <git-info> | get <repo> <username> | push [--force]
---

Manage a repoed deployment. Full spec: `.catalyst-proj/CODE-OF-CONDUCT.md`
§4, mechanism: `.catalyst-proj/rules/Rules-of-Rules.md` §13.
Input: $ARGUMENTS

**Creating a repo, or force-pushing, is externally-visible and
hard-to-reverse — confirm with the user before doing either, even though
invoking this command already implies intent to push.**

## `create <name> <git-info>`

**First call for this deployment** (`.catalyst-proj/DEPLOYMENT.md` doesn't
show `repoed: true` yet):
1. Check whether `<git-info>` already exists. If it does, register it
   as-is. If it doesn't, confirm with the user, then create it there
   under `<name>`.
2. Write `repoed: true`, `catalyst_repo: <name>`, `catalyst_repo_url:
   <git-info>`, `created_by: <current Signed-off-by actor>` to
   `.catalyst-proj/DEPLOYMENT.md`.
3. Push the current local `.catalyst-proj/` state as the first commit on
   a branch named `thingamabob` — the canonical, master version. Nothing
   is vetted on this first push.
4. Run the **identity migration** (below) for the current actor.
5. Report the result.

**Called again, already repoed:** don't refuse.
- If `<git-info>` matches the already-registered `catalyst_repo_url`,
  this branches: create a new branch off `thingamabob`'s current state,
  named `<name>` in its branch-safe form. No `.catalyst-proj/DEPLOYMENT.md` change.
- If `<git-info>` names a *different* repo, confirm explicitly with the
  user first — this is an unusual second-repo scenario, not ordinary
  branching.

## `get <repo> <username>`

For a user with no local `.catalyst-proj/` copy of an already-repoed
deployment yet — the join path.
1. Validate `<username>` against the branch-safe-name rule (below);
   refuse with a suggested alternative if it doesn't survive
   sanitization uniquely against already-registered users.
2. Download `<repo>`'s `thingamabob` branch content and check out
   `<username>.catalyst-proj` (branch-safe form) from it as this user's
   local `.catalyst-proj/`. Create a `development/users.json` entry for
   them first if one doesn't exist yet.
3. Run the identity migration (below) for this user.
4. Report the result.

## Branch-safe names

Every git ref name derived from a person's identity — `create`'s
branching `<name>`, `get`'s `<username>`, a push branch before a
`git_username` exists — uses that name's branch-safe form: lowercase,
every run of non-`[a-z0-9]` characters collapsed to a single `-`,
leading/trailing `-` trimmed (e.g. "Olivier Steck" → "olivier-steck"). If
two distinct registered names would collapse to the same form, refuse
and ask for a manual override rather than silently colliding branches.

## Identity migration

Part of both `create`'s first call and `get`. Set `git_username` on the
current user's `development/users.json` entry (`git config user.name`,
branch-safe form, for `create`; the given `<username>` for `get`).
Rewrite every existing artifact's `Signed-off-by` field currently naming
this user's old `name` to their new `git_username` — from here on, every
`Signed-off-by`/journal `actor` written for them uses `git_username`,
never `name`. **Never rewrite the journal itself** — entries are
immutable (INV-17), no exception here either; instead append one new
entry (`action: "update"`, `intent` describing the migration) covering
every artifact file actually rewritten.

## `push [--force]`

1. Refuse if `.catalyst-proj/DEPLOYMENT.md` doesn't show `repoed: true` (point to
   `/thingamabob create`).
2. Resolve the current actor's push branch — `<git_username>.catalyst-proj`
   if they have one, otherwise the branch-safe form of `name` — and push
   local `.catalyst-proj/` there (creating the branch on their first
   push).
3. If `--force`: refuse unless the current actor matches `.catalyst-proj/DEPLOYMENT.md`'s
   `created_by`. Otherwise confirm with the user, then overwrite
   `thingamabob` directly from local state and skip everything below.
4. Otherwise:
   a. **Vet**: run `/check-rules` against the merged-in state, plus an
      independent four-eyes sub-agent pass checking whether it still
      matches what its own rules claim. Disagreement between the two
      sub-agents, or a flagged violation, stops here. (This is the exact
      procedure `/dogfood` runs standalone when developing catalyst
      itself — not available here, so described directly instead.)
   b. **Merge**: attempt a normal merge first. Only where that leaves
      conflicts (git-level or vetting-flagged), have a sub-agent propose
      a resolution guided by `Rules-of-Rules.md` §1's conflict-check
      principle — never silently drop either side's rule-compliant
      intent, and stop to ask if a conflict is genuinely irreconcilable.
   c. **Update both branches**: `thingamabob` gets the merge commit; the
      contributor's own branch is fast-forwarded to match.
   d. **Refresh locally**: pull the updated `thingamabob` and overwrite
      the local `.catalyst-proj/` directory and this session's in-memory
      record of it.
5. Report the result.

Not a replacement for `/sync-framework` (that syncs the framework
*template* into a deployment; this syncs one deployment's *own state*
across contributors), and not a substitute for the journal — a
`thingamabob` merge is itself journaled like any other change once it
lands locally.

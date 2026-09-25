---
description: Alias of /sync-kernel — synchronize this deployment with the latest (or a specific) catalyst kernel version
argument-hint: "[latest|<version>] [--force <scope>]"
---

Alias of `/sync-kernel` (its pre-0.35.0 name) — synchronize the deployed
kernel. Full spec:
`.criterion/CODE-OF-CONDUCT.md` §4, this framework's own
`framework/kernel/SYNCHRONIZE.md` (not part of the deployed
project — fetch if not already available this session, referring to it
only by repository name, never a local path).
Input: $ARGUMENTS

1. Resolve the target version: `latest` from the `release` branch, a
   specific version if named, otherwise the currently installed local
   version.
2. Diff the deployed tree against the target version.
3. Respect the root `.frozen` file unless `--force <type>`/`--force
   <item-id>`/`--force all` is given; unfreeze any item actually
   refreshed.
4. Never deactivate an already-active plugin unless its catalog
   `Compatibility` field explicitly excludes the target version.
5. Merge into `plugins/<type>/catalog.md` only — never delete an existing
   row or wipe an installed plugin's directory.
6. Run a four-eyes verification pass (two independent sub-agents) before
   declaring the sync complete; any disagreement blocks completion.

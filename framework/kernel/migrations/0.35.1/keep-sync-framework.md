# Migration 0.35.1: keep `/sync-framework`

> Apply this migration when synchronizing a deployment whose `version.txt`
> is being advanced to `0.35.1` or later. See `SYNCHRONIZE.md` for the full
> synchronization procedure.

`/sync-framework` synchronizes the whole framework (kernel and modules), so it
keeps its name. The `/sync-kernel` command introduced in 0.35.0 is withdrawn.
Everything else in 0.35.0 (the kernel, `kernel_version`, `kernelVersion`)
stands.

## Steps for deployed projects

1. **Command spec.** In `.criterion/CODE-OF-CONDUCT.md` §4, restore the
   `/sync-framework [latest|<version>]` bullet and its behavior paragraph from
   `framework/kernel/rules-of-development.template.md`, dropping any
   `/sync-kernel` wording.
2. **Command files.** Delete `.claude/commands/sync-kernel.md` if present, and
   refresh `sync-framework.md` from the command template so it is no longer an
   alias.
3. **Taskfile.** Remove the `sync-kernel` task from
   `.criterion/Taskfile.common.yml`; keep `sync-framework`.
4. **Version.** Set `.criterion/version.txt` and the pointer's
   `kernel_version` to `0.35.1`.

# Migration: agent-owned working copy + `<app-name>.catalyst` pointer

> Target version: `0.11.0` — this is the migration that produces the
> shape `0.11.0` introduced. Triggered by `SYNCHRONIZE.md`'s
> "Version-specific one-time migrations" (`From 0.10.1`). Applies once,
> the first time a deployment's `version.txt` advances past `0.10.1` to
> `0.11.0` or later, to any project still on the pre-INV-6-revision
> layout (`.catalyst-proj/` built directly inside the target project's
> own tree, no pointer file). Never re-run on a later sync once applied.

## What changed

`.catalyst-proj/` stopped being required to live inside the target
project's own tree. The full mechanism and revised INV-6 are in
`Rules-of-Rules.md` §14 — this entry exists only as the version-boundary
pointer to it, not a duplicate of its content.

## Steps

Follow `Rules-of-Rules.md` §14 "Migration from the pre-pointer-file
model" in full: resolve `agent-source`, move the existing `.catalyst-proj/`
tree there (or recognize the in-project fallback already *is* the target
shape if the running agent has no owned-space concept), write
`<app-name>.catalyst` at the project root, remove the now-empty
`.catalyst-proj/` and its `.gitignore` line if the tree actually
relocated, journal the migration, then report the result.

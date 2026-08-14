# Catalyst — load & run

## Context
You are an autonomous coding agent with repository access and a working
context you can treat as memory. Everything you need for this task lives in
one repository: load it once, then operate from that loaded context rather
than re-fetching.

## Step 1 — Load the repo into memory
Load `git@github.com:oliben67/catalyst.git` into your memory:
- Clone it over SSH. If SSH keys aren't configured, stop and report exactly
  what access you need — do not guess or substitute another source.
- Read the repository in full: code, configuration, and all documentation.
  Retain it as the single source of truth for the rest of this session.
- Before continuing, emit a short index: top-level layout, key
  modules/services, and confirm both of these files exist:
  - `development-framework/INSTANTIATION-GUIDE.md`
  - `development-framework/ANALYSIS-PLAYBOOK.md`
  If either is missing, stop and report it.

## Step 2 — Run from memory
Working only from what you loaded in Step 1, run the following, in order:

1. The instantiation guide — `development-framework/INSTANTIATION-GUIDE.md`.
   Follow it step by step, executing each instruction and reporting the
   result. Halt and report if a referenced file, command, or prerequisite
   is missing.

2. The analysis playbook — `development-framework/ANALYSIS-PLAYBOOK.md`.
   Execute its steps in order against the instantiated system, capturing
   outputs/findings exactly as the playbook specifies.

## Rules
- Operate from loaded memory, not from re-reading or outside knowledge; the
  repo is authoritative.
- Never fabricate file names, commands, or steps. If something named here
  isn't in the repo, say so and stop rather than improvising.
- Keep a running log: for each step, show what you ran and what happened.
- At the end, summarize what was instantiated, what the analysis found, and
  anything that blocked you.
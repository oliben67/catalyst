# Analysis Playbook

A recipe for bootstrapping this framework's rules/sections/bugs against an
**existing** codebase that has no prior rules documentation — the process
actually used to build this project's own
`<resolved-proj-data-target>/rules/` directory (for example
`../.thingamabob/rules/` when `proj-data.target` resolves to
`.thingamabob`). Reusable
on any project once you've picked your rule document(s) and prefixes per
[`INSTANTIATION-GUIDE.md`](INSTANTIATION-GUIDE.md).

## The four-eyes principle

Every extraction pass in this playbook is run **twice, independently**,
by two agents that cannot see each other's output, followed by a
**reconciliation pass** that diffs the two and produces the final
document. Two independent full passes catch what a single pass misses
(an agent that stops early, misreads a code path, or hallucinates a rule
that doesn't exist in the code) far more reliably than one pass plus a
self-review, because the second agent has no anchor bias from the first
agent's framing. This is not the same as the internal "N passes" some of
the individual prompts below already do (a single agent re-reading its
own work) — four-eyes is a second, wholly separate agent.

```
Agent A (independent) ──┐
                         ├──▶ Reconciliation pass ──▶ final document
Agent B (independent) ──┘
```

Use `Agent` tool calls with `run_in_background: true`, launched in the
**same message** so they run in parallel, `subagent_type:
general-purpose`, and (for this kind of long, careful reading task)
`model: opus`. Give A and B the *same* prompt verbatim — the independence
comes from them being separate agent instances with no shared context,
not from varying the instructions.

---

## Recipe 1 — Extract rules for one document (e.g. UI rules)

Run once per **rule category** you split the document by (this project
used four: Validation, Presentation/Display, Calculation, State/Flow), ×2
for four-eyes = 8 parallel agents for a 4-category document. For UI-focused
rule documents, common categories to look for include:

- **Presentation Logic:** Controls how the interface looks and behaves based on user actions or screen states (for example, hiding a submit button until a box is checked).
- **Validation Rules:** Checks whether typed data is correct before letting the user move forward (for example, making sure an email address contains an "@" sign).
- **Interaction/Behavior Rules:** Dictates dynamic screen changes (for example, showing a credit card box only when "Credit Card" is selected as the payment type).
- **Initialization Rules:** Sets default values on a form.

**Prompt template** (send identically to both agents of each pair):

```
Audit this codebase for {{RULE_CATEGORY}} rules — {{one-line definition
of the category, with 2-3 examples, explicitly marked as EXAMPLES not an
exhaustive list}}.

Do THREE separate passes over the code, in this order, then reconcile
them into one list before reporting back:
  1. A keyword/pattern sweep (grep-style) across {{relevant source dirs}}
     for the kind of code that implements this rule category.
  2. A manual walkthrough of every {{dialog/flow/module}}, reading the
     actual logic rather than trusting names/comments.
  3. A cross-check against the test suite ({{test paths}}) — does a test
     exist for each rule you found? Note ones that don't.

For every rule found, report:
  - A short bold name for the rule
  - A one-line description of the actual behavior, citing file:line
  - Status: ✅ working as intended / ⚠️ buggy or incomplete / ❌ documented
    intent but not actually implemented
  - Which functional area of the app it belongs to (e.g. "Gateway
    Management", "Recording") — group your final report by this

Only report what you can point to real code for. Do not report intended/
aspirational behavior as if it were current. Flag anything you're unsure
about explicitly rather than guessing.
```

Launch A and B for each category in one message (background, parallel).
When both return, run **Recipe 3 (reconciliation)** on the pair before
moving to the next category.

## Recipe 2 — Extract rules for a cross-cutting document (e.g. business rules)

Same shape as Recipe 1, but split by **domain area** instead of rule
category (this project used: connectivity/security, data/persistence,
orchestration/lifecycle) rather than Validation/Presentation/Calculation/
Flow, since business rules tend to cluster by subsystem rather than by
what kind of rule they are. Everything else — three passes, four-eyes
pairing, per-rule reporting fields — is identical to Recipe 1.

## Recipe 3 — Reconciliation pass (four-eyes merge)

Run as a single foreground agent (or do it yourself) once both of a
pair's independent reports are in hand.

**Prompt template:**

```
Two independent audits of {{scope}} were run separately; their raw
reports are below. Reconcile them into one final list:

  - A rule both agents found: keep it, merge the best citation/wording
    from each.
  - A rule only one agent found: include it, but verify it yourself
    against the actual code before keeping it — don't take either
    agent's word alone. If you can't verify it, mark it explicitly as
    unverified rather than dropping it silently.
  - A rule where the two agents *disagree* on status (✅ vs ⚠️/❌) or
    on the actual behavior: this is the most important case to catch —
    resolve it by reading the code yourself, and note in the final
    entry that this was a disagreement worth double-checking again
    later.

Output the reconciled list in the target document's existing format
(see {{path to doc if one exists, else the format spec above}}).

--- AGENT A REPORT ---
{{paste}}

--- AGENT B REPORT ---
{{paste}}
```

Repeat Recipe 1/2 + Recipe 3 for each category/area, then merge all
reconciled category lists into the final document, grouped by
functional area (§ per area, not per rule category) — do this merge
yourself; it's editorial work (matching this project's format,
resolving cross-category overlaps), not another audit pass.

## Recipe 4 — Derive sections from a reconciled rule list

Once a document's rules are reconciled and grouped by functional area,
turn each group into a formal section per
[`rules-of-rules.template.md` §6](rules-of-rules.template.md):

```
For each functional-area group in this reconciled rule list, propose:
  - A `##` section heading (the area name)
  - A short SECTION code (3-7 uppercase chars, unique in this document)
  - A one-two sentence Scope statement
  - Whether it plausibly overlaps/conflicts with any other proposed
    section in this same list — if so, say which and why, so a human
    can decide whether to merge them before finalizing.
```

Then mechanically assign IDs (`<prefix>-<CODE>-<NNN>`, in document
order) and create each section's `sections/<prefix>-<CODE>.md` file per
§6 — this step is deterministic, not another agent pass; a short script
or careful manual edit is more reliable than delegating it.

## Recipe 5 — Cross-reference known bugs to rule IDs

Once rules have IDs, existing "Known Bugs" material (or bugs discovered
during Recipe 1/2's audits — an ⚠️/❌ rule *is* a bug) gets linked back:

```
For each bug in this list, find the rule bullet in {{rules doc}} that it
violates (its description should match the ⚠️/❌ rule's behavior almost
exactly, since that's where it came from). Report the bug number and the
matching rule ID. If no matching rule bullet exists, say so explicitly —
that means the rule was never written down and needs to be added first.
```

Then open `BUG-NNNN` docs per
[`rules-of-development.template.md`](rules-of-development.template.md),
citing the matched rule ID in `Targets`.

## Recipe 6 — Meta-rule / process changes

Changes to the process itself (new ID scheme, retirement policy, section
standard — the kind of thing that becomes an `rr-META-NNN`) are
**not** run through four-eyes agent audits — they're a direct design
conversation with whoever owns the process, then written once. Four-eyes
is for *extracting what already exists in code*, where independent
verification catches misreadings; it isn't useful for *deciding what the
process should be*, which has no ground truth to independently verify
against.

---

## Why this shape (lessons from actually running it)

- **Background + parallel, not sequential**: launching a full category's
  A/B pair sequentially wastes the wall-clock four-eyes is supposed to
  buy you for free — always launch both in the same message.
- **Research agents only, never edit agents**: every agent in Recipes
  1/2/4/5 only reads code and returns a report; none of them write files
  directly. Direct file edits (creating the actual `.md` docs, inserting
  IDs, writing section files) are done by the orchestrating
  session/agent after reconciliation, because letting research agents
  also own the merge step is how disagreements get silently
  auto-resolved in whichever agent happened to run last, defeating the
  point of four-eyes.
- **Three-digit `NNN` sequencing must happen after full reconciliation**,
  never per-agent — two independent agents numbering rules `001, 002, …`
  in parallel will collide the moment you merge.
- **Delegation drift**: watch for an agent re-delegating to further
  sub-agents instead of doing the audit itself — this wastes significant
  time with no findings landing. If it happens, tell it directly to stop
  delegating and do the reading itself.

# `FEAT-NNNN` — short title

| Field | Value |
|---|---|
| **ID** | `FEAT-NNNN` |
| **Status** | proposed / approved / in-progress / shipped / rejected |
| **Opened** | YYYY-MM-DD |
| **Targets** | one or more **existing** rule IDs this feature extends or acts on — required if any exist; if none, define first (see New rules proposed) |
| **Domain** | the `DOMAIN` code the targeted/new rule(s) belong to, or `NEW: <CODE>` if this feature also proposes a new domain |
| **Area** | free-text area label |

## Description

What the feature does, from the user's/operator's point of view.

## Rationale

Why — tied to the targeted rule(s): does the current rule under-specify
this case, or does the feature sit entirely outside existing coverage?

## New domain proposed

*(omit if the feature fits an existing domain.)*

Per `rules-of-rules.md` §6: domain-level conflict check performed;
proposed code; the domain file content (`domains/<prefix>-<CODE>.md`)
:this will create, including Scope and Relationship to other domains.

## New rules proposed

*(omit if none.)* List each new rule here **before** implementation
starts, in the exact form it will take once added to the rule document:
proposed ID, rule text, starting status marker (almost always ❌). Run the
`rules-of-rules.md` §1 conflict check first.

## Design / implementation plan

Brief — files touched, approach.

## Acceptance criteria

Concrete, checkable conditions — map 1:1 onto the targeted/new rules.

## Test plan

Per rule targeted or introduced, the specific test that will cover it. A
rule with no test is not "done" regardless of whether the code exists.

## Related

Other `BUG-`/`FEAT-`/`HK-` IDs, or rule IDs.

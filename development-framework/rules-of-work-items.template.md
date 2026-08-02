# Rules of Work Items — template

> Copy to `{{WORK_ITEMS_DIR}}/rules-of-work-items.md` and resolve every
> `{{PLACEHOLDER}}`. See [`INSTANTIATION-GUIDE.md`](INSTANTIATION-GUIDE.md).

Standards for the agile process layer — epics, stories, tasks, spikes,
sprints (or your methodology's equivalents; see the "Agile-methodology
agnostic" note in the framework [`README.md`](README.md)). Sits above
`{{DEV_DIR}}/rules-of-development.md`, which sits above
`{{RULES_DIR}}/rules-of-rules.md`. Work items never bypass that chain.

```
EPIC ─▶ STORY ─▶ TASK           (agile layer — this document)
          │
          ▼
       FEAT- / BUG- / HK-       (rule-linked work)
          │
          ▼
       rule IDs                 (documented behavior)
```

---

## 1. A story is not a substitute for a `FEAT-`/`BUG-` doc

Every `STORY-NNNN` links to exactly one `FEAT-NNNN` (or `BUG-NNNN`). The
`FEAT-`/`BUG-` doc owns rule targets, conflict checks, and new-rule
proposals. The story is the sized, scheduled slice of that same work.

If a story has no `FEAT-`/`BUG-` doc yet, create one before pulling the
story into a sprint/iteration.

## 2. Tasks inherit their parent story's rule target

A `TASK-NNNN` never gets its own rule target — it inherits its parent
story's. If task-level work needs a rule the story doesn't cover, fix the
story/feature doc first rather than letting scope creep in unreviewed.

## 3. Spikes exist to produce rules or estimates, not code

A `SPIKE-NNNN` is time-boxed and never itself "implements" anything. Its
outcome is a new rule proposal (handed to a `FEAT-NNNN`), an
implementation approach, or a go/no-go decision. A spike that ships
production code has stopped being a spike.

## 4. Epics are decomposition, not a fourth rule namespace

An epic names the `DOMAIN` code(s) it spans and groups child stories. It
never targets a rule directly. "Done" means all child stories are done.

## 5. Iteration containers schedule work items; they don't reclassify them

Whatever container your methodology uses (`SPRINT-NNN`, a Kanban column,
etc.) holds `STORY-`/`TASK-`/`SPIKE-` IDs as-is — it never restates
acceptance criteria or rule targets. Retro/review action items that imply
a process change get filed as `HK-NNNN`, not left as an untracked note.

## 6. IDs

Per `rules-of-rules.md` §7: `(EPIC|STORY|TASK|SPIKE)-NNNN` (4 digits),
`SPRINT-NNN` (3 digits), each sequence global within its own type, never
reused.

## 7. Templates

| Type | Folder | Template |
|---|---|---|
| Epic | `epics/` | `templates/epic.template.md` |
| Story | `stories/` | `templates/story.template.md` |
| Task | `tasks/` | `templates/task.template.md` |
| Spike | `spikes/` | `templates/spike.template.md` |
| Sprint | `sprints/` | `templates/sprint.template.md` |

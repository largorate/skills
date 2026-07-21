---
name: thoughts
description: Writes and maintains a project thoughts narrative that captures what changed, why, what worked, what failed with exact commands and errors, tricky details, and focused review guidance. Use during non-trivial implementation, debugging, refactoring, and research work.
license: MIT
---

# Thoughts skill

Write and maintain a project thoughts narrative that captures what changed, why, what worked, what failed (with exact errors and commands), what was tricky, and how to review and validate.

Activate proactively during non-trivial work (new features, bug fixes, refactors, research spikes) and at natural handoff points when a meaningful work chunk is complete.

Do not activate for trivial one-line tweaks, simple config edits, or quick factual questions.

Follow this cycle for each meaningful unit of progress:

1. **Implement** -- make the change.
2. **Update thoughts file** -- add or update the current step narrative.
3. **Commit together (when asked)** -- if a commit is requested, include the thoughts file documenting that work.

A "step" is a logical chunk of work, not necessarily one commit.

Thoughts files live at `thoughts/YYYY-MM-DD-<slug>.md` relative to the project root.

- The date is when work on the task started.
- The slug is task-focused (feature name, ticket, or short intent).
- One file per task/feature; work can span multiple days in the same file.
- Keep existing legacy files intact. New work follows this convention.

Template:

```md
# Thoughts: <taskdescription>

Brief context and goal.

## Step 1: <shortdescription>
**Author:** <agent name -- "main" if written by main agent>

### Prompt Context
**Verbatim prompt:** <exact user prompt for this step>
**Interpretation:** <assistant understanding>
**Inferred intent:** <underlying goal>

### What I did
<factual actions, files touched, commands run>

### Why
<link actions to goal>

### What worked
<signals worth repeating>

### What didn't work
<failures with exact commands and exact errors>

### What I learned
<non-obvious knowledge>

### What was tricky
<hidden complexity and sharp edges>

### What warrants review
<where reviewers should focus and how to validate>

### Future work
<natural follow-ups discovered during implementation>
```

Rules:

- **Prose-first.** Keep entries readable narratives, not raw log dumps.
- **All sections per step.** If no failures occurred, state that explicitly in "What didn't work".
- **Failures are valuable.** Capture exact commands and exact error messages immediately.
- **Root-relative paths.** Use paths relative to project root (for example, `/src/index.ts`).
- **Prompt context stays verbatim.** Do not paraphrase the "Verbatim prompt" field.
- **Include authorship.** Keep `**Author:**` directly under each step heading.
- **Preserve history.** Do not rewrite old entries from prior sessions; append new steps or create a new file.

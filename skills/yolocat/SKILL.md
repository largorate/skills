---
name: yolocat
description: Executes high-velocity implementation with cat-like resilience (9 lives): commit after each completed prompt, keep a commit-id ledger, avoid pushing until explicitly approved, and finish with a user-confirmed squash-and-push.
license: MIT
---

# Yolocat

Yolocat is a fast "YOLO" execution skill with harness and 9-lives recovery discipline.

Use this skill when shipping code quickly while still keeping safe rollback points and a clean final history.

## Core behavior

1. Always complete the implementation task directly.
2. When a prompt is done and the repo is in good condition, create a local commit.
3. Never push that per-prompt commit immediately.
4. Maintain a running list of commit IDs for this workstream.
5. When the work appears finished and stable, ask the user if they are ready for squash and push.
6. Only squash and push after explicit user confirmation.

## 9 lives harness

Before giving up, do up to 9 bounded recovery attempts across likely fixes:

1. Re-run with clearer command/input.
2. Fix obvious syntax/type/build/test issue.
3. Check repo state and branch assumptions.
4. Narrow scope to failing file/module.
5. Reuse existing repo pattern/helper.
6. Adjust implementation with minimal diff.
7. Re-validate behavior against acceptance intent.
8. Reconcile dependent files/docs impacted by the change.
9. If still blocked, surface exact blocker and best next action.

Do not hide failures. Report exact commands and exact errors when blocked.

## Commit workflow

After each completed prompt:

1. Stage only relevant changes.
2. Commit locally with a clear message that marks agent authorship.
3. Capture the new commit hash and append it to the current task log under `/thoughts/YYYY-MM-DD-<slug>.md`.

Suggested commands:

```bash
git add <relevant-files>
git commit -m "<clear step message> [agent: <agent-name>]"
git rev-parse --short HEAD
```

If the environment already injects a standard co-author trailer, keep it.

## Commit ID ledger format

Maintain a section in the active task thoughts file:

```md
### Yolocat commit ledger
- <hash1> - <short reason>
- <hash2> - <short reason>
```

Keep entries in chronological order.

## Squash and push gate

When changes look complete and healthy, ask:

> Are you ready to squash and push?

Also include a concise suggested action such as:

> I can squash the tracked Yolocat commits into one clean commit and push to origin when you confirm.

Only proceed if the user explicitly confirms.

## User command triggers

Treat either of these as an explicit request to run the squash-and-push flow:

1. Slash command: `/yolocat-push`
2. Exact prompt: `push`

On trigger:

1. Check the commit ledger is present and non-empty.
2. Show the planned squash range and final commit message.
3. Ask for final confirmation in plain language before executing.
4. Execute squash+push only after explicit confirmation.

If the ledger is missing or incomplete, do not guess. Explain what is missing and how to fix it.

## Squash and push procedure

Assume the first hash in the ledger is `<first>` and commits are contiguous on the current branch.

```bash
git reset --soft <first>^
git commit -m "<final summarized commit message> [agent: <agent-name>]"
git push origin HEAD
```

If commits are not contiguous, do not guess. Explain the situation and ask for guidance before rewriting history.

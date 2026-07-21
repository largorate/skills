---
name: goodnight
description: "Runs an end-of-day completion flow for late autonomous work: finish tasks, verify readiness, commit, push, then hibernate Windows (fallback to shutdown if hibernate is unavailable). Trigger with /goodnight."
license: MIT
---

# Goodnight

Goodnight is a "work late" completion skill for when the user is going to bed and wants the agent to wrap up safely.

## Trigger

Treat either of these as an explicit arm-and-run trigger:

1. Slash command: `/goodnight`
2. Prompt containing the intent phrase, for example:
   - `Good night my love. I'm going to bed now. When you are done with your tasks and all is working, please commit, push and run shutdown /h in terminal.`

## Core behavior

Once armed, continue working until the active tasks are complete and in good condition, then run this sequence:

1. Stage relevant changes.
2. Commit with explicit agent attribution in the message.
3. Push to the current branch on origin.
4. Hibernate the Windows machine.

Suggested commands:

```bash
git add <relevant-files>
git commit -m "<final message> [agent: <agent-name>]"
git push origin HEAD
shutdown /h
```

## Hibernate and fallback policy

1. Prefer hibernate: `shutdown /h`.
2. If hibernate is unavailable or fails, use shutdown fallback:

```bash
shutdown /s /t 60
```

When using fallback, report that hibernate failed and that timed shutdown was used instead.

## Safety boundaries

1. Do not run power commands before commit and push succeed.
2. Do not run power commands if there are unresolved errors in the requested work.
3. If commit or push fails, report exact command and error, then stop before power actions.

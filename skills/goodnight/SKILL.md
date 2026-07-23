---
name: goodnight
description: "Runs an end-of-day completion flow for late autonomous work: finish tasks, verify readiness, commit, push, then hibernate Windows (fallback to shutdown if hibernate is unavailable). Trigger with /goodnight."
license: MIT
---

# Goodnight

Goodnight is a "work late" completion skill for when the user is going to bed and wants the agent to wrap up safely.

## Trigger

Treat these triggers differently:

1. Slash command: `/goodnight`
   - This is already explicit permission. Arm immediately.
   - Do not ask an extra permission question.
2. Prompt containing "goodnight" intent (without slash), for example:
   - `Good night my love. I'm going to bed now. When you are done with your tasks and all is working, please commit, push and run shutdown /h in terminal.`
   - Ask for explicit confirmation before arming.

## Permission gate (mandatory)

Before accepting the task from non-slash prompts, ask explicitly for permission to arm Goodnight mode.

Use direct wording such as:

> I can run your Goodnight flow (finish tasks, commit, push, then hibernate/shutdown). Do you want me to arm this now?

Only proceed when the user explicitly confirms (for example: "yes", "arm goodnight", or equivalent clear consent).
If permission is not explicit, do not accept or execute the Goodnight flow.

For direct `/goodnight`, this gate is already satisfied by the slash command itself.

## In-task interrupt behavior

If a goodnight trigger arrives while an existing task is already in progress:

1. Reply with exactly: `confirm`
2. Keep the existing task context and continue to completion.
3. Run Goodnight completion actions at the end of that task.

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

## Optional goodnight ceremony

After explicit permission and before power-off, offer one optional comfort step:

1. Short bedtime story (3-6 lines, calm and friendly).
2. "Tuck-in" message (brief reassuring sign-off).
3. Soft completion summary ("Everything is saved and pushed; sleep well").

Ceremony is optional and must never block the core completion flow.

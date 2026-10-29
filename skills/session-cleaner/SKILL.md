---
name: session-cleaner
description: Audit whether work across configured projects and agent sessions is committed and pushed, or perform explicitly authorized cross-repository commit, push, then pull synchronization. Use for session/repository Git hygiene, unpublished-work checks, and requests to synchronize multiple checkouts. Default to a read-only audit; this skill does not delete or archive sessions.
license: MIT
---

# Session Cleaner

Account for local work without losing it or publishing private data. This is Git hygiene, not session deletion, feature development, or permission to make every status clean.

## Permission and ownership

- **Audit is the default**, including `/session-cleaner` alone. Do not fetch, stage, commit, create refs, push, pull, or modify files without explicit authorization for that operation and scope. Permission to commit does not imply permission to publish. Autonomy settings do not expand authorization.
- Never create worktrees, switch shared checkout branches, initialize repositories, create remotes, delete user data, archive sessions, or automatically change history. Do not amend, force-push, destructively reset, automatically rebase, or pop/drop stashes.
- Respect workspace-access limits. A general chat whose primary checkouts are read-only must delegate authorized writes to project sessions using `workspace_type: branch`. Prefer an existing suitable session; otherwise use the minimum necessary writers in existing local checkouts. Do not evade access restrictions through a shell.
- Assign one Git owner per common repository, even when multiple projects or sessions share it. Coordinate active editors and obtain explicit paused handoffs before staging; recheck HEAD, index, and status after handoff. Do not assume an idle indicator means permission to take ownership.
- Read repository instructions and relevant user decisions. Preserve prior staging and unrelated edits. Stop the affected write if ownership, authorization, destination, or conflicting changes remain unresolved; continue independent safe audits.

## 1. Discover the bounded scope

Use available app tools such as `list_projects`, `list_sessions_and_chats`, `get_sessions_status`, and `get_session` to find configured projects, current sessions, actual checkout paths, branches, activity, access limits, and returned session links. Inspect registered existing checkouts, including inactive projects; do not assume project defaults describe live session workspaces.

Resolve each existing path with Git, using `rev-parse --show-toplevel`, `rev-parse --absolute-git-dir`, and `rev-parse --path-format=absolute --git-common-dir`. Normalize native OS paths and deduplicate identical checkouts. Group distinct registered checkouts by common Git directory: refs, history, and stashes are shared, but each checkout has its own files and index. Existing worktree registrations may help account for known paths; never create one or scan arbitrary unrelated directories.

Record absent, inaccessible, non-Git, unborn, and detached checkouts explicitly. Do not initialize, recreate, overwrite, or silently omit them. If app discovery, a host, or registered checkout is unavailable, state the coverage gap instead of claiming a complete audit.

## 2. Audit without changing Git state

Use native OS commands, noninteractive Git, disabled pagers, and optional status locks disabled, for example `git --no-pager --no-optional-locks -C <checkout> ...`. Do not print credentials, secret values, raw sensitive diffs, or credential-bearing remote URLs.

For each unique checkout and common repository, account for:

- Actual branch/HEAD, staged and unstaged changes, untracked files, conflicts, and in-progress Git operations. Use machine-readable status when parsing.
- All local branch heads, their upstreams and push destinations, not only HEAD. Record local commits even on inactive branches; never switch branches to inspect them.
- Every stash, its parents, and file inventories. Untracked/ignored files saved by a stash may live in its third parent; inspect that tree as well as tracked stash changes. Preserve stashes, including local deployment configuration, without applying or publishing them.
- Remote configuration and **live remote refs**, using read-only `git ls-remote` against the intended destination. Tracking refs alone may be stale. Missing remotes, authentication failures, and unreachable hosts are real blockers or coverage gaps, not evidence that commits are unpublished.

Compare ancestry against live destination refs where their objects are already available locally. A local tip contained in remote history is already published even if no remote branch has that exact name; do not publish redundant historical branches. A tip unequal to a live SHA is not proof of unpublished work. If missing objects prevent an ancestry check, label it unverified; do not fetch during read-only audit. Distinguish published, truly unpublished, behind, diverged, and unknown states.

On Windows, investigate apparent deletions at very long paths by comparing status and diff with `git -c core.longpaths=true ...` before treating them as intentional. Checkout artifacts are not authorization to restore or delete files.

## 3. Review the entire proposed publication

Only enter write mode for explicitly authorized repositories and actions. Fetching is allowed here to obtain live destination objects; fetching is not permission to integrate or publish.

Before any push, review **all commits and reachable objects newly introduced at the destination**, not just the pending diff or latest commit. Compare candidate tips against the verified destination history; enumerate the complete introduced history and blobs, including intermediate versions later deleted. Use `git rev-list --objects`, `git cat-file --batch-check`, and available repository secret scanning as appropriate. Batch revision/object input through stdin to avoid Windows command-line length limits.

Review intended source, documentation, assets, delivery reports, and legitimate deletions/moves. Inspect names, sizes, and content with safe redaction. Never print secret values. Never publish credentials, sensitive production logs or identifiers, local deployment configuration, or oversized blobs. Check the host's actual limits; GitHub blocks regular Git blobs larger than 100 MiB. A clean final tree does not make unsafe ancestors safe, and moving a file to LFS now does not remove earlier raw blobs.

If existing unpublished history is unsafe, do not push it or rewrite/delete the original commits. Report the blocker. Within explicit publication authorization, a **separately reviewed sanitized ordinary publication branch** may be built from the existing remote base using a separate index or publication tree, without switching the shared checkout or creating a worktree. Preserve safe source/report changes, exclude or redact sensitive inputs, and keep original raw files and local history intact. Never merge unsafe parents into this branch. Verify the exact candidate tree, ancestry, every newly reachable object, and size/secret checks before pushing; report that the original branch remains ahead intentionally. Do not invent a feature fix or use an unreviewed blanket snapshot to make publication succeed.

## 4. Commit only authorized, reviewed work

After editor handoff, recheck state and review the exact proposed commit. Stage explicit paths, including reviewed moves/deletions; do not blanket-stage the repository. Preserve previously staged user work rather than accidentally including or unstaging it. If overlapping staging cannot be safely separated, stop and report it.

Run the smallest existing checks covering the intended changes. Make a meaningful nonempty commit only when requested. Follow repository attribution rules and include required trailers, such as the Copilot default when applicable:

```text
Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>
```

Recheck the committed diff and publication history before pushing. If no remote exists, authorized local commits can still be completed, but push/pull are blocked. Never invent a destination or retry a known missing one.

## 5. Push intended branches, then safely pull

Push ordinary intended branches to the correct destination, usually `origin`, with explicit source/destination refs. Do not push every branch or every remote, especially deployment-only remotes. Do not force or bypass protection.

- If origin advanced, preserve local commits. Use a conflict-free, non-rebasing integration only within the authorized synchronization scope and repository policy. Preflight when possible; never guess conflict resolutions or use automatic stashing. Stop and report conflicts, preserving user work.
- If protection rejects the current branch, an ordinary existing/new feature branch may be published without a checkout switch when publication authorization allows it. Do not bypass rules or open a PR automatically. Leave local main intact and explain that it may remain ahead until a human PR is merged.
- After successful pushes, pull the **currently checked-out branch** from its appropriate upstream/counterpart, normally with `git -c rebase.autoStash=false -c merge.autoStash=false pull --ff-only <remote> <branch>`. Confirm that the counterpart is the intended branch, not an unrelated or deployment upstream. Do not silently change tracking configuration.
- Do not switch to or rewrite inactive branches merely because they are behind. Skip detached HEADs, unborn branches, and ancestor-only historical branch names without counterparts. If a necessary integration preceded a retry push, perform another safe pull after the successful push and report that ordering.

A protected-main fallback can succeed at publication while main remains locally ahead. A failed pull is still a partial outcome even when push succeeded. Do not conceal these distinctions.

## 6. Verify and report

Recheck every scoped checkout's final clean/dirty status, actual branch and upstream, preserved staging/stashes, and in-progress operations. Verify intended commits against live remote SHAs or ancestry, not merely a successful command or stale tracking ref. Account for all registered paths and local branch heads.

Report concise **done**, **partial**, or **blocked** outcomes per repository, with returned app session links when available. Include what was audited, committed and published, push-then-pull results, and remaining work. Explicitly label preserved unsafe local history, no-remote repositories, protected-main cases, preserved stashes, missing/non-Git folders, inaccessible hosts, and unverified coverage. Stop at genuine external blockers; never claim everything is synchronized just because the checked-out files look clean.

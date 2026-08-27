# Git workflow
- NEVER create a git worktree. Always work directly in the current working directory, on the current branch.
- NEVER create branches automatically. If a branch is needed, ask me first.
- Do not commit automatically. After making changes, stop and hand control back to me — I will review, test, and either ask for changes or commit myself.
- Before starting any task, run `git status` and `git fetch && git log HEAD..origin/main --oneline` to confirm the branch is current against main. If it's behind, tell me — don't rebase/merge automatically unless I ask.

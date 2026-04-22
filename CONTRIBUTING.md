# GitHub Workflow Guide

> **A3 note:** For Assessment 3, the integration branch is **`assessment3`**, not `main`. All A3 feature branches start from `assessment3` and PRs target `assessment3`. `main` is frozen at the A2 submission state until A3 is finalised.

---

## 1. One-time setup

Clone the repo and configure your identity:

```bash
git clone git@github.com:sendhello/student_library2.git
cd student_library2
git config --global user.name "Your Name"
git config --global user.email "you@email.com"
```

---

## 2. Start working on a task

Always create a branch from the current A3 integration branch, `assessment3`. Name it after the GitHub issue number and a short slug.

```bash
git checkout assessment3
git pull origin assessment3
git checkout -b feature/a3-27-member-faculty
```

Branch naming convention for A3:

- `feature/a3-NN-short-description` — new functionality (NN is the GitHub issue number)
- `fix/a3-NN-short-description` — bug fix

Examples: `feature/a3-28-item-extension`, `feature/a3-33-test-validator`, `fix/a3-40-startup-menu`.

---

## 3. Work and commit

Make your changes, then stage and commit:

```bash
git add entities/member.py tests/test_member.py
git commit -m "a3/#27: add faculty and year_level to Member"
```

Commit message format: `a3/#NN: short description`. Where NN is the issue number (25–47).

Push your branch to GitHub:

```bash
git push origin feature/a3-27-member-faculty
```

Repeat add → commit → push as you work. Commit often.

---

## 4. Create a Pull Request (PR)

1. Go to the repo on **github.com**
2. Click the **"Compare & pull request"** button (appears after you push)
3. **Make sure the base branch is `assessment3`** (not `main`)
4. Fill in:
   - **Title** — `a3/#27: add faculty and year_level to Member`
   - **Description** — brief summary + `Closes #27`
5. In the right sidebar:
   - **Assignees** — yourself
   - **Reviewers** — `@sendhello` (Ivan, TL — always)
   - **Labels** — GitHub auto-inherits from the issue; no action needed
6. Click **"Create pull request"**

---

## 5. Link a PR to an Issue

In the PR description, add this line:

```txt
Closes #27
```

Replace `27` with the issue number you're working on. GitHub auto-closes the issue when the PR is merged.

---

## 6. Respond to review comments

Ivan will leave comments on your PR. Fix them locally:

```bash
# edit the files, then:
git add .
git commit -m "a3/#27: address review comments"
git push origin feature/a3-27-member-faculty
```

The PR updates automatically. Reply to each comment with **"Resolved"** when done and click the **Resolve conversation** button on GitHub.

Note: any new push dismisses previous approvals — Ivan needs to re-approve after your changes.

---

## 7. Merge the PR

**Only Ivan (`@sendhello`) merges PRs.** This is the team's convention and also enforced indirectly by branch protection (see section 10 below).

Process:
1. Ivan confirms all review comments are resolved
2. Ivan confirms the PR is approved by him
3. Ivan clicks **"Squash and merge"**
4. Branch is merged into `assessment3`, the linked issue closes automatically

---

## 8. Sync your local branch after a merge

After any PR is merged (yours or someone else's), update your local `assessment3`:

```bash
git checkout assessment3
git pull origin assessment3
```

Then branch off again for your next task.

---

## 9. Resolve a merge conflict

If GitHub shows a conflict on your PR:

```bash
git checkout assessment3
git pull origin assessment3
git checkout feature/a3-27-member-faculty
git merge assessment3
# open the conflicting file(s), resolve manually, then:
git add .
git commit -m "a3/#27: resolve merge conflict with assessment3"
git push origin feature/a3-27-member-faculty
```

---

## 10. Branch protection — what's enforced

`main` and `assessment3` are protected branches. GitHub enforces:

- **No direct pushes** — all changes must go through a Pull Request
- **At least 1 approving review required** before a PR can be merged
- **Stale approvals are dismissed** on any new push to the PR (re-review needed)
- **All conversations must be resolved** before merge
- **Force pushes blocked** — cannot rewrite history
- **Branch deletion blocked** — cannot accidentally delete these branches

Admins (`@sendhello`) have override for emergency housekeeping commits (infrastructure, dataset regen, branch-protection changes), but feature code always goes through PRs.

---

## 11. The merge convention — why only Ivan

Branch protection on a personal GitHub repo cannot restrict **who** is allowed to merge (that's an organisation-repo feature). So technically any collaborator with write access could click "Merge" on an approved PR. The team has agreed on the convention:

> **Only Ivan merges PRs.** Team members do not click "Squash and merge" on their own or each other's PRs, even when they are approved.

This keeps `assessment3` consistent (Ivan owns integration) and avoids accidental merges of PRs that still need his review.

---

## Quick reference

| Action | Command |
| --- | --- |
| Sync integration branch | `git checkout assessment3 && git pull origin assessment3` |
| Create feature branch | `git checkout -b feature/a3-NN-name` |
| Stage changes | `git add <files>` |
| Commit | `git commit -m "a3/#NN: message"` |
| Push branch | `git push origin feature/a3-NN-name` |
| Check status | `git status` |
| See commit history | `git log --oneline` |

---

## Rules for this project

- **Never commit directly to `main` or `assessment3`** — always use a branch + PR (and branch protection will refuse you anyway)
- **One issue = one branch = one PR** — do not bundle unrelated changes
- **Always pull latest `assessment3`** before creating a new branch
- **Link every PR to its issue** with `Closes #NN`
- **Only Ivan merges** PRs

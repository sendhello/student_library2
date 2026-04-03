# GitHub Workflow Guide

## 1. One-time setup

Clone the repo and configure your identity:

```bash
git clone https://github.com/your-org/your-repo.git
cd your-repo
git config --global user.name "Your Name"
git config --global user.email "you@email.com"
```

---

## 2. Start working on a task

Always create a branch from `main`. Name it after the task ID:

```bash
git checkout main
git pull origin main
git checkout -b feature/TASK-02-member-class
```

Branch naming convention:

- `feature/TASK-XX-short-description` — new functionality
- `fix/TASK-XX-short-description` — bug fix

---

## 3. Work and commit

Make your changes, then stage and commit:

```bash
git add .
git commit -m "TASK-02: implement Member class with borrow/return methods"
```

Commit message format: `TASK-XX: short description of what was done`

Push your branch to GitHub:

```bash
git push origin feature/TASK-02-member-class
```

Repeat add → commit → push as you work. Commit often.

---

## 4. Create a Pull Request (PR)

1. Go to the repo on **github.com**
2. Click the **"Compare & pull request"** button (appears after you push)
3. Fill in:
   - **Title** — `TASK-02: implement Member class`
   - **Description** — briefly what you did and any notes for the reviewer
4. In the right sidebar:
   - **Assignees** — assign yourself
   - **Reviewers** — assign the TL
   - **Labels** — pick from `feature`, `fix`, etc.
5. Click **"Create pull request"**

---

## 5. Link a PR to an Issue (task)

In the PR description, add this line:

```txt
Closes #3
```

Replace `3` with the issue number. GitHub will automatically close the issue when the PR is merged.

You can also link manually: on the PR page → right sidebar → **"Development"** → **"Link an issue"**.

---

## 6. Respond to review comments

The TL will leave comments on your PR. To fix them:

```bash
# make the requested changes in your editor, then:
git add .
git commit -m "TASK-02: address review comments"
git push origin feature/TASK-02-member-class
```

The PR updates automatically. Reply to each comment with **"Resolved"** when done.

---

## 7. Merge the PR

Only the TL merges. Steps on GitHub:

1. Open the PR
2. Confirm all review comments are resolved
3. Click **"Squash and merge"**
4. Confirm — the branch is merged into `main` and the linked issue closes

---

## 8. Sync your local main after a merge

After any PR is merged (yours or someone else's), update your local `main`:

```bash
git checkout main
git pull origin main
```

Then branch off again for your next task.

---

## 9. Resolve a merge conflict

If GitHub shows a conflict on your PR:

```bash
git checkout main
git pull origin main
git checkout feature/TASK-02-member-class
git merge main
# open the conflicting file(s), fix the marked sections, then:
git add .
git commit -m "TASK-02: resolve merge conflict"
git push origin feature/TASK-02-member-class
```

---

## Quick reference

| Action | Command |
| --- | --- |
| Create branch | `git checkout -b feature/TASK-XX-name` |
| Stage all changes | `git add .` |
| Commit | `git commit -m "TASK-XX: message"` |
| Push branch | `git push origin feature/TASK-XX-name` |
| Update local main | `git checkout main && git pull origin main` |
| Check current status | `git status` |
| See commit history | `git log --oneline` |

---

## Rules for this project

- **Never commit directly to `main`** — always use a branch + PR
- **One task = one branch = one PR**
- **Always pull latest `main`** before creating a new branch
- Link every PR to its issue (`Closes #N`)
- TL is the only one who merges

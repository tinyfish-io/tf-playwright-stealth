---
description: Org best practices loader — runs for all files
globs: "**/*"
---

# Org Best Practices

Before starting any task in this repo, load org standards in this order:

## Step 1: General Coding Standards
Read `.claude/best-practices/coding-standards.md`.
If not found, skip and note it to the user.

## Step 2: Repo-Type Standards
Determine the repo type:
1. Check for `.claude/repo-type` and read its contents (single word, e.g. `python_app`)
2. If not found, infer from project files:
   - `pyproject.toml` or `setup.py` → `python_app`
   - `package.json` + `next.config.*` → `nextjs_app`
   - `package.json` alone → `node_service`
   - `Dockerfile` only → `generic_service`
3. If type cannot be determined, skip and note it to the user.

Once type is known, read `.claude/best-practices/<repo_type>/best-practices.md`.
If not found, skip and note it to the user.

## Step 3: Conflict Resolution
- `coding-standards.md` wins on: style, naming, structure, and DRY principles
- Repo-type standards win on: tooling, framework patterns, and implementation details
- If a genuine conflict cannot be resolved by the above, flag it to the user before proceeding

## Step 4: Confirm (first task only)
On the first task of the session, briefly tell the user:
- Which standards files were loaded
- The detected repo type
- Any files that were missing or could not be determined
Do not repeat this on subsequent tasks.

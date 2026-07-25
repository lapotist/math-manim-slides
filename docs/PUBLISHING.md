# Publishing Walkthrough

This checklist publishes the committed repository, not the multi-gigabyte
working directory with its ignored environments, source downloads, renders,
and QA frames. Stop on the first failing check.

## 1. Verify The Candidate

Start from a clean branch and confirm the generated indexes and catalog agree:

```bash
git status --short --branch
pixi run test
pixi run validate-catalog
pixi run check-sources
pixi run lessons list
```

The README must continue to report the exact catalog states. A public
in-progress repository is acceptable; changing unfinished rows to `published`
is not. Only a rights-cleared lesson with a reachable public artifact may use
that state.

## 2. Decide Commit Identity Before Authentication

List every address that a first push would expose:

```bash
git log --all --format='%an <%ae> | %cn <%ce>' | sort -u
git config user.name
git config user.email
```

Choose one of these outcomes explicitly:

1. Confirm every listed address is intentionally public.
2. Use the verified GitHub no-reply address shown in the account's email
   settings and approve rewriting every local commit before the first push.

Changing `git config user.email` affects only future commits. A history rewrite
changes commit IDs, so first create and verify a local bundle backup, perform
the rewrite before any public push, and rerun this entire checklist afterward.
Do not guess the no-reply address: its format depends on the account.

GitHub documents commit-email privacy at
<https://docs.github.com/en/account-and-profile/reference/email-addresses-reference>
and repository-local email configuration at
<https://docs.github.com/en/account-and-profile/how-tos/email-preferences/setting-your-commit-email-address>.

## 3. Audit The Committed Tree In Isolation

Create a temporary directory and extract only tracked content from `HEAD`:

```bash
release_audit_dir="$(mktemp -d)"
git archive HEAD | tar -x -C "$release_audit_dir"
cd "$release_audit_dir"
pixi install --frozen
pixi run test
pixi run validate-catalog
pixi run check-sources
pixi run prepare-tex
pixi run lessons render carlo.tcfs_115_math_gifted.q09 --quality l
```

Question 9 exercises the single shared `CarloSlide` base, CJK text, TeX,
updaters, a loop, geometry, and the Manim Slides manifest path. Inspect its
generated manifest and first/last frames. If a new base/template family is
introduced, add one representative clean-tree render for that family.

Record the commit ID, tool versions, commands, and results under
`docs/releases/` before publication. Do not commit the temporary environment or
rendered media.

## 4. Authenticate Deliberately

GitHub CLI is pinned in the Pixi environment. Authenticate only after the
identity decision and clean-tree audit pass:

```bash
pixi run gh auth login --hostname github.com --git-protocol https --web
pixi run gh auth status
pixi run gh api user --jq '{login: .login, id: .id}'
```

The browser step belongs to the maintainer. Never paste an access token into a
tracked file, shell history, chat, or command argument.

## 5. Create And Push Once

Choose the final owner and repository name. From the audited local repository:

```bash
pixi run gh repo create OWNER/carlo-math-manim-slides \
  --public \
  --source=. \
  --remote=origin \
  --description="Intuitive Traditional Chinese math lessons built with Manim Slides"
git remote -v
git push --set-upstream origin main
```

Do not ask GitHub to add a README, `.gitignore`, or license: the split-license
files in this repository are authoritative. Creating and pushing separately
makes the new remote inspectable before any history is transferred. GitHub's
current command reference is <https://cli.github.com/manual/gh_repo_create>.

## 6. Verify The Public Result

```bash
pixi run gh repo view OWNER/carlo-math-manim-slides --json nameWithOwner,url,visibility,defaultBranchRef
git ls-remote --heads origin main
```

Open the reported URL and verify that `main` visibly contains `LICENSE`,
`LICENSE-CONTENT`, `NOTICE.md`, `SOURCES.md`, the permission note, build
instructions, and the honest 46/20/10 inventory. Confirm that ignored PDFs,
videos, HTML, credentials, and build directories are absent.

Finally, send the repository URL to the Carlo site owner, as requested in the
recorded permission exchange. Sharing the link is a courtesy and project
follow-up, not a CC BY condition.

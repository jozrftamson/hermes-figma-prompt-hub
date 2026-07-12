# Collaboration plan

This project welcomes contributors for Python, Figma API work, MCP integration, prompt engineering, validation, docs, examples, and project maintenance.

## Who to invite

- Python developers interested in small tooling projects.
- Figma plugin/API users.
- MCP developers.
- Prompt engineers who want structured prompt catalogs.
- Documentation contributors.
- Maintainers who like triage, examples, and onboarding.

## How contributors can start

1. Read `CONTRIBUTING.md`.
2. Pick a `good first issue` or `help wanted` issue.
3. If they are not sure where to start, open a `Collaborator interest` issue.
4. Open a focused PR.
5. Run `python scripts/validate_repo.py` before requesting review.

## Maintainer routine

- Weekly: review issues and PRs.
- Weekly: keep at least one `good first issue` open.
- Monthly: run the `Collaboration digest` workflow and share the created issue.
- Monthly: review automatically created good-first issues and monthly sponsor updates.
- Monthly: review the `Contributor scout` report and contact only a few relevant people manually.
- Monthly: publish a short sponsor/contributor update.
- Each release: update `ROADMAP.md` and prompt examples.

## Automation in use

- `Good first issue seeding`: creates recurring small tasks for new contributors.
- `Stale issue ping`: adds a friendly non-closing ping to inactive issues.
- `Contributor recognition`: updates `CONTRIBUTORS.md` after merged PRs.
- `Schema release suggestion`: opens a release issue when prompt schema files change.
- `Sponsor and contributor monthly update`: creates a monthly update issue.
- `Prompt catalog`: regenerates `docs/prompt-catalog.md`.
- `Figma contract check`: verifies README, contract, and fixtures stay aligned.
- `Contributor scout`: searches public GitHub repositories and creates a manual-review shortlist. It does not contact anyone automatically.

## Outreach channels

- GitHub issues and discussions.
- Figma communities.
- MCP and agent development communities.
- Python tooling communities.
- Open-source sponsorship updates through OpenCollective.

## Invite message

```text
Hi <name>,

I am building Hermes Figma Prompt Hub, an open-source project for designing, validating, versioning, and serving Figma-based prompt assets through MCP-compatible workflows.

Your experience with <topic> would be useful, especially around <specific area>. The repo has contributor docs, good first issues, and CI validation:

https://github.com/jozrftamson/hermes-figma-prompt-hub

If you are interested, comment on an issue or open a small PR.
```

## Maintainer response for new contributors

```text
Thanks for offering to help. A good first step is to pick one small issue and comment with the files you expect to touch. Please run `python scripts/validate_repo.py` before opening the PR.
```

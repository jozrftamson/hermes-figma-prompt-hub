# Contributing

Thanks for helping improve Hermes Figma Prompt Hub. This project is intentionally external to the Hermes core tree, so contributions should keep Figma-specific logic here.

## Ways to contribute

- Add Figma API import/export code.
- Build the MCP server integration.
- Add prompt examples and eval cases.
- Improve validation and tests.
- Improve setup docs for Hermes users.

## Local setup

```bash
git clone https://github.com/jozrftamson/hermes-figma-prompt-hub.git
cd hermes-figma-prompt-hub
python3 -m venv .venv
. .venv/bin/activate
pip install jsonschema
python scripts/validate_prompt.py prompts/raw/nous-central-v1.json
python scripts/validate_repo.py
```

## Pull request checklist

- Keep changes scoped to one contribution.
- Update README or docs when behavior changes.
- Add or update examples when the prompt format changes.
- Run validation before opening a PR:

```bash
python scripts/validate_repo.py
```

## Automation

GitHub Actions run validation on pushes and pull requests. New issues and pull requests receive automatic comments with contributor links and checklists.

Maintainers can run the manual `Collaboration digest` workflow from the GitHub Actions tab to create a fresh issue that advertises current contributor opportunities.

## Good first issues

Good first issues should be small, testable, and documented. Examples:

- Add a new prompt example under `prompts/raw`.
- Add an eval case under `evals/cases`.
- Improve error messages in `scripts/validate_prompt.py`.
- Document one Hermes MCP setup path.

## Maintainer notes

When reviewing contributions, prefer small PRs with clear user value. For larger features, ask contributors to open an issue first so the design can be discussed before implementation.

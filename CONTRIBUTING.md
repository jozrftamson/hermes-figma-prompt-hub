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
```

## Pull request checklist

- Keep changes scoped to one contribution.
- Update README or docs when behavior changes.
- Add or update examples when the prompt format changes.
- Run validation before opening a PR:

```bash
python scripts/validate_prompt.py prompts/raw/nous-central-v1.json
```

## Good first issues

Good first issues should be small, testable, and documented. Examples:

- Add a new prompt example under `prompts/raw`.
- Add an eval case under `evals/cases`.
- Improve error messages in `scripts/validate_prompt.py`.
- Document one Hermes MCP setup path.

## Maintainer notes

When reviewing contributions, prefer small PRs with clear user value. For larger features, ask contributors to open an issue first so the design can be discussed before implementation.


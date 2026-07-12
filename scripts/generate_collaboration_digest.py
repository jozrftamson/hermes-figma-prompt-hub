from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


TEMPLATE = """# Collaboration digest

Use this digest in GitHub Discussions, social posts, or maintainer updates.

## Current focus

- Figma importer: convert `PROMPT/<id>` frames into prompt JSON.
- MCP server: list, validate, and export prompt assets.
- Prompt quality: add examples, eval cases, and schema improvements.
- Documentation: make setup easier for Hermes users.

## Good first contributions

- Add one prompt example under `prompts/raw`.
- Add one Figma fixture under `evals/cases`.
- Improve validation errors or docs.
- Test the scaffold on a new local project.

## Contributor links

- Repository: https://github.com/jozrftamson/hermes-figma-prompt-hub
- Contributing: https://github.com/jozrftamson/hermes-figma-prompt-hub/blob/main/CONTRIBUTING.md
- Roadmap: https://github.com/jozrftamson/hermes-figma-prompt-hub/blob/main/ROADMAP.md
- Sponsoring: https://github.com/jozrftamson/hermes-figma-prompt-hub/blob/main/SPONSORING.md

## Short outreach post

I am building Hermes Figma Prompt Hub, an open-source Figma-to-Hermes prompt workflow for designing, validating, versioning, and serving prompts through MCP.

Looking for collaborators interested in Python, Figma APIs, MCP, prompt engineering, validation, docs, and examples.

Good first issues and roadmap:
https://github.com/jozrftamson/hermes-figma-prompt-hub
"""


def main() -> None:
    output = ROOT / "docs/outreach/collaboration-digest.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(TEMPLATE, encoding="utf-8")
    print(f"Wrote {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()


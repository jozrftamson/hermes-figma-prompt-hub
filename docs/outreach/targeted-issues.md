# Targeted contributor issues

Use these issue drafts to invite focused collaboration without mass-pinging people.

## Figma Importer Developer

Title:

```text
help wanted: build Figma frame importer
```

Body:

```text
Build an importer that reads Figma frames named `PROMPT/<id>` and converts supported text layers into prompt JSON.

Done when:
- Importer can process fixture data from `evals/cases`.
- Layer mapping follows `prompts/figma-layer-contract.txt`.
- Output validates with `python scripts/validate_repo.py`.
- No private Figma tokens or file data are committed.
```

## MCP Server Developer

Title:

```text
help wanted: implement MCP prompt tools
```

Body:

```text
Implement MCP tools for prompt workflows.

Suggested tools:
- List prompt IDs.
- Validate a prompt by ID.
- Export prompt content as structured JSON.

Done when:
- Tools operate on `prompts/raw/*.json`.
- Validation reuses `scripts/validate_prompt.py`.
- README documents local usage.
```

## Prompt Eval Maintainer

Title:

```text
help wanted: expand prompt eval checks
```

Body:

```text
Expand prompt eval coverage for prompt quality.

Useful work:
- Add examples for `contains`, `not_contains`, `regex`, `json_schema`, and `max_length`.
- Add fixtures under `evals/cases`.
- Document expected behavior in README.

Done when `python scripts/validate_repo.py` passes.
```

## Docs Contributor

Title:

```text
help wanted: improve contributor setup docs
```

Body:

```text
Improve the first-time contributor path.

Good targets:
- Fresh clone setup.
- How to validate prompt files.
- How to update `docs/prompt-catalog.md`.
- How to choose a good first issue.

Done when a new contributor can complete setup and validation from README/CONTRIBUTING alone.
```


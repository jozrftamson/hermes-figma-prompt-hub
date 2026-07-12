# Roadmap

This roadmap is meant to help contributors find useful work.

## Phase 1: Contributor-ready scaffold

- Document local setup.
- Provide issue templates.
- Add example prompt JSON and schema validation.
- Mark small tasks as `good first issue`.

## Phase 2: Figma import

- Add a Figma API client that reads a file by `FIGMA_FILE_KEY`.
- Parse frames named `PROMPT/<id>`.
- Map text layers using `prompts/figma-layer-contract.txt`.
- Write prompt JSON into `prompts/raw/<id>.json`.
- Add tests with fixture JSON.

## Phase 3: MCP server

- Implement `mcp/server.py`.
- Expose tools for listing prompt IDs.
- Expose tools for validating prompt files.
- Expose tools for exporting prompt content to Hermes-compatible payloads.
- Document Hermes MCP configuration.

## Phase 4: Quality and examples

- Add sample prompts.
- Add eval cases.
- Add CI validation.
- Add release notes for stable prompt schema versions.


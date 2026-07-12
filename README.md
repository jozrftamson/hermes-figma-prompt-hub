# Hermes Figma Prompt Hub

Standalone Figma/Hermes prompt hub scaffold for designing, versioning, and validating structured prompt assets outside the Hermes core tree.

This project was split out from a Hermes core-tree integration proposal. It is intended to be used as an external project or plugin-style companion repository.

## Contributors wanted

This repository is looking for contributors who want to help turn the scaffold into a useful Figma/Hermes MCP integration.

Good first areas:

- Build a Figma API importer that converts `PROMPT/<id>` frames into prompt JSON.
- Implement `mcp/server.py` with tools for listing, validating, and exporting prompts.
- Add prompt examples and eval cases under `prompts/raw` and `evals/cases`.
- Improve docs for Hermes MCP setup and Figma token handling.
- Add tests for schema validation and future importer behavior.

Start here:

- Read [CONTRIBUTING.md](CONTRIBUTING.md).
- Pick an item from [ROADMAP.md](ROADMAP.md).
- Open or claim an issue with the `good first issue` or `help wanted` label.

## Sponsor development

If this project is useful to you, you can sponsor ongoing development through GitHub Sponsors:

https://opencollective.com/hermes-figma-prompt-hub

https://github.com/sponsors/jozrftamson

OpenCollective is the recommended option for transparent project funding. GitHub Sponsors, Buy Me a Coffee, and Ko-fi are also documented in [SPONSORING.md](SPONSORING.md).

Sponsorship helps fund Figma API importer work, MCP server development, prompt validation, documentation, and contributor support.

## Installation

```bash
git clone https://github.com/jozrftamson/hermes-figma-prompt-hub.git
cd hermes-figma-prompt-hub
python3 -m venv .venv
. .venv/bin/activate
pip install jsonschema
```

Validate the included example prompt:

```bash
python scripts/validate_prompt.py prompts/raw/nous-central-v1.json
```

Create or refresh the scaffold files in the current project:

```bash
python install/scaffold.py
```

To scaffold into another directory:

```bash
python install/scaffold.py /path/to/figma-hermes-prompt-hub
```

## Figma token and API configuration

Create a Figma personal access token in Figma and keep it outside source control:

```bash
export FIGMA_ACCESS_TOKEN="figd_..."
export FIGMA_FILE_KEY="your-file-key"
```

The current scaffold defines the prompt contract and validation format. A Figma sync command can read frames named `PROMPT/<id>` and map layers using `prompts/figma-layer-contract.txt`.

Expected Figma frame/layer contract:

```text
Figma Layer Contract (Frame: PROMPT/<id>)
00_system
01_developer
02_user_template
10_guardrail_<n>
20_example_in_<n>
21_example_out_<n>
90_eval_must_include_<n>
91_eval_must_not_include_<n>
```

## Hermes MCP configuration

Use Hermes' external MCP configuration path instead of adding vendor-specific code to the Hermes repository.

Example MCP server entry:

```json
{
  "mcp_servers": {
    "figma-prompt-hub": {
      "command": "python",
      "args": [
        "/absolute/path/to/hermes-figma-prompt-hub/mcp/server.py"
      ],
      "env": {
        "FIGMA_ACCESS_TOKEN": "${FIGMA_ACCESS_TOKEN}",
        "FIGMA_FILE_KEY": "${FIGMA_FILE_KEY}"
      }
    }
  }
}
```

`mcp/server.py` is intentionally left as an integration point. Keep Figma API access and Hermes-specific MCP wiring in this external repository.

## Example prompt workflow

1. Design a Figma frame named `PROMPT/nous-central-v1`.
2. Add text layers matching `prompts/figma-layer-contract.txt`.
3. Export or sync the frame into `prompts/raw/nous-central-v1.json`.
4. Validate the prompt:

```bash
python scripts/validate_prompt.py prompts/raw/nous-central-v1.json
```

5. Use the validated prompt JSON from Hermes or an MCP tool.

## Prompt format

Prompt JSON files must match `prompts/schema/prompt.schema.json`:

```json
{
  "id": "nous-central-v1",
  "version": "0.1.0",
  "system": "Du bist ein präziser Assistent.",
  "developer": "Antwort kurz, korrekt, ohne Floskeln.",
  "user_template": "Kontext: {{context}}\nAufgabe: {{task}}",
  "variables": ["context", "task"],
  "guardrails": ["Keine erfundenen Fakten", "Bei Unsicherheit klar markieren"],
  "few_shots": [
    {
      "input": "task=Summarize X",
      "output": "Kurzfassung ..."
    }
  ],
  "eval": {
    "must_include": ["Kurzfassung"],
    "must_not_include": ["Great question", "As an AI"]
  }
}
```

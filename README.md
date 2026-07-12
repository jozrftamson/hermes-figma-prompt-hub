# Hermes Figma Prompt Hub

[![CI](https://github.com/jozrftamson/hermes-figma-prompt-hub/actions/workflows/ci.yml/badge.svg)](https://github.com/jozrftamson/hermes-figma-prompt-hub/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Sponsor](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-fafbfc?logo=github-sponsors)](https://github.com/sponsors/jozrftamson)
[![OpenCollective](https://img.shields.io/badge/OpenCollective-support-blue?logo=opencollective)](https://opencollective.com/hermes-figma-prompt-hub)

Figma-to-MCP prompt management for Hermes workflows.

Hermes Figma Prompt Hub is an open-source scaffold for designing, versioning, validating, and eventually serving structured prompt assets from Figma into Hermes-compatible MCP workflows.

The project keeps Figma-specific integration work outside the Hermes core repository while giving teams a clear place to build prompt tooling, validation, importer logic, examples, and automation.

## Status

This repository is currently an integration scaffold.

- Ready: prompt schema, example prompt, validation scripts, Figma layer contract, CI, contributor automation, sponsorship docs.
- In progress: Figma frame importer and MCP server implementation.
- Not ready yet: production Figma sync, full MCP tool server, package release.

## What It Provides

- A structured JSON prompt format for system, developer, user template, variables, guardrails, tools, output format, examples, changelog, and eval checks.
- A Figma layer naming contract for frames named `PROMPT/<id>`.
- Validation scripts for prompts, schema consistency, prompt catalog generation, and Figma contract alignment.
- Prompt pattern analysis and prompt security audit reports.
- GitHub automation for CI, code review, contributor onboarding, issue health, prompt catalog updates, and collaboration scouting.
- Documentation and issue templates for contributors, sponsors, and maintainers.

## Use Cases

- Design prompts visually in Figma and map layers into structured prompt JSON.
- Maintain prompt versions with guardrails, examples, output contracts, and eval checks.
- Prepare prompt assets for Hermes or MCP-compatible tools.
- Build a shared prompt hub for design, product, and engineering workflows.
- Invite collaborators around Figma API, MCP, prompt evaluation, docs, and automation.

## Quickstart

```bash
git clone https://github.com/jozrftamson/hermes-figma-prompt-hub.git
cd hermes-figma-prompt-hub
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python scripts/validate_repo.py
```

Validate one prompt:

```bash
python scripts/validate_prompt.py prompts/raw/nous-central-v1.json
```

Regenerate the prompt catalog:

```bash
python scripts/generate_prompt_catalog.py
```

Create a scaffold in another directory:

```bash
python install/scaffold.py /path/to/figma-hermes-prompt-hub
```

## Prompt Format

Prompt files live under `prompts/raw/*.json` and must match `prompts/schema/prompt.schema.json`.

Core fields:

- `id`, `version`, `status`, `category`, `tags`
- `system`, `developer`, `user_template`
- `variables`, `context_sources`, `tools`
- `guardrails`, `constraints`, `style_rules`
- `output_format`
- `few_shots`
- `changelog`
- `eval.must_include`, `eval.must_not_include`, `eval.checks`

Example:

```json
{
  "id": "nous-central-v1",
  "version": "0.2.0",
  "status": "active",
  "category": "general-assistant",
  "variables": ["context", "task", "format"],
  "output_format": {
    "type": "json",
    "instructions": "Return valid JSON with summary, reasoning_notes and next_actions."
  },
  "guardrails": ["Keine erfundenen Fakten", "Bei Unsicherheit klar markieren"],
  "eval": {
    "must_include": ["summary", "next_actions"],
    "must_not_include": ["Great question", "As an AI"],
    "checks": [
      {
        "name": "valid_json_output",
        "type": "json_schema"
      }
    ]
  }
}
```

See the full example at `prompts/raw/nous-central-v1.json`.

## Figma Contract

Create Figma frames named `PROMPT/<id>`. Text layers should use the naming contract in `prompts/figma-layer-contract.txt`.

Current layer names:

```text
00_system
01_developer
02_user_template
03_output_format
04_tool_policy
05_context_source_<name>
10_guardrail_<n>
11_constraint_<n>
12_style_rule_<n>
20_example_in_<n>
21_example_out_<n>
22_example_note_<n>
30_variable_<name>
40_test_case_<n>
50_expected_output_<n>
80_changelog_<version>
90_eval_must_include_<n>
91_eval_must_not_include_<n>
92_eval_check_<n>
```

Fixture data for importer development lives under `evals/cases`.

## MCP Direction

The planned MCP server should expose tools for:

- listing available prompt IDs
- validating prompt files
- exporting prompt content as structured JSON
- later syncing or importing Figma frames

Hermes should consume this as an external MCP integration instead of adding Figma-specific code to the Hermes core tree.

Example configuration shape:

```json
{
  "mcp_servers": {
    "figma-prompt-hub": {
      "command": "python",
      "args": ["/absolute/path/to/hermes-figma-prompt-hub/mcp/server.py"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "${FIGMA_ACCESS_TOKEN}",
        "FIGMA_FILE_KEY": "${FIGMA_FILE_KEY}"
      }
    }
  }
}
```

## Automation

The repository includes automation for development quality and community growth:

- CI validation
- automated code review with severity policy, labels, inline comments, and PR score
- Figma contract check
- prompt catalog generation
- automation failure diagnostics
- good-first-issue seeding
- stale issue pings without automatic closing
- contributor recognition
- contributor scout reports
- monthly sponsor and contributor updates
- CODEOWNERS routing

Useful local commands:

```bash
python scripts/validate_repo.py
python scripts/check_figma_contract.py
python scripts/analyze_prompt_patterns.py
python scripts/security_prompt_audit.py
python scripts/import_prompt_text.py local-prompt.txt --id my-prompt
python scripts/generate_prompt_catalog.py
python scripts/code_review.py --base origin/main
python scripts/diagnose_automation_failures.py --limit 30
python scripts/scout_collaborators.py
```

## Roadmap

Near-term work:

1. Implement the Figma importer for `PROMPT/<id>` frames.
2. Implement the first MCP server tools.
3. Add more prompt examples and eval fixtures.
4. Improve prompt semantic review.
5. Prepare a stable schema release.

See [ROADMAP.md](ROADMAP.md).

For a deeper technical overview, see [docs/architecture.md](docs/architecture.md). For first-time setup, see [docs/getting-started.md](docs/getting-started.md).
For project-board setup, see [docs/project-board.md](docs/project-board.md).

## Contributing

Good first areas:

- Figma API importer
- MCP server tools
- prompt examples
- eval fixtures
- validation and review automation
- documentation

Start with [CONTRIBUTING.md](CONTRIBUTING.md), [COLLABORATION.md](COLLABORATION.md), and open issues labeled `good first issue` or `help wanted`.

## Sponsoring

OpenCollective is the recommended funding path for transparent project support:

https://opencollective.com/hermes-figma-prompt-hub

GitHub Sponsors:

https://github.com/sponsors/jozrftamson

See [SPONSORING.md](SPONSORING.md).

## License

MIT. See [LICENSE](LICENSE).

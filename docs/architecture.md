# Architecture

Hermes Figma Prompt Hub is organized around structured prompt assets and automation.

## Core Concepts

- Figma frames named `PROMPT/<id>` represent prompt assets visually.
- Text layers follow `prompts/figma-layer-contract.txt`.
- Prompt JSON files live under `prompts/raw`.
- Prompt JSON files validate against `prompts/schema/prompt.schema.json`.
- Generated docs such as `docs/prompt-catalog.md` make prompts discoverable.

## Main Components

### Prompt Schema

The schema defines metadata, prompt roles, variables, context sources, tools, guardrails, constraints, style rules, output format, examples, changelog, and eval checks.

### Figma Contract

The contract maps Figma text layers into prompt fields. It is intentionally text-based so designers and developers can inspect it without special tooling.

### Validation

Validation scripts check:

- JSON syntax
- prompt schema compliance
- prompt catalog freshness
- Figma contract consistency across README and fixtures
- prompt pattern report freshness
- prompt security audit freshness

### MCP Direction

The planned MCP server should expose prompt listing, validation, export, and later Figma import/sync tools. Hermes should consume this as an external MCP integration.

### Automation

GitHub Actions provide CI, review automation, contributor onboarding, issue health, release suggestions, prompt catalog updates, and automation failure diagnostics.

## Data Flow

```text
Figma PROMPT/<id> frame
  -> layer contract
  -> importer
  -> prompts/raw/<id>.json
  -> schema validation
  -> prompt catalog
  -> MCP tools
  -> Hermes workflow
```

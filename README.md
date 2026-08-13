# Hermes Figma Prompt Hub
=====================================================

[![CI](https://github.com/jozrftamson/hermes-figma-prompt-hub/actions/workflows/ci.yml/badge.svg)](https://github.com/jozrftamson/hermes-figma-prompt-hub/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Sponsor](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-fafbfc?logo=github-sponsors)](https://github.com/sponsors/jozrftamson)
[![OpenCollective](https://img.shields.io/badge/OpenCollective-support-blue?logo=opencollective)](https://opencollective.com/hermes-figma-prompt-hub)

Figma-to-MCP prompt management for Hermes workflows.

Hermes Figma Prompt Hub is an open-source scaffold for designing, versioning, validating, and eventually serving structured prompt assets from Figma into Hermes-compatible MCP workflows.

The project keeps Figma-specific integration work outside the Hermes core repository while giving teams a clear place to build prompt tooling, validation, importer logic, examples, and automation.

## Upstream

Hermes core repository:
```text
https://github.com/NousResearch/hermes-agent
```

Local upstream remote:
```bash
git remote add upstream git@github.com:NousResearch/hermes-agent.git
```

This project remains an external integration repository so Figma-specific code can evolve outside the Hermes core tree.

## Status

This repository is currently an integration scaffold.

* Ready: prompt schema, example prompt, validation scripts, Figma layer contract, CI, contributor automation, sponsorship docs.
* In progress: Figma frame importer and MCP server implementation.
* Not ready yet: production Figma sync, full MCP tool server, package release.

## What It Provides

* A structured JSON prompt format for system, developer, user template, variables, guardrails, tools, output format, examples, changelog, and eval checks.
* A Figma layer naming contract for frames named `PROMPT/<id>`.
* Validation scripts for prompts, schema consistency, prompt catalog generation, and Figma contract alignment.
* Prompt pattern analysis and prompt security audit reports.
* GitHub automation for CI, code review, contributor onboarding, issue health, prompt catalog updates, and collaboration scouting.
* Documentation and issue templates for contributors, sponsors, and maintainers.

## Use Cases

* Design prompts visually in Figma and map layers into structured prompt JSON.
* Maintain prompt versions with guardrails, examples, output contracts, and eval checks.
* Prepare prompt assets for Hermes or MCP-compatible tools.
* Build a shared prompt hub for design, product, and engineering workflows.
* Invite collaborators around Figma API, MCP, prompt evaluation, docs, and automation.

## Setup and Validation

To set up the project, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/jozrftamson/hermes-figma-prompt-hub.git
```
2. Change into the project directory:
```bash
cd hermes-figma-prompt-hub
```
3. Create a virtual environment:
```bash
python3 -m venv .venv
```
4. Activate the virtual environment:
```bash
. .venv/bin/activate
```
5. Install the required dependencies:
```bash
pip install -r requirements.txt
```
6. Validate the repository:
```bash
python scripts/validate_repo.py
```

To validate a single prompt, use the following command:
```bash
python scripts/validate_prompt.py <prompt_id>
```
Replace `<prompt_id>` with the ID of the prompt you want to validate.

## Quickstart

For a quick start, you can use the following command to set up the project and validate the repository:
```bash
git clone https://github.com/jozrftamson/hermes-figma-prompt-hub.git
cd hermes-figma-prompt-hub
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python scripts/validate_repo.py
```
This will set up the project, install the required dependencies, and validate the repository.
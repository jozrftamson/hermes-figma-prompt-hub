# Getting Started

## Prerequisites

- Python 3.12 or newer
- Git
- GitHub CLI for maintainer automation

## Setup

```bash
git clone https://github.com/jozrftamson/hermes-figma-prompt-hub.git
cd hermes-figma-prompt-hub
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python scripts/validate_repo.py
```

## Validate a Prompt

```bash
python scripts/validate_prompt.py prompts/raw/nous-central-v1.json
```

## Add a Prompt

1. Copy an existing file from `prompts/raw`.
2. Change `id`, `version`, `category`, `variables`, and prompt content.
3. Add guardrails and eval checks.
4. Run validation:

```bash
python scripts/validate_repo.py
```

5. Regenerate the catalog if needed:

```bash
python scripts/generate_prompt_catalog.py
```

## Work on Figma Import

Use fixtures in `evals/cases` and the layer contract in `prompts/figma-layer-contract.txt`.

Do not commit real Figma tokens or private Figma file data.


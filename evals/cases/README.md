# Figma Importer Test Fixtures

This directory contains test fixtures for the Figma PROMPT frame importer.

## Fixtures

### `figma_prompt_example_v1.json`

Complete test fixture representing a Figma PROMPT frame that conforms to the layer contract.

**Metadata:**
- Created: July 12, 2026
- Purpose: Testing Figma layer contract compliance and frame extraction
- Privacy: No real Figma tokens or private file data included

**Structure:**
- METADATA group with prompt metadata (title, description, category, strategy, version)
- CONTENT group with system, user template, guardrails, and output format
- EXAMPLES group with sample input/output pairs
- STRATEGY_CONFIG group with chain-of-thought specific settings

## Usage

### Import Test Fixture

```bash
# With fixture support in importer
python3 scripts/figma_importer.py --fixture evals/cases/figma_prompt_example_v1.json

# Validate fixture structure
python3 scripts/figma_layer_validator.py evals/cases/figma_prompt_example_v1.json

# Validate fixture schema
python3 scripts/schema_validator.py evals/cases/figma_prompt_example_v1.json
```

### Validate Layer Contract

The fixture demonstrates all required layers:

```
✅ METADATA (group)
   ✅ title, description, category, strategy, version

✅ CONTENT (group)
   ✅ system, user_template, guardrails, output_format

✅ EXAMPLES (group)
   ✅ example_1 with input, output, explanation

✅ STRATEGY_CONFIG (group)
   ✅ num_steps, step_structure
```

## Adding New Fixtures

When adding new test fixtures:

1. Follow the layer contract structure (see `README.md`)
2. Use realistic but non-private example data
3. Include metadata with purpose and privacy notes
4. Update this README with the new fixture description
5. Test with both layer validator and schema validator

## Layer Contract Reference

See `README.md` "Figma Layer Contract" section for the authoritative layer structure.

#!/usr/bin/env python3
import json
import sys
import textwrap
from pathlib import Path


def project_root() -> Path:
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).expanduser().resolve()
    return Path(__file__).resolve().parents[1]


root = project_root()
paths = [
    "mcp",
    "scripts",
    "prompts/raw",
    "prompts/build",
    "prompts/schema",
    "evals/cases",
]

for path in paths:
    (root / path).mkdir(parents=True, exist_ok=True)

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": [
        "id",
        "version",
        "system",
        "developer",
        "user_template",
        "variables",
        "guardrails",
        "few_shots",
        "eval",
    ],
    "properties": {
        "id": {"type": "string"},
        "version": {"type": "string"},
        "status": {"type": "string", "enum": ["draft", "active", "deprecated"]},
        "category": {"type": "string"},
        "tags": {"type": "array", "items": {"type": "string"}},
        "model": {"type": "string"},
        "temperature": {"type": "number", "minimum": 0, "maximum": 2},
        "system": {"type": "string"},
        "developer": {"type": "string"},
        "user_template": {"type": "string"},
        "output_format": {
            "type": "object",
            "required": ["type"],
            "properties": {
                "type": {"type": "string", "enum": ["text", "markdown", "json"]},
                "schema": {"type": "object"},
                "instructions": {"type": "string"},
            },
        },
        "variables": {"type": "array", "items": {"type": "string"}},
        "context_sources": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "type"],
                "properties": {
                    "name": {"type": "string"},
                    "type": {"type": "string"},
                    "required": {"type": "boolean"},
                    "description": {"type": "string"},
                },
            },
        },
        "tools": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name"],
                "properties": {
                    "name": {"type": "string"},
                    "allowed": {"type": "boolean"},
                    "policy": {"type": "string"},
                },
            },
        },
        "guardrails": {"type": "array", "items": {"type": "string"}},
        "constraints": {"type": "array", "items": {"type": "string"}},
        "style_rules": {"type": "array", "items": {"type": "string"}},
        "few_shots": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["input", "output"],
                "properties": {
                    "input": {"type": "string"},
                    "output": {"type": "string"},
                    "notes": {"type": "string"},
                },
            },
        },
        "changelog": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["version", "changes"],
                "properties": {
                    "version": {"type": "string"},
                    "date": {"type": "string"},
                    "changes": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
        "eval": {
            "type": "object",
            "required": ["must_include", "must_not_include"],
            "properties": {
                "must_include": {"type": "array", "items": {"type": "string"}},
                "must_not_include": {"type": "array", "items": {"type": "string"}},
                "checks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["name", "type"],
                        "properties": {
                            "name": {"type": "string"},
                            "type": {
                                "type": "string",
                                "enum": [
                                    "contains",
                                    "not_contains",
                                    "regex",
                                    "json_schema",
                                    "max_length",
                                ],
                            },
                            "value": {},
                            "description": {"type": "string"},
                        },
                    },
                },
            },
        },
    },
}

example = {
    "id": "nous-central-v1",
    "version": "0.2.0",
    "status": "active",
    "category": "general-assistant",
    "tags": ["hermes", "figma", "prompt-hub"],
    "model": "gpt-4.1",
    "temperature": 0.2,
    "system": "Du bist ein präziser Assistent.",
    "developer": "Antwort kurz, korrekt, ohne Floskeln. Markiere Unsicherheit klar.",
    "user_template": "Kontext: {{context}}\nAufgabe: {{task}}\nGewünschtes Format: {{format}}",
    "output_format": {
        "type": "json",
        "instructions": "Return valid JSON with summary and next_actions.",
        "schema": {
            "type": "object",
            "required": ["summary", "next_actions"],
            "properties": {
                "summary": {"type": "string"},
                "next_actions": {"type": "array", "items": {"type": "string"}},
            },
        },
    },
    "variables": ["context", "task", "format"],
    "context_sources": [
        {
            "name": "figma_frame",
            "type": "figma",
            "required": False,
            "description": "Optional Figma frame or layer context.",
        }
    ],
    "tools": [
        {
            "name": "mcp",
            "allowed": True,
            "policy": "Use MCP tools for prompt listing, validation and export.",
        }
    ],
    "guardrails": [
        "Keine erfundenen Fakten",
        "Bei Unsicherheit klar markieren",
        "Keine privaten Tokens oder Secrets ausgeben",
    ],
    "constraints": ["Use only supplied context.", "Keep output concise."],
    "style_rules": ["Use direct language.", "Prefer actionable next steps."],
    "few_shots": [
        {
            "input": "context=Design notes\ntask=Summarize issues\nformat=json",
            "output": "{\"summary\":\"Kurzfassung ...\",\"next_actions\":[\"Review copy\"]}",
            "notes": "Shows compact JSON output.",
        }
    ],
    "changelog": [
        {
            "version": "0.2.0",
            "changes": ["Added output format, tools, constraints and eval checks"],
        },
        {"version": "0.1.0", "changes": ["Initial prompt scaffold"]},
    ],
    "eval": {
        "must_include": ["summary", "next_actions"],
        "must_not_include": ["Great question", "As an AI"],
        "checks": [
            {
                "name": "valid_json_output",
                "type": "json_schema",
                "value": {"type": "object", "required": ["summary", "next_actions"]},
            },
            {"name": "no_ai_disclaimer", "type": "not_contains", "value": "As an AI"},
        ],
    },
}

validate_py = textwrap.dedent(
    """\
    import json
    import sys
    from pathlib import Path

    from jsonschema import validate

    root = Path(__file__).resolve().parents[1]
    schema = json.loads((root / "prompts/schema/prompt.schema.json").read_text())
    target = Path(sys.argv[1])
    data = json.loads(target.read_text())
    validate(instance=data, schema=schema)
    print("OK:", target)
    """
)

contract = """Figma Layer Contract (Frame: PROMPT/<id>)
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
"""

(root / "prompts/schema/prompt.schema.json").write_text(
    json.dumps(schema, indent=2) + "\n", encoding="utf-8"
)
(root / "prompts/raw/nous-central-v1.json").write_text(
    json.dumps(example, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
)
(root / "scripts/validate_prompt.py").write_text(validate_py, encoding="utf-8")
(root / "prompts/figma-layer-contract.txt").write_text(contract, encoding="utf-8")

print("Scaffold created at:", root)

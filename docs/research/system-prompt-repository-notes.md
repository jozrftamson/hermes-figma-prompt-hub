# System prompt repository notes

Reference reviewed:

```text
https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools
```

Observed useful patterns:

- Large prompt collections need strict metadata, provenance, and license boundaries.
- Prompt catalogs should separate raw prompt content from analysis, summaries, and generated indexes.
- System prompts often include recurring sections: identity, tool policy, safety constraints, output format, workflow steps, and refusal rules.
- Public prompt collections create security risks when they expose internal behavior, tool names, or prompt extraction weaknesses.

License note:

The referenced repository is GPL-3.0 licensed. This project is MIT licensed, so do not copy prompt content, repository files, or code from that repository into this repository. Use only independently written tooling and high-level structural ideas.

Implemented from these observations:

- `scripts/import_prompt_text.py`: convert locally owned text prompts into this repository's JSON prompt schema.
- `scripts/analyze_prompt_patterns.py`: generate a pattern report from prompt files without copying external content.
- `scripts/security_prompt_audit.py`: flag prompt leakage and sensitive-data risks.


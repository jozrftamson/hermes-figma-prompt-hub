import argparse
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = ROOT / "prompts/raw"
OUTPUT_PATH = ROOT / "docs/prompt-patterns.md"


def load_prompts() -> list[tuple[Path, dict]]:
    prompts = []
    for path in sorted(PROMPTS_DIR.glob("*.json")):
        prompts.append((path, json.loads(path.read_text())))
    return prompts


def build_report() -> str:
    prompts = load_prompts()
    categories = Counter(prompt.get("category", "uncategorized") for _, prompt in prompts)
    tags = Counter(tag for _, prompt in prompts for tag in prompt.get("tags", []))
    output_formats = Counter(prompt.get("output_format", {}).get("type", "unspecified") for _, prompt in prompts)
    tools = Counter(tool.get("name", "unnamed") for _, prompt in prompts for tool in prompt.get("tools", []))
    eval_checks = Counter(check.get("type", "unknown") for _, prompt in prompts for check in prompt.get("eval", {}).get("checks", []))

    lines = [
        "# Prompt patterns",
        "",
        "Generated from `prompts/raw/*.json`.",
        "",
        f"Prompt count: `{len(prompts)}`",
        "",
        "## Categories",
        "",
    ]
    lines.extend(f"- `{name}`: {count}" for name, count in categories.most_common())
    lines.extend(["", "## Tags", ""])
    lines.extend(f"- `{name}`: {count}" for name, count in tags.most_common() or [("none", 0)])
    lines.extend(["", "## Output formats", ""])
    lines.extend(f"- `{name}`: {count}" for name, count in output_formats.most_common())
    lines.extend(["", "## Tools", ""])
    lines.extend(f"- `{name}`: {count}" for name, count in tools.most_common() or [("none", 0)])
    lines.extend(["", "## Eval check types", ""])
    lines.extend(f"- `{name}`: {count}" for name, count in eval_checks.most_common() or [("none", 0)])
    lines.extend(["", "## Prompt details", ""])

    for path, prompt in prompts:
        lines.extend(
            [
                f"### {prompt.get('id', path.stem)}",
                "",
                f"- File: `{path.relative_to(ROOT)}`",
                f"- Version: `{prompt.get('version', 'unknown')}`",
                f"- Status: `{prompt.get('status', 'unknown')}`",
                f"- Guardrails: `{len(prompt.get('guardrails', []))}`",
                f"- Constraints: `{len(prompt.get('constraints', []))}`",
                f"- Style rules: `{len(prompt.get('style_rules', []))}`",
                f"- Eval checks: `{len(prompt.get('eval', {}).get('checks', []))}`",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze prompt patterns and generate docs/prompt-patterns.md")
    parser.add_argument("--check", action="store_true", help="Fail if generated report is stale")
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()

    output = args.output if args.output.is_absolute() else ROOT / args.output
    report = build_report()
    if args.check:
        existing = output.read_text() if output.exists() else ""
        if existing != report:
            raise SystemExit(f"{output.relative_to(ROOT)} is stale. Run scripts/analyze_prompt_patterns.py")
        print("OK: prompt pattern report is current")
        return

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")
    print(f"Wrote {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()


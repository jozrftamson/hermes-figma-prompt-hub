import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = ROOT / "prompts/raw"
OUTPUT_PATH = ROOT / "docs/prompt-catalog.md"


def load_prompt(path: Path) -> dict:
    return json.loads(path.read_text())


def render_prompt(prompt: dict, path: Path) -> str:
    title = prompt.get("id", path.stem)
    version = prompt.get("version", "unknown")
    status = prompt.get("status", "unknown")
    category = prompt.get("category", "uncategorized")
    tags = ", ".join(prompt.get("tags", [])) or "none"
    variables = ", ".join(prompt.get("variables", [])) or "none"
    output_type = prompt.get("output_format", {}).get("type", "unspecified")
    checks = prompt.get("eval", {}).get("checks", [])
    check_names = ", ".join(check.get("name", "unnamed") for check in checks) or "none"

    return "\n".join(
        [
            f"## {title}",
            "",
            f"- File: `{path.relative_to(ROOT)}`",
            f"- Version: `{version}`",
            f"- Status: `{status}`",
            f"- Category: `{category}`",
            f"- Tags: {tags}",
            f"- Variables: {variables}",
            f"- Output format: `{output_type}`",
            f"- Eval checks: {check_names}",
            "",
        ]
    )


def build_catalog() -> str:
    prompt_paths = sorted(PROMPTS_DIR.glob("*.json"))
    lines = [
        "# Prompt catalog",
        "",
        "This file is generated from `prompts/raw/*.json`.",
        "",
    ]

    if not prompt_paths:
        lines.append("No prompts found.")
        lines.append("")
        return "\n".join(lines)

    for path in prompt_paths:
        lines.append(render_prompt(load_prompt(path), path))

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate docs/prompt-catalog.md")
    parser.add_argument("--check", action="store_true", help="Fail if catalog is stale")
    args = parser.parse_args()

    content = build_catalog()
    if args.check:
        existing = OUTPUT_PATH.read_text() if OUTPUT_PATH.exists() else ""
        if existing != content:
            raise SystemExit("docs/prompt-catalog.md is stale. Run scripts/generate_prompt_catalog.py")
        print("OK: prompt catalog is current")
        return

    OUTPUT_PATH.write_text(content, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()


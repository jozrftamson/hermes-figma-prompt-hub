import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "prompts/figma-layer-contract.txt"
README_PATH = ROOT / "README.md"
FIXTURES_DIR = ROOT / "evals/cases"


def contract_entries() -> list[str]:
    entries = []
    for line in CONTRACT_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("Figma Layer Contract"):
            continue
        entries.append(line)
    return entries


def entry_pattern(entry: str) -> re.Pattern[str]:
    escaped = re.escape(entry)
    escaped = escaped.replace(re.escape("<n>"), r"\d+")
    escaped = escaped.replace(re.escape("<name>"), r"[A-Za-z0-9_-]+")
    escaped = escaped.replace(re.escape("<version>"), r"[A-Za-z0-9_.-]+")
    return re.compile(rf'"name":\s*"{escaped}"|{escaped}')


def main() -> None:
    entries = contract_entries()
    readme = README_PATH.read_text()
    fixture_text = "\n".join(path.read_text() for path in sorted(FIXTURES_DIR.glob("*.json")))

    errors = []
    for entry in entries:
        if entry not in readme:
            errors.append(f"README is missing contract entry `{entry}`")
        if not entry_pattern(entry).search(fixture_text):
            errors.append(f"Fixtures are missing an example for `{entry}`")

    if errors:
        print("Figma contract check failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("OK: Figma contract matches README and fixtures")


if __name__ == "__main__":
    main()


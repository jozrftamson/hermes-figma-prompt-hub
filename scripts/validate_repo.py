import json
from pathlib import Path

from validate_prompt import PromptValidationError, validate_prompt


ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = ROOT / "prompts/raw"
JSON_DIRS = [
    ROOT / "prompts/raw",
    ROOT / "prompts/schema",
    ROOT / "evals/cases",
]


def validate_json_files() -> list[str]:
    errors: list[str] = []
    for directory in JSON_DIRS:
        for path in sorted(directory.glob("*.json")):
            try:
                json.loads(path.read_text())
            except json.JSONDecodeError as exc:
                errors.append(
                    f"{path.relative_to(ROOT)}: invalid JSON at line {exc.lineno}, "
                    f"column {exc.colno}: {exc.msg}"
                )
    return errors


def validate_prompts() -> list[str]:
    errors: list[str] = []
    prompt_files = sorted(PROMPTS_DIR.glob("*.json"))
    if not prompt_files:
        errors.append("No prompt files found under prompts/raw")
        return errors

    for path in prompt_files:
        try:
            validate_prompt(path)
        except PromptValidationError as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
    return errors


def main() -> None:
    errors = []
    errors.extend(validate_json_files())
    errors.extend(validate_prompts())

    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("OK: repository validation passed")


if __name__ == "__main__":
    main()


import argparse
import json
from pathlib import Path

from jsonschema import SchemaError, ValidationError, validate


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "prompts/schema/prompt.schema.json"


class PromptValidationError(Exception):
    """Raised when a prompt file cannot be loaded or validated."""


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError as exc:
        raise PromptValidationError(f"File not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise PromptValidationError(
            f"Invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def format_validation_error(error: ValidationError) -> str:
    location = ".".join(str(part) for part in error.absolute_path)
    if not location:
        location = "<root>"
    return f"Schema validation failed at {location}: {error.message}"


def validate_prompt(target: Path) -> None:
    schema = load_json(SCHEMA_PATH)
    data = load_json(target)

    try:
        validate(instance=data, schema=schema)
    except SchemaError as exc:
        raise PromptValidationError(
            f"Invalid prompt schema in {SCHEMA_PATH}: {exc.message}"
        ) from exc
    except ValidationError as exc:
        raise PromptValidationError(format_validation_error(exc)) from exc


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a prompt JSON file.")
    parser.add_argument("prompt", type=Path, help="Path to the prompt JSON file")
    args = parser.parse_args()

    try:
        validate_prompt(args.prompt)
    except PromptValidationError as exc:
        raise SystemExit(str(exc)) from exc

    print("OK:", args.prompt)


if __name__ == "__main__":
    main()


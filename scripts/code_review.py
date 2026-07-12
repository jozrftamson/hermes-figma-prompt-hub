import argparse
import json
import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SECRET_PATTERNS = [
    re.compile(r"figd_[A-Za-z0-9_-]{12,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"(?i)(api[_-]?key|token|secret)\s*[:=]\s*['\"][^'\"]{12,}['\"]"),
]


@dataclass
class Finding:
    severity: str
    path: str
    message: str
    code: str
    line: int | None = None


def run(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout


def changed_files(base: str) -> list[str]:
    output = run(["git", "diff", "--name-only", f"{base}...HEAD"])
    return [line.strip() for line in output.splitlines() if line.strip()]


def read_text(path: str) -> str:
    try:
        return (ROOT / path).read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""
    except FileNotFoundError:
        return ""


def first_matching_line(path: str, patterns: list[re.Pattern[str]]) -> int | None:
    text = read_text(path)
    for index, line in enumerate(text.splitlines(), start=1):
        if any(pattern.search(line) for pattern in patterns):
            return index
    return None


def json_data(path: str) -> dict[str, Any] | None:
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError:
        return None


def add_finding(findings: list[Finding], severity: str, path: str, message: str, code: str, line: int | None = None) -> None:
    findings.append(Finding(severity=severity, path=path, message=message, code=code, line=line))


def review_prompt_semantics(files: list[str], findings: list[Finding]) -> None:
    for path in files:
        if not path.startswith("prompts/raw/") or not path.endswith(".json"):
            continue
        data = json_data(path)
        if data is None:
            add_finding(findings, "error", path, "Prompt file is not valid JSON.", "prompt-invalid-json", 1)
            continue
        checks = data.get("eval", {}).get("checks")
        if not checks:
            add_finding(findings, "warning", path, "Prompt should define `eval.checks` for quality validation.", "prompt-missing-eval-checks", 1)
        if not data.get("guardrails"):
            add_finding(findings, "warning", path, "Prompt should define `guardrails`.", "prompt-missing-guardrails", 1)
        if not data.get("output_format"):
            add_finding(findings, "warning", path, "Prompt should define `output_format`.", "prompt-missing-output-format", 1)
        if not data.get("changelog"):
            add_finding(findings, "info", path, "Prompt should include `changelog` entries for format changes.", "prompt-missing-changelog", 1)


def review_workflow_security(files: list[str], findings: list[Finding]) -> None:
    for path in files:
        if not path.startswith(".github/workflows/"):
            continue
        text = read_text(path)
        if "permissions:" not in text:
            add_finding(findings, "warning", path, "Workflow should declare minimal `permissions`.", "workflow-missing-permissions", 1)
        if "contents: write" in text:
            line = first_matching_line(path, [re.compile(r"contents:\s*write")])
            add_finding(findings, "info", path, "Workflow uses `contents: write`; confirm this is required.", "workflow-contents-write", line)
        if "pull_request_target" in text:
            line = first_matching_line(path, [re.compile(r"pull_request_target")])
            add_finding(
                findings,
                "warning",
                path,
                "`pull_request_target` needs careful review because it runs with elevated repository context.",
                "workflow-pull-request-target",
                line,
            )
            if "checkout@v4" in text:
                checkout_line = first_matching_line(path, [re.compile(r"checkout@v4")])
                add_finding(
                    findings,
                    "warning",
                    path,
                    "`pull_request_target` with checkout can expose tokens to untrusted PR code. Avoid checking out PR code in this context.",
                    "workflow-pr-target-checkout",
                    checkout_line,
                )
        if re.search(r"\$\{\{\s*github\.event\.pull_request\.(title|body|head\.ref)", text):
            line = first_matching_line(path, [re.compile(r"github\.event\.pull_request")])
            add_finding(findings, "warning", path, "Workflow appears to use untrusted PR input. Quote and sanitize before shell use.", "workflow-untrusted-pr-input", line)


def review_files(files: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    changed = set(files)

    for path in files:
        text = read_text(path)
        if "__pycache__" in path or path.endswith(".pyc"):
            add_finding(findings, "error", path, "Generated Python cache files should not be committed.", "generated-cache")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                add_finding(
                    findings,
                    "error",
                    path,
                    "Possible token, API key, or secret found. Remove it before merge.",
                    "possible-secret",
                    first_matching_line(path, SECRET_PATTERNS),
                )

    review_prompt_semantics(files, findings)
    review_workflow_security(files, findings)

    if any(path.startswith("prompts/raw/") for path in files) and "docs/prompt-catalog.md" not in changed:
        add_finding(findings, "warning", "docs/prompt-catalog.md", "Prompt files changed but the generated prompt catalog was not updated.", "prompt-catalog-stale")

    if "prompts/figma-layer-contract.txt" in changed:
        expected = {"README.md", "evals/cases/figma-extended-prompt-frame.json"}
        missing = [path for path in expected if path not in changed]
        if missing:
            add_finding(findings, "warning", "prompts/figma-layer-contract.txt", f"Figma contract changed; consider updating related files: {', '.join(missing)}.", "figma-contract-related-files", 1)

    if "prompts/schema/prompt.schema.json" in changed:
        expected = {"README.md", "prompts/raw/nous-central-v1.json"}
        missing = [path for path in expected if path not in changed]
        if missing:
            add_finding(findings, "warning", "prompts/schema/prompt.schema.json", f"Schema changed; consider updating docs/examples: {', '.join(missing)}.", "schema-related-files", 1)

    return findings


def routing_labels(files: list[str], findings: list[Finding]) -> list[str]:
    labels = set()
    if any(path.startswith("prompts/") for path in files):
        labels.add("needs-prompt-review")
    if any(path.startswith("mcp/") for path in files):
        labels.add("needs-mcp-review")
    if any(path.endswith(".md") or path.startswith("docs/") for path in files):
        labels.add("needs-docs-review")
    if any(path.startswith(".github/") for path in files) or any(finding.severity == "error" for finding in findings):
        labels.add("needs-security-review")
    return sorted(labels)


def quality_score(files: list[str], findings: list[Finding]) -> tuple[int, list[str]]:
    score = 100
    notes = []
    errors = sum(1 for finding in findings if finding.severity == "error")
    warnings = sum(1 for finding in findings if finding.severity == "warning")
    score -= errors * 30
    score -= warnings * 10
    if len(files) > 12:
        score -= 10
        notes.append("Large PR: more than 12 files changed.")
    if not any(path.endswith(".md") or path.startswith("docs/") for path in files):
        score -= 5
        notes.append("No docs update detected.")
    if not any(path.startswith("evals/") or "test" in path for path in files):
        score -= 5
        notes.append("No tests or eval fixtures changed.")
    if not findings:
        notes.append("No automated review findings.")
    return max(score, 0), notes


def render_markdown(files: list[str], findings: list[Finding], labels: list[str], score: int, score_notes: list[str]) -> str:
    lines = [
        "## Automated code review",
        "",
        "This review is generated by repository automation. It does not replace maintainer review.",
        "",
        "Severity policy:",
        "- `error`: blocks the PR until fixed.",
        "- `warning`: does not block, but should be reviewed.",
        "- `info`: advisory only.",
        "",
        f"Changed files reviewed: `{len(files)}`",
        f"PR quality score: `{score}/100`",
        f"Suggested labels: {', '.join(f'`{label}`' for label in labels) or '`none`'}",
        "",
    ]
    if score_notes:
        lines.extend(["Score notes:", ""])
        lines.extend(f"- {note}" for note in score_notes)
        lines.append("")
    if not findings:
        lines.extend(
            [
                "No blocking findings detected by the automated checks.",
                "",
                "Maintainer checklist:",
                "- Confirm the change matches the issue or PR scope.",
                "- Confirm validation output is included in the PR.",
                "- Review behavior manually for docs, workflows, and prompt semantics.",
                "",
            ]
        )
        return "\n".join(lines)

    lines.extend(["### Findings", ""])
    severity_order = {"error": 0, "warning": 1, "info": 2}
    for finding in sorted(findings, key=lambda item: severity_order.get(item.severity, 99)):
        location = f"{finding.path}:{finding.line}" if finding.line else finding.path
        lines.append(f"- **{finding.severity.upper()}** `{location}` `{finding.code}`: {finding.message}")
    lines.extend(
        [
            "",
            "Suggested validation:",
            "",
            "```bash",
            "python scripts/validate_repo.py",
            "python -m py_compile install/scaffold.py scripts/*.py",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an automated PR code review.")
    parser.add_argument("--base", default="origin/main", help="Base ref to diff against")
    parser.add_argument("--output", type=Path, default=ROOT / "docs/code-review-report.md")
    parser.add_argument("--json-output", type=Path, default=ROOT / "docs/code-review-findings.json")
    args = parser.parse_args()

    files = changed_files(args.base)
    findings = review_files(files)
    labels = routing_labels(files, findings)
    score, score_notes = quality_score(files, findings)

    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_markdown(files, findings, labels, score, score_notes), encoding="utf-8")

    json_output = args.json_output if args.json_output.is_absolute() else ROOT / args.json_output
    write_json(
        json_output,
        {
            "changed_files": files,
            "findings": [asdict(finding) for finding in findings],
            "labels": labels,
            "score": score,
            "score_notes": score_notes,
            "has_errors": any(finding.severity == "error" for finding in findings),
        },
    )
    print(f"Wrote {output.relative_to(ROOT)}")
    print(f"Wrote {json_output.relative_to(ROOT)}")
    if any(finding.severity == "error" for finding in findings):
        raise SystemExit(1)


if __name__ == "__main__":
    main()


import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs/automation-health.md"
REPO = "jozrftamson/hermes-figma-prompt-hub"


@dataclass
class FailedStep:
    job: str
    step: str
    conclusion: str
    job_url: str


@dataclass
class FailedRun:
    run_id: int
    workflow: str
    conclusion: str
    event: str
    created_at: str
    head_sha: str
    url: str
    failed_steps: list[FailedStep]


def run_command(args: list[str]) -> str:
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout


def gh_json(args: list[str]) -> object:
    return json.loads(run_command(["gh", *args]))


def list_failed_runs(limit: int) -> list[dict]:
    runs = gh_json(
        [
            "run",
            "list",
            "--repo",
            REPO,
            "--limit",
            str(limit),
            "--json",
            "databaseId,workflowName,status,conclusion,event,createdAt,updatedAt,url,headSha",
        ]
    )
    return [
        run
        for run in runs
        if run.get("status") == "completed"
        and run.get("conclusion") not in {"success", "skipped", "neutral"}
    ]


def inspect_run(run: dict) -> FailedRun:
    details = gh_json(
        [
            "run",
            "view",
            str(run["databaseId"]),
            "--repo",
            REPO,
            "--json",
            "jobs,workflowName,conclusion,event,url,createdAt,headSha",
        ]
    )
    failed_steps = []
    for job in details.get("jobs", []):
        job_conclusion = job.get("conclusion")
        if job_conclusion in {"success", "skipped", "neutral"}:
            continue
        for step in job.get("steps", []):
            step_conclusion = step.get("conclusion")
            if step_conclusion and step_conclusion not in {"success", "skipped", "neutral"}:
                failed_steps.append(
                    FailedStep(
                        job=job.get("name", "unknown job"),
                        step=step.get("name", "unknown step"),
                        conclusion=step_conclusion,
                        job_url=job.get("url", details.get("url", "")),
                    )
                )
        if not failed_steps:
            failed_steps.append(
                FailedStep(
                    job=job.get("name", "unknown job"),
                    step="unknown failing step",
                    conclusion=job_conclusion or "failure",
                    job_url=job.get("url", details.get("url", "")),
                )
            )

    return FailedRun(
        run_id=run["databaseId"],
        workflow=details.get("workflowName") or run.get("workflowName") or "unknown workflow",
        conclusion=details.get("conclusion") or run.get("conclusion") or "failure",
        event=details.get("event") or run.get("event") or "unknown",
        created_at=details.get("createdAt") or run.get("createdAt") or "",
        head_sha=(details.get("headSha") or run.get("headSha") or "")[:12],
        url=details.get("url") or run.get("url") or "",
        failed_steps=failed_steps,
    )


def infer_reason(run: FailedRun) -> str:
    text = " ".join([run.workflow, *(step.step for step in run.failed_steps)]).lower()
    if "install" in text or "pip" in text or "dependencies" in text:
        return "Likely dependency installation or package resolution failure."
    if "validate" in text or "prompt" in text or "schema" in text:
        return "Likely prompt/schema/catalog validation drift."
    if "figma contract" in text or "contract" in text:
        return "Likely mismatch between Figma contract, README, and fixtures."
    if "scout" in text or "gh " in text or "github" in text:
        return "Likely GitHub API, token permission, rate limit, or search query issue."
    if "issue" in text or "pull request" in text or "comment" in text:
        return "Likely GitHub issue/PR permission or label automation issue."
    if "release" in text:
        return "Likely release planning workflow or label creation issue."
    return "Needs manual log review. Start with the failed step and job URL."


def suggest_automation(run: FailedRun) -> list[str]:
    suggestions = [
        "Add a local reproduction command to the failing workflow step.",
        "Add clearer error output before the failing command exits.",
    ]
    text = " ".join([run.workflow, *(step.step for step in run.failed_steps)]).lower()
    if "gh" in text or "github" in text or "issue" in text:
        suggestions.append("Add preflight checks for GitHub token permissions and required labels.")
    if "validate" in text or "schema" in text or "prompt" in text:
        suggestions.append("Add an auto-generated repair hint that names the stale file to regenerate.")
    if "scout" in text:
        suggestions.append("Cache the scout report and reduce search limits when rate limits are detected.")
    return suggestions


def issue_title(run: FailedRun) -> str:
    return f"automation failure: {run.workflow} run {run.run_id}"


def issue_body(run: FailedRun) -> str:
    failed_steps = "\n".join(
        f"- Job `{step.job}`, step `{step.step}`: `{step.conclusion}` ([job log]({step.job_url}))"
        for step in run.failed_steps
    )
    suggestions = "\n".join(f"- {item}" for item in suggest_automation(run))
    return f"""Automation failure detected.

## Summary

- Workflow: `{run.workflow}`
- Run ID: `{run.run_id}`
- Conclusion: `{run.conclusion}`
- Event: `{run.event}`
- Commit: `{run.head_sha}`
- Created: `{run.created_at}`
- Run: {run.url}

## Failed jobs or steps

{failed_steps or "- No failed step metadata available. Open the run logs."}

## Likely reason

{infer_reason(run)}

## Suggested follow-up automation

{suggestions}

## Maintainer checklist

- [ ] Open the run logs and confirm the root cause.
- [ ] Reproduce locally where possible.
- [ ] Patch the workflow or script.
- [ ] Add a guard so the same failure becomes easier to diagnose next time.
"""


def existing_issue_titles() -> set[str]:
    issues = gh_json(
        [
            "issue",
            "list",
            "--repo",
            REPO,
            "--state",
            "open",
            "--search",
            "automation failure:",
            "--json",
            "title",
            "--limit",
            "100",
        ]
    )
    return {issue["title"] for issue in issues}


def ensure_label(name: str, color: str, description: str) -> None:
    result = subprocess.run(
        ["gh", "label", "create", name, "--repo", REPO, "--color", color, "--description", description, "--force"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())


def create_issues(runs: list[FailedRun]) -> None:
    ensure_label("automation-failure", "d73a4a", "Failure detected in repository automation")
    ensure_label("automation-improvement", "1d76db", "Follow-up work to improve automation")
    existing = existing_issue_titles()
    for run in runs:
        title = issue_title(run)
        if title in existing:
            print(f"Skipping existing issue: {title}")
            continue
        run_command(
            [
                "gh",
                "issue",
                "create",
                "--repo",
                REPO,
                "--title",
                title,
                "--body",
                issue_body(run),
                "--label",
                "automation-failure,automation-improvement",
            ]
        )
        print(f"Created issue: {title}")


def render_report(runs: list[FailedRun]) -> str:
    lines = [
        "# Automation health",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "",
    ]
    if not runs:
        lines.extend(
            [
                "No failed automation runs found in the scanned window.",
                "",
                "## Suggested next automation improvements",
                "",
                "- Keep failure diagnostics scheduled daily.",
                "- Add workflow-specific preflight checks when a new automation is introduced.",
                "- Keep local commands documented for every CI step.",
                "",
            ]
        )
        return "\n".join(lines)

    for run in runs:
        lines.extend(
            [
                f"## {run.workflow} run {run.run_id}",
                "",
                f"- Conclusion: `{run.conclusion}`",
                f"- Event: `{run.event}`",
                f"- Commit: `{run.head_sha}`",
                f"- Created: `{run.created_at}`",
                f"- Run: {run.url}",
                f"- Likely reason: {infer_reason(run)}",
                "",
                "Failed jobs or steps:",
                "",
            ]
        )
        for step in run.failed_steps:
            lines.append(f"- `{step.job}` / `{step.step}`: `{step.conclusion}` - {step.job_url}")
        lines.extend(["", "Suggested follow-up automation:", ""])
        lines.extend(f"- {item}" for item in suggest_automation(run))
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Diagnose failed GitHub Actions runs.")
    parser.add_argument("--limit", type=int, default=30, help="Number of recent runs to scan")
    parser.add_argument("--create-issues", action="store_true", help="Create GitHub issues for failures")
    parser.add_argument("--report", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    failed_runs = [inspect_run(run) for run in list_failed_runs(args.limit)]
    args.report.write_text(render_report(failed_runs), encoding="utf-8")
    print(f"Wrote {args.report.relative_to(ROOT)}")

    if args.create_issues and failed_runs:
        create_issues(failed_runs)
    elif args.create_issues:
        print("No failures found; no issues created.")


if __name__ == "__main__":
    main()


# GitHub Actions: Auto-Create PR for Resolved Issues

Zwei GitHub Actions zur Automatisierung der Pull Request Erstellung aus gelösten Issues.

## Actions Übersicht

### 1. Auto-Create PR for Resolved Issues
**File:** `.github/workflows/auto-create-pr.yml`

Erstellt automatisch eine Pull Request für jedes geschlossene Issue.

#### Trigger
- **Automatically:** Wenn ein Issue geschlossen wird (`issues.closed`)
- **Manually:** Via GitHub UI (`workflow_dispatch`)

#### Funktionsweise
```
Issue wird geschlossen
    ↓
GitHub Action triggert
    ↓
Findet alle Commits mit #issue_number
    ↓
Erstellt Feature Branch
    ↓
Erstellt Pull Request
    ↓
Kommentiert Issue mit PR Link
```

#### Verwendung

**Automatisch (beim Issue Schließen):**
```
1. Issue schließen auf GitHub
2. Action triggert automatisch
3. PR wird erstellt
4. Comment auf Issue mit PR Link
```

**Manuell (via Workflow Dispatch):**
```bash
# Via GitHub CLI
gh workflow run auto-create-pr.yml -f issue_number=42

# Or visit GitHub Actions Tab:
# Actions → Auto-Create PR for Resolved Issues → Run workflow
```

#### Output
```
✅ PR #25 created successfully!
- Closes: Issue #42
- Branch: feature/issue-42-my-issue-title
- Status: Draft
- Commits: 3
```

---

### 2. Auto-Consolidate Resolved Issues into PR
**File:** `.github/workflows/auto-consolidate-issues.yml`

Batcht mehrere gelöste Issues in eine einzelne Pull Request.

#### Trigger
- **Automatically:** Wenn Issues geschlossen werden
- **Manually:** Via Workflow Dispatch mit `batch_size` Parameter

#### Funktionsweise
```
Multiple Issues werden geschlossen
    ↓
GitHub Action sammelt alle
    ↓
Gruppiert ihre Commits
    ↓
Erstellt ONE Pull Request
    ↓
Verlinkt alle Issues zur PR
```

#### Verwendung

**Automatisch (Standard):**
```
1. Issues schließen
2. Action batcht automatisch bis zu 5 Issues
3. Erstellt konsolidierte PR
4. Kommentiert alle Issues
```

**Mit Custom Batch Size:**
```bash
gh workflow run auto-consolidate-issues.yml -f batch_size=10
```

#### Output
```
✅ Consolidated PR #26 created!
- Closes: #40, #41, #42
- Commits: 8 total
- Issues: 3
- Branch: feature/resolve-issues-batch-20241013-120000
```

---

## Features

### Auto-Create PR
- ✅ Detektiert geschlossene Issues automatisch
- ✅ Sucht nach verwandten Commits (mit #issue_number)
- ✅ Erstellt Feature Branch
- ✅ Generiert aussagekräftige PR Description
- ✅ Erstellt Draft PR
- ✅ Kommentiert Issue mit PR Link
- ✅ Unterstützt manuelle Triggers

### Auto-Consolidate
- ✅ Batcht mehrere Issues zusammen
- ✅ Sammelt alle Commits
- ✅ Erstellt One PR pro Batch
- ✅ Verlinkt alle geschlossenen Issues
- ✅ Fügt "in-pr" Label hinzu
- ✅ Konfigurierbarer Batch Size

---

## Installation

### 1. Kopiere Workflow Files
```bash
# Files sind bereits in .github/workflows/

# auto-create-pr.yml
# auto-consolidate-issues.yml
```

### 2. Pushe zu GitHub
```bash
git add .github/workflows/auto-*.yml
git commit -m "ci: Add auto-PR creation workflows"
git push origin main
```

### 3. Verify Actions
```bash
# Via GitHub UI:
# Settings → Actions → General → Workflows
# Du solltest beide Actions sehen
```

---

## Konfiguration

### Auto-Create PR Config

In `.github/workflows/auto-create-pr.yml`:

```yaml
# Trigger nur bei bestimmten Labels
on:
  issues:
    types: [closed]
    # Optional: Nur mit bestimmtem Label
```

### Auto-Consolidate Config

In `.github/workflows/auto-consolidate-issues.yml`:

```yaml
# Default batch size: 5 issues
# Überschreibbar via workflow_dispatch input
batch_size: 5  # Ändere hier für andere Default
```

---

## Commit Message Konvention

Für beste Ergebnisse, verwende diese Commit Konvention:

```bash
# Fix resolves single issue
git commit -m "fix(#42): Improve validator error messages"

# Feature resolves multiple issues
git commit -m "feat(#40, #41, #42): Add MCP server and validator"

# Optional: Link issues in PR/Commit body
git commit -m "fix: Resolve validator issues

Closes #40
Closes #41
Closes #42"
```

---

## Beispiele

### Beispiel 1: Single Issue → Single PR

```
1. Issue #42 wird geschlossen
   Title: "Improve validator error messages"

2. Action findet Commits:
   - d28ceca: fix(#42): improve validator error messages

3. Erstellt PR:
   - Title: "Resolve Issue #42: Improve validator error messages"
   - Branch: feature/issue-42-improve-validator-error-messages
   - Commits: 1
   - Status: Draft

4. Kommentiert Issue:
   "🚀 Pull Request Automatically Created
    This issue has been resolved and a PR has been created: #25"
```

### Beispiel 2: Multiple Issues → Consolidated PR

```
1. Issues #40, #41, #42 werden geschlossen

2. Action sammelt:
   - Issue #40: 2 Commits
   - Issue #41: 3 Commits
   - Issue #42: 2 Commits
   - Total: 7 Commits

3. Erstellt consolidierte PR:
   - Title: "feat: Resolve Issues - Batch #3 (#40, #41, #42)"
   - Branch: feature/resolve-issues-batch-20241013-120000
   - Commits: 7 total
   - Status: Ready for Review

4. Labels & Links:
   - Alle Issues bekommen "in-pr" Label
   - Alle Issues bekommen Kommentar mit PR Link
```

---

## Permissions & Tokens

Die Actions nutzen `GITHUB_TOKEN` für:
- ✅ Lesen von Issues
- ✅ Lesen von Commits
- ✅ Erstellen von PRs
- ✅ Kommentieren auf Issues
- ✅ Ändern von Labels

**KEINE** zusätzlichen Tokens erforderlich!

```yaml
permissions:
  contents: read
  issues: read
  pull-requests: write
```

---

## Troubleshooting

### Problem: Action triggert nicht
**Lösung:**
```bash
# Check workflow status
gh workflow list

# Enable workflow if disabled
gh workflow enable auto-create-pr.yml
gh workflow enable auto-consolidate-issues.yml

# Run manually to test
gh workflow run auto-create-pr.yml
```

### Problem: PR nicht erstellt
**Gründe:**
- Keine Commits mit #issue_number gefunden
- PR existiert bereits
- Insufficient permissions

**Debug:**
```bash
# Check recent workflow runs
gh run list --workflow auto-create-pr.yml --limit 5

# View run logs
gh run view <run_id> --log
```

### Problem: Falsche Branch Erstellt
**Lösung:**
```bash
# Manuell löschen und PR neu erstellen
git push origin --delete wrong-branch
gh pr close <pr_number>
```

---

## Best Practices

1. **Commit Naming:** Immer `#issue_number` in Commit Message verwenden
   ```bash
   git commit -m "fix(#42): description"
   ```

2. **Issue Closing:** Nutze GitHub's Auto-Close Feature
   ```bash
   git commit -m "fix: description
   
   Closes #42"
   ```

3. **Batch Size:** Für kleine Teams: 3-5, für große Teams: 5-10

4. **Review Process:** Draft PRs geben Zeit zum Review vor automatischem Merge

5. **Labels:** Nutze "in-pr" Label um offene PRs zu filtern
   ```bash
   gh issue list --label "in-pr"
   ```

---

## Erweiterte Konfiguration

### Custom PR Templates

Ändere PR Description in Workflows:

```yaml
# In auto-create-pr.yml
PR_BODY="## Automated PR for Issue #$ISSUE_NUMBER
...
custom content here
..."
```

### Branch Naming Strategy

```yaml
# Aktuell: feature/issue-42-title
# Änderbar zu:
BRANCH_NAME="issue/$ISSUE_NUMBER"  # issue/42
BRANCH_NAME="resolve/$ISSUE_NUMBER"  # resolve/42
BRANCH_NAME="fix/$ISSUE_NUMBER"  # fix/42
```

### Conditional PR Creation

Filter nach Labels:

```yaml
# Nur Issues mit "auto-pr" Label
if: contains(github.event.issue.labels.*.name, 'auto-pr')
```

---

## Integrationen

### Mit GitHub Projects
```bash
# Auto-add PR zu Project
gh pr create --title "..." --project-v2 <project_id>
```

### Mit Slack Notifications
```yaml
# Füge Slack Action hinzu
- name: Notify Slack
  uses: slackapi/slack-github-action@v1
```

### Mit CI/CD
```yaml
# Auto-merge nach Tests
- name: Auto-merge PR
  if: github.event.check_suite.conclusion == 'success'
  run: gh pr merge $PR_NUMBER --auto
```

---

## Deaktivieren

Falls Actions deaktiviert werden sollen:

```bash
# Deaktiviere Workflow
gh workflow disable auto-create-pr.yml
gh workflow disable auto-consolidate-issues.yml

# Oder lösche Files
git rm .github/workflows/auto-*.yml
git commit -m "ci: Remove auto-PR workflows"
git push origin main
```

---

## Support & Questions

Für Fragen oder Issues mit den Workflows:
1. Check GitHub Actions Logs
2. Verify commit messages have #issue_number
3. Check permissions in repository settings
4. Report issue in GitHub Issues

---

## See Also

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub CLI Reference](https://cli.github.com/manual/)
- [Hermes Project README](../README.md)

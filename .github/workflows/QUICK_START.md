# Auto-PR Creation: Quick Start

Schnelle Anleitung für automatische Pull Request Erstellung aus gelösten Issues.

## 🚀 30-Sekunden Setup

Die Actions sind bereits konfiguriert und aktiv!

**Nur 1 Sache erforderlich:** Commit Messages mit `#issue_number` verwenden.

```bash
# ✅ Correct
git commit -m "fix(#42): improve error messages"

# ❌ Wrong (Action kann Issue nicht finden)
git commit -m "fix: improve error messages"
```

---

## 🔄 Workflow

### Automatisch (Standard)

```
1. Issue auf GitHub schließen
   ↓
2. Action triggert automatisch
   ↓
3. Sucht nach Commits mit #issue_number
   ↓
4. Erstellt Pull Request
   ↓
5. Kommentiert Issue mit PR Link
```

### Manuell

```bash
# Trigger Action für spezifisches Issue
gh workflow run auto-create-pr.yml -f issue_number=42
```

---

## 📊 Was passiert?

### Single Issue
```
Issue #42 geschlossen
    ↓
Findet 1-3 Commits
    ↓
Erstellt PR #25
    ↓
Branch: feature/issue-42-...
    ↓
Status: Draft (Bereit zum Review)
```

### Multiple Issues (Auto-Consolidate)
```
Issues #40, #41, #42 geschlossen
    ↓
Findet alle Commits
    ↓
Erstellt ONE PR für alle 3
    ↓
Branch: feature/resolve-issues-batch-...
    ↓
Verlinkt alle Issues
```

---

## 💡 Beispiele

### Beispiel 1: Einzelnes Issue

```bash
# 1. Fix Validator Issue
git commit -m "fix(#3): improve validator error messages"

# 2. Pushe
git push origin main

# 3. Schließe Issue #3 auf GitHub
# (via PR oder Issue UI)

# 4. Action triggert automatisch
# 5. PR #25 wird erstellt
```

**Result:**
```
✅ PR #25: Resolve Issue #3 - improve validator error messages
- Branch: feature/issue-3-improve-validator-error-messages
- Commits: 1
- Status: Draft
```

### Beispiel 2: Batch Multiple Issues

```bash
# Fix multiple issues in single commit
git commit -m "feat: resolve issues

Fixes #40 - Figma fixture
Fixes #41 - MCP server
Fixes #42 - Validator errors"

# Trigger consolidation
gh workflow run auto-consolidate-issues.yml -f batch_size=5

# Result: One PR for all 3 issues
```

**Result:**
```
✅ PR #26: Resolve Issues - Batch #3 (#40, #41, #42)
- Branch: feature/resolve-issues-batch-20241013-...
- Commits: 3
- Status: Ready for Review
```

---

## 🎯 Use Cases

| Use Case | Action | Command |
|----------|--------|---------|
| Close 1 Issue → 1 PR | Auto-Create PR | `gh issue close #42` |
| Close 5 Issues → 1 PR | Auto-Consolidate | `gh workflow run auto-consolidate-issues.yml` |
| Manual Trigger | Auto-Create PR | `gh workflow run auto-create-pr.yml` |

---

## ⚙️ Configuration

### Batch Size ändern

```bash
# Default: 5 issues
# Use 10 issues instead:
gh workflow run auto-consolidate-issues.yml -f batch_size=10
```

### Bestimmtes Issue triggern

```bash
# Trigger for issue #42
gh workflow run auto-create-pr.yml -f issue_number=42
```

---

## 🔍 Monitor Actions

### Check Workflow Status
```bash
# View recent runs
gh run list --workflow auto-create-pr.yml --limit 10

# View latest run
gh run view --latest --workflow auto-create-pr.yml
```

### View Run Logs
```bash
# View logs for specific run
gh run view <run_id> --log

# Follow live logs
gh run view <run_id> --log --tail
```

### Re-run Failed Action
```bash
# Re-run failed run
gh run rerun <run_id>
```

---

## ✅ Checklist

- [ ] Workflows sind in `.github/workflows/` vorhanden
- [ ] Actions sind in GitHub UI sichtbar
- [ ] Du verstehst Commit Message Convention (`#issue_number`)
- [ ] Du hast GitHub CLI installiert (optional)
- [ ] Du kennst die Workflow Logs Location

---

## 🆘 Troubleshooting

### Action triggert nicht?

**Check 1:** Workflow aktiv?
```bash
gh workflow list | grep auto
# Sollte beide Workflows zeigen
```

**Check 2:** Richtige Commit Message?
```bash
git commit -m "fix(#42): description"  # ✅
git commit -m "fix: description"       # ❌
```

**Check 3:** Issue auf main Branch?
```bash
# Der Commit muss auf main sein für Actions zu triggern
git log main --grep="#42"
```

### PR nicht erstellt?

**Gründe:**
1. Kein Commit mit `#issue_number` gefunden
2. PR existiert bereits
3. Action hat nicht genug Permissions

**Debug:**
```bash
# Check latest run
gh run list --workflow auto-create-pr.yml --limit 1

# View logs
gh run view <run_id> --log
```

### Falsche Branch Name?

Das ist OK! Branch Name wird automatisch generiert:
- Single Issue: `feature/issue-42-issue-title`
- Batch: `feature/resolve-issues-batch-timestamp`

Kann manuell umbenannt werden:
```bash
git branch -m old-name new-name
git push origin --delete old-name
git push origin new-name
```

---

## 📚 Full Documentation

Siehe `.github/workflows/README.md` für:
- Detaillierte Funktionsweise
- Erweiterte Konfiguration
- Integration mit anderen Tools
- Best Practices

---

## 🎓 Learning

### Was die Action macht:
```yaml
1. Detektiert geschlossene Issues
2. Sucht nach verwandten Commits
3. Erstellt Feature Branch
4. Generiert PR Description
5. Erstellt Draft PR
6. Kommentiert Issue
```

### Warum Draft PRs?
- Zeit zum Review geben
- Verhindert versehentliche Merges
- Ermöglicht weitere Changes

### Warum #issue_number wichtig?
- Action findet Commits nur damit
- GitHub verlinkt Issues automatisch
- Hilft beim Tracking

---

## 🚀 Next Steps

1. **Schließe ein Issue** auf GitHub
   → Action triggert automatisch
   → PR wird erstellt
   
2. **Review PR** auf GitHub
   → Nimm Draft → Ready for Review
   
3. **Merge PR** wenn alles OK
   → Issues werden automatisch geschlossen

---

## 💬 Questions?

Für Fragen schau in:
- `.github/workflows/README.md` - Detaillierte Doku
- `.github/workflows/auto-create-pr.yml` - Inline Comments
- `.github/workflows/auto-consolidate-issues.yml` - Inline Comments

Oder erstelle ein GitHub Issue!

---

**That's it! Actions sind ready to go.** 🎉

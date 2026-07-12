# Project Board

Recommended GitHub Project board:

```text
Hermes Figma Prompt Hub Roadmap
```

Columns/status values:

- Backlog
- Ready
- In progress
- Review
- Done

Suggested views:

- Roadmap by Status
- Good First Issues
- Automation
- MCP and Figma Importer

To create this with GitHub CLI, first grant the `project` scope:

```bash
gh auth refresh -s project
```

Then create and link the project:

```bash
gh project create --owner jozrftamson --title "Hermes Figma Prompt Hub Roadmap"
gh project link <project-number> --owner jozrftamson --repo hermes-figma-prompt-hub
```

After creation, add a single-select status field with:

```text
Backlog
Ready
In progress
Review
Done
```


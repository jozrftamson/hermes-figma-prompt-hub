# Project Board

Recommended GitHub Project board:

```text
Hermes Figma Prompt Hub Roadmap
```

Created board:

```text
https://github.com/users/jozrftamson/projects/5
```

Project number:

```text
5
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

The board is linked to:

```text
jozrftamson/hermes-figma-prompt-hub
```

If this needs to be recreated with GitHub CLI, first grant the `project` scope:

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

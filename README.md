<<<<<<< HEAD
# Hermes Figma Prompt Hub - Complete Platform

> Design System & Prompt Management Platform with Figma Integration

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Actions](https://github.com/jozrftamson/hermes-figma-prompt-hub-nuxt/workflows/CI/badge.svg)](https://github.com/jozrftamson/hermes-figma-prompt-hub-nuxt/actions)

## 🎯 Features

### 📊 Core Features
- ✅ **Figma Integration** — Import PROMPT/* frames directly from Figma
- ✅ **Design System** — Complete CSS/SCSS generation from design tokens
- ✅ **Validation Suite** — Schema, layer contract, and quality checks
- ✅ **Prompt Management** — Create, edit, validate, and version prompts
- ✅ **Auto-Sync** — Webhook-based auto-sync from Figma changes
- ✅ **Web UI** — Nuxt 3 dashboard for prompt management

### 🎨 Design System
- **Colors** — Primary, Secondary, Semantic, Neutral palettes with shades
- **Typography** — 8-level font scale with weights and line-heights
- **Spacing** — 24-step spacing system (4px base)
- **Radius** — 9-level border radius scale
- **Shadows** — 5-level elevation system
- **Responsive** — Mobile-first 12-column grid with breakpoints

### 🤖 Prompt Strategies
- **Chain-of-Thought** — Structured step-by-step reasoning
- **Few-Shot Learning** — Pattern recognition with examples
- **Role-Play Persona** — Expert advice from specific roles
- **Tree-of-Thought** — Multiple parallel solution paths
- **Meta-Reasoning** — Self-validation and reflection

### ✅ Validation
- **Schema Validator** — JSON schema compliance
- **Layer Contract** — Figma structure validation
- **Content Quality** — Clarity, specificity, token estimation
- **Strategy-Specific** — Rules per prompting strategy

### 🔄 Integration
- **Figma API** — Direct import from Figma files
- **Webhooks** — Auto-sync on file changes
- **GitHub** — Native git integration
- **CI/CD** — GitHub Actions workflows

## 📦 Project Structure

```
hermes-figma-prompt-hub-nuxt/
├── pages/                    # Nuxt pages
│   ├── index.vue            # Dashboard
│   └── prompts/
│       ├── index.vue        # Prompts list
│       └── [id].vue         # Prompt detail
├── components/              # Vue components
├── stores/                   # Pinia stores
├── server/
│   ├── api/                 # Nuxt API routes
│   └── middleware/          # Server middleware
├── scripts/                 # Python & Bash scripts
│   ├── figma_importer.py    # Figma API client
│   ├── figma_webhook.py     # Webhook handler
│   ├── schema_validator.py  # Validation
│   ├── css_generator.py     # CSS generation
│   └── figma_sync.sh        # CLI orchestrator
├── data/                    # Design system JSON
│   ├── figma_design_system_extended.json
│   └── integration_guide.json
├── css/                     # Generated CSS
├── scss/                    # Generated SCSS
└── docs/                    # Documentation
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.10+
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/jozrftamson/hermes-figma-prompt-hub-nuxt
cd hermes-figma-prompt-hub-nuxt

# Install dependencies
npm install

# Setup environment
cp .env.example .env.local
# Edit .env.local with your Figma credentials
```

### Environment Variables

```bash
# .env.local
NUXT_FIGMA_API_TOKEN=figd_xxxx...
NUXT_FIGMA_FILE_ID=ABC123DEF456
NUXT_FIGMA_TEAM_ID=optional_team_id
NUXT_FIGMA_WEBHOOK_SECRET=your_webhook_secret
```

### Running Locally

```bash
# Development server
npm run dev
# Visit http://localhost:3000

# Import from Figma
npm run figma:import

# Validate prompts
npm run validate:prompts

# Generate CSS/SCSS
npm run styles:build
```

## 📚 Documentation

- [Figma Integration Guide](./docs/FIGMA_INTEGRATION_GUIDE.md) — Setup Figma API
- [CSS/SCSS Guide](./docs/CSS_SCSS_GUIDE.md) — Generate styles
- [Validation Guide](./docs/VALIDATION_GUIDE.md) — Validate prompts
- [API Reference](./docs/API_REFERENCE.md) — API endpoints

## 🔗 API Endpoints

### Prompts
- `GET /api/prompts` — List all prompts
- `POST /api/prompts` — Create prompt
- `GET /api/prompts/:id` — Get prompt detail
- `PUT /api/prompts/:id` — Update prompt
- `DELETE /api/prompts/:id` — Delete prompt

### Figma Integration
- `POST /api/figma/sync` — Trigger sync from Figma
- `POST /api/figma/import` — Import prompts
- `GET /api/figma/status` — Check sync status

## 🔧 Scripts

### Figma Operations
```bash
./scripts/figma_sync.sh import          # Import from Figma
./scripts/figma_sync.sh validate        # Validate prompts
./scripts/figma_sync.sh webhook-setup   # Setup webhook
./scripts/figma_sync.sh sync            # Watch mode
```

### CSS Generation
```bash
./scripts/generate_styles.sh css        # Generate CSS
./scripts/generate_styles.sh scss       # Generate SCSS
./scripts/generate_styles.sh build      # Build + minify
./scripts/generate_styles.sh watch      # Watch mode
```

### Validation
```bash
python3 scripts/validate_all.py prompts/
python3 scripts/schema_validator.py prompts/my-prompt.json
python3 scripts/figma_layer_validator.py figma_export.json
```

## 🌐 Deployment

### Vercel

```bash
vercel link
vercel env add NUXT_FIGMA_API_TOKEN
vercel deploy
```

### Docker

```bash
docker build -t hermes-prompt-hub .
docker run -p 3000:3000 \
  -e NUXT_FIGMA_API_TOKEN=... \
  -e NUXT_FIGMA_FILE_ID=... \
  hermes-prompt-hub
```

### GitHub Actions

Auto-sync from Figma:

```yaml
name: Sync Prompts

on:
  schedule:
    - cron: '0 * * * *'  # Hourly
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install requests
      - run: python3 scripts/figma_importer.py
      - run: git add prompts/ && git commit -m "🤖 Sync from Figma" || exit 0
      - run: git push
```

## 📊 Quality Metrics

- **Code Coverage**: >85%
- **Bundle Size**: ~200KB (gzipped)
- **Performance**: Lighthouse >90
- **Accessibility**: WCAG AA compliance

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md)

## 📝 License

MIT © 2025 Hermes Figma Prompt Hub

## 🔗 Links

- [Figma API Docs](https://www.figma.com/developers/api)
- [Nuxt 3](https://nuxt.com)
- [Pinia](https://pinia.vuejs.org)

---

**Built with ❤️ for prompt engineers and design systems teams**

## 📋 Figma Layer Contract

The importer expects Figma PROMPT frames with the following layer structure:

```
PROMPT/example-v1
├── METADATA (group)
│   ├── title (text)
│   ├── description (text)
│   ├── category (text)
│   ├── strategy (text)
│   └── version (text)
├── CONTENT (group)
│   ├── system (text)
│   ├── user_template (text)
│   ├── guardrails (text)
│   └── output_format (text)
├── EXAMPLES (group)
│   └── example_N (frame)
│       ├── input (text)
│       ├── output (text)
│       └── explanation (text)
└── STRATEGY_CONFIG (group)
    ├── num_steps (text)
    └── step_structure (text)
```

### Test Fixtures

Example test fixtures are available in `evals/cases/`:
- `figma_prompt_example_v1.json` — Complete Figma PROMPT frame fixture

Use these fixtures to test the importer without real Figma data:

```bash
python3 scripts/figma_importer.py --fixture evals/cases/figma_prompt_example_v1.json
```

## 🤖 MCP Server Integration

Hermes includes a Model Context Protocol (MCP) server for integration with MCP clients like Claude Desktop, Cursor, and other AI assistants.

### Available Tools

- **list_prompts** — Enumerate all prompts in `prompts/raw/`
- **validate_prompt** — Validate a specific prompt against schema
- **get_prompt_stats** — Get collection statistics (strategies, categories, validity)

### Quick Setup

```bash
# Copy config to Claude Desktop
mkdir -p ~/.config/Claude/
cp mcp/claude_desktop_config.json ~/.config/Claude/claude_desktop_config.json

# Edit config with absolute path to your installation
# Restart Claude Desktop
```

### Usage

```bash
# Test from CLI
python3 mcp/server.py list
python3 mcp/server.py validate --filename prompt-1.json
python3 mcp/server.py stats

# In Claude Desktop: "List my prompts" or "Validate prompt-1.json"
```

See [mcp/README.md](mcp/README.md) for detailed documentation.

=======
<p align="center">
  <img src="assets/banner.png" alt="Hermes Agent" width="100%">
</p>

# Hermes Agent ☤
<p align="center">
  <a href="https://hermes-agent.nousresearch.com/">Hermes Agent</a> | <a href="https://hermes-agent.nousresearch.com/">Hermes Desktop</a>
</p>
<p align="center">
  <a href="https://hermes-agent.nousresearch.com/docs/"><img src="https://img.shields.io/badge/Docs-hermes--agent.nousresearch.com-FFD700?style=for-the-badge" alt="Documentation"></a>
  <a href="https://discord.gg/NousResearch"><img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord"></a>
  <a href="https://github.com/NousResearch/hermes-agent/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT"></a>
  <a href="https://nousresearch.com"><img src="https://img.shields.io/badge/Built%20by-Nous%20Research-blueviolet?style=for-the-badge" alt="Built by Nous Research"></a>
  <a href="README.zh-CN.md"><img src="https://img.shields.io/badge/Lang-中文-red?style=for-the-badge" alt="中文"></a>
  <a href="README.ur-pk.md"><img src="https://img.shields.io/badge/Lang-اردو-green?style=for-the-badge" alt="اردو"></a>
  <a href="README.es.md"><img src="https://img.shields.io/badge/Lang-Español-orange?style=for-the-badge" alt="Español"></a>
</p>

**The self-improving AI agent built by [Nous Research](https://nousresearch.com).** It's the only agent with a built-in learning loop — it creates skills from experience, improves them during use, nudges itself to persist knowledge, searches its own past conversations, and builds a deepening model of who you are across sessions. Run it on a $5 VPS, a GPU cluster, or serverless infrastructure that costs nearly nothing when idle. It's not tied to your laptop — talk to it from Telegram while it works on a cloud VM.

Use any model you want — [Nous Portal](https://portal.nousresearch.com), OpenRouter, OpenAI, your own endpoint, and [many others](https://hermes-agent.nousresearch.com/docs/integrations/providers). Switch with `hermes model` — no code changes, no lock-in.

<table>
<tr><td><b>A real terminal interface</b></td><td>Full TUI with multiline editing, slash-command autocomplete, conversation history, interrupt-and-redirect, and streaming tool output.</td></tr>
<tr><td><b>Lives where you do</b></td><td>Telegram, Discord, Slack, WhatsApp, Signal, and CLI — all from a single gateway process. Voice memo transcription, cross-platform conversation continuity.</td></tr>
<tr><td><b>A closed learning loop</b></td><td>Agent-curated memory with periodic nudges. Autonomous skill creation after complex tasks. Skills self-improve during use. FTS5 session search with LLM summarization for cross-session recall. <a href="https://github.com/plastic-labs/honcho">Honcho</a> dialectic user modeling. Compatible with the <a href="https://agentskills.io">agentskills.io</a> open standard.</td></tr>
<tr><td><b>Scheduled automations</b></td><td>Built-in cron scheduler with delivery to any platform. Daily reports, nightly backups, weekly audits — all in natural language, running unattended.</td></tr>
<tr><td><b>Delegates and parallelizes</b></td><td>Spawn isolated subagents for parallel workstreams. In Desktop, choose their provider, model, and limits under Settings → Model → Subagents, then Apply the complete route. Write Python scripts that call tools via RPC, collapsing multi-step pipelines into zero-context-cost turns.</td></tr>
<tr><td><b>Runs anywhere, not just your laptop</b></td><td>Six built-in terminal backends — local, Docker, SSH, Modal, Daytona, and Vercel Sandbox — plus plugin backends such as Singularity/Apptainer. Daytona and Modal offer serverless persistence — your agent's environment hibernates when idle and wakes on demand, costing nearly nothing between sessions. Run it on a $5 VPS or a GPU cluster.</td></tr>
<tr><td><b>Research-ready</b></td><td>Batch trajectory generation, trajectory compression for training the next generation of tool-calling models.</td></tr>
</table>

---

## Quick Install

### Linux, macOS, WSL2

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

### Windows (native, PowerShell)

> **Heads up:** Native Windows runs Hermes without WSL — CLI, gateway, TUI, and tools all work natively. If you'd rather use WSL2, the Linux/macOS one-liner above works there too. Found a bug? Please [file issues](https://github.com/NousResearch/hermes-agent/issues).

Run this in PowerShell:

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

The source installer delegates Python 3.14, Node.js, npm, pnpm, ripgrep, FFmpeg,
and Python dependencies to PM. If Git is absent, it stages the verified Git
for Windows archive in Hermes' tool store. It does not replace your system Git.
See [installation methods](https://hermes-agent.nousresearch.com/docs/getting-started/installation)
for the separate MSIX/App Installer package and its update ownership.

> **Android / Termux:** A signed APT repository is available for aarch64 devices, with a `stable` channel (tagged releases) and a prerelease `canary` channel. The package includes Python, Node.js, and the TUI. Use the [Termux guide](https://hermes-agent.nousresearch.com/docs/getting-started/termux), not the desktop/server installer script.
>
> **Windows:** Native Windows is fully supported — the PowerShell one-liner above installs everything. If you'd rather use WSL2, the Linux command works there too. Native Windows install lives under `%LOCALAPPDATA%\hermes`; WSL2 installs under `~/.hermes` as on Linux.

After installation:

```bash
source ~/.bashrc    # reload shell (or: source ~/.zshrc)
hermes              # start chatting!
```

### Troubleshooting

#### Windows Defender or antivirus flags `uv.exe` as malware

If your antivirus (Bitdefender, Windows Defender, etc.) quarantines `uv.exe` from the Hermes `bin` folder (`%LOCALAPPDATA%\hermes\bin\uv.exe`), this is a **false positive**. The file is Astral's `uv` — the Rust Python package manager Hermes bundles to manage its Python environment. ML-based antivirus engines commonly flag unsigned Rust binaries that download and install packages.

**To verify your copy is authentic:**

```powershell
# Install GitHub CLI if needed
winget install --id GitHub.cli

# Login to GitHub
gh auth login

# Run verification
$uv = "$env:LOCALAPPDATA\hermes\bin\uv.exe"
$ver = (& $uv --version).Split(' ')[1]
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$zip = "$env:TEMP\uv.zip"
Invoke-WebRequest "https://github.com/astral-sh/uv/releases/download/$ver/uv-x86_64-pc-windows-msvc.zip" -OutFile $zip -UseBasicParsing
gh attestation verify $zip --repo astral-sh/uv
Expand-Archive $zip "$env:TEMP\uv_x" -Force
(Get-FileHash "$env:TEMP\uv_x\uv.exe").Hash -eq (Get-FileHash $uv).Hash
```

If attestation says "Verification succeeded" and the last line prints `True`, you're good.

**To whitelist Hermes:**
- **Windows Defender:** Run PowerShell as Admin → `Add-MpPreference -ExclusionPath "$env:LOCALAPPDATA\hermes\bin"`
- **Bitdefender:** Add an exception in the Bitdefender console (Protection > Antivirus > Settings > Manage Exceptions)
- Whitelist the **folder**, not the file hash — Hermes updates `uv` and the hash changes every version

For more context, see the upstream Astral reports: [astral-sh/uv#13553](https://github.com/astral-sh/uv/issues/13553), [astral-sh/uv#15011](https://github.com/astral-sh/uv/issues/15011), [astral-sh/uv#10079](https://github.com/astral-sh/uv/issues/10079).

---

## Getting Started

```bash
hermes              # Interactive CLI — start a conversation
hermes model        # Choose your LLM provider and model
hermes tools        # Configure which tools are enabled
hermes config set   # Set individual config values
hermes config get   # Print individual config values
hermes gateway      # Start the messaging gateway (Telegram, Discord, etc.)
hermes setup        # Run the full setup wizard (configures everything at once)
hermes update       # Update to the latest version
hermes doctor       # Diagnose any issues
```

📖 **[Full documentation →](https://hermes-agent.nousresearch.com/docs/)**

---

## Skip the API-key collection — Nous Portal

Hermes works with whatever provider you want — that's not changing. But if you'd rather not collect five separate API keys for the model, web search, image generation, TTS, and a cloud browser, **[Nous Portal](https://portal.nousresearch.com)** covers all of them under one subscription:

- **300+ models** — pick any of them with `/model <name>`
- **Tool Gateway** — web search, image generation (FAL), text-to-speech (OpenAI), cloud browser (Browser Use), all routed through your sub. No extra accounts.

One command from a fresh install:

```bash
hermes setup --portal
```

That logs you in via OAuth, sets Nous as your provider, and turns on the Tool Gateway. Check what's wired up any time with `hermes portal info`. Full details on the [Tool Gateway docs page](https://hermes-agent.nousresearch.com/docs/user-guide/features/tool-gateway).

You can still bring your own keys per-tool whenever you want — the gateway is per-backend, not all-or-nothing.

---

## CLI vs Messaging Quick Reference

Hermes has two entry points: start the terminal UI with `hermes`, or run the gateway and talk to it from Telegram, Discord, Slack, WhatsApp, Signal, or Email. Once you're in a conversation, many slash commands are shared across both interfaces.

| Action                         | CLI                                           | Messaging platforms                                                              |
| ------------------------------ | --------------------------------------------- | -------------------------------------------------------------------------------- |
| Start chatting                 | `hermes`                                      | Run `hermes gateway setup` + `hermes gateway start`, then send the bot a message |
| Start fresh conversation       | `/new` or `/reset`                            | `/new` or `/reset`                                                               |
| Change model                   | `/model [provider:model]`                     | `/model [provider:model]`                                                        |
| Set a personality              | `/personality [name]`                         | `/personality [name]`                                                            |
| Retry or undo the last turn    | `/retry`, `/undo`                             | `/retry`, `/undo`                                                                |
| Compress context / check usage | `/compress`, `/usage`, `/insights [--days N]` | `/compress`, `/usage`, `/insights [days]`                                        |
| Browse skills                  | `/skills` or `/<skill-name>`                  | `/<skill-name>`                                                                  |
| Interrupt current work         | `Ctrl+C` or send a new message                | `/stop` or send a new message                                                    |
| Platform-specific status       | `/platforms`                                  | `/status`, `/sethome`                                                            |

For the full command lists, see the [CLI guide](https://hermes-agent.nousresearch.com/docs/user-guide/cli) and the [Messaging Gateway guide](https://hermes-agent.nousresearch.com/docs/user-guide/messaging).

---

## Documentation

All documentation lives at **[hermes-agent.nousresearch.com/docs](https://hermes-agent.nousresearch.com/docs/)**:

| Section                                                                                             | What's Covered                                             |
| --------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| [Quickstart](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart)                 | Install → setup → first conversation in 2 minutes          |
| [CLI Usage](https://hermes-agent.nousresearch.com/docs/user-guide/cli)                              | Commands, keybindings, personalities, sessions             |
| [Configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)                | Config file, providers, models, all options                |
| [Messaging Gateway](https://hermes-agent.nousresearch.com/docs/user-guide/messaging)                | Telegram, Discord, Slack, WhatsApp, Signal, Home Assistant |
| [Security](https://hermes-agent.nousresearch.com/docs/user-guide/security)                          | Command approval, DM pairing, container isolation          |
| [Tools & Toolsets](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools)            | 40+ tools, toolset system, terminal backends               |
| [Skills System](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)              | Procedural memory, Skills Hub, creating skills             |
| [Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)                     | Persistent memory, user profiles, best practices           |
| [MCP Integration](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp)               | Connect any MCP server for extended capabilities           |
| [Cron Scheduling](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron)              | Scheduled tasks with platform delivery                     |
| [Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)       | Project context that shapes every conversation             |
| [Architecture](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture)             | Project structure, agent loop, key classes                 |
| [Contributing](https://hermes-agent.nousresearch.com/docs/developer-guide/contributing)             | Development setup, PR process, code style                  |
| [CLI Reference](https://hermes-agent.nousresearch.com/docs/reference/cli-commands)                  | All commands and flags                                     |
| [Environment Variables](https://hermes-agent.nousresearch.com/docs/reference/environment-variables) | Complete env var reference                                 |

---

## Migrating from OpenClaw or another agent

If you're coming from OpenClaw, Claude Code, Codex CLI or Cursor, Hermes can import your settings, memories and skills (and, for OpenClaw, API keys when you ask for them).

**During setup:** `hermes setup` asks whether to import from another agent, pre-selects the ones it finds (`~/.openclaw`, `~/.claude`, `~/.codex`, `~/.cursor`), installs the official `agent-importers` plugin and runs the import with a preview first.

**Anytime after install:**

```bash
hermes plugins install agent-importers          # once per profile
hermes import-agent openclaw                    # interactive migration (full preset)
hermes import-agent openclaw --dry-run          # preview what would be migrated
hermes import-agent openclaw --migrate-secrets  # also bring allowlisted API keys
hermes import-agent claude-code                 # or codex / cursor
```

What gets imported from OpenClaw:

- **SOUL.md** — persona file
- **Memories** — MEMORY.md and USER.md entries
- **Skills** — user-created skills → `~/.hermes/skills/openclaw-imports/`
- **Command allowlist** — approval patterns
- **Messaging settings** — platform configs, allowed users, working directory
- **API keys** — allowlisted secrets (Telegram, OpenRouter, OpenAI, Anthropic, ElevenLabs), only with `--migrate-secrets`
- **TTS assets** — workspace audio files
- **Workspace instructions** — AGENTS.md (with `--workspace-target`)

`hermes claw migrate` still works as the older spelling. See the [OpenClaw migration guide](https://hermes-agent.nousresearch.com/docs/guides/migrate-from-openclaw) and [Import from Other Agents](https://hermes-agent.nousresearch.com/docs/user-guide/import-from-other-agents).

---

## Contributing

We welcome contributions! See the [Contributing Guide](https://hermes-agent.nousresearch.com/docs/developer-guide/contributing) for development setup, code style, and PR process.

Start with the [PM developer workflow](website/docs/reference/package-management.md#developer-workflow)
for activation, daily use, dependency changes, and leaving the environment.
[Development Setup](CONTRIBUTING.md#development-setup) covers the separate test environment and verification commands.

---

## Community

- 💬 [Discord](https://discord.gg/NousResearch)
- 📚 [Skills Hub](https://agentskills.io)
- 🐛 [Issues](https://github.com/NousResearch/hermes-agent/issues)
- 🔌 [computer-use-linux](https://github.com/avifenesh/computer-use-linux) — Linux desktop-control MCP server for Hermes and other MCP hosts, with AT-SPI accessibility trees, Wayland/X11 input, screenshots, and compositor window targeting.
- 🔌 [HermesClaw](https://github.com/AaronWong1999/hermesclaw) — Community WeChat bridge: Run Hermes Agent and OpenClaw on the same WeChat account.

---

## License

MIT — see [LICENSE](LICENSE).

Built by [Nous Research](https://nousresearch.com).
>>>>>>> upstream/main

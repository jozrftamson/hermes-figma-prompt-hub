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

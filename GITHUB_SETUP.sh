#!/bin/bash

# 🚀 HERMES FIGMA PROMPT HUB - GITHUB SETUP GUIDE

cat << 'EOF'

╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║     🚀 HERMES FIGMA PROMPT HUB - NUXT IMPLEMENTATION                      ║
║     Complete Design System & Prompt Management Platform                   ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

📦 PROJECT DETAILS
═══════════════════════════════════════════════════════════════════════════

Repository Name:  hermes-figma-prompt-hub-nuxt
Type:            Full-stack Nuxt 3 application
Language:        TypeScript, Python, Vue 3
Size:            ~860 KB
Files:           24 files

📁 PROJECT CONTENTS
═══════════════════════════════════════════════════════════════════════════

✅ Frontend (Nuxt 3)
   • Dashboard (index.vue)
   • Prompts Library (/prompts/index.vue)
   • Responsive UI with Tailwind CSS
   • Pinia state management

✅ Backend (Nuxt Server)
   • API endpoints (/server/api/prompts.ts)
   • Figma sync endpoint
   • TypeScript support

✅ Python Scripts
   • figma_importer.py       - Import from Figma API
   • figma_webhook.py        - Auto-sync webhooks
   • schema_validator.py     - JSON validation
   • figma_layer_validator.py - Layer contract validation
   • validate_all.py         - Comprehensive validation
   • css_generator.py        - CSS from design tokens
   • scss_generator.py       - SCSS with mixins

✅ Design System
   • Complete color palette with shades
   • 8-level typography scale
   • 24-step spacing system
   • 9-level border radius
   • 5-level shadow elevation
   • Responsive grid system

✅ Documentation
   • README.md               - Project overview
   • Figma integration guide
   • CSS/SCSS guide
   • Validation guide
   • GitHub Actions workflows

🔗 GITHUB UPLOAD INSTRUCTIONS
═══════════════════════════════════════════════════════════════════════════

STEP 1: Create GitHub Repository
────────────────────────────────────────────────────────────────────────────
1. Go to: https://github.com/new
2. Repository name: hermes-figma-prompt-hub-nuxt
3. Description: Design System & Prompt Management with Figma Integration
4. Visibility: Public
5. Skip README, .gitignore, license (we have them)
6. Click "Create repository"

STEP 2: Push Local Repository
────────────────────────────────────────────────────────────────────────────
cd /tmp/hermes-figma-prompt-hub-nuxt

# Change branch to main (GitHub default)
git branch -M main

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/hermes-figma-prompt-hub-nuxt.git

# Push to GitHub
git push -u origin main

STEP 3: Setup Repository Secrets (For GitHub Actions)
────────────────────────────────────────────────────────────────────────────
Go to: Settings → Secrets and variables → Actions → New repository secret

Add these secrets:
  • FIGMA_API_TOKEN       → figd_xxxx...
  • FIGMA_FILE_ID        → your_figma_file_id
  • FIGMA_TEAM_ID        → your_figma_team_id (optional)
  • VERCEL_TOKEN         → your_vercel_token (for auto-deploy)

STEP 4: Enable GitHub Actions
────────────────────────────────────────────────────────────────────────────
Go to: Settings → Actions → General
  • Allow all actions and reusable workflows
  • Save default workflow permissions

✅ GITHUB REPOSITORY URL FORMAT
═══════════════════════════════════════════════════════════════════════════

Standard Format:
  https://github.com/YOUR_USERNAME/hermes-figma-prompt-hub-nuxt

SSH Format (for git operations):
  git@github.com:YOUR_USERNAME/hermes-figma-prompt-hub-nuxt.git

Clone Command:
  git clone https://github.com/YOUR_USERNAME/hermes-figma-prompt-hub-nuxt.git

🚀 DEPLOYMENT OPTIONS
═══════════════════════════════════════════════════════════════════════════

Option 1: Vercel (Recommended - automatic from GitHub)
────────────────────────────────────────────────────────────────────────────
1. Go to: https://vercel.com/import
2. Select your GitHub repo
3. Add environment variables
4. Deploy
5. Live at: https://hermes-figma-prompt-hub-nuxt.vercel.app

Option 2: GitHub Pages
────────────────────────────────────────────────────────────────────────────
Settings → Pages → Source: GitHub Actions
(Uses existing deploy.yml workflow)

Option 3: Docker / Self-hosted
────────────────────────────────────────────────────────────────────────────
docker build -t hermes-prompt-hub .
docker run -p 3000:3000 hermes-prompt-hub

📊 GIT COMMIT HISTORY
═══════════════════════════════════════════════════════════════════════════

EOF

# Show git log
cd /tmp/hermes-figma-prompt-hub-nuxt
echo ""
echo "Current commits in repository:"
git log --oneline --all
echo ""

cat << 'EOF'

🔗 UPSTREAM LINK
═══════════════════════════════════════════════════════════════════════════

Once pushed to GitHub, your upstream will be:

  https://github.com/YOUR_USERNAME/hermes-figma-prompt-hub-nuxt

Add as upstream:
  git remote add upstream https://github.com/YOUR_USERNAME/hermes-figma-prompt-hub-nuxt.git

Fetch upstream:
  git fetch upstream
  git merge upstream/main

🎯 NEXT STEPS
═══════════════════════════════════════════════════════════════════════════

1. Create GitHub repository (see STEP 1 above)
2. Push local code (STEP 2)
3. Configure GitHub secrets (STEP 3)
4. Enable GitHub Actions (STEP 4)
5. Deploy to Vercel
6. Setup Figma webhook (optional)

📚 USEFUL COMMANDS
═══════════════════════════════════════════════════════════════════════════

# View remote URLs
git remote -v

# Add upstream
git remote add upstream https://github.com/YOUR_USERNAME/hermes-figma-prompt-hub-nuxt.git

# Sync with upstream
git fetch upstream
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature
git push origin feature/your-feature

# Create pull request
# Go to GitHub and click "Compare & pull request"

📖 DOCUMENTATION LINKS
═══════════════════════════════════════════════════════════════════════════

Local paths (after pushing):
  • README.md               - docs/README.md
  • FIGMA_INTEGRATION.md    - docs/FIGMA_INTEGRATION_GUIDE.md
  • CSS_SCSS_GUIDE.md       - docs/CSS_SCSS_GUIDE.md
  • VALIDATION_GUIDE.md     - docs/VALIDATION_GUIDE.md

Web links (on GitHub):
  • https://github.com/YOUR_USERNAME/hermes-figma-prompt-hub-nuxt/blob/main/README.md
  • https://github.com/YOUR_USERNAME/hermes-figma-prompt-hub-nuxt/tree/main/docs

💡 TIPS
═══════════════════════════════════════════════════════════════════════════

• Use descriptive commit messages (we follow conventional commits)
• Each feature should have its own branch
• Keep main branch production-ready
• GitHub Actions automatically validate all pushes
• Vercel auto-deploys from main branch

❌ TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════════

"fatal: remote origin already exists"
  → git remote set-url origin https://github.com/YOUR_USERNAME/...

"Permission denied (publickey)"
  → Setup SSH key or use HTTPS token
  → https://docs.github.com/en/authentication

"Failed to push"
  → git pull origin main (sync first)
  → git push origin main

═══════════════════════════════════════════════════════════════════════════
✅ Ready to push! Follow the steps above to upload to GitHub.
═══════════════════════════════════════════════════════════════════════════

EOF

#!/bin/bash
# Setup and Push to GitHub

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🚀 Hermes Figma Prompt Hub - Setup Guide${NC}"
echo ""

# Step 1: Create GitHub Repository
echo -e "${YELLOW}Step 1: Create GitHub Repository${NC}"
echo "1. Go to https://github.com/new"
echo "2. Repository name: hermes-figma-prompt-hub-nuxt"
echo "3. Description: Design System & Prompt Management Platform with Figma Integration"
echo "4. Choose Public"
echo "5. Click Create"
echo ""

# Step 2: Add Remote
echo -e "${YELLOW}Step 2: Add Remote and Push${NC}"
echo "Run these commands:"
echo ""
echo "cd /tmp/hermes-figma-prompt-hub-nuxt"
echo "git branch -M main"
echo "git remote add origin https://github.com/YOUR_USERNAME/hermes-figma-prompt-hub-nuxt.git"
echo "git push -u origin main"
echo ""

# Step 3: Setup GitHub Secrets
echo -e "${YELLOW}Step 3: Setup GitHub Secrets${NC}"
echo "Go to: Settings → Secrets and variables → Actions"
echo ""
echo "Add these secrets:"
echo "  - FIGMA_API_TOKEN: figd_xxxx..."
echo "  - FIGMA_FILE_ID: your_figma_file_id"
echo "  - FIGMA_TEAM_ID: your_figma_team_id"
echo ""

# Step 4: Deployment
echo -e "${YELLOW}Step 4: Deploy (Optional)${NC}"
echo ""
echo "Option A: Vercel (Recommended)"
echo "  npm install -g vercel"
echo "  vercel link"
echo "  vercel env add NUXT_FIGMA_API_TOKEN"
echo "  vercel deploy"
echo ""
echo "Option B: GitHub Pages + Actions"
echo "  Set in: Settings → Pages → Source: GitHub Actions"
echo ""

# Display project info
echo -e "${GREEN}✅ Project Ready!${NC}"
echo ""
echo "📁 Project Location: /tmp/hermes-figma-prompt-hub-nuxt"
echo ""
echo "📊 Project Contents:"
echo "  ├── 🎨 Design System JSON files"
echo "  ├── 🔧 Python validation & Figma scripts"
echo "  ├── 📄 Nuxt 3 components & pages"
echo "  ├── 🚀 Server API endpoints"
echo "  ├── 📚 Complete documentation"
echo "  └── 📦 Ready for deployment"
echo ""
echo "🔗 Next Steps:"
echo "  1. Create GitHub repo at https://github.com/new"
echo "  2. Add remote: git remote add origin https://github.com/YOUR_USERNAME/hermes-figma-prompt-hub-nuxt.git"
echo "  3. Push: git push -u origin main"
echo "  4. Deploy to Vercel or GitHub Pages"
echo ""

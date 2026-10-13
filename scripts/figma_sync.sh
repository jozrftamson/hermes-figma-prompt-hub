#!/bin/bash
# Figma Integration CLI
# Orchestriert Import, Sync und Webhook Management

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_TOKEN="${FIGMA_API_TOKEN}"
FILE_ID="${FIGMA_FILE_ID}"
TEAM_ID="${FIGMA_TEAM_ID}"
OUTPUT_DIR="${PROMPT_OUTPUT_DIR:=./prompts}"
WEBHOOK_SECRET="${FIGMA_WEBHOOK_SECRET}"
WEBHOOK_URL="${FIGMA_WEBHOOK_URL}"

show_usage() {
    cat << EOF
Usage: $0 [COMMAND] [OPTIONS]

Commands:
  import          Import prompts from Figma
  sync            Sync (watch for changes)
  webhook-setup   Setup webhook for auto-sync
  webhook-list    List registered webhooks
  webhook-delete  Delete webhook
  validate        Validate imported prompts
  push            Push imported prompts to repo

Options:
  -t, --token TOKEN       Figma API token (or FIGMA_API_TOKEN env)
  -f, --file FILE_ID      Figma file ID (or FIGMA_FILE_ID env)
  -o, --output DIR        Output directory (default: $OUTPUT_DIR)
  -h, --help              Show this help

Examples:
  FIGMA_API_TOKEN=... FIGMA_FILE_ID=... $0 import
  $0 webhook-setup -f <file_id>
  $0 sync

Required Environment Variables:
  FIGMA_API_TOKEN   - Your personal Figma API token
  FIGMA_FILE_ID     - Your Figma file ID
  (Optional: FIGMA_TEAM_ID for webhooks)

EOF
}

# ============================================
# Import Prompts
# ============================================
import_prompts() {
    if [ -z "$API_TOKEN" ]; then
        log_error "FIGMA_API_TOKEN not set"
        return 1
    fi
    
    if [ -z "$FILE_ID" ]; then
        log_error "FIGMA_FILE_ID not set"
        return 1
    fi
    
    log_info "Importing prompts from Figma..."
    log_info "  File ID: $FILE_ID"
    log_info "  Output: $OUTPUT_DIR"
    
    python3 "$SCRIPT_DIR/figma_importer.py" "$API_TOKEN" "$FILE_ID" "$OUTPUT_DIR"
}

# ============================================
# Validate Imported Prompts
# ============================================
validate_imported() {
    log_info "Validating imported prompts..."
    
    if command -v python3 &> /dev/null; then
        python3 "$SCRIPT_DIR/validate_all.py" "$OUTPUT_DIR"
    else
        log_warning "Python3 not found, skipping validation"
    fi
}

# ============================================
# Setup Webhook
# ============================================
setup_webhook() {
    if [ -z "$TEAM_ID" ]; then
        log_error "FIGMA_TEAM_ID not set"
        return 1
    fi
    
    if [ -z "$WEBHOOK_URL" ]; then
        log_error "FIGMA_WEBHOOK_URL not set"
        return 1
    fi
    
    log_info "Setting up Figma webhook..."
    log_info "  Team ID: $TEAM_ID"
    log_info "  Callback URL: $WEBHOOK_URL"
    
    python3 << 'PYTHON'
import os
from figma_webhook import FigmaWebhookClient

api_token = os.getenv("FIGMA_API_TOKEN")
team_id = os.getenv("FIGMA_TEAM_ID")
webhook_url = os.getenv("FIGMA_WEBHOOK_URL")

client = FigmaWebhookClient(api_token)
result = client.register_webhook(team_id, webhook_url)

print()
print("✅ Webhook registered!")
print(f"  Webhook ID: {result.get('id')}")
print(f"  Status: {result.get('status')}")
PYTHON
}

# ============================================
# List Webhooks
# ============================================
list_webhooks() {
    if [ -z "$TEAM_ID" ]; then
        log_error "FIGMA_TEAM_ID not set"
        return 1
    fi
    
    log_info "Listing webhooks for team: $TEAM_ID"
    
    python3 << 'PYTHON'
import os
import json
from figma_webhook import FigmaWebhookClient

api_token = os.getenv("FIGMA_API_TOKEN")
team_id = os.getenv("FIGMA_TEAM_ID")

client = FigmaWebhookClient(api_token)
result = client.list_webhooks(team_id)

webhooks = result.get('webhooks', [])
print()
echo "Webhooks: ${#webhooks[@]}"
for webhook in "${webhooks[@]}"; do
    echo "  - ID: $webhook_id"
    echo "    URL: $webhook_url"
    echo "    Events: $webhook_events"
done
PYTHON
}

# ============================================
# Delete Webhook
# ============================================
delete_webhook() {
    if [ -z "$TEAM_ID" ] || [ -z "$1" ]; then
        log_error "Usage: $0 webhook-delete <webhook_id>"
        return 1
    fi
    
    webhook_id=$1
    
    log_warning "Deleting webhook: $webhook_id"
    
    python3 << PYTHON
import os
from figma_webhook import FigmaWebhookClient

api_token = os.getenv("FIGMA_API_TOKEN")
team_id = os.getenv("FIGMA_TEAM_ID")

client = FigmaWebhookClient(api_token)
result = client.delete_webhook(team_id, "$webhook_id")

print("✅ Webhook deleted!")
PYTHON
}

# ============================================
# Watch for Changes
# ============================================
watch_sync() {
    log_info "Watching for Figma changes..."
    log_info "Press Ctrl+C to stop"
    echo
    
    while true; do
        sleep 60
        log_info "Syncing from Figma..."
        import_prompts
        validate_imported
        echo
    done
}

# ============================================
# Push to Git
# ============================================
push_to_git() {
    log_info "Preparing to push prompts..."
    
    if ! command -v git &> /dev/null; then
        log_error "git not found"
        return 1
    fi
    
    cd "$OUTPUT_DIR"
    
    # Check for changes
    if ! git diff --quiet; then
        log_info "Changes detected, creating commit..."
        
        git add -A
        git commit -m "🤖 Auto-sync: Update prompts from Figma"
        
        log_success "Committed changes"
        
        log_info "Pushing to remote..."
        git push
        
        log_success "Pushed successfully!"
    else
        log_info "No changes to commit"
    fi
}

# ============================================
# Main
# ============================================

case "${1:-help}" in
    import)
        import_prompts
        ;;
    sync)
        watch_sync
        ;;
    validate)
        validate_imported
        ;;
    webhook-setup)
        setup_webhook
        ;;
    webhook-list)
        list_webhooks
        ;;
    webhook-delete)
        delete_webhook "$2"
        ;;
    push)
        push_to_git
        ;;
    -h|--help|help)
        show_usage
        ;;
    *)
        log_error "Unknown command: $1"
        show_usage
        exit 1
        ;;
esac

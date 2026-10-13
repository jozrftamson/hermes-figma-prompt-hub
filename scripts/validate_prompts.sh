#!/bin/bash
# Validation Scripts Runner
# Orchestriert alle Validierungsskripte

set -e

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging Funktionen
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verzeichnis-Setup
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPT_DIR="${PROMPT_DIR:-.}"
OUTPUT_DIR="${OUTPUT_DIR:=./validation_reports}"

mkdir -p "$OUTPUT_DIR"

log_info "Starting Validation Suite"
log_info "Prompt Directory: $PROMPT_DIR"
log_info "Output Directory: $OUTPUT_DIR"

# ============================================
# 1. Schema Validation
# ============================================

validate_schema() {
    local file=$1
    local report_file="$OUTPUT_DIR/$(basename "$file" .json)_schema.json"
    
    log_info "Validating Schema: $file"
    
    python3 "$SCRIPT_DIR/schema_validator.py" "$file" > /tmp/schema_output.txt 2>&1
    
    if [ $? -eq 0 ]; then
        log_success "Schema validation passed: $file"
        return 0
    else
        log_error "Schema validation failed: $file"
        cat /tmp/schema_output.txt
        return 1
    fi
}

# ============================================
# 2. Figma Layer Contract Validation
# ============================================

validate_figma_contract() {
    local file=$1
    local report_file="$OUTPUT_DIR/$(basename "$file" .json)_figma.json"
    
    log_info "Validating Figma Contract: $file"
    
    python3 "$SCRIPT_DIR/figma_layer_validator.py" "$file" > /tmp/figma_output.txt 2>&1
    
    if [ $? -eq 0 ]; then
        log_success "Figma contract validation passed: $file"
        return 0
    else
        log_warning "Figma contract validation has issues: $file"
        cat /tmp/figma_output.txt
        return 1
    fi
}

# ============================================
# 3. Design System Compliance
# ============================================

validate_design_system() {
    local file=$1
    local report_file="$OUTPUT_DIR/$(basename "$file" .json)_design.json"
    
    log_info "Checking Design System Compliance: $file"
    
    # Prüfe ob Datei Design System Elemente referenziert
    if grep -q "color\|typography\|spacing" "$file" 2>/dev/null; then
        log_success "Design system references found"
        return 0
    else
        log_warning "No design system references found"
        return 0
    fi
}

# ============================================
# 4. Content Quality Checks
# ============================================

validate_content_quality() {
    local file=$1
    
    log_info "Checking Content Quality: $file"
    
    # Prüfe ob system prompt zu kurz ist
    system_length=$(python3 -c "
import json
with open('$file') as f:
    data = json.load(f)
    print(len(data.get('system', '')))
" 2>/dev/null || echo "0")
    
    if [ "$system_length" -lt 20 ]; then
        log_warning "System message might be too short ($system_length chars)"
        return 1
    else
        log_success "Content quality looks good"
        return 0
    fi
}

# ============================================
# Main Validation Loop
# ============================================

validate_all_prompts() {
    local total=0
    local passed=0
    local failed=0
    
    echo
    log_info "Starting validation of all prompts..."
    echo
    
    for prompt_file in $(find "$PROMPT_DIR" -name "*.json" -type f | sort); do
        ((total++))
        
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "[$total] Validating: $(basename "$prompt_file")"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        schema_ok=true
        figma_ok=true
        design_ok=true
        quality_ok=true
        
        validate_schema "$prompt_file" || schema_ok=false
        validate_figma_contract "$prompt_file" || figma_ok=false
        validate_design_system "$prompt_file" || design_ok=false
        validate_content_quality "$prompt_file" || quality_ok=false
        
        if [ "$schema_ok" = true ] && [ "$figma_ok" = true ]; then
            log_success "Overall validation passed"
            ((passed++))
        else
            log_error "Overall validation failed"
            ((failed++))
        fi
        
        echo
    done
    
    # ============================================
    # Summary Report
    # ============================================
    
    echo
    echo "╔════════════════════════════════════════╗"
    echo "║      VALIDATION SUMMARY REPORT        ║"
    echo "╚════════════════════════════════════════╝"
    echo
    echo "Total Files:     $total"
    echo "Passed:          $passed"
    echo "Failed:          $failed"
    echo "Pass Rate:       $(echo "scale=1; $passed * 100 / $total" | bc)%"
    echo
    
    if [ $failed -eq 0 ]; then
        log_success "All validations passed! 🎉"
        return 0
    else
        log_error "Some validations failed"
        return 1
    fi
}

# ============================================
# Einzelne Datei Validierung
# ============================================

validate_single_file() {
    local file=$1
    
    if [ ! -f "$file" ]; then
        log_error "File not found: $file"
        return 1
    fi
    
    echo
    echo "╔════════════════════════════════════════╗"
    echo "║   VALIDATING SINGLE PROMPT FILE      ║"
    echo "╚════════════════════════════════════════╝"
    echo
    
    validate_schema "$file"
    local schema_result=$?
    
    validate_figma_contract "$file"
    local figma_result=$?
    
    validate_design_system "$file"
    local design_result=$?
    
    validate_content_quality "$file"
    local quality_result=$?
    
    echo
    if [ $schema_result -eq 0 ] && [ $figma_result -eq 0 ]; then
        log_success "File validation completed successfully"
        return 0
    else
        log_error "File validation has issues"
        return 1
    fi
}

# ============================================
# CLI
# ============================================

show_usage() {
    cat << EOF
Usage: $0 [OPTION] [FILE]

Options:
  all           Validate all prompts in directory
  file FILE     Validate single prompt file
  -h, --help    Show this help message

Environment Variables:
  PROMPT_DIR    Directory containing prompts (default: .)
  OUTPUT_DIR    Directory for reports (default: ./validation_reports)

Examples:
  $0 all
  $0 file prompts/my-prompt.json
  PROMPT_DIR=./prompts $0 all

EOF
}

# ============================================
# Main
# ============================================

case "${1:-all}" in
    all)
        validate_all_prompts
        exit $?
        ;;
    file)
        if [ -z "$2" ]; then
            log_error "No file specified"
            show_usage
            exit 1
        fi
        validate_single_file "$2"
        exit $?
        ;;
    -h|--help|help)
        show_usage
        exit 0
        ;;
    *)
        log_error "Unknown option: $1"
        show_usage
        exit 1
        ;;
esac

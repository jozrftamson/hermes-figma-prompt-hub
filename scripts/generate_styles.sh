#!/bin/bash
# CSS/SCSS Generator & Build System
# Automatisiert CSS-Generierung und Optimierung

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Functions
log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESIGN_SYSTEM_FILE="${DESIGN_SYSTEM_FILE:=./figma_design_system_extended.json}"
CSS_OUTPUT="${CSS_OUTPUT:=./css}"
SCSS_OUTPUT="${SCSS_OUTPUT:=./scss}"

show_usage() {
    cat << EOF
Usage: $0 [COMMAND] [OPTIONS]

Commands:
  css             Generate CSS files
  scss            Generate SCSS files
  all             Generate both CSS and SCSS
  watch           Watch and regenerate on changes
  build           Generate and minify all
  clean           Remove generated files
  serve           Serve CSS files locally
  -h, --help      Show this help

Options:
  -i, --input FILE         Design system JSON file (default: $DESIGN_SYSTEM_FILE)
  -o, --output DIR         Output directory (default: $CSS_OUTPUT)
  --no-minify              Skip minification
  --watch-dir DIR          Directory to watch for changes

Examples:
  $0 css -i design_system.json -o ./dist/css
  $0 scss
  $0 watch --watch-dir ./design
  $0 build

EOF
}

# ============================================
# Generate CSS
# ============================================
generate_css() {
    log_info "Generating CSS..."
    python3 "$SCRIPT_DIR/css_generator.py" "$DESIGN_SYSTEM_FILE" "$CSS_OUTPUT"
    log_success "CSS generation complete!"
}

# ============================================
# Generate SCSS
# ============================================
generate_scss() {
    log_info "Generating SCSS..."
    python3 "$SCRIPT_DIR/scss_generator.py" "$DESIGN_SYSTEM_FILE" "$SCSS_OUTPUT"
    log_success "SCSS generation complete!"
}

# ============================================
# Compile SCSS to CSS
# ============================================
compile_scss() {
    log_info "Compiling SCSS to CSS..."
    
    if ! command -v sass &> /dev/null; then
        log_warning "sass not found. Install with: npm install -g sass"
        return 1
    fi
    
    sass "$SCSS_OUTPUT/styles.scss" "$CSS_OUTPUT/styles.css"
    log_success "SCSS compiled!"
}

# ============================================
# Minify CSS
# ============================================
minify_css() {
    log_info "Minifying CSS..."
    
    if ! command -v csso &> /dev/null; then
        log_warning "csso not found. Install with: npm install -g csso-cli"
        return 1
    fi
    
    for file in "$CSS_OUTPUT"/*.css; do
        if [ -f "$file" ] && [[ ! "$file" == *.min.css ]]; then
            output="${file%.css}.min.css"
            csso "$file" --output "$output"
            log_success "Minified: $(basename "$output")"
        fi
    done
}

# ============================================
# Watch for changes
# ============================================
watch_changes() {
    local watch_dir="${1:-.}"
    
    log_info "Watching $watch_dir for changes..."
    
    if ! command -v fswatch &> /dev/null; then
        log_warning "fswatch not found. Install with: brew install fswatch"
        return 1
    fi
    
    fswatch -o "$watch_dir" | while read; do
        clear
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "Changes detected, regenerating..."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo
        generate_css
        generate_scss
        echo
        log_success "Ready for next change..."
        echo
    done
}

# ============================================
# Clean generated files
# ============================================
clean_build() {
    log_warning "Removing generated files..."
    
    rm -rf "$CSS_OUTPUT" "$SCSS_OUTPUT"
    
    log_success "Cleaned!"
}

# ============================================
# Build (generate + minify)
# ============================================
build_all() {
    log_info "Building CSS/SCSS..."
    
    generate_css
    generate_scss
    
    if command -v sass &> /dev/null; then
        compile_scss
    fi
    
    if command -v csso &> /dev/null; then
        minify_css
    else
        log_warning "csso not available, skipping minification"
    fi
    
    log_success "Build complete!"
    
    # Statistics
    echo
    echo "📊 Build Statistics:"
    echo "  CSS files: $(find "$CSS_OUTPUT" -name "*.css" -type f | wc -l)"
    echo "  SCSS files: $(find "$SCSS_OUTPUT" -name "*.scss" -type f | wc -l)"
    
    css_size=$(du -sh "$CSS_OUTPUT" | cut -f1)
    echo "  Total CSS size: $css_size"
}

# ============================================
# Serve CSS files
# ============================================
serve_css() {
    log_info "Serving CSS files..."
    
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 not found"
        return 1
    fi
    
    cd "$CSS_OUTPUT"
    python3 -m http.server 8000
}

# ============================================
# Analyze CSS
# ============================================
analyze_css() {
    log_info "Analyzing CSS..."
    
    total_size=0
    total_lines=0
    
    for file in "$CSS_OUTPUT"/*.css; do
        if [ -f "$file" ]; then
            size=$(du -h "$file" | cut -f1)
            lines=$(wc -l < "$file")
            filename=$(basename "$file")
            
            echo "  $filename: $lines lines, $size"
            total_size=$((total_size + $(du -b "$file" | cut -f1)))
            total_lines=$((total_lines + lines))
        fi
    done
    
    echo
    echo "📊 Total: $total_lines lines, ~$(numfmt --to=iec-i --suffix=B $total_size 2>/dev/null || echo "$total_size bytes")"
}

# ============================================
# Main
# ============================================

case "${1:-help}" in
    css)
        generate_css
        ;;
    scss)
        generate_scss
        ;;
    all)
        generate_css
        generate_scss
        ;;
    watch)
        watch_dir="${3:-.}"
        watch_changes "$watch_dir"
        ;;
    build)
        build_all
        ;;
    clean)
        clean_build
        ;;
    serve)
        serve_css
        ;;
    analyze)
        analyze_css
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

"""
SCSS Generator - Erweiterte Version mit SCSS Features
Generiert professionelles SCSS mit Mixins, Functions, Nesting
"""

import json
from pathlib import Path
from typing import Dict, List


class SCSSGenerator:
    """Generiert SCSS aus Design System JSON"""
    
    def __init__(self, design_system_path: str):
        """Lade Design System JSON"""
        with open(design_system_path, 'r', encoding='utf-8') as f:
            self.design_system = json.load(f)
        
        self.ds = self.design_system.get('figma_design_system', {})
    
    def generate_variables_scss(self) -> str:
        """Generiert SCSS Variablen-Datei"""
        lines = [
            "// ========================================",
            "// SCSS Design System Variables",
            "// ========================================",
            "",
            "// Colors",
            "$colors: (",
        ]
        
        colors = self.ds.get('color_palette', {})
        
        # Primary
        if colors.get('primary'):
            primary = colors['primary']
            lines.append(f"  'primary': {primary.get('hex')},")
            lines.append(f"  'primary-dark': {primary.get('variants', {}).get('700', '#1D4ED8')},")
            lines.append(f"  'primary-light': {primary.get('variants', {}).get('100', '#DBEAFE')},")
        
        # Secondary
        if colors.get('secondary'):
            secondary = colors['secondary']
            lines.append(f"  'secondary': {secondary.get('hex')},")
            lines.append(f"  'secondary-dark': {secondary.get('variants', {}).get('700', '#7E22CE')},")
        
        # Semantic
        semantic = colors.get('semantic', {})
        for color_name, color_data in semantic.items():
            lines.append(f"  '{color_name}': {color_data.get('hex')},")
        
        lines.append(");")
        lines.append("")
        
        # Typography
        lines.append("// Typography")
        typography = self.ds.get('typography', {})
        fonts = typography.get('font_families', {})
        
        if fonts:
            lines.append("$fonts: (")
            for font_name, font_data in fonts.items():
                lines.append(f"  'sans': {font_data.get('stack')},")
            lines.append(");")
            lines.append("")
        
        # Text sizes
        scales = typography.get('scales', {})
        lines.append("$text-sizes: (")
        for scale_name, scale_data in scales.items():
            lines.append(f"  '{scale_name}': {scale_data.get('size')},")
        lines.append(");")
        lines.append("")
        
        # Spacing
        lines.append("// Spacing Scale")
        spacing = self.ds.get('spacing', {})
        scale = spacing.get('scale', {})
        
        lines.append("$spacing: (")
        for space_name, space_value in scale.items():
            lines.append(f"  '{space_name}': {space_value},")
        lines.append(");")
        lines.append("")
        
        # Border radius
        lines.append("// Border Radius")
        radii = self.ds.get('border_radius', {})
        values = radii.get('values', {})
        
        lines.append("$radii: (")
        for radius_name, radius_value in values.items():
            lines.append(f"  '{radius_name}': {radius_value},")
        lines.append(");")
        lines.append("")
        
        # Shadows
        lines.append("// Shadows")
        shadows = self.ds.get('shadows', {})
        elevation = shadows.get('elevation', {})
        
        lines.append("$shadows: (")
        for shadow_name, shadow_data in elevation.items():
            lines.append(f"  '{shadow_name}': {shadow_data.get('css', 'none')},")
        lines.append(");")
        lines.append("")
        
        return "\n".join(lines)
    
    def generate_mixins_scss(self) -> str:
        """Generiert SCSS Mixins"""
        lines = [
            "// ========================================",
            "// SCSS Mixins",
            "// ========================================",
            "",
            "// Color Helper",
            "@mixin color($color) {",
            "  color: map-get($colors, $color);",
            "}",
            "",
            "@mixin bg($color) {",
            "  background-color: map-get($colors, $color);",
            "}",
            "",
            "// Shadow Elevation",
            "@mixin shadow($level: 'base') {",
            "  box-shadow: map-get($shadows, $level);",
            "}",
            "",
            "// Spacing",
            "@mixin spacing($property, $scale) {",
            "  #{$property}: map-get($spacing, $scale);",
            "}",
            "",
            "@mixin margin($top: null, $right: null, $bottom: null, $left: null) {",
            "  @if $top { margin-top: map-get($spacing, $top); }",
            "  @if $right { margin-right: map-get($spacing, $right); }",
            "  @if $bottom { margin-bottom: map-get($spacing, $bottom); }",
            "  @if $left { margin-left: map-get($spacing, $left); }",
            "}",
            "",
            "@mixin padding($top: null, $right: null, $bottom: null, $left: null) {",
            "  @if $top { padding-top: map-get($spacing, $top); }",
            "  @if $right { padding-right: map-get($spacing, $right); }",
            "  @if $bottom { padding-bottom: map-get($spacing, $bottom); }",
            "  @if $left { padding-left: map-get($spacing, $left); }",
            "}",
            "",
            "// Flexbox",
            "@mixin flex($direction: row, $justify: center, $align: center) {",
            "  display: flex;",
            "  flex-direction: $direction;",
            "  justify-content: $justify;",
            "  align-items: $align;",
            "}",
            "",
            "// Responsive",
            "@mixin mobile {",
            "  @media (max-width: 640px) { @content; }",
            "}",
            "",
            "@mixin tablet {",
            "  @media (min-width: 640px) and (max-width: 1024px) { @content; }",
            "}",
            "",
            "@mixin desktop {",
            "  @media (min-width: 1024px) { @content; }",
            "}",
            "",
            "// Button Styles",
            "@mixin button-base {",
            "  display: inline-flex;",
            "  align-items: center;",
            "  justify-content: center;",
            "  font-weight: 600;",
            "  transition: all 300ms ease-out;",
            "  cursor: pointer;",
            "  border: none;",
            "  outline: none;",
            "  border-radius: map-get($radii, 'lg');",
            "}",
            "",
            "@mixin button-variant($bg, $color, $hover-bg) {",
            "  @include button-base;",
            "  @include bg($bg);",
            "  @include color($color);",
            "",
            "  &:hover {",
            "    @include bg($hover-bg);",
            "    @include shadow('md');",
            "  }",
            "}",
            "",
            "// Cards",
            "@mixin card {",
            "  background: white;",
            "  border-radius: map-get($radii, 'xl');",
            "  @include padding('6', '6', '6', '6');",
            "  @include shadow('base');",
            "  transition: all 300ms ease;",
            "",
            "  &:hover {",
            "    @include shadow('lg');",
            "    transform: translateY(-2px);",
            "  }",
            "}",
            "",
            "// Input Focus",
            "@mixin input-focus {",
            "  border-color: map-get($colors, 'primary');",
            "  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);",
            "  outline: none;",
            "}",
            "",
            "// Truncate Text",
            "@mixin truncate {",
            "  overflow: hidden;",
            "  text-overflow: ellipsis;",
            "  white-space: nowrap;",
            "}",
            "",
            "// Line Clamp",
            "@mixin line-clamp($lines: 2) {",
            "  display: -webkit-box;",
            "  -webkit-line-clamp: $lines;",
            "  -webkit-box-orient: vertical;",
            "  overflow: hidden;",
            "}",
            "",
            "// Aspect Ratio",
            "@mixin aspect-ratio($width, $height) {",
            "  position: relative;",
            "",
            "  &::before {",
            "    content: '';",
            "    display: block;",
            "    padding-top: ($height / $width) * 100%;",
            "  }",
            "}",
            "",
            "// Container Queries (if supported)",
            "@mixin container-query($type: normal) {",
            "  @supports (container-type: $type) {",
            "    @content;",
            "  }",
            "}",
            "",
        ]
        
        return "\n".join(lines)
    
    def generate_functions_scss(self) -> str:
        """Generiert SCSS Functions"""
        lines = [
            "// ========================================",
            "// SCSS Functions",
            "// ========================================",
            "",
            "// Get color",
            "@function color($name) {",
            "  @return map-get($colors, $name);",
            "}",
            "",
            "// Get spacing",
            "@function spacing($scale) {",
            "  @return map-get($spacing, $scale);",
            "}",
            "",
            "// Get radius",
            "@function radius($type) {",
            "  @return map-get($radii, $type);",
            "}",
            "",
            "// Get shadow",
            "@function shadow($level) {",
            "  @return map-get($shadows, $level);",
            "}",
            "",
            "// Get text size",
            "@function text-size($scale) {",
            "  @return map-get($text-sizes, $scale);",
            "}",
            "",
            "// Color Lighten",
            "@function lighten-color($color, $amount) {",
            "  @return lighten($color, $amount);",
            "}",
            "",
            "// Color Darken",
            "@function darken-color($color, $amount) {",
            "  @return darken($color, $amount);",
            "}",
            "",
            "// Convert px to rem",
            "@function px-to-rem($px) {",
            "  @return ($px / 16px) * 1rem;",
            "}",
            "",
            "// Z-index Management",
            "$z-indexes: (",
            "  'dropdown': 1000,",
            "  'sticky': 1020,",
            "  'fixed': 1030,",
            "  'modal-backdrop': 1040,",
            "  'modal': 1050,",
            "  'popover': 1060,",
            "  'tooltip': 1070,",
            ");",
            "",
            "@function z($layer) {",
            "  @return map-get($z-indexes, $layer);",
            "}",
            "",
        ]
        
        return "\n".join(lines)
    
    def generate_utilities_scss(self) -> str:
        """Generiert SCSS Utility Classes"""
        lines = [
            "// ========================================",
            "// SCSS Utility Classes",
            "// ========================================",
            "",
            "// Display",
            ".d-flex { display: flex; }",
            ".d-grid { display: grid; }",
            ".d-block { display: block; }",
            ".d-inline { display: inline; }",
            ".d-inline-block { display: inline-block; }",
            ".d-none { display: none; }",
            "",
            "// Flexbox Direction",
            ".flex-row { flex-direction: row; }",
            ".flex-col { flex-direction: column; }",
            ".flex-row-reverse { flex-direction: row-reverse; }",
            ".flex-col-reverse { flex-direction: column-reverse; }",
            "",
            "// Justify Content",
            ".justify-start { justify-content: flex-start; }",
            ".justify-end { justify-content: flex-end; }",
            ".justify-center { justify-content: center; }",
            ".justify-between { justify-content: space-between; }",
            ".justify-around { justify-content: space-around; }",
            ".justify-evenly { justify-content: space-evenly; }",
            "",
            "// Align Items",
            ".items-start { align-items: flex-start; }",
            ".items-end { align-items: flex-end; }",
            ".items-center { align-items: center; }",
            ".items-baseline { align-items: baseline; }",
            ".items-stretch { align-items: stretch; }",
            "",
            "// Margin & Padding Utilities",
        ]
        
        spacing = self.ds.get('spacing', {}).get('scale', {})
        for space_name in ['1', '2', '3', '4', '5', '6', '8', '10']:
            if space_name in spacing:
                lines.append(f".m-{space_name} {{ @include spacing('margin', '{space_name}'); }}")
                lines.append(f".p-{space_name} {{ @include spacing('padding', '{space_name}'); }}")
        
        lines.extend([
            "",
            "// Text Utilities",
            ".text-center { text-align: center; }",
            ".text-left { text-align: left; }",
            ".text-right { text-align: right; }",
            ".text-justify { text-align: justify; }",
            "",
            ".font-normal { font-weight: 400; }",
            ".font-medium { font-weight: 500; }",
            ".font-semibold { font-weight: 600; }",
            ".font-bold { font-weight: 700; }",
            "",
            ".italic { font-style: italic; }",
            ".not-italic { font-style: normal; }",
            "",
            ".underline { text-decoration: underline; }",
            ".no-underline { text-decoration: none; }",
            "",
            ".uppercase { text-transform: uppercase; }",
            ".lowercase { text-transform: lowercase; }",
            ".capitalize { text-transform: capitalize; }",
            "",
            "// Overflow",
            ".overflow-auto { overflow: auto; }",
            ".overflow-hidden { overflow: hidden; }",
            ".overflow-visible { overflow: visible; }",
            ".overflow-scroll { overflow: scroll; }",
            "",
            ".truncate { @include truncate; }",
            "",
            "// Visibility",
            ".visible { visibility: visible; }",
            ".invisible { visibility: hidden; }",
            "",
            "// Opacity",
            ".opacity-0 { opacity: 0; }",
            ".opacity-25 { opacity: 0.25; }",
            ".opacity-50 { opacity: 0.5; }",
            ".opacity-75 { opacity: 0.75; }",
            ".opacity-100 { opacity: 1; }",
            "",
            "// Cursor",
            ".cursor-auto { cursor: auto; }",
            ".cursor-default { cursor: default; }",
            ".cursor-pointer { cursor: pointer; }",
            ".cursor-wait { cursor: wait; }",
            ".cursor-move { cursor: move; }",
            ".cursor-not-allowed { cursor: not-allowed; }",
            "",
            "// Background",
            ".bg-white { @include bg('white'); }",
            ".bg-black { @include bg('black'); }",
            ".bg-primary { @include bg('primary'); }",
            ".bg-secondary { @include bg('secondary'); }",
            "",
        ])
        
        return "\n".join(lines)
    
    def save_all_scss(self, output_dir: str = "./scss") -> Dict[str, str]:
        """Speichert alle SCSS-Dateien"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        files = {
            '_variables.scss': self.generate_variables_scss(),
            '_mixins.scss': self.generate_mixins_scss(),
            '_functions.scss': self.generate_functions_scss(),
            '_utilities.scss': self.generate_utilities_scss(),
        }
        
        # Main index file
        index_lines = [
            "// ========================================",
            "// Design System SCSS - Main Index",
            "// ========================================",
            "",
            "@import 'variables';",
            "@import 'functions';",
            "@import 'mixins';",
            "@import 'utilities';",
            "",
        ]
        files['styles.scss'] = "\n".join(index_lines)
        
        results = {}
        for filename, content in files.items():
            file_path = output_path / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            results[filename] = str(file_path)
            print(f"✅ Generated: {file_path}")
        
        return results


def generate_scss_from_file(design_system_path: str, output_dir: str = "./scss") -> Dict[str, str]:
    """Hilfsfunktion: SCSS aus Design System generieren"""
    generator = SCSSGenerator(design_system_path)
    return generator.save_all_scss(output_dir)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python scss_generator.py <design_system.json> [output_dir]")
        sys.exit(1)
    
    design_system_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./scss"
    
    print(f"🎨 Generating SCSS from: {design_system_file}")
    print(f"📁 Output directory: {output_dir}")
    print()
    
    results = generate_scss_from_file(design_system_file, output_dir)
    
    print()
    print("=" * 50)
    print("✅ SCSS Generation Complete!")
    print("=" * 50)
    print()
    print(f"Generated files:")
    for filename, path in sorted(results.items()):
        print(f"  - {filename}")

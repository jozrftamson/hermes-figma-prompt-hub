"""
CSS Generator aus Design System JSON
Generiert Production-ready CSS aus der Struktur
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass


@dataclass
class CSSOutput:
    variables: str
    typography: str
    layout: str
    components: str
    animations: str
    responsive: str


class CSSGenerator:
    """Generiert CSS aus Design System JSON"""
    
    def __init__(self, design_system_path: str):
        """Lade Design System JSON"""
        with open(design_system_path, 'r', encoding='utf-8') as f:
            self.design_system = json.load(f)
        
        self.ds = self.design_system.get('figma_design_system', {})
    
    def generate_all(self) -> CSSOutput:
        """Generiert all CSS-Dateien"""
        return CSSOutput(
            variables=self.generate_variables(),
            typography=self.generate_typography(),
            layout=self.generate_layout(),
            components=self.generate_components(),
            animations=self.generate_animations(),
            responsive=self.generate_responsive()
        )
    
    def generate_variables(self) -> str:
        """Generiert CSS Variables (CSS Custom Properties)"""
        lines = [
            "/* ========================================",
            "   Design System Variables",
            "   ======================================== */",
            "",
            ":root {",
            "  /* Color Palette */"
        ]
        
        # Colors
        colors = self.ds.get('color_palette', {})
        
        # Primary colors
        primary = colors.get('primary', {})
        if primary:
            lines.append(f"  {primary.get('css_variable')}: {primary.get('hex')};")
            variants = primary.get('variants', {})
            for shade, hex_color in variants.items():
                lines.append(f"  {primary.get('css_variable')}-{shade}: {hex_color};")
        
        # Secondary colors
        secondary = colors.get('secondary', {})
        if secondary:
            lines.append(f"  {secondary.get('css_variable')}: {secondary.get('hex')};")
            variants = secondary.get('variants', {})
            for shade, hex_color in variants.items():
                lines.append(f"  {secondary.get('css_variable')}-{shade}: {hex_color};")
        
        # Semantic colors
        semantic = colors.get('semantic', {})
        for color_name, color_data in semantic.items():
            lines.append(f"  {color_data.get('css_variable')}: {color_data.get('hex')};")
        
        # Neutral/Gray colors
        neutral = colors.get('neutral', {})
        for color_name, color_data in neutral.items():
            if isinstance(color_data, dict):
                lines.append(f"  {color_data.get('css_variable')}: {color_data.get('hex')};")
            elif isinstance(color_data, str):
                # Single value like white/black
                lines.append(f"  --color-{color_name}: {color_data};")
        
        # Gray scale (if present)
        if 'gray' in neutral and isinstance(neutral['gray'], dict):
            for shade, hex_color in neutral['gray'].items():
                lines.append(f"  --color-gray-{shade}: {hex_color};")
        
        lines.append("")
        lines.append("  /* Typography */")
        
        # Typography variables
        typography = self.ds.get('typography', {})
        
        # Font families
        fonts = typography.get('font_families', {})
        for font_name, font_data in fonts.items():
            lines.append(f"  {font_data.get('css_variable')}: {font_data.get('stack')};")
        
        # Text sizes
        scales = typography.get('scales', {})
        for scale_name, scale_data in scales.items():
            lines.append(f"  {scale_data.get('css_variable')}: {scale_data.get('size')};")
            lines.append(f"  --line-height-{scale_name}: {scale_data.get('line_height')};")
        
        lines.append("")
        lines.append("  /* Spacing */")
        
        # Spacing scale
        spacing = self.ds.get('spacing', {})
        scale = spacing.get('scale', {})
        for space_name, space_value in scale.items():
            lines.append(f"  --spacing-{space_name}: {space_value};")
        
        lines.append("")
        lines.append("  /* Border Radius */")
        
        # Border radius
        radii = self.ds.get('border_radius', {})
        values = radii.get('values', {})
        for radius_name, radius_value in values.items():
            lines.append(f"  --radius-{radius_name}: {radius_value};")
        
        lines.append("")
        lines.append("  /* Shadows / Elevation */")
        
        # Shadows
        shadows = self.ds.get('shadows', {})
        elevation = shadows.get('elevation', {})
        for shadow_name, shadow_data in elevation.items():
            css_shadow = shadow_data.get('css', 'none')
            lines.append(f"  --shadow-{shadow_name}: {css_shadow};")
        
        lines.append("}")
        lines.append("")
        
        return "\n".join(lines)
    
    def generate_typography(self) -> str:
        """Generiert Typography CSS"""
        lines = [
            "/* ========================================",
            "   Typography Styles",
            "   ======================================== */",
            ""
        ]
        
        typography = self.ds.get('typography', {})
        
        # Font families base
        fonts = typography.get('font_families', {})
        for font_name, font_data in fonts.items():
            lines.append(f".font-{font_name} {{")
            lines.append(f"  font-family: {font_data.get('css_variable')};")
            lines.append("}")
            lines.append("")
        
        # Heading hierarchy
        headings = {
            'h1': typography.get('scales', {}).get('4xl', {}),
            'h2': typography.get('scales', {}).get('3xl', {}),
            'h3': typography.get('scales', {}).get('2xl', {}),
            'h4': typography.get('scales', {}).get('xl', {}),
            'h5': typography.get('scales', {}).get('lg', {}),
            'h6': typography.get('scales', {}).get('base', {}),
        }
        
        for heading_name, heading_style in headings.items():
            if heading_style:
                lines.append(f"{heading_name} {{")
                lines.append(f"  font-size: {heading_style.get('css_variable')};")
                lines.append(f"  font-weight: 700;")
                lines.append(f"  line-height: {heading_style.get('line_height')};")
                lines.append(f"  letter-spacing: {heading_style.get('letter_spacing', '0')};")
                lines.append(f"  margin-bottom: var(--spacing-4);")
                lines.append("}")
                lines.append("")
        
        # Body text
        base_scale = typography.get('scales', {}).get('base', {})
        lines.append("body, p {")
        lines.append(f"  font-family: var(--font-sans);")
        lines.append(f"  font-size: {base_scale.get('css_variable')};")
        lines.append(f"  line-height: {base_scale.get('line_height')};")
        lines.append(f"  color: var(--color-gray-700);")
        lines.append("}")
        lines.append("")
        
        # Text utility classes
        scales = typography.get('scales', {})
        for scale_name, scale_data in scales.items():
            lines.append(f".text-{scale_name} {{")
            lines.append(f"  font-size: {scale_data.get('css_variable')};")
            lines.append(f"  line-height: {scale_data.get('line_height')};")
            lines.append("}")
            lines.append("")
        
        # Font weights
        lines.append("/* Font Weights */")
        lines.append(".font-thin { font-weight: 300; }")
        lines.append(".font-normal { font-weight: 400; }")
        lines.append(".font-medium { font-weight: 500; }")
        lines.append(".font-semibold { font-weight: 600; }")
        lines.append(".font-bold { font-weight: 700; }")
        lines.append(".font-extrabold { font-weight: 800; }")
        lines.append("")
        
        return "\n".join(lines)
    
    def generate_layout(self) -> str:
        """Generiert Layout CSS (Grid, Flex)"""
        lines = [
            "/* ========================================",
            "   Layout System",
            "   ======================================== */",
            ""
        ]
        
        layout = self.ds.get('layout_grid', {})
        breakpoints = layout.get('breakpoints', {})
        
        # Base container
        lines.append(".container {")
        lines.append("  width: 100%;")
        lines.append("  margin: 0 auto;")
        lines.append("  padding: 0 var(--spacing-4);")
        lines.append("}")
        lines.append("")
        
        # Grid system (12-column)
        lines.append("/* 12-Column Grid System */")
        lines.append(".grid {")
        lines.append("  display: grid;")
        lines.append("  grid-template-columns: repeat(12, 1fr);")
        lines.append("  gap: var(--spacing-4);")
        lines.append("}")
        lines.append("")
        
        # Column classes
        for col in range(1, 13):
            lines.append(f".col-{col} {{ grid-column: span {col}; }}")
        
        lines.append("")
        lines.append("/* Flexbox Utilities */")
        lines.append(".flex { display: flex; }")
        lines.append(".flex-col { flex-direction: column; }")
        lines.append(".flex-row { flex-direction: row; }")
        lines.append(".flex-center { align-items: center; justify-content: center; }")
        lines.append(".flex-between { justify-content: space-between; }")
        lines.append(".flex-around { justify-content: space-around; }")
        lines.append(".flex-end { justify-content: flex-end; }")
        lines.append(".flex-start { justify-content: flex-start; }")
        lines.append(".flex-wrap { flex-wrap: wrap; }")
        lines.append(".gap-4 { gap: var(--spacing-4); }")
        lines.append(".gap-8 { gap: var(--spacing-8); }")
        lines.append("")
        
        # Spacing utilities
        lines.append("/* Margin & Padding Utilities */")
        spacing = self.ds.get('spacing', {}).get('scale', {})
        for space_name in ['1', '2', '3', '4', '5', '6', '8', '10']:
            if space_name in spacing:
                lines.append(f".m-{space_name} {{ margin: var(--spacing-{space_name}); }}")
                lines.append(f".p-{space_name} {{ padding: var(--spacing-{space_name}); }}")
                lines.append(f".mx-{space_name} {{ margin-left: var(--spacing-{space_name}); margin-right: var(--spacing-{space_name}); }}")
                lines.append(f".my-{space_name} {{ margin-top: var(--spacing-{space_name}); margin-bottom: var(--spacing-{space_name}); }}")
        
        lines.append("")
        
        return "\n".join(lines)
    
    def generate_components(self) -> str:
        """Generiert Component CSS"""
        lines = [
            "/* ========================================",
            "   Component Styles",
            "   ======================================== */",
            ""
        ]
        
        components = self.ds.get('components', {})
        
        # Buttons
        if 'button' in components:
            button = components['button']
            
            lines.append("/* Buttons */")
            lines.append(".btn, button {")
            lines.append("  display: inline-flex;")
            lines.append("  align-items: center;")
            lines.append("  justify-content: center;")
            lines.append("  font-weight: 600;")
            lines.append("  transition: all 300ms ease-out;")
            lines.append("  cursor: pointer;")
            lines.append("  border: none;")
            lines.append("  outline: none;")
            lines.append("}")
            lines.append("")
            
            # Button variants
            variants = button.get('variants', {})
            for variant_name, variant_style in variants.items():
                lines.append(f".btn-{variant_name}, .btn.{variant_name} {{")
                lines.append(f"  background: {variant_style.get('background')};")
                lines.append(f"  color: {variant_style.get('color')};")
                lines.append(f"  padding: {variant_style.get('padding')};")
                lines.append(f"  border-radius: {variant_style.get('border_radius')};")
                if variant_style.get('border'):
                    lines.append(f"  border: {variant_style.get('border')};")
                lines.append(f"  box-shadow: {variant_style.get('shadow', 'none')};")
                lines.append("}")
                lines.append("")
                
                # Hover state
                hover = variant_style.get('hover', {})
                if hover:
                    lines.append(f".btn-{variant_name}:hover, .btn.{variant_name}:hover {{")
                    if hover.get('background'):
                        lines.append(f"  background: {hover.get('background')};")
                    if hover.get('shadow'):
                        lines.append(f"  box-shadow: {hover.get('shadow')};")
                    lines.append("}")
                    lines.append("")
            
            # Button sizes
            sizes = button.get('sizes', {})
            for size_name, size_style in sizes.items():
                lines.append(f".btn-{size_name} {{")
                lines.append(f"  padding: {size_style.get('padding')};")
                lines.append(f"  font-size: {size_style.get('font_size')};")
                lines.append("}")
                lines.append("")
        
        # Inputs
        if 'input' in components:
            input_comp = components['input']
            
            lines.append("/* Form Inputs */")
            lines.append("input, textarea, select {")
            lines.append("  padding: 12px 16px;")
            lines.append("  border: 1px solid var(--color-gray-200);")
            lines.append("  border-radius: var(--radius-md);")
            lines.append("  font-family: var(--font-sans);")
            lines.append("  font-size: var(--text-base);")
            lines.append("  transition: border-color 300ms ease, box-shadow 300ms ease;")
            lines.append("}")
            lines.append("")
            
            lines.append("input:focus, textarea:focus, select:focus {")
            lines.append("  border-color: var(--color-primary);")
            lines.append("  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);")
            lines.append("  outline: none;")
            lines.append("}")
            lines.append("")
            
            lines.append("input:disabled, textarea:disabled {")
            lines.append("  background: var(--color-gray-100);")
            lines.append("  border-color: var(--color-gray-200);")
            lines.append("  color: var(--color-gray-500);")
            lines.append("  cursor: not-allowed;")
            lines.append("}")
            lines.append("")
            
            lines.append("input[type='error'] {")
            lines.append("  border-color: var(--color-error);")
            lines.append("  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);")
            lines.append("}")
            lines.append("")
        
        # Cards
        if 'card' in components:
            card = components['card']
            
            lines.append("/* Cards */")
            variants = card.get('variants', {})
            for variant_name, variant_style in variants.items():
                lines.append(f".card.{variant_name}, .card-{variant_name} {{")
                lines.append(f"  background: {variant_style.get('background')};")
                lines.append(f"  border: {variant_style.get('border', 'none')};")
                lines.append(f"  border-radius: {variant_style.get('border_radius')};")
                lines.append(f"  padding: {variant_style.get('padding')};")
                if variant_style.get('shadow'):
                    lines.append(f"  box-shadow: {variant_style.get('shadow')};")
                
                hover = variant_style.get('hover', {})
                if hover:
                    lines.append("}")
                    lines.append("")
                    lines.append(f".card.{variant_name}:hover, .card-{variant_name}:hover {{")
                    if hover.get('shadow'):
                        lines.append(f"  box-shadow: {hover.get('shadow')};")
                    if hover.get('transform'):
                        lines.append(f"  transform: {hover.get('transform')};")
                    if hover.get('transition'):
                        lines.append(f"  transition: {hover.get('transition')};")
                
                lines.append("}")
                lines.append("")
        
        # Modal
        if 'modal' in components:
            modal = components['modal']
            
            lines.append("/* Modal Dialogs */")
            lines.append(".modal-overlay {")
            overlay = modal.get('overlay', {})
            lines.append(f"  background: {overlay.get('background')};")
            if overlay.get('backdrop_filter'):
                lines.append(f"  backdrop-filter: {overlay.get('backdrop_filter')};")
            lines.append("  position: fixed;")
            lines.append("  top: 0;")
            lines.append("  left: 0;")
            lines.append("  right: 0;")
            lines.append("  bottom: 0;")
            lines.append("}")
            lines.append("")
            
            lines.append(".modal-content {")
            content = modal.get('content', {})
            lines.append(f"  background: {content.get('background')};")
            lines.append(f"  border-radius: {content.get('border_radius')};")
            lines.append(f"  padding: {content.get('padding')};")
            lines.append(f"  max-width: {content.get('max_width')};")
            lines.append(f"  box-shadow: {content.get('shadow')};")
            lines.append("}")
            lines.append("")
        
        return "\n".join(lines)
    
    def generate_animations(self) -> str:
        """Generiert Animation CSS"""
        lines = [
            "/* ========================================",
            "   Animations & Transitions",
            "   ======================================== */",
            ""
        ]
        
        animations = self.ds.get('animations', {})
        
        # Transitions
        lines.append("/* Transitions */")
        transitions = animations.get('transitions', {})
        for transition_name, transition_value in transitions.items():
            lines.append(f".transition-{transition_name} {{")
            lines.append(f"  transition: all {transition_value};")
            lines.append("}")
        lines.append("")
        
        # Keyframes
        lines.append("/* Keyframe Animations */")
        keyframes = animations.get('keyframes', {})
        for keyframe_name, keyframe_data in keyframes.items():
            lines.append(f"@keyframes {keyframe_name} {{")
            
            for percent, styles in keyframe_data.items():
                if percent not in ['duration', 'iteration']:
                    lines.append(f"  {percent} {{")
                    if isinstance(styles, str):
                        lines.append(f"    {styles}")
                    else:
                        for prop, value in styles.items():
                            lines.append(f"    {prop}: {value};")
                    lines.append("  }")
            
            lines.append("}")
            lines.append("")
            
            # Create animation class
            duration = keyframe_data.get('duration', '1000ms')
            iteration = keyframe_data.get('iteration', 'normal')
            
            lines.append(f".animate-{keyframe_name} {{")
            lines.append(f"  animation: {keyframe_name} {duration} ease-out {iteration};")
            lines.append("}")
            lines.append("")
        
        return "\n".join(lines)
    
    def generate_responsive(self) -> str:
        """Generiert Responsive/Media Query CSS"""
        lines = [
            "/* ========================================",
            "   Responsive Design - Media Queries",
            "   ======================================== */",
            ""
        ]
        
        layout = self.ds.get('layout_grid', {})
        breakpoints = layout.get('breakpoints', {})
        
        for breakpoint_name, breakpoint_data in breakpoints.items():
            media_query = breakpoint_data.get('media_query', '')
            
            if not media_query:
                # Generate media query
                min_width = breakpoint_data.get('min_width', '')
                max_width = breakpoint_data.get('max_width', '')
                
                if min_width and max_width:
                    media_query = f"@media (min-width: {min_width}) and (max-width: {max_width})"
                elif min_width:
                    media_query = f"@media (min-width: {min_width})"
                elif max_width:
                    media_query = f"@media (max-width: {max_width})"
            
            if media_query:
                lines.append(media_query + " {")
                lines.append(f"  /* {breakpoint_name.upper()} */")
                lines.append("")
                
                # Grid settings
                columns = breakpoint_data.get('columns', 12)
                gutter = breakpoint_data.get('gutter', '16px')
                
                lines.append("  .grid {")
                lines.append(f"    grid-template-columns: repeat({columns}, 1fr);")
                lines.append(f"    gap: {gutter};")
                lines.append("  }")
                lines.append("")
                
                # Container settings
                container_padding = breakpoint_data.get('container_padding', '16px')
                lines.append("  .container {")
                lines.append(f"    padding: 0 {container_padding};")
                lines.append("  }")
                lines.append("")
                
                # Typography scaling
                typography = self.ds.get('typography', {})
                scales = typography.get('scales', {})
                
                lines.append("  /* Typography Scaling */")
                for scale_name, scale_data in scales.items():
                    if 'font_sizes' in breakpoint_data and scale_name in breakpoint_data['font_sizes']:
                        responsive_size = breakpoint_data['font_sizes'][scale_name]
                        lines.append(f"  .text-{scale_name} {{")
                        lines.append(f"    font-size: {responsive_size};")
                        lines.append("  }")
                
                lines.append("")
                
                # Column helpers
                lines.append("  /* Responsive Column Classes */")
                for col in range(1, columns + 1):
                    lines.append(f"  .col-{breakpoint_name}-{col} {{ grid-column: span {col}; }}")
                
                lines.append("}")
                lines.append("")
        
        return "\n".join(lines)
    
    def save_all(self, output_dir: str = "./css") -> Dict[str, str]:
        """Speichert alle CSS-Dateien"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        css_output = self.generate_all()
        
        files = {
            'variables.css': css_output.variables,
            'typography.css': css_output.typography,
            'layout.css': css_output.layout,
            'components.css': css_output.components,
            'animations.css': css_output.animations,
            'responsive.css': css_output.responsive,
        }
        
        results = {}
        for filename, content in files.items():
            file_path = output_path / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            results[filename] = str(file_path)
            print(f"✅ Generated: {file_path}")
        
        # Generate main index file
        index_path = output_path / 'index.css'
        index_content = self._generate_index(files.keys())
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
        results['index.css'] = str(index_path)
        print(f"✅ Generated: {index_path}")
        
        # Generate minified versions
        self._generate_minified(output_path, files)
        
        return results
    
    def _generate_index(self, filenames) -> str:
        """Generiert Index CSS Datei"""
        lines = [
            "/* ========================================",
            "   Design System CSS - Index",
            "   Import all CSS files from here",
            "   ======================================== */",
            "",
        ]
        
        for filename in sorted(filenames):
            if filename != 'index.css':
                import_name = filename.replace('.css', '')
                lines.append(f"@import './variables.css';")
        
        lines.extend([
            "@import './typography.css';",
            "@import './layout.css';",
            "@import './components.css';",
            "@import './animations.css';",
            "@import './responsive.css';",
            "",
        ])
        
        return "\n".join(lines)
    
    def _generate_minified(self, output_path: Path, files: Dict[str, str]) -> None:
        """Generiert minifizierte Versionen"""
        for filename, content in files.items():
            if filename != 'index.css':
                # Simple minification
                minified = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)  # Remove comments
                minified = re.sub(r'\s+', ' ', minified)  # Collapse whitespace
                minified = re.sub(r'\s*([{}:;,])\s*', r'\1', minified)  # Remove spaces around symbols
                minified = minified.strip()
                
                minified_path = output_path / filename.replace('.css', '.min.css')
                with open(minified_path, 'w', encoding='utf-8') as f:
                    f.write(minified)
                print(f"✅ Generated: {minified_path}")


def generate_css_from_file(design_system_path: str, output_dir: str = "./css") -> Dict[str, str]:
    """Hilfsfunktion: CSS aus Design System generieren"""
    generator = CSSGenerator(design_system_path)
    return generator.save_all(output_dir)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python css_generator.py <design_system.json> [output_dir]")
        sys.exit(1)
    
    design_system_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./css"
    
    print(f"🎨 Generating CSS from: {design_system_file}")
    print(f"📁 Output directory: {output_dir}")
    print()
    
    results = generate_css_from_file(design_system_file, output_dir)
    
    print()
    print("=" * 50)
    print("✅ CSS Generation Complete!")
    print("=" * 50)
    print()
    print(f"Generated files:")
    for filename, path in sorted(results.items()):
        print(f"  - {filename}")
    print()
    print(f"Total: {len(results)} files")

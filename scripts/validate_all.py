"""
Integrated Validation Runner
Orchestriert alle Validierungen (Schema, Layer Contract, Design System)
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# Import validators (würde in echtem Projekt absolute Imports sein)
# from schema_validator import PromptValidator, ValidationResult, ValidationLevel
# from figma_layer_validator import FigmaLayerValidator, ContractViolation, ContractLevel


class ValidationReport:
    """Generiert Validierungsbericht"""
    
    def __init__(self):
        self.timestamp = None
        self.file_path = None
        self.schema_results = []
        self.figma_results = []
        self.design_system_results = []
        self.quality_score = 0.0
        self.overall_valid = True
    
    def to_json(self) -> str:
        """Exportiert Report als JSON"""
        return json.dumps({
            "timestamp": self.timestamp,
            "file_path": self.file_path,
            "overall_valid": self.overall_valid,
            "quality_score": self.quality_score,
            "summary": {
                "schema_errors": len([r for r in self.schema_results if "ERROR" in str(r.get("level", ""))]),
                "figma_violations": len([r for r in self.figma_results if r.get("level") == "critical"]),
                "design_system_issues": len(self.design_system_results)
            },
            "schema_validation": self.schema_results,
            "figma_validation": self.figma_results,
            "design_system_validation": self.design_system_results
        }, indent=2)
    
    def to_markdown(self) -> str:
        """Exportiert Report als Markdown"""
        lines = [
            "# Prompt Validation Report",
            f"\n**File:** {self.file_path}",
            f"**Overall Valid:** {'✅ Yes' if self.overall_valid else '❌ No'}",
            f"**Quality Score:** {self.quality_score:.1%}",
            ""
        ]
        
        if self.schema_results:
            lines.append("## Schema Validation")
            errors = [r for r in self.schema_results if "ERROR" in str(r.get("level", ""))]
            warnings = [r for r in self.schema_results if "WARNING" in str(r.get("level", ""))]
            
            if errors:
                lines.append("### Errors")
                for error in errors:
                    lines.append(f"- **{error.get('code')}**: {error.get('message')}")
            
            if warnings:
                lines.append("### Warnings")
                for warning in warnings:
                    lines.append(f"- {warning.get('message')}")
        
        if self.figma_results:
            lines.append("\n## Figma Layer Contract")
            critical = [r for r in self.figma_results if r.get("level") == "critical"]
            if critical:
                lines.append("### Critical Violations")
                for v in critical:
                    lines.append(f"- **{v.get('code')}**: {v.get('message')}")
        
        return "\n".join(lines)


class ValidationSuite:
    """Orchestriert alle Validierungen"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.report = ValidationReport()
    
    def validate_prompt_file(self, file_path: str) -> Dict:
        """Validiert komplette Prompt-Datei mit allen Checks"""
        
        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            print(f"❌ File not found: {file_path}")
            return {"valid": False, "error": "FILE_NOT_FOUND"}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {e}")
            return {"valid": False, "error": "INVALID_JSON"}
        
        self.report.file_path = str(file_path)
        
        # 1. Schema Validation
        if self.verbose:
            print("\n📋 Running Schema Validation...")
        schema_valid = self._validate_schema(data)
        
        # 2. Figma Layer Contract (wenn from Figma)
        if self.verbose:
            print("📐 Running Figma Layer Contract Validation...")
        figma_valid = self._validate_figma_contract(data)
        
        # 3. Design System Compliance (wenn from Design System)
        if self.verbose:
            print("🎨 Running Design System Compliance Check...")
        design_valid = self._validate_design_system_compliance(data)
        
        # 4. Calculate Quality Score
        self.report.quality_score = self._calculate_quality_score()
        
        self.report.overall_valid = schema_valid and figma_valid and design_valid
        
        if self.verbose:
            self._print_summary()
        
        return {
            "valid": self.report.overall_valid,
            "quality_score": self.report.quality_score,
            "schema_valid": schema_valid,
            "figma_valid": figma_valid,
            "design_valid": design_valid
        }
    
    def _validate_schema(self, data: Dict) -> bool:
        """Schema Validation"""
        required_fields = ["prompt_id", "name", "description", "version", "strategy", "category", "system", "user_template"]
        errors = []
        
        for field in required_fields:
            if field not in data:
                errors.append({
                    "level": "ERROR",
                    "code": "MISSING_FIELD",
                    "message": f"Missing required field: {field}",
                    "path": field
                })
            elif not data[field]:
                errors.append({
                    "level": "ERROR",
                    "code": "EMPTY_FIELD",
                    "message": f"Field '{field}' is empty",
                    "path": field
                })
        
        # Type checks
        strategy = data.get("strategy")
        if strategy not in ["chain-of-thought", "few-shot", "role-play", "tree-of-thought", "meta-reasoning"]:
            errors.append({
                "level": "ERROR",
                "code": "INVALID_STRATEGY",
                "message": f"Invalid strategy: {strategy}",
                "path": "strategy"
            })
        
        # Strategy-specific checks
        if strategy == "few-shot":
            if "examples" not in data or len(data.get("examples", [])) < 2:
                errors.append({
                    "level": "ERROR",
                    "code": "MISSING_EXAMPLES",
                    "message": "Few-shot strategy requires at least 2 examples",
                    "path": "examples"
                })
        
        self.report.schema_results = errors
        
        if self.verbose and errors:
            print(f"  ⚠️  Found {len(errors)} issues")
            for error in errors[:3]:
                print(f"    - {error['code']}: {error['message']}")
        
        return len(errors) == 0
    
    def _validate_figma_contract(self, data: Dict) -> bool:
        """Figma Layer Contract Validation"""
        violations = []
        
        # Check if has figma-specific fields
        if "figma_metadata" in data:
            figma_data = data.get("figma_metadata", {})
            
            # Validate frame naming
            frame_name = figma_data.get("frame_name", "")
            if not frame_name.startswith("PROMPT/"):
                violations.append({
                    "level": "high",
                    "code": "INVALID_FRAME_NAME",
                    "message": f"Frame should start with 'PROMPT/', got: {frame_name}"
                })
            
            # Validate layer structure
            required_layers = ["METADATA", "CONTENT", "EXAMPLES"]
            for layer in required_layers:
                if layer not in figma_data.get("layers", []):
                    violations.append({
                        "level": "critical",
                        "code": "MISSING_LAYER",
                        "message": f"Missing required layer: {layer}"
                    })
        
        self.report.figma_results = violations
        
        if self.verbose and violations:
            print(f"  ⚠️  Found {len(violations)} contract violations")
        
        return len([v for v in violations if v.get("level") == "critical"]) == 0
    
    def _validate_design_system_compliance(self, data: Dict) -> bool:
        """Design System Compliance"""
        issues = []
        
        # Check colors
        if "colors" in data:
            valid_colors = ["primary", "secondary", "success", "warning", "error", "info"]
            for color in data.get("colors", []):
                if color not in valid_colors:
                    issues.append({
                        "level": "warning",
                        "code": "UNKNOWN_COLOR",
                        "message": f"Unknown color: {color}, should be one of {valid_colors}"
                    })
        
        # Check typography
        if "typography" in data:
            valid_scales = ["xs", "sm", "base", "lg", "xl", "2xl", "3xl", "4xl"]
            for scale in data.get("typography", []):
                if scale not in valid_scales:
                    issues.append({
                        "level": "info",
                        "code": "UNKNOWN_TYPE_SCALE",
                        "message": f"Unknown typography scale: {scale}"
                    })
        
        self.report.design_system_results = issues
        
        if self.verbose and issues:
            print(f"  ℹ️  Found {len(issues)} design system notes")
        
        return True
    
    def _calculate_quality_score(self) -> float:
        """Berechnet Gesamtqualitäts-Score"""
        max_score = 1.0
        deductions = 0.0
        
        # Schema errors: -0.2 each (max 0.3)
        schema_errors = len([r for r in self.report.schema_results if r.get("level") == "ERROR"])
        deductions += min(0.3, schema_errors * 0.1)
        
        # Schema warnings: -0.1 each (max 0.15)
        schema_warnings = len([r for r in self.report.schema_results if r.get("level") == "WARNING"])
        deductions += min(0.15, schema_warnings * 0.05)
        
        # Figma violations: -0.2 each (max 0.4)
        figma_critical = len([r for r in self.report.figma_results if r.get("level") == "critical"])
        deductions += min(0.4, figma_critical * 0.1)
        
        figma_high = len([r for r in self.report.figma_results if r.get("level") == "high"])
        deductions += min(0.2, figma_high * 0.05)
        
        return max(0.0, max_score - deductions)
    
    def _print_summary(self) -> None:
        """Gibt Zusammenfassung aus"""
        status = "✅ VALID" if self.report.overall_valid else "❌ INVALID"
        print(f"\n{'='*50}")
        print(f"Status: {status}")
        print(f"Quality Score: {self.report.quality_score:.1%}")
        print(f"{'='*50}")
    
    def export_report(self, output_format: str = "json") -> str:
        """Exportiert Report"""
        if output_format == "json":
            return self.report.to_json()
        elif output_format == "markdown":
            return self.report.to_markdown()
        else:
            raise ValueError(f"Unknown format: {output_format}")


def validate_directory(directory: str, pattern: str = "*.json") -> Dict:
    """Validiert alle Prompts in Verzeichnis"""
    dir_path = Path(directory)
    results = {}
    
    print(f"\n🔍 Scanning directory: {directory}")
    
    for file_path in sorted(dir_path.glob(pattern)):
        if file_path.is_file():
            print(f"\n📄 Validating: {file_path.name}")
            suite = ValidationSuite(verbose=False)
            result = suite.validate_prompt_file(str(file_path))
            results[file_path.name] = result
    
    # Summary
    total = len(results)
    valid = len([r for r in results.values() if r.get("valid")])
    avg_score = sum(r.get("quality_score", 0) for r in results.values()) / total if total > 0 else 0
    
    print(f"\n{'='*50}")
    print(f"📊 SUMMARY")
    print(f"{'='*50}")
    print(f"Total files: {total}")
    print(f"Valid: {valid}/{total}")
    print(f"Average Quality Score: {avg_score:.1%}")
    print(f"{'='*50}\n")
    
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_all.py <file_or_directory> [format: json|markdown]")
        sys.exit(1)
    
    path = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else "json"
    
    path_obj = Path(path)
    
    if path_obj.is_file():
        print(f"🔍 Validating single file: {path}")
        suite = ValidationSuite(verbose=True)
        result = suite.validate_prompt_file(path)
        
        # Export report
        report = suite.export_report(output_format)
        
        if output_format == "markdown":
            print("\n" + report)
        else:
            print("\n" + report)
        
        sys.exit(0 if result.get("valid") else 1)
    
    elif path_obj.is_dir():
        results = validate_directory(path)
        valid_count = len([r for r in results.values() if r.get("valid")])
        sys.exit(0 if valid_count == len(results) else 1)
    
    else:
        print(f"❌ Path not found: {path}")
        sys.exit(1)

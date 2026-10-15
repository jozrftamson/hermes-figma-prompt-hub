"""
Figma Layer Contract Validator
Prüft ob Figma Frame-Struktur dem Layer Contract entspricht
"""

import json
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class ContractLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class ContractViolation:
    level: ContractLevel
    code: str
    message: str
    path: str = ""
    suggestion: Optional[str] = None


class FigmaLayerContract:
    """Definiert den Figma Layer Contract"""
    
    FRAME_NAME_PATTERN = r"^PROMPT/[a-z0-9\-_]+(/v\d+(\.\d+)*)?$"
    
    REQUIRED_CHILD_FRAMES = {
        "METADATA": {
            "type": "group",
            "required_fields": ["title", "description", "category", "strategy", "version"],
            "field_types": {
                "title": "text",
                "description": "text",
                "category": "enum",
                "strategy": "enum",
                "version": "text"
            }
        },
        "CONTENT": {
            "type": "group",
            "required_children": {
                "system": {"type": "text", "min_length": 20},
                "user_template": {"type": "text", "min_length": 10},
                "guardrails": {"type": "text", "min_length": 0},
                "output_format": {"type": "text", "min_length": 0}
            }
        },
        "EXAMPLES": {
            "type": "group",
            "min_examples": 1,
            "example_structure": {
                "input": {"type": "text", "required": True},
                "output": {"type": "text", "required": True},
                "explanation": {"type": "text", "required": False}
            }
        },
        "STRATEGY_CONFIG": {
            "type": "group",
            "strategy_specific": True
        }
    }
    
    ENUM_VALUES = {
        "category": ["analysis", "generation", "reasoning", "classification", "other"],
        "strategy": ["chain-of-thought", "few-shot", "role-play", "tree-of-thought", "meta-reasoning"]
    }


class FigmaLayerValidator:
    """Validiert Figma Layer-Struktur"""
    
    def __init__(self):
        self.violations: List[ContractViolation] = []
        self.contract = FigmaLayerContract()
    
    def validate_figma_export(self, figma_data: Dict) -> Tuple[bool, List[ContractViolation]]:
        """
        Validiert exportierte Figma-Daten
        Erwartet Format: {"pages": [{"frames": [...]}]}
        """
        self.violations = []
        
        # Prüfe grundstruktur
        if "pages" not in figma_data:
            self.violations.append(ContractViolation(
                level=ContractLevel.CRITICAL,
                code="INVALID_EXPORT_FORMAT",
                message="Figma export must have 'pages' field",
                suggestion="Export file should be from Figma plugin with proper structure"
            ))
            return False, self.violations
        
        # Prüfe jeden Frame
        for page_idx, page in enumerate(figma_data.get("pages", [])):
            for frame_idx, frame in enumerate(page.get("frames", [])):
                frame_path = f"pages[{page_idx}].frames[{frame_idx}]"
                self._validate_prompt_frame(frame, frame_path)
        
        is_valid = not any(v.level == ContractLevel.CRITICAL for v in self.violations)
        return is_valid, self.violations
    
    def _validate_prompt_frame(self, frame: Dict, path: str) -> None:
        """Validiert einzelnen PROMPT/* Frame"""
        frame_name = frame.get("name", "")
        
        # 1. Frame Name Format
        if not re.match(self.contract.FRAME_NAME_PATTERN, frame_name):
            self.violations.append(ContractViolation(
                level=ContractLevel.CRITICAL,
                code="INVALID_FRAME_NAME",
                message=f"Frame name '{frame_name}' doesn't match pattern PROMPT/{{id}}[/vX.X]",
                path=path,
                suggestion="Rename frame to: PROMPT/my-prompt-name or PROMPT/my-prompt-name/v1"
            ))
            return
        
        # 2. Prüfe erforderliche Child Frames
        children = frame.get("children", [])
        child_names = {child.get("name") for child in children}
        
        for required_name, requirements in self.contract.REQUIRED_CHILD_FRAMES.items():
            if required_name not in child_names:
                self.violations.append(ContractViolation(
                    level=ContractLevel.CRITICAL if required_name in ["METADATA", "CONTENT"] else ContractLevel.HIGH,
                    code="MISSING_REQUIRED_FRAME",
                    message=f"Required child frame missing: {required_name}",
                    path=f"{path}.children",
                    suggestion=f"Add a group frame named '{required_name}'"
                ))
                continue
            
            # Validiere diesen Child Frame
            child_frame = next(c for c in children if c.get("name") == required_name)
            child_path = f"{path}.children.{required_name}"
            
            if required_name == "METADATA":
                self._validate_metadata_frame(child_frame, child_path)
            elif required_name == "CONTENT":
                self._validate_content_frame(child_frame, child_path)
            elif required_name == "EXAMPLES":
                self._validate_examples_frame(child_frame, child_path)
    
    def _validate_metadata_frame(self, frame: Dict, path: str) -> None:
        """Validiert METADATA Frame"""
        required_fields = self.contract.REQUIRED_CHILD_FRAMES["METADATA"]["required_fields"]
        children = frame.get("children", [])
        child_names = {child.get("name") for child in children}
        
        for field in required_fields:
            if field not in child_names:
                self.violations.append(ContractViolation(
                    level=ContractLevel.HIGH,
                    code="MISSING_METADATA_FIELD",
                    message=f"METADATA missing required field: {field}",
                    path=f"{path}.{field}",
                    suggestion=f"Add text element named '{field}' to METADATA"
                ))
    
    def _validate_content_frame(self, frame: Dict, path: str) -> None:
        """Validiert CONTENT Frame"""
        required_children = self.contract.REQUIRED_CHILD_FRAMES["CONTENT"]["required_children"]
        children = frame.get("children", [])
        child_names = {child.get("name") for child in children}
        
        for field_name, field_spec in required_children.items():
            if field_name not in child_names and field_spec["min_length"] > 0:
                self.violations.append(ContractViolation(
                    level=ContractLevel.CRITICAL if field_name in ["system", "user_template"] else ContractLevel.HIGH,
                    code="MISSING_CONTENT_FIELD",
                    message=f"CONTENT missing required field: {field_name}",
                    path=f"{path}.{field_name}",
                    suggestion=f"Add text element named '{field_name}' to CONTENT"
                ))
            elif field_name in child_names:
                # Prüfe Mindestlänge
                text_frame = next(c for c in children if c.get("name") == field_name)
                content = text_frame.get("content", "")
                
                if len(content) < field_spec["min_length"]:
                    self.violations.append(ContractViolation(
                        level=ContractLevel.WARNING if field_spec["min_length"] < 50 else ContractLevel.MEDIUM,
                        code="CONTENT_TOO_SHORT",
                        message=f"{field_name} is too short (min: {field_spec['min_length']}, got: {len(content)})",
                        path=f"{path}.{field_name}",
                        suggestion=f"Expand content to at least {field_spec['min_length']} characters"
                    ))
    
    def _validate_examples_frame(self, frame: Dict, path: str) -> None:
        """Validiert EXAMPLES Frame"""
        examples = frame.get("children", [])
        min_examples = self.contract.REQUIRED_CHILD_FRAMES["EXAMPLES"]["min_examples"]
        
        # Zähle valide Beispiele (haben input + output)
        valid_examples = 0
        for idx, example in enumerate(examples):
            example_children = example.get("children", [])
            child_names = {c.get("name") for c in example_children}
            
            if "input" in child_names and "output" in child_names:
                valid_examples += 1
            else:
                self.violations.append(ContractViolation(
                    level=ContractLevel.MEDIUM,
                    code="INCOMPLETE_EXAMPLE",
                    message=f"Example {idx} missing 'input' or 'output' field",
                    path=f"{path}.examples[{idx}]",
                    suggestion="Each example should have: input, output, and optionally explanation"
                ))
        
        if valid_examples < min_examples:
            self.violations.append(ContractViolation(
                level=ContractLevel.HIGH,
                code="INSUFFICIENT_EXAMPLES",
                message=f"Need at least {min_examples} complete examples, got {valid_examples}",
                path=f"{path}",
                suggestion=f"Add at least {min_examples - valid_examples} more complete examples"
            ))
    
    def print_violations(self) -> None:
        """Gibt Violations aus"""
        if not self.violations:
            print("✓ Figma layer contract validated successfully!")
            return
        
        critical = [v for v in self.violations if v.level == ContractLevel.CRITICAL]
        high = [v for v in self.violations if v.level == ContractLevel.HIGH]
        medium = [v for v in self.violations if v.level == ContractLevel.MEDIUM]
        low = [v for v in self.violations if v.level == ContractLevel.LOW]
        
        if critical:
            print(f"\n🔴 CRITICAL ({len(critical)}):")
            for v in critical:
                print(f"  [{v.code}] {v.message}")
                if v.suggestion:
                    print(f"    → {v.suggestion}")
        
        if high:
            print(f"\n🟠 HIGH ({len(high)}):")
            for v in high:
                print(f"  [{v.code}] {v.message}")
                if v.suggestion:
                    print(f"    → {v.suggestion}")
        
        if medium:
            print(f"\n🟡 MEDIUM ({len(medium)}):")
            for v in medium:
                print(f"  [{v.code}] {v.message}")
                if v.suggestion:
                    print(f"    → {v.suggestion}")
        
        if low:
            print(f"\n🔵 LOW ({len(low)}):")
            for v in low:
                print(f"  [{v.code}] {v.message}")


def validate_figma_export_file(file_path: str) -> Tuple[bool, List[ContractViolation]]:
    """Validiert Figma Export JSON"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            figma_data = json.load(f)
    except json.JSONDecodeError as e:
        return False, [ContractViolation(
            level=ContractLevel.CRITICAL,
            code="INVALID_JSON",
            message=f"Invalid JSON: {str(e)}",
            path=file_path
        )]
    except FileNotFoundError:
        return False, [ContractViolation(
            level=ContractLevel.CRITICAL,
            code="FILE_NOT_FOUND",
            message=f"File not found: {file_path}",
            path=file_path
        )]
    
    validator = FigmaLayerValidator()
    return validator.validate_figma_export(figma_data)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python figma_layer_validator.py <figma_export.json>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    is_valid, violations = validate_figma_export_file(file_path)
    
    validator = FigmaLayerValidator()
    validator.violations = violations
    validator.print_violations()
    
    sys.exit(0 if is_valid else 1)

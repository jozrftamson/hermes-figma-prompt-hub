"""
Schema Validator für Hermes Figma Prompt Hub
Validiert Prompt JSON gegen Hermes Schema und Custom Constraints
"""

import json
import re
from typing import Dict, List, Tuple, Any, Optional
from enum import Enum
from dataclasses import dataclass
from pathlib import Path


class ValidationLevel(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationResult:
    level: ValidationLevel
    code: str
    message: str
    path: str = ""
    value: Any = None
    suggestion: Optional[str] = None


class HermesPromptSchema:
    """Definiert das vollständige Hermes Prompt Schema"""
    
    REQUIRED_FIELDS = {
        "prompt_id": "string",
        "name": "string",
        "description": "string",
        "version": "string",
        "strategy": "enum",
        "category": "enum",
        "system": "string",
        "user_template": "string",
    }
    
    OPTIONAL_FIELDS = {
        "guardrails": "array",
        "examples": "array",
        "variables": "object",
        "output_format": "object",
        "metadata": "object",
        "tags": "array",
        "changelog": "array",
    }
    
    ENUM_VALUES = {
        "strategy": ["chain-of-thought", "few-shot", "role-play", "tree-of-thought", "meta-reasoning"],
        "category": ["analysis", "generation", "reasoning", "classification", "other"],
        "version": r"^v\d+(\.\d+)*$",  # regex for semantic versioning
    }
    
    CONSTRAINTS = {
        "prompt_id": {
            "min_length": 3,
            "max_length": 100,
            "pattern": r"^[a-z0-9\-_]+$",
            "description": "Lowercase alphanumeric, hyphens, underscores only"
        },
        "name": {
            "min_length": 5,
            "max_length": 150,
            "description": "Human-readable prompt name"
        },
        "description": {
            "min_length": 10,
            "max_length": 1000,
            "description": "Clear description of prompt purpose"
        },
        "system": {
            "min_length": 20,
            "max_length": 10000,
            "description": "System message defining AI behavior"
        },
        "user_template": {
            "min_length": 10,
            "max_length": 10000,
            "description": "User message template with {{variables}}"
        },
        "version": {
            "pattern": r"^v\d+(\.\d+)*$",
            "description": "Semantic versioning: v1, v1.0, v1.2.3"
        }
    }
    
    STRATEGY_SPECIFIC_REQUIREMENTS = {
        "chain-of-thought": {
            "required_keywords": ["step", "reason", "structured"],
            "recommend_field": "guardrails",
            "min_system_length": 50
        },
        "few-shot": {
            "required_field": "examples",
            "min_examples": 2,
            "max_examples": 5,
            "recommend_structure": "input_output_pairs"
        },
        "role-play": {
            "required_keywords": ["role", "expertise", "personality"],
            "recommend_field": "guardrails",
            "min_system_length": 80
        },
        "tree-of-thought": {
            "required_keywords": ["approach", "branch", "compare"],
            "min_approaches": 2,
            "max_approaches": 5
        },
        "meta-reasoning": {
            "required_keywords": ["validate", "check", "verify"],
            "recommend_field": "validation_checklist"
        }
    }


class PromptValidator:
    """Validiert Prompts gegen Schema und Best Practices"""
    
    def __init__(self):
        self.results: List[ValidationResult] = []
        self.schema = HermesPromptSchema()
    
    def validate(self, prompt_data: Dict) -> Tuple[bool, List[ValidationResult]]:
        """
        Hauptvalidierungsfunktion
        Returns: (is_valid, results_list)
        """
        self.results = []
        
        # 1. Basis-Feldvalidierung
        self._validate_required_fields(prompt_data)
        
        # 2. Feldtyp-Validierung
        self._validate_field_types(prompt_data)
        
        # 3. Constraint-Validierung
        self._validate_constraints(prompt_data)
        
        # 4. Strategie-spezifische Validierung
        self._validate_strategy_requirements(prompt_data)
        
        # 5. Variable-Validierung
        self._validate_variables(prompt_data)
        
        # 6. Beispiele-Validierung
        self._validate_examples(prompt_data)
        
        # 7. Content-Qualität
        self._validate_content_quality(prompt_data)
        
        # 8. Token-Schätzung
        self._estimate_tokens(prompt_data)
        
        is_valid = not any(r.level == ValidationLevel.ERROR for r in self.results)
        return is_valid, self.results
    
    def _validate_required_fields(self, prompt_data: Dict) -> None:
        """Prüft ob alle erforderlichen Felder vorhanden sind"""
        for field in self.schema.REQUIRED_FIELDS.keys():
            if field not in prompt_data:
                self.results.append(ValidationResult(
                    level=ValidationLevel.ERROR,
                    code="MISSING_REQUIRED_FIELD",
                    message=f"Required field missing: {field}",
                    path=field,
                    suggestion=f"Add '{field}' field to prompt specification"
                ))
            elif not prompt_data[field]:
                self.results.append(ValidationResult(
                    level=ValidationLevel.ERROR,
                    code="EMPTY_REQUIRED_FIELD",
                    message=f"Required field is empty: {field}",
                    path=field,
                    value=prompt_data[field],
                    suggestion=f"Populate '{field}' with meaningful content"
                ))
    
    def _validate_field_types(self, prompt_data: Dict) -> None:
        """Prüft Feldtypen"""
        all_fields = {**self.schema.REQUIRED_FIELDS, **self.schema.OPTIONAL_FIELDS}
        
        for field, expected_type in all_fields.items():
            if field not in prompt_data:
                continue
            
            value = prompt_data[field]
            
            if expected_type == "string" and not isinstance(value, str):
                self.results.append(ValidationResult(
                    level=ValidationLevel.ERROR,
                    code="INVALID_FIELD_TYPE",
                    message=f"Field '{field}' should be string, got {type(value).__name__}",
                    path=field,
                    value=value
                ))
            elif expected_type == "array" and not isinstance(value, list):
                self.results.append(ValidationResult(
                    level=ValidationLevel.ERROR,
                    code="INVALID_FIELD_TYPE",
                    message=f"Field '{field}' should be array, got {type(value).__name__}",
                    path=field,
                    value=value
                ))
            elif expected_type == "object" and not isinstance(value, dict):
                self.results.append(ValidationResult(
                    level=ValidationLevel.ERROR,
                    code="INVALID_FIELD_TYPE",
                    message=f"Field '{field}' should be object, got {type(value).__name__}",
                    path=field,
                    value=value
                ))
            elif expected_type == "enum":
                self._validate_enum(field, value)
    
    def _validate_enum(self, field: str, value: str) -> None:
        """Prüft ENUM-Werte"""
        if field not in self.schema.ENUM_VALUES:
            return
        
        allowed_values = self.schema.ENUM_VALUES[field]
        
        if isinstance(allowed_values, list):
            if value not in allowed_values:
                self.results.append(ValidationResult(
                    level=ValidationLevel.ERROR,
                    code="INVALID_ENUM_VALUE",
                    message=f"Invalid value for '{field}': '{value}'",
                    path=field,
                    value=value,
                    suggestion=f"Must be one of: {', '.join(allowed_values)}"
                ))
    
    def _validate_constraints(self, prompt_data: Dict) -> None:
        """Prüft String-Constraints (Länge, Pattern)"""
        for field, constraints in self.schema.CONSTRAINTS.items():
            if field not in prompt_data:
                continue
            
            value = prompt_data[field]
            if not isinstance(value, str):
                continue
            
            # Min/Max Länge
            if "min_length" in constraints:
                if len(value) < constraints["min_length"]:
                    self.results.append(ValidationResult(
                        level=ValidationLevel.WARNING,
                        code="FIELD_TOO_SHORT",
                        message=f"Field '{field}' is too short (min: {constraints['min_length']}, got: {len(value)})",
                        path=field,
                        value=value,
                        suggestion=f"Expand '{field}' to at least {constraints['min_length']} characters"
                    ))
            
            if "max_length" in constraints:
                if len(value) > constraints["max_length"]:
                    self.results.append(ValidationResult(
                        level=ValidationLevel.ERROR,
                        code="FIELD_TOO_LONG",
                        message=f"Field '{field}' is too long (max: {constraints['max_length']}, got: {len(value)})",
                        path=field,
                        value=value,
                        suggestion=f"Reduce '{field}' to {constraints['max_length']} characters"
                    ))
            
            # Pattern (Regex)
            if "pattern" in constraints:
                pattern = constraints["pattern"]
                if not re.match(pattern, value):
                    self.results.append(ValidationResult(
                        level=ValidationLevel.ERROR,
                        code="INVALID_FORMAT",
                        message=f"Field '{field}' doesn't match required format: {pattern}",
                        path=field,
                        value=value,
                        suggestion=constraints.get("description", "Check field format")
                    ))
    
    def _validate_strategy_requirements(self, prompt_data: Dict) -> None:
        """Prüft strategie-spezifische Anforderungen"""
        strategy = prompt_data.get("strategy")
        if not strategy or strategy not in self.schema.STRATEGY_SPECIFIC_REQUIREMENTS:
            return
        
        requirements = self.schema.STRATEGY_SPECIFIC_REQUIREMENTS[strategy]
        
        # Prüfe erforderliche Keywords
        if "required_keywords" in requirements:
            system_text = prompt_data.get("system", "").lower()
            for keyword in requirements["required_keywords"]:
                if keyword.lower() not in system_text:
                    self.results.append(ValidationResult(
                        level=ValidationLevel.WARNING,
                        code="MISSING_STRATEGY_KEYWORD",
                        message=f"Strategy '{strategy}' should mention '{keyword}' in system message",
                        path="system",
                        suggestion=f"Add mention of '{keyword}' to system prompt"
                    ))
        
        # Prüfe erforderliche Felder
        if "required_field" in requirements:
            field = requirements["required_field"]
            if field not in prompt_data or not prompt_data[field]:
                self.results.append(ValidationResult(
                    level=ValidationLevel.ERROR,
                    code="MISSING_STRATEGY_FIELD",
                    message=f"Strategy '{strategy}' requires field '{field}'",
                    path=field,
                    suggestion=f"Add '{field}' for {strategy} strategy"
                ))
        
        # Prüfe Anzahl Beispiele (Few-Shot)
        if strategy == "few-shot" and "examples" in prompt_data:
            examples = prompt_data["examples"]
            min_examples = requirements.get("min_examples", 2)
            max_examples = requirements.get("max_examples", 5)
            
            if len(examples) < min_examples:
                self.results.append(ValidationResult(
                    level=ValidationLevel.ERROR,
                    code="INSUFFICIENT_EXAMPLES",
                    message=f"Few-shot requires at least {min_examples} examples, got {len(examples)}",
                    path="examples",
                    suggestion=f"Add at least {min_examples - len(examples)} more examples"
                ))
            
            if len(examples) > max_examples:
                self.results.append(ValidationResult(
                    level=ValidationLevel.WARNING,
                    code="TOO_MANY_EXAMPLES",
                    message=f"Few-shot typically uses max {max_examples} examples, you have {len(examples)}",
                    path="examples",
                    suggestion=f"Consider reducing to {max_examples} most important examples"
                ))
    
    def _validate_variables(self, prompt_data: Dict) -> None:
        """Prüft Variablen-Konsistenz"""
        user_template = prompt_data.get("user_template", "")
        variables = prompt_data.get("variables", {})
        
        # Finde alle {{variable}} in Template
        template_vars = set(re.findall(r'\{\{(\w+)\}\}', user_template))
        defined_vars = set(variables.keys())
        
        # Undefined variables
        undefined = template_vars - defined_vars
        if undefined:
            self.results.append(ValidationResult(
                level=ValidationLevel.WARNING,
                code="UNDEFINED_VARIABLES",
                message=f"Variables used but not defined: {', '.join(undefined)}",
                path="variables",
                suggestion=f"Define variables: {', '.join(undefined)}"
            ))
        
        # Unused variables
        unused = defined_vars - template_vars
        if unused:
            self.results.append(ValidationResult(
                level=ValidationLevel.INFO,
                code="UNUSED_VARIABLES",
                message=f"Defined but unused variables: {', '.join(unused)}",
                path="variables",
                suggestion=f"Remove or use variables: {', '.join(unused)}"
            ))
    
    def _validate_examples(self, prompt_data: Dict) -> None:
        """Prüft Beispiel-Struktur"""
        examples = prompt_data.get("examples", [])
        
        for idx, example in enumerate(examples):
            if not isinstance(example, dict):
                self.results.append(ValidationResult(
                    level=ValidationLevel.ERROR,
                    code="INVALID_EXAMPLE_FORMAT",
                    message=f"Example {idx} should be object, got {type(example).__name__}",
                    path=f"examples[{idx}]"
                ))
                continue
            
            # Prüfe erforderliche Felder in Beispielen
            if "input" not in example or "output" not in example:
                self.results.append(ValidationResult(
                    level=ValidationLevel.ERROR,
                    code="INCOMPLETE_EXAMPLE",
                    message=f"Example {idx} must have 'input' and 'output' fields",
                    path=f"examples[{idx}]",
                    suggestion="Each example should have: input, output, and optionally explanation"
                ))
    
    def _validate_content_quality(self, prompt_data: Dict) -> None:
        """Bewertet Content-Qualität"""
        scores = {}
        
        # Clarity
        system = prompt_data.get("system", "")
        clarity_score = self._score_clarity(system)
        scores["clarity"] = clarity_score
        
        if clarity_score < 0.70:
            self.results.append(ValidationResult(
                level=ValidationLevel.WARNING,
                code="LOW_CLARITY",
                message=f"System message clarity score: {clarity_score:.2f}/1.0 (target: >0.75)",
                path="system",
                suggestion="Use clearer, more specific language. Avoid ambiguity."
            ))
        
        # Completeness
        has_all_sections = all([
            prompt_data.get("system"),
            prompt_data.get("user_template"),
            prompt_data.get("examples") if prompt_data.get("strategy") == "few-shot" else True
        ])
        
        if not has_all_sections:
            self.results.append(ValidationResult(
                level=ValidationLevel.WARNING,
                code="INCOMPLETE_CONTENT",
                message="Prompt missing important sections",
                path="root",
                suggestion="Add system message, user template, and examples if applicable"
            ))
        
        # Specificity
        specificity = self._score_specificity(prompt_data)
        if specificity < 0.70:
            self.results.append(ValidationResult(
                level=ValidationLevel.WARNING,
                code="LOW_SPECIFICITY",
                message=f"Prompt specificity score: {specificity:.2f}/1.0 (target: >0.75)",
                path="system",
                suggestion="Make prompt more specific with concrete examples or constraints"
            ))
    
    def _score_clarity(self, text: str) -> float:
        """Bewertet Klarheit (0-1)"""
        if not text:
            return 0.0
        
        score = 1.0
        words = text.split()
        
        # Penalize very long sentences
        sentences = text.split(".")
        avg_sentence_length = len(words) / max(len(sentences), 1)
        if avg_sentence_length > 20:
            score -= 0.2
        
        # Penalize vague words
        vague_words = ["maybe", "probably", "sort of", "kind of", "generally", "basically"]
        vague_count = sum(1 for word in vague_words if word in text.lower())
        score -= vague_count * 0.1
        
        # Reward specificity markers
        specific_markers = ["example", "specifically", "exactly", "must", "should"]
        specific_count = sum(1 for marker in specific_markers if marker in text.lower())
        score += specific_count * 0.05
        
        return max(0.0, min(1.0, score))
    
    def _score_specificity(self, prompt_data: Dict) -> float:
        """Bewertet Spezifität (0-1)"""
        score = 0.0
        text = " ".join([
            prompt_data.get("system", ""),
            prompt_data.get("user_template", "")
        ]).lower()
        
        # Check for specific keywords/patterns
        if "step" in text or "numbered" in text:
            score += 0.2
        if "example" in text or "such as" in text:
            score += 0.2
        if "must" in text or "must not" in text or "should" in text:
            score += 0.2
        if "{{" in text:  # Has variables
            score += 0.2
        if prompt_data.get("guardrails"):
            score += 0.2
        
        return min(1.0, score)
    
    def _estimate_tokens(self, prompt_data: Dict) -> None:
        """Schätzt Token-Verwendung"""
        # Rough estimation: 1 token ≈ 4 characters
        system = prompt_data.get("system", "")
        user_template = prompt_data.get("user_template", "")
        examples = prompt_data.get("examples", [])
        
        total_chars = len(system) + len(user_template)
        for example in examples:
            if isinstance(example, dict):
                total_chars += len(str(example.get("input", ""))) + len(str(example.get("output", "")))
        
        estimated_tokens = total_chars / 4
        
        if estimated_tokens > 4000:
            self.results.append(ValidationResult(
                level=ValidationLevel.WARNING,
                code="HIGH_TOKEN_COUNT",
                message=f"Estimated token count: {int(estimated_tokens)} (high for standard models)",
                path="root",
                suggestion="Consider reducing prompt size or breaking into multiple prompts"
            ))
        elif estimated_tokens > 2000:
            self.results.append(ValidationResult(
                level=ValidationLevel.INFO,
                code="MODERATE_TOKEN_COUNT",
                message=f"Estimated token count: {int(estimated_tokens)}",
                path="root"
            ))
    
    def print_results(self) -> None:
        """Gibt Validierungsergebnisse aus"""
        if not self.results:
            print("✓ All validations passed!")
            return
        
        errors = [r for r in self.results if r.level == ValidationLevel.ERROR]
        warnings = [r for r in self.results if r.level == ValidationLevel.WARNING]
        infos = [r for r in self.results if r.level == ValidationLevel.INFO]
        
        if errors:
            print(f"\n❌ ERRORS ({len(errors)}):")
            for result in errors:
                print(f"  [{result.code}] {result.message}")
                if result.suggestion:
                    print(f"    💡 {result.suggestion}")
        
        if warnings:
            print(f"\n⚠️  WARNINGS ({len(warnings)}):")
            for result in warnings:
                print(f"  [{result.code}] {result.message}")
                if result.suggestion:
                    print(f"    💡 {result.suggestion}")
        
        if infos:
            print(f"\nℹ️  INFO ({len(infos)}):")
            for result in infos:
                print(f"  [{result.code}] {result.message}")


def validate_prompt_file(file_path: str) -> Tuple[bool, List[ValidationResult]]:
    """Hilfsfunktion: Validiere Datei"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            prompt_data = json.load(f)
    except json.JSONDecodeError as e:
        return False, [ValidationResult(
            level=ValidationLevel.ERROR,
            code="INVALID_JSON",
            message=f"Invalid JSON: {str(e)}",
            path=file_path
        )]
    except FileNotFoundError:
        return False, [ValidationResult(
            level=ValidationLevel.ERROR,
            code="FILE_NOT_FOUND",
            message=f"File not found: {file_path}",
            path=file_path
        )]
    
    validator = PromptValidator()
    return validator.validate(prompt_data)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python schema_validator.py <prompt_file.json>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    is_valid, results = validate_prompt_file(file_path)
    
    validator = PromptValidator()
    validator.results = results
    validator.print_results()
    
    sys.exit(0 if is_valid else 1)

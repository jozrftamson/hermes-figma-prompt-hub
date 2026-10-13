#!/usr/bin/env python3
"""
Prompt Validator with Improved Error Messages

Validates individual prompt files with clear, actionable error reporting.
Separates JSON errors from schema validation errors.

Usage:
    python3 scripts/validate_prompt.py <prompt_file>
    python3 scripts/validate_prompt.py <prompt_file> --format json
    python3 scripts/validate_prompt.py <prompt_file> --verbose
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import argparse


@dataclass
class ValidationError:
    """Represents a validation error with context"""
    error_type: str  # 'json', 'schema', 'constraint'
    field: Optional[str]
    message: str
    expected: Optional[str] = None
    actual: Optional[str] = None
    suggestion: Optional[str] = None


class PromptValidator:
    """Validates prompt files with improved error messages"""
    
    REQUIRED_FIELDS = {
        'prompt_id': 'string',
        'name': 'string',
        'description': 'string',
        'version': 'string',
        'strategy': 'enum',
        'category': 'enum',
        'system': 'string',
        'user_template': 'string',
    }
    
    OPTIONAL_FIELDS = {
        'guardrails': 'array',
        'examples': 'array',
        'variables': 'object',
        'output_format': 'object',
        'metadata': 'object',
        'tags': 'array',
    }
    
    VALID_STRATEGIES = [
        'chain-of-thought',
        'few-shot',
        'role-play',
        'tree-of-thought',
        'meta-reasoning'
    ]
    
    VALID_CATEGORIES = [
        'analysis',
        'generation',
        'reasoning',
        'classification',
        'other'
    ]
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []
    
    def validate_file(self, file_path: str) -> Tuple[bool, List[ValidationError], List[ValidationError]]:
        """
        Validate a prompt file.
        
        Returns:
            (is_valid, errors_list, warnings_list)
        """
        self.errors = []
        self.warnings = []
        
        # Step 1: Check file exists
        path = Path(file_path)
        if not path.exists():
            self.errors.append(ValidationError(
                error_type='file',
                field=None,
                message=f"File not found: {file_path}",
                suggestion=f"Check that the file path is correct"
            ))
            return False, self.errors, self.warnings
        
        # Step 2: Try to load JSON
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(ValidationError(
                error_type='json',
                field=None,
                message=f"Invalid JSON syntax: {str(e)}",
                suggestion="Check for missing commas, quotes, or brackets in your JSON file"
            ))
            return False, self.errors, self.warnings
        except Exception as e:
            self.errors.append(ValidationError(
                error_type='json',
                field=None,
                message=f"Error reading file: {str(e)}",
                suggestion="Ensure the file is readable and contains valid UTF-8 text"
            ))
            return False, self.errors, self.warnings
        
        # Step 3: Validate it's an object
        if not isinstance(data, dict):
            self.errors.append(ValidationError(
                error_type='schema',
                field='root',
                message="Prompt must be a JSON object (not array or primitive)",
                expected='{ ... }',
                actual=type(data).__name__
            ))
            return False, self.errors, self.warnings
        
        # Step 4: Check required fields
        self._validate_required_fields(data)
        
        # Step 5: Check field types and enums
        self._validate_field_types(data)
        
        # Step 6: Check field constraints
        self._validate_constraints(data)
        
        # Step 7: Check strategy-specific requirements
        self._validate_strategy_requirements(data)
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings
    
    def _validate_required_fields(self, data: Dict) -> None:
        """Check that all required fields are present and not empty"""
        for field_name in self.REQUIRED_FIELDS:
            if field_name not in data:
                self.errors.append(ValidationError(
                    error_type='schema',
                    field=field_name,
                    message=f"Missing required field: '{field_name}'",
                    suggestion=f"Add a '{field_name}' field to your prompt JSON"
                ))
            elif data[field_name] is None or (isinstance(data[field_name], str) and not data[field_name].strip()):
                self.errors.append(ValidationError(
                    error_type='schema',
                    field=field_name,
                    message=f"Required field '{field_name}' is empty",
                    actual='empty/null',
                    suggestion=f"Populate '{field_name}' with a meaningful value"
                ))
    
    def _validate_field_types(self, data: Dict) -> None:
        """Validate field types"""
        all_fields = {**self.REQUIRED_FIELDS, **self.OPTIONAL_FIELDS}
        
        for field_name, expected_type in all_fields.items():
            if field_name not in data:
                continue
            
            value = data[field_name]
            actual_type = type(value).__name__
            
            # Type checks
            if expected_type == 'string' and not isinstance(value, str):
                self.errors.append(ValidationError(
                    error_type='schema',
                    field=field_name,
                    message=f"Field '{field_name}' must be a string",
                    expected='string (e.g., "value")',
                    actual=f'{actual_type} ({str(value)[:50]})'
                ))
            
            elif expected_type == 'array' and not isinstance(value, list):
                self.errors.append(ValidationError(
                    error_type='schema',
                    field=field_name,
                    message=f"Field '{field_name}' must be an array",
                    expected='array (e.g., [...])',
                    actual=f'{actual_type}'
                ))
            
            elif expected_type == 'object' and not isinstance(value, dict):
                self.errors.append(ValidationError(
                    error_type='schema',
                    field=field_name,
                    message=f"Field '{field_name}' must be an object",
                    expected='object (e.g., {...})',
                    actual=f'{actual_type}'
                ))
            
            elif expected_type == 'enum':
                self._validate_enum_field(field_name, value)
    
    def _validate_enum_field(self, field_name: str, value: str) -> None:
        """Validate enum fields"""
        if field_name == 'strategy':
            valid_values = self.VALID_STRATEGIES
        elif field_name == 'category':
            valid_values = self.VALID_CATEGORIES
        else:
            return
        
        if value not in valid_values:
            self.errors.append(ValidationError(
                error_type='schema',
                field=field_name,
                message=f"Invalid '{field_name}': '{value}'",
                expected=f"One of: {', '.join(valid_values)}",
                actual=f"'{value}'",
                suggestion=f"Use one of the valid values: {', '.join(valid_values)}"
            ))
    
    def _validate_constraints(self, data: Dict) -> None:
        """Validate field constraints (length, format, etc.)"""
        constraints = {
            'prompt_id': {
                'min_length': 3,
                'max_length': 100,
                'description': 'Lowercase alphanumeric, hyphens, underscores'
            },
            'name': {
                'min_length': 5,
                'max_length': 150,
                'description': 'Human-readable name'
            },
            'description': {
                'min_length': 10,
                'max_length': 1000,
                'description': 'Detailed description'
            },
            'system': {
                'min_length': 20,
                'max_length': 10000,
                'description': 'System message'
            },
            'user_template': {
                'min_length': 10,
                'max_length': 10000,
                'description': 'User message template'
            },
        }
        
        for field_name, limits in constraints.items():
            if field_name not in data or not isinstance(data[field_name], str):
                continue
            
            value = data[field_name]
            length = len(value)
            
            if length < limits.get('min_length', 0):
                self.warnings.append(ValidationError(
                    error_type='constraint',
                    field=field_name,
                    message=f"Field '{field_name}' is too short ({length} chars)",
                    expected=f">= {limits.get('min_length')} characters",
                    actual=f"{length} characters",
                    suggestion=f"Expand '{field_name}' to provide more context (min {limits.get('min_length')} chars)"
                ))
            
            if length > limits.get('max_length', float('inf')):
                self.errors.append(ValidationError(
                    error_type='constraint',
                    field=field_name,
                    message=f"Field '{field_name}' is too long ({length} chars)",
                    expected=f"<= {limits.get('max_length')} characters",
                    actual=f"{length} characters",
                    suggestion=f"Reduce '{field_name}' to {limits.get('max_length')} characters or less"
                ))
    
    def _validate_strategy_requirements(self, data: Dict) -> None:
        """Validate strategy-specific requirements"""
        strategy = data.get('strategy')
        
        if strategy == 'few-shot':
            examples = data.get('examples', [])
            if not examples:
                self.errors.append(ValidationError(
                    error_type='schema',
                    field='examples',
                    message="Few-shot strategy requires 'examples' field",
                    suggestion="Add examples showing input/output pairs for few-shot learning"
                ))
            elif len(examples) < 2:
                self.warnings.append(ValidationError(
                    error_type='constraint',
                    field='examples',
                    message=f"Few-shot typically needs at least 2 examples (you have {len(examples)})",
                    suggestion=f"Add {2 - len(examples)} more example(s) to improve few-shot effectiveness"
                ))
    
    def print_report(self) -> None:
        """Print a formatted validation report"""
        has_errors = len(self.errors) > 0
        has_warnings = len(self.warnings) > 0
        
        if not has_errors and not has_warnings:
            print("✅ Validation passed! Prompt is valid and ready to use.")
            return
        
        print()
        
        if has_errors:
            print("❌ VALIDATION ERRORS:")
            print("=" * 70)
            for i, error in enumerate(self.errors, 1):
                print(f"\n{i}. {error.message}")
                if error.field:
                    print(f"   Field: {error.field}")
                if error.expected:
                    print(f"   Expected: {error.expected}")
                if error.actual:
                    print(f"   Actual: {error.actual}")
                if error.suggestion:
                    print(f"   💡 {error.suggestion}")
        
        if has_warnings:
            print("\n⚠️  VALIDATION WARNINGS:")
            print("=" * 70)
            for i, warning in enumerate(self.warnings, 1):
                print(f"\n{i}. {warning.message}")
                if warning.field:
                    print(f"   Field: {warning.field}")
                if warning.expected:
                    print(f"   Expected: {warning.expected}")
                if warning.actual:
                    print(f"   Actual: {warning.actual}")
                if warning.suggestion:
                    print(f"   💡 {warning.suggestion}")
        
        print("\n" + "=" * 70)
    
    def print_json_report(self) -> None:
        """Print JSON formatted validation report"""
        report = {
            'valid': len(self.errors) == 0,
            'error_count': len(self.errors),
            'warning_count': len(self.warnings),
            'errors': [
                {
                    'type': e.error_type,
                    'field': e.field,
                    'message': e.message,
                    'expected': e.expected,
                    'actual': e.actual,
                    'suggestion': e.suggestion
                }
                for e in self.errors
            ],
            'warnings': [
                {
                    'type': w.error_type,
                    'field': w.field,
                    'message': w.message,
                    'expected': w.expected,
                    'actual': w.actual,
                    'suggestion': w.suggestion
                }
                for w in self.warnings
            ]
        }
        print(json.dumps(report, indent=2))


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Validate Hermes prompt files with improved error messages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/validate_prompt.py prompts/raw/code-review.json
  python3 scripts/validate_prompt.py prompts/raw/code-review.json --verbose
  python3 scripts/validate_prompt.py prompts/raw/code-review.json --format json
        """
    )
    
    parser.add_argument(
        'file',
        help='Path to prompt file to validate'
    )
    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    validator = PromptValidator(verbose=args.verbose)
    is_valid, errors, warnings = validator.validate_file(args.file)
    
    if args.format == 'json':
        validator.print_json_report()
    else:
        validator.print_report()
    
    sys.exit(0 if is_valid else 1)


if __name__ == '__main__':
    main()

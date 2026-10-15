#!/usr/bin/env python3
"""
Validate prompt against schema.
"""

import json
import sys
from pathlib import Path


def validate_schema(file_path):
    """Validate a prompt file against schema."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Define schema
        schema_errors = []
        
        # Check required top-level fields
        if 'id' not in data:
            schema_errors.append('Missing required field: id')
        
        if 'title' not in data:
            schema_errors.append('Missing required field: title')
        
        if 'content' not in data:
            schema_errors.append('Missing required field: content')
        
        # Validate field types
        if 'title' in data and not isinstance(data['title'], str):
            schema_errors.append('Field "title" must be a string')
        
        if 'content' in data and not isinstance(data['content'], str):
            schema_errors.append('Field "content" must be a string')
        
        if 'tags' in data and not isinstance(data['tags'], list):
            schema_errors.append('Field "tags" must be an array')
        
        if schema_errors:
            print(f'❌ Schema validation failed for {file_path}:')
            for error in schema_errors:
                print(f'  - {error}')
            return False
        else:
            print(f'✅ Schema valid for {file_path}')
            return True
            
    except json.JSONDecodeError as e:
        print(f'❌ JSON error in {file_path}: {str(e)}')
        return False
    except Exception as e:
        print(f'❌ Error validating {file_path}: {str(e)}')
        return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: schema_validator.py <file_path>')
        sys.exit(1)
    
    file_path = sys.argv[1]
    valid = validate_schema(file_path)
    sys.exit(0 if valid else 1)

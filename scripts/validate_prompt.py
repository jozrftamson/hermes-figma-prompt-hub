#!/usr/bin/env python3
"""
Validate a single prompt file against schema.
"""

import json
import sys
from pathlib import Path


def validate_prompt(file_path):
    """Validate a prompt file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Basic validation checks
        required_fields = ['id', 'title', 'content']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return {
                'valid': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}',
                'file': str(file_path)
            }
        
        return {
            'valid': True,
            'message': f'Prompt "{data.get("title", "unknown")}" is valid',
            'file': str(file_path)
        }
        
    except json.JSONDecodeError as e:
        return {
            'valid': False,
            'error': f'JSON decode error: {str(e)}',
            'file': str(file_path)
        }
    except Exception as e:
        return {
            'valid': False,
            'error': str(e),
            'file': str(file_path)
        }


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: validate_prompt.py <file_path>')
        sys.exit(1)
    
    file_path = sys.argv[1]
    result = validate_prompt(file_path)
    
    print(json.dumps(result, indent=2))
    
    sys.exit(0 if result['valid'] else 1)

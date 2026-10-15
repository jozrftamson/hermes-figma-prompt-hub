#!/usr/bin/env python3
"""
Validate all prompts in a directory.
"""

import json
import sys
from pathlib import Path


def validate_all_prompts(directory):
    """Validate all prompts in a directory."""
    prompt_dir = Path(directory)
    
    if not prompt_dir.exists():
        print(f'Directory not found: {directory}')
        return
    
    results = {'total': 0, 'valid': 0, 'invalid': 0, 'errors': []}
    
    for prompt_file in prompt_dir.glob('**/*.json'):
        results['total'] += 1
        
        try:
            with open(prompt_file, 'r') as f:
                data = json.load(f)
            
            # Basic validation
            required_fields = ['id', 'title', 'content']
            missing = [f for f in required_fields if f not in data]
            
            if missing:
                results['invalid'] += 1
                results['errors'].append({
                    'file': str(prompt_file),
                    'error': f'Missing fields: {", ".join(missing)}'
                })
            else:
                results['valid'] += 1
                print(f'✅ {prompt_file.name}')
                
        except json.JSONDecodeError as e:
            results['invalid'] += 1
            results['errors'].append({
                'file': str(prompt_file),
                'error': f'JSON error: {str(e)}'
            })
        except Exception as e:
            results['invalid'] += 1
            results['errors'].append({
                'file': str(prompt_file),
                'error': str(e)
            })
    
    print(f'\nValidation Summary:')
    print(f'Total: {results["total"]} | Valid: {results["valid"]} | Invalid: {results["invalid"]}')
    
    if results['errors']:
        print('\nErrors:')
        for error in results['errors']:
            print(f'  - {error["file"]}: {error["error"]}')


if __name__ == '__main__':
    directory = sys.argv[1] if len(sys.argv) > 1 else 'prompts/'
    validate_all_prompts(directory)

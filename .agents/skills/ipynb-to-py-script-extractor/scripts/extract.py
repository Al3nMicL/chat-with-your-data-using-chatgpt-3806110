#!/usr/bin/env python3
import json
import sys

def extract_code(notebook_path):
    with open(notebook_path, 'r') as f:
        nb = json.load(f)
    
    for cell in nb.get('cells', []):
        if cell.get('cell_type') == 'code':
            source = ''.join(cell.get('source', []))
            # Ignore cells that are purely pip installs
            if source.strip().startswith('pip install') or source.strip().startswith('uv pip install'):
                continue
            
            print(source)
            print('# ---')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract.py <notebook.ipynb>")
        sys.exit(1)
    extract_code(sys.argv[1])
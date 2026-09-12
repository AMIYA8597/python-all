import json
import os
import re

root = r'd:\work\python-all'
with open('audit.json') as f:
    data = json.load(f)

master_files = [x for x in data if x['path'].startswith('/Python-DSA-AI-Master')]

structured = 0
not_structured = 0
unstructured_files = []

for item in master_files:
    if item['path'].endswith('.py') or item['path'].endswith('.md'):
        path = root + item['path'].replace('/', '\\')
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Simple check for the required template
                if '## A. Concept Name' in content or 'Concept Name' in content or 'A. Concept Name' in content:
                    structured += 1
                elif 'class' in content or 'def' in content or '#' in content or '*' in content:
                    not_structured += 1
                    unstructured_files.append(item['path'])
        except Exception as e:
            pass

print(f"Files following structure: {structured}")
print(f"Files not strictly following structure: {not_structured}")

# Group unstructured files by directory
dirs = {}
for path in unstructured_files:
    d = path.split('/')[2] if len(path.split('/')) > 2 else 'root'
    dirs[d] = dirs.get(d, 0) + 1

print("\nUnstructured files by directory:")
for k, v in sorted(dirs.items()):
    print(f"{k}: {v}")

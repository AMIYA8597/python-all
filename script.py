import os
import json

root = r'd:\work\python-all'
data = []
for root_dir, dirs, files in os.walk(root):
    if '.git' in root_dir or '.venv' in root_dir or '__pycache__' in root_dir:
        continue
    for file in files:
        if file.endswith('.py') or file.endswith('.md') or file.endswith('.pdf'):
            path = os.path.join(root_dir, file)
            size = os.path.getsize(path)
            data.append({'path': path.replace(root, '').replace('\\', '/'), 'size': size})

with open('audit.json', 'w') as f:
    json.dump(data, f, indent=2)

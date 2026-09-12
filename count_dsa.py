import os
import json

root = r'd:\work\python-all\Python-DSA-AI-Master\02-Data-Structures'
data = []
for dirpath, _, filenames in os.walk(root):
    for f in filenames:
        if f.endswith('.py') or f.endswith('.md'):
            data.append(os.path.relpath(os.path.join(dirpath, f), root))
            
print(f"Total files in 02-Data-Structures: {len(data)}")
for i, d in enumerate(data[:10]):
    print(d)
if len(data) > 10:
    print("...")

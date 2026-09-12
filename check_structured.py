import os

root = r'd:\work\python-all\Python-DSA-AI-Master\01-Python-Fundamentals'
structured = []
for dirpath, _, filenames in os.walk(root):
    for f in filenames:
        if f.endswith('.py') or f.endswith('.md'):
            path = os.path.join(dirpath, f)
            with open(path, 'r', encoding='utf-8') as file:
                if '## A. Concept Name' in file.read():
                    structured.append(os.path.relpath(path, root))

print("Structured files:")
for s in structured:
    print(s)

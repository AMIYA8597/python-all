import os
import re

root_dir = r'd:\work\python-all\Python-DSA-AI-Master'

def audit_repo(directory):
    total_py = 0
    compliant_py = 0
    missing = []
    
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.py'):
                total_py += 1
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Check for a few key headers to gauge compliance
                        if 'A. Concept Name' in content and 'X. Project Connection' in content:
                            compliant_py += 1
                        else:
                            missing.append(os.path.relpath(filepath, directory))
                except Exception as e:
                    pass
    
    return total_py, compliant_py, missing

total, compliant, missing = audit_repo(root_dir)
print(f"Total Python Files: {total}")
print(f"Compliant A-X Files: {compliant}")
print(f"Compliance Rate: {(compliant/total)*100:.2f}%" if total > 0 else "0%")
print("A sample of non-compliant files:")
for m in missing[:10]:
    print(" -", m)


import os, json
root = 'd:/work/python-all/Python-DSA-AI-Master'
state_file = os.path.join(root, 'BATCH_STATE.json')

state = {'pending': [], 'in_progress': [], 'completed': []}
for dirpath, dirnames, filenames in os.walk(root):
    for filename in filenames:
        if filename.endswith('.py') or filename.endswith('.md'):
            if filename in ['FINAL_MANIFEST.json', 'BATCH_STATE.json', 'status_report.json', 'COMPLETION-STATUS.md', 'PROGRESS-SUMMARY.md', 'MASTER-ROADMAP.md', 'JOB-READINESS-MATRIX.md']:
                continue
            filepath = os.path.join(dirpath, filename)
            size = os.path.getsize(filepath)
            
            needs_work = False
            if size < 3500:
                needs_work = True
            else:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'TODO' in content or 'placeholder' in content.lower() or 'content omitted' in content.lower():
                            needs_work = True
                except:
                    needs_work = True
            
            if needs_work:
                state['pending'].append(filepath)
            else:
                state['completed'].append(filepath)

with open(state_file, 'w') as f:
    json.dump(state, f, indent=2)

print(f"Pending: {len(state['pending'])}")
print(f"Completed: {len(state['completed'])}")

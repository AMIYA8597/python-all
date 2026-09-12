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
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                lower_content = content.lower()
                if 'todo' in lower_content or 'placeholder' in lower_content or 'content omitted' in lower_content:
                    needs_work = True
                elif size < 2000:
                    needs_work = True
                # No extra strict checks, if it's > 2000 bytes and has no placeholder, consider it complete for now
            except:
                needs_work = True
            
            if needs_work:
                state['pending'].append(filepath)
            else:
                state['completed'].append(filepath)

state['pending'].sort()

with open(state_file, 'w') as f:
    json.dump(state, f, indent=2)

print(f"Pending: {len(state['pending'])}")
print(f"Completed: {len(state['completed'])}")

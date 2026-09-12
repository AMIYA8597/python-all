import os, json

root = 'd:/work/python-all/Python-DSA-AI-Master'
state_file = os.path.join(root, 'BATCH_STATE.json')

def init_state():
    state = {'pending': [], 'in_progress': [], 'completed': []}
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith('.py') or filename.endswith('.md'):
                # Exclude manifest files and state files
                if filename in ['FINAL_MANIFEST.json', 'BATCH_STATE.json', 'status_report.json']:
                    continue
                filepath = os.path.join(dirpath, filename)
                size = os.path.getsize(filepath)
                # If size < 8000 bytes, it needs expansion (with a few exceptions like ROADMAP which is ok)
                if size < 8000 and "ROADMAP" not in filename and "MATRIX" not in filename:
                    state['pending'].append(filepath)
                else:
                    state['completed'].append(filepath)
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)
    return state

def get_next_batch(batch_size=10):
    if not os.path.exists(state_file):
        state = init_state()
    else:
        with open(state_file, 'r') as f:
            state = json.load(f)
            
    # clear in_progress (assume previous batch finished or failed, we just retry pending)
    # Actually, we should move in_progress to completed if they are large now.
    new_in_progress = []
    for p in state['in_progress']:
        if os.path.exists(p) and os.path.getsize(p) >= 8000:
            state['completed'].append(p)
        else:
            state['pending'].insert(0, p)
            
    state['in_progress'] = []
    
    batch = state['pending'][:batch_size]
    state['pending'] = state['pending'][batch_size:]
    state['in_progress'] = batch
    
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)
        
    return batch

if __name__ == '__main__':
    batch = get_next_batch(10)
    for b in batch:
        print(b)

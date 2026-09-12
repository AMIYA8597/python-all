import os, json

root = 'd:/work/python-all/Python-DSA-AI-Master'
state_file = os.path.join(root, 'BATCH_STATE.json')

with open(state_file, 'r') as f:
    state = json.load(f)

pending = state['pending']
batch = pending[:24]
state['pending'] = pending[24:]
state['in_progress'] = batch

with open(state_file, 'w') as f:
    json.dump(state, f, indent=2)

print("Batch files:")
for i in range(0, len(batch), 3):
    chunk = batch[i:i+3]
    print(f"Subagent {i//3 + 1}:")
    for b in chunk:
        print(f"  - {b}")

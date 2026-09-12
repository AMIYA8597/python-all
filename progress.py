import json
with open('d:/work/python-all/Python-DSA-AI-Master/BATCH_STATE.json', 'r') as f:
    state = json.load(f)
print(f"Total: {len(state['pending']) + len(state['completed']) + len(state['in_progress'])}")
print(f"Completed: {len(state['completed'])}")
print(f"In Progress: {len(state['in_progress'])}")
print(f"Pending: {len(state['pending'])}")

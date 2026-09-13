import json
with open('MASTER_AUDIT.json') as f:
    data = json.load(f)['files']
for x in data:
    if '18-Agentic-AI' in x['path']:
        print(f"{x['path']}: {x['status']}")

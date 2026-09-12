import os
import re
import shutil

base_dir = r'd:\work\python-all'

# Clean up existing bad files
master_dir = os.path.join(base_dir, 'Python-DSA-AI-Master')
if os.path.exists(master_dir):
    shutil.rmtree(master_dir)

tree_path = r'd:\work\python-all\tree.txt'

with open(tree_path, 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()

start_idx = 0
for i, line in enumerate(lines):
    if line.startswith('Python-DSA-AI-Master/'):
        start_idx = i
        break

lines = lines[start_idx:]

path_stack = []
current_file = None
file_content = []

def flush_file():
    global current_file, file_content
    if current_file and file_content:
        file_path = os.path.join(base_dir, current_file)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as out:
            out.write('\n'.join(file_content) + '\n')
    current_file = None
    file_content = []

for line in lines:
    if line.startswith('</USER_REQUEST>'):
        break
        
    if not line.strip():
        continue
        
    m = re.match(r'^([ \t\│\├\└\─]*)(.*)', line)
    if not m:
        continue
    
    prefix = m.group(1)
    content = m.group(2)
    
    if not content:
        continue
        
    depth = len(prefix) // 4
    
    # Node condition
    is_node = ('├' in prefix or '└' in prefix or depth == 0) and ('/' in content or content.endswith('.pdf') or content.endswith('.py') or content.endswith('.md') or content.endswith('.txt'))
    
    if is_node:
        flush_file()
        
        while len(path_stack) > depth:
            path_stack.pop()
            
        name = content.strip()
        is_dir = name.endswith('/')
        if is_dir:
            name = name[:-1]
            
        path_stack.append(name)
        
        full_rel_path = os.path.join(*path_stack)
        full_abs_path = os.path.join(base_dir, full_rel_path)
        
        if is_dir:
            os.makedirs(full_abs_path, exist_ok=True)
        else:
            current_file = full_rel_path
    else:
        if current_file is not None:
            expected_len = (len(path_stack) - 1) * 4
            prefix_len = len(prefix)
            strip_len = min(expected_len, prefix_len)
            
            # Wait, if the line contains ONLY prefix characters, e.g. a blank line in code
            # content would be empty, but we already skipped if not content: above.
            # But what if there's a line with just │   │   ? 
            # The regex matches it, content is empty. We skipped it. That's fine.
            
            file_content.append(line[strip_len:])

flush_file()
print('Done creating structure with min(expected, prefix) indentation logic!')

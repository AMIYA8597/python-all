import os
import json
import re

def analyze_file(path, rel_path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return {"path": rel_path, "status": "ERROR"}

    lines = content.split('\n')
    num_lines = len(lines)
    
    # Heuristics
    if num_lines < 5 and not content.strip():
        return {"path": rel_path, "status": "EMPTY", "lines": num_lines}
    
    if re.search(r'TODO|TBD|Coming soon|Add content', content, re.IGNORECASE):
        return {"path": rel_path, "status": "PLACEHOLDER", "lines": num_lines}

    if num_lines < 20:
        return {"path": rel_path, "status": "SUPERFICIAL", "lines": num_lines}

    # Checking for depth markers in Markdown
    if path.endswith('.md'):
        has_memory = bool(re.search(r'memory anchor|active recall|spaced repetition', content, re.IGNORECASE))
        has_deep_sections = bool(re.search(r'from scratch|under the hood|internal mechanism|common mistakes|why this matters', content, re.IGNORECASE))
        if has_memory and has_deep_sections and num_lines > 100:
            return {"path": rel_path, "status": "COMPLETE", "lines": num_lines}
        else:
            return {"path": rel_path, "status": "NEEDS-DEEPENING", "lines": num_lines}
            
    # Checking for depth markers in Python
    if path.endswith('.py'):
        has_functions = 'def ' in content
        has_classes = 'class ' in content
        has_tests = 'assert ' in content or 'unittest' in content or 'pytest' in content
        has_docs = '"""' in content or "'''" in content
        if has_functions and has_docs and has_tests and num_lines > 50:
            return {"path": rel_path, "status": "GOOD", "lines": num_lines}
        else:
            return {"path": rel_path, "status": "PARTIAL", "lines": num_lines}
            
    return {"path": rel_path, "status": "UNKNOWN", "lines": num_lines}


def main():
    root_dir = r"d:\work\python-all\Python-DSA-AI-Master"
    results = []
    stats = {}
    
    for dirpath, _, filenames in os.walk(root_dir):
        if '.git' in dirpath:
            continue
        for f in filenames:
            if not f.endswith(('.py', '.md')):
                continue
            path = os.path.join(dirpath, f)
            rel_path = os.path.relpath(path, root_dir)
            
            res = analyze_file(path, rel_path)
            results.append(res)
            
            status = res.get('status', 'UNKNOWN')
            stats[status] = stats.get(status, 0) + 1
            
    with open(os.path.join(root_dir, 'MASTER_AUDIT.json'), 'w', encoding='utf-8') as f:
        json.dump({"files": results, "stats": stats}, f, indent=4)
        
    print(f"Audit completed: {len(results)} files analyzed.")
    for k, v in stats.items():
        print(f"{k}: {v}")

if __name__ == '__main__':
    main()

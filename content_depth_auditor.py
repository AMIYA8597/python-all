import os
import json
import re

def analyze_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return None

    lines = content.split('\n')
    word_count = len(re.findall(r'\b\w+\b', content))
    line_count = len(lines)
    
    # Heuristics for markdown elements
    headings = len(re.findall(r'^#{1,6}\s+.+', content, re.MULTILINE))
    code_blocks = len(re.findall(r'```.*?```', content, re.DOTALL))
    
    examples = len(re.findall(r'(?i)example', content))
    exercises = len(re.findall(r'(?i)exercise', content))
    questions = len(re.findall(r'(?i)question', content))

    # Determine status based on prompt
    status = "SHALLOW"
    if word_count == 0:
        status = "EMPTY"
    elif word_count < 800:
        status = "SHALLOW"
    elif word_count < 1500:
        status = "MICRO"
    elif word_count < 3000:
        status = "BASIC"
    elif word_count < 5000:
        status = "INTERMEDIATE"
    elif word_count < 7000:
        status = "DEEP"
    else:
        status = "TEXTBOOK"
        
    placeholders = len(re.findall(r'(?i)TODO|TBD|FIXME|Coming Soon|Placeholder|Add content here|To be added', content))
    if placeholders > 0:
        status = "INCOMPLETE"

    filename = os.path.basename(filepath)
    is_python = filename.endswith('.py')
    if is_python:
        code_blocks = 1 # The file itself is code
        if word_count < 200:
            status = "SHALLOW"

    return {
        "path": filepath,
        "subject": os.path.basename(os.path.dirname(os.path.dirname(filepath))),
        "topic": os.path.basename(os.path.dirname(filepath)),
        "level": "Unknown",
        "word_count": word_count,
        "line_count": line_count,
        "code_blocks": code_blocks,
        "examples": examples,
        "exercises": exercises,
        "depth_score": round((word_count / 1000) + (code_blocks * 0.5) + (examples * 0.2), 2),
        "accuracy_score": 0,
        "beginner_completeness": 0,
        "advanced_completeness": 0,
        "status": status
    }

def main():
    root_dir = r"d:\work\python-all"
    ignore_dirs = {'.git', '.gemini', 'venv', '__pycache__', 'leetcode'}
    
    audit_results = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Mutate dirnames to ignore directories
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
        
        for filename in filenames:
            if (filename.endswith('.md') or filename.endswith('.py')) and not filename in ['README.md', 'PROGRESS-SUMMARY.md', 'FINAL_BUILD_REPORT.md', 'COMPLETION-STATUS.md', 'COMPREHENSIVE_REPOSITORY_ANALYSIS.md', 'content_depth_auditor.py', 'builder.py', 'analyze.py']:
                filepath = os.path.join(dirpath, filename)
                res = analyze_file(filepath)
                if res:
                    audit_results.append(res)
                    
    with open(os.path.join(root_dir, "CONTENT_DEPTH_AUDIT.json"), "w", encoding='utf-8') as f:
        json.dump(audit_results, f, indent=2)

    shallow_count = sum(1 for r in audit_results if r['status'] in ['EMPTY', 'SHALLOW', 'INCOMPLETE'])
    print(f"Total MD/PY educational files: {len(audit_results)}")
    print(f"Shallow/Empty/Incomplete: {shallow_count}")

if __name__ == '__main__':
    main()

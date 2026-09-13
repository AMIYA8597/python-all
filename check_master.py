import os
import re

ROOT = r"d:\work\python-all\Python-DSA-AI-Master"

MASTER_SUBJECTS = [
    "01 COMPUTER / SOFTWARE FOUNDATIONS",
    "02 PYTHON FUNDAMENTALS",
    "03 ADVANCED PYTHON",
    "04 DATA STRUCTURES",
    "05 ALGORITHMS",
    "06 PYTHON DSA",
    "07 COMPETITIVE PROGRAMMING",
    "08 PYTHON DATA LIBRARIES",
    "09 SQL",
    "10 DATABASES",
    "11 MATHEMATICS",
    "12 LINEAR ALGEBRA",
    "13 CALCULUS",
    "14 PROBABILITY",
    "15 STATISTICS",
    "16 DATA ANALYTICS",
    "17 DATA SCIENCE",
    "18 MACHINE LEARNING",
    "19 ML MATHEMATICS",
    "20 ML ENGINEERING",
    "21 DEEP LEARNING",
    "22 PYTORCH",
    "23 TENSORFLOW",
    "24 NLP",
    "25 COMPUTER VISION",
    "26 TRANSFORMERS",
    "27 LLM FUNDAMENTALS",
    "28 GENERATIVE AI",
    "29 PROMPT ENGINEERING",
    "30 EMBEDDINGS",
    "31 VECTOR SEARCH",
    "32 VECTOR DATABASES",
    "33 RAG",
    "34 ADVANCED RAG",
    "35 FINE-TUNING",
    "36 PEFT",
    "37 LoRA",
    "38 QLoRA",
    "39 QUANTIZATION",
    "40 MULTIMODAL AI",
    "41 TOOL CALLING",
    "42 FUNCTION CALLING",
    "43 WORKFLOWS",
    "44 AGENTIC AI",
    "45 MULTI-AGENT SYSTEMS",
    "46 AI EVALUATION",
    "47 AI SAFETY",
    "48 AI SECURITY",
    "49 MLOPS",
    "50 LLMOPS",
    "51 DEPLOYMENT",
    "52 CLOUD FOUNDATIONS",
    "53 DATA ENGINEERING FOUNDATIONS",
    "54 SYSTEM DESIGN",
    "55 AI SYSTEM DESIGN",
    "56 PERFORMANCE",
    "57 TESTING",
    "58 DEBUGGING",
    "59 PROJECTS",
    "60 INTERVIEWS",
    "61 CAREER PREPARATION"
]

def map_and_create():
    existing_dirs = [d for d in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT, d)) and not d.startswith(".")]
    existing_lower = [d.lower() for d in existing_dirs]
    
    # We will just print what's missing so the Agent can decide.
    missing = []
    
    for subject in MASTER_SUBJECTS:
        # e.g., "01 COMPUTER / SOFTWARE FOUNDATIONS"
        parts = subject.split(" ", 1)
        num = parts[0]
        name = parts[1]
        
        # Simple heuristic to see if the topic exists in the folder names
        found = False
        keywords = name.lower().replace("/", " ").split()
        
        # some common mappings
        if "sql" in keywords or "databases" in keywords:
            if any("sql" in d or "database" in d for d in existing_lower): found = True
        elif "python fundamentals" in name.lower():
            if any("python-fundamentals" in d for d in existing_lower): found = True
        elif "data structures" in name.lower() or "algorithms" in name.lower() or "dsa" in name.lower():
            if any("data-structures" in d or "algorithms" in d for d in existing_lower): found = True
        elif "machine learning" in name.lower() or "ml " in name.lower():
            if any("machine-learning" in d for d in existing_lower): found = True
        elif "deep learning" in name.lower():
            if any("deep-learning" in d for d in existing_lower): found = True
        else:
            # check if at least one long keyword is in any directory name
            for kw in keywords:
                if len(kw) > 3 and any(kw in d for d in existing_lower):
                    found = True
                    break
                    
        if not found:
            missing.append(subject)
            
    print("Likely missing master subjects:")
    for m in missing:
        print(f" - {m}")

if __name__ == "__main__":
    map_and_create()

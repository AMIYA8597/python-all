"""
# ==============================================================================
# LABORATORY: ADVANCED AGENT SYSTEMS (MULTI-AGENT & LANGGRAPH)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# The basic "ReAct" Agent loop (Reason -> Act -> Reason) is powerful, but it 
# fails completely on long, complex projects like "Write a 50-page research 
# report on quantum computing."
#
# A single LLM gets overwhelmed, hallucinates, forgets its initial instructions, 
# and gets trapped in infinite loops.
#
# To solve this, we use Advanced Agent Systems (like LangGraph or AutoGen). 
# We split the task among multiple, specialized "Personas" that talk to each other:
# 1. The Planner: Breaks the big task into 5 micro-tasks.
# 2. The Researcher: Given a micro-task, it uses the Web Search tool.
# 3. The Writer: Takes the research and drafts a paragraph.
# 4. The Critic: Reads the paragraph, finds flaws, and rejects it!
#
# By forcing the LLM to reflect, self-correct, and pass a state graph, we 
# achieve superhuman reliability.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Plan-and-Execute architectures.
# - Understand Multi-Agent Communication (The Critic Pattern).
# - Understand State Machines in Agentic workflows (LangGraph concepts).
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. PLAN-AND-EXECUTE ARCHITECTURE
# ==============================================================================
def demonstrate_plan_and_execute():
    section_header("Plan-and-Execute Architecture")
    
    print("If you ask an LLM to 'Build a Python Web Scraper', it will immediately ")
    print("start writing random Python code, often forgetting to install libraries ")
    print("or handle HTTP errors.")
    
    print("\n--- The Architecture ---")
    print("1. THE PLANNER AGENT:")
    print("   We prompt the LLM: 'Do not write any code. Given the user request, ")
    print("   output a strict JSON array of 4 sequential steps.'")
    print("   LLM Outputs:")
    print("   [")
    print("     '1. Pip install requests and beautifulsoup4.',")
    print("     '2. Write a function to fetch the HTML with a User-Agent.',")
    print("     '3. Parse the DOM to extract all <a> tags.',")
    print("     '4. Save the links to a CSV file.'")
    print("   ]")
    
    print("\n2. THE EXECUTOR AGENT:")
    print("   Our Python code loops through the JSON array.")
    print("   For Step 1, it calls a new LLM instance with the prompt:")
    print("   'Execute this specific task: Pip install...'.")
    
    print("\nWhy is this better?")
    print("The Executor LLM's Context Window is incredibly focused. It is ONLY ")
    print("thinking about Step 2. It doesn't get confused by Step 4. This mathematically ")
    print("guarantees high-quality, bug-free outputs for complex projects.")


# ==============================================================================
# 4. THE CRITIC (REFLECTION AND SELF-CORRECTION)
# ==============================================================================
def demonstrate_critic_pattern():
    section_header("Multi-Agent Reflection (The Critic)")
    
    print("LLMs suffer from 'Sycophancy'. If you ask an LLM to write a poem, ")
    print("and then ask 'Is this poem good?', it will always say 'Yes, it is excellent!'.")
    
    print("\nWe solve this by instantiating two completely separate Agent Personas.")
    
    print("\n--- The Workflow ---")
    print("1. THE GENERATOR:")
    print("   Prompt: 'You are an expert Python Developer. Write a sorting algorithm.'")
    print("   Result: The LLM writes a Bubble Sort (which is very slow).")
    
    print("\n2. THE CRITIC:")
    print("   Prompt: 'You are a ruthless Senior Principal Engineer at Google. ")
    print("   Your job is to find security flaws, performance bugs, and bad practices ")
    print("   in the following code. Do NOT be polite. Reject bad code.'")
    print("   Input: [The Generator's Bubble Sort code]")
    
    print("\n   Result: The Critic mathematically analyzes the code and outputs: ")
    print("   'REJECTED. Bubble sort is O(N^2). Use a native Timsort or Quicksort.'")
    
    print("\n3. THE SELF-CORRECTION LOOP:")
    print("   The Python orchestrator takes the Critic's rejection and feeds it ")
    print("   BACK to the Generator: 'Your code failed review. Fix these issues: ...'")
    
    print("\nThis loop runs until the Critic explicitly outputs 'APPROVED'. ")
    print("This dramatically reduces hallucination and forces high-quality reasoning.")


# ==============================================================================
# 5. STATE MACHINES (LANGGRAPH CONCEPTS)
# ==============================================================================
def demonstrate_state_machine():
    section_header("Agentic State Machines (LangGraph)")
    
    print("Basic Agents use a simple `while` loop (ReAct).")
    print("Advanced Agents use a Directed Acyclic Graph (DAG) or a cyclic State Machine.")
    
    print("\nImagine a Graph with Nodes (Functions) and Edges (Conditionals):")
    
    print("\n[Node A: Supervisor Agent]")
    print("   |-- Evaluates the user query.")
    print("   |-- Edge 1: If query is math -> Route to Node B.")
    print("   |-- Edge 2: If query is news -> Route to Node C.")
    
    print("\n[Node B: Math Execution Node]")
    print("   |-- Writes Python code to solve the math.")
    print("   |-- Executes the code in a Docker container.")
    print("   |-- Edge: Returns result back to Node A.")
    
    print("\n[Node C: Web Search Node]")
    print("   |-- Queries Google API.")
    print("   |-- Scrapes top 3 websites.")
    print("   |-- Edge: Returns text back to Node A.")
    
    print("\nIn frameworks like LangGraph, the entire system shares a single ")
    print("global 'State' Dictionary. As the data bounces infinitely between ")
    print("Node A, B, and C, each Node updates the Dictionary. This allows for ")
    print("massively complex, deterministic routing that a single LLM could never achieve.")


def run_all_labs():
    demonstrate_plan_and_execute()
    demonstrate_critic_pattern()
    demonstrate_state_machine()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does a "Plan-and-Execute" architecture outperform a standard ReAct loop on complex tasks?
   Answer: A standard ReAct loop asks the LLM to think about the *entire* overarching goal on every single turn. For a 50-step task, the LLM's context window becomes flooded with irrelevant information, causing it to lose focus and hallucinate. Plan-and-Execute splits the cognitive load. The Planner mathematically maps out the trajectory once. The Executor is entirely blind to the overarching goal; it only receives a tiny, hyper-focused prompt (e.g., "Step 14: Write a SQL join"). This guarantees strict logical adherence and prevents infinite loops.

2. Why is "The Critic" pattern effective at reducing hallucinations?
   Answer: LLMs are trained on human data to be highly agreeable (Sycophancy). If an LLM generates a hallucinated fact, and you ask the *same* LLM instance to review it, its mathematical weights will naturally bias toward confirming its own previous output. By instantiating a completely new API call with a brutally adversarial System Prompt ("You are a ruthless auditor..."), you force the LLM into a completely different region of its geometric latent space. It is no longer trying to be agreeable; it is mathematically optimized to detect flaws, allowing it to easily spot the hallucination of the previous instance.

3. What is the fundamental advantage of defining an Agent workflow as a Graph (e.g., LangGraph) instead of a linear Python script?
   Answer: A linear Python script is deterministic and brittle; it cannot easily handle infinite loops of self-correction or dynamic routing. A Graph architecture treats the workflow as a Finite State Machine. You define Nodes (which can be Python functions, LLM calls, or API calls) and Conditional Edges (routing logic). Because the entire system passes a global "State" object between nodes, you can define highly complex cyclic behaviors (e.g., `Generator -> Critic -> [If Failed] -> Generator -> [If Passed] -> Human Review -> End`). This allows for truly autonomous, resilient systems that can gracefully recover from errors.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced Agent Systems Completed.")

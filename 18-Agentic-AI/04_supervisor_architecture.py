"""
# 04 - Agentic AI: The Supervisor Architecture (Multi-Agent Systems)

## A. Concept Name
Multi-Agent Systems: The Supervisor (Orchestrator) Architecture.

## B. One-Sentence Definition
A Supervisor Architecture uses one primary LLM agent to act as a manager that routes tasks, coordinates data, and delegates specialized sub-tasks to a team of worker LLM agents, ensuring complex multi-step goals are achieved reliably.

## C. Why Does This Exist?
A single LLM cannot do everything. If you give one LLM a massive prompt like "Write a React app, test it, style it, and deploy it," it will get confused, forget instructions in the middle (context window degradation), or hallucinate.
By splitting the task across specialized agents (e.g., a Coder Agent, a Reviewer Agent, a Designer Agent) managed by a Supervisor, you mimic a real human development team. This drastically reduces hallucinations and improves output quality.

## D. Intuition & Real-World Analogy
Think of a Construction Site.
- **The Supervisor**: The Foreman. They hold the blueprint but don't swing hammers. They look at the plan and say: "Electrician, wire the house. Plumber, install the pipes."
- **The Worker Agents**: The Electrician and Plumber. They have narrow, highly specialized instructions. They do their job and report back to the Foreman.
- If the Plumber makes a mistake, the Foreman sees it and asks the Plumber to fix it.

## E. Core Mechanics

### 1. The Supervisor Prompt
The Supervisor LLM is prompted not to solve the task, but to *plan* the task. Its available "tools" are literally the other agents.
Example Tool: `delegate_to_coder(task_description)`

### 2. State Management (The Blackboard)
Multi-agent systems require shared memory (often called a "Blackboard" or "State Graph"). As agents work, they write their outputs to this shared state so the Supervisor knows what has been completed.

### 3. Routing vs Orchestration
- **Routing**: A simple router looks at a query and sends it to one specific agent (e.g., "Math query? Send to Math Agent. Done.").
- **Orchestration**: The Supervisor actively manages a conversation loop, sending task A to Agent 1, taking Agent 1's output, and feeding it as input to Agent 2.

## F. Common Mistakes & Anti-Patterns
1. **Infinite Loops**: The Coder Agent writes bad code. The Reviewer Agent rejects it. The Coder Agent writes the same bad code again. The system gets stuck in a loop and burns $50 in API tokens.
   **Fix**: Always implement a `max_retries` counter in the Supervisor's state loop.
2. **God Agents**: Making the sub-agents too generalized. If your "Database Agent" also writes HTML, it's not a sub-agent, it's just a second messy LLM. Keep sub-agents highly scoped!

## G. Interview Connection
**Q: "How would you design an agentic system to write and review code?"**
A: "I would use a Supervisor Architecture using a state graph (like LangGraph). The Supervisor receives the user request and delegates it to a 'Software Engineer' agent. The Engineer writes the code and returns it to the Supervisor. The Supervisor then passes the code to a 'QA Reviewer' agent. If QA finds bugs, the Supervisor routes it back to the Engineer. I would enforce a maximum loop limit of 3 to prevent infinite loops."

## H. Implementation & Guided Practice
"""

import time
import random

# ==========================================
# 1. Simulating Sub-Agents (Workers)
# ==========================================
class Agent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    def execute(self, task: str) -> str:
        """Simulates an LLM generating a response to a specific task."""
        print(f"    [{self.name} the {self.role}] Working on: '{task}'...")
        time.sleep(1) # Simulating API latency
        return self._mock_llm_response(task)
        
    def _mock_llm_response(self, task: str) -> str:
        # Mock logic based on agent role
        if self.role == "Researcher":
            return "Research Data: PyTorch is a framework for Deep Learning."
        elif self.role == "Writer":
            return "Draft: Dive into PyTorch, the ultimate deep learning framework!"
        elif self.role == "Reviewer":
            # Simulate a 30% chance the reviewer rejects the draft
            if random.random() < 0.3:
                return "REJECTED: Draft is too informal. Needs more technical depth."
            return "APPROVED: Draft looks great."
        return "Task complete."

# ==========================================
# 2. The Supervisor (Orchestrator)
# ==========================================
class Supervisor:
    def __init__(self):
        # Register the team
        self.researcher = Agent("Alice", "Researcher")
        self.writer = Agent("Bob", "Writer")
        self.reviewer = Agent("Charlie", "Reviewer")
        
        # Shared State (The Blackboard)
        self.state = {
            "research_data": None,
            "draft": None,
            "final_article": None,
            "status": "NOT_STARTED",
            "revisions": 0
        }

    def run_workflow(self, user_request: str):
        print(f"\n[SUPERVISOR] Received Goal: '{user_request}'")
        self.state["status"] = "IN_PROGRESS"
        
        # STEP 1: Research
        print("\n[SUPERVISOR] Delegating to Researcher...")
        self.state["research_data"] = self.researcher.execute(f"Find data about: {user_request}")
        
        # STEP 2: Writing & Review Loop (The core of Agentic behavior)
        max_revisions = 3
        
        while self.state["revisions"] < max_revisions:
            print("\n[SUPERVISOR] Delegating to Writer...")
            self.state["draft"] = self.writer.execute(
                f"Write an article using this data: {self.state['research_data']}"
            )
            
            print("\n[SUPERVISOR] Delegating to Reviewer...")
            review_feedback = self.reviewer.execute(
                f"Review this draft: {self.state['draft']}"
            )
            
            if "APPROVED" in review_feedback:
                print("\n[SUPERVISOR] Draft Approved by QA!")
                self.state["final_article"] = self.state["draft"]
                self.state["status"] = "COMPLETED"
                break
            else:
                print(f"\n[SUPERVISOR] Draft Rejected. Feedback: {review_feedback}")
                self.state["revisions"] += 1
                print(f"[SUPERVISOR] Forcing revision. (Attempt {self.state['revisions']}/{max_revisions})")
                
        # Handle failure case
        if self.state["status"] != "COMPLETED":
            print("\n[SUPERVISOR] ERROR: Max revisions reached. Workflow aborted.")
            self.state["status"] = "FAILED"
            
        return self.state


## I. Active Recall Questions
"""
1. Why does a Multi-Agent system reduce hallucinations compared to a single LLM?
   *Answer: Because each sub-agent has a highly specific system prompt and narrow context window. Instead of juggling 10 different constraints at once, an agent only focuses on one narrow job (e.g., just reviewing code for security flaws), making it much more accurate.*
2. What is the "Blackboard" pattern in Multi-Agent systems?
   *Answer: It is a shared state object (like a dictionary or graph state) that all agents read from and write to. It allows the Supervisor to keep track of what has been done and pass data between agents.*
3. How do you prevent a Supervisor-Critic loop from running infinitely?
   *Answer: You must hardcode a programmatic `max_loops` or `max_retries` constraint in the orchestrator's code. LLMs cannot reliably break out of loops on their own.*
"""

if __name__ == "__main__":
    print("========== MULTI-AGENT SUPERVISOR MASTERCLASS ==========\n")
    
    # We fix the random seed just for this demonstration so it fails once and then passes
    random.seed(42) 
    
    supervisor = Supervisor()
    final_state = supervisor.run_workflow("Explain PyTorch Basics")
    
    print("\n--- Final Workflow State ---")
    for key, value in final_state.items():
        print(f"{key}: {value}")
        
    print("\n========== MASTERCLASS COMPLETE ==========")

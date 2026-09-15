"""
# ==============================================================================
# LABORATORY: AGENTIC AI (AGENT MEMORY & THE ReAct LOOP)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer builds a multi-step Agent. They let the Agent run a tool, 
# and then they prompt the LLM: "What is the answer?". The LLM hallucinates 
# because it has absolutely no idea what the tool output was. 
#
# A senior AI engineer understands "Context Window Management". LLMs are entirely 
# stateless mathematical functions. They have zero biological memory. To create 
# the illusion of an intelligent, multi-step Agent, the engineer must manually 
# append every single Thought, Tool Call, and Tool Observation into a massive 
# JSON array (the Message History). On every single loop iteration, the ENTIRE 
# array is mathematically passed back through the LLM. 
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Stateless Memory Buffers (Message History arrays).
# - Execute Context appending during a ReAct loop.
# - Architect the illusion of continuous "Agent Intelligence".
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (MEMORY BUFFER ARCHITECTURE)
# ==============================================================================
class AgentMemorySimulator:
    
    def __init__(self):
        # [SECURE] The Memory Buffer!
        # This list physically stores the entire state of the Agent.
        # If this list is deleted, the Agent instantly develops total amnesia.
        self.message_history = [
            {"role": "system", "content": "You are a ReAct Agent. You can use Tools to solve problems."}
        ]

    def add_message(self, role: str, content: str):
        """Appends a new event to the exact end of the Context Window."""
        self.message_history.append({"role": role, "content": content})
        print(f"     [MEMORY BUFFER] Appended {role.upper()} message. Total size: {len(self.message_history)} messages.")

    def display_memory(self):
        print("\n  [CURRENT AGENT CONTEXT WINDOW]")
        for idx, msg in enumerate(self.message_history):
            role = msg['role'].upper()
            content = msg['content']
            # Truncate for display purposes if it's very long
            if len(content) > 60:
                content = content[:57] + "..."
            print(f"  {idx}: [{role}] {content}")


# ==============================================================================
# 4. THE ARCHITECTURAL PATTERN: THE ReAct LOOP
# ==============================================================================
class ReActLoopSimulator:
    
    def __init__(self):
        self.memory = AgentMemorySimulator()
        
    def simulate_agentic_workflow(self, user_goal: str):
        """
        [SECURE] Simulating the multi-step Autoregressive loop.
        Notice how the ENTIRE memory is required for the LLM to make the next decision!
        """
        print(f"  [INIT] Starting ReAct Loop for Goal: '{user_goal}'")
        
        # Step 1: User provides the goal
        self.memory.add_message("user", user_goal)
        self.memory.display_memory()
        
        # ---------------------------------------------------------
        # LOOP ITERATION 1: Initial Reasoning & Action
        # ---------------------------------------------------------
        print("\n  [LOOP 1: LLM Forward Pass]")
        # The LLM looks at the Memory [System, User] and generates a response.
        llm_response_1 = "Thought: I need to calculate 245 * 13. I am an LLM and cannot do math natively. Action: calculate(245 * 13)"
        print(f"  -> Generated: {llm_response_1}")
        
        # We append the LLM's thought to the memory!
        self.memory.add_message("assistant", llm_response_1)
        
        # The Python Execution Boundary intercepts the Action!
        print("  -> Python executes: eval('245 * 13')")
        tool_result = "3185"
        
        # We append the Tool Observation to the memory!
        self.memory.add_message("tool", f"Observation: {tool_result}")
        self.memory.display_memory()
        
        # ---------------------------------------------------------
        # LOOP ITERATION 2: Synthesis & Final Answer
        # ---------------------------------------------------------
        print("\n  [LOOP 2: LLM Forward Pass]")
        # The LLM looks at the Memory [System, User, Assistant(Thought/Action), Tool(Observation)]
        # Because the observation '3185' is physically in the context, the LLM can use it!
        llm_response_2 = "Thought: I now have the result from the calculator. Final Answer: The result is 3185."
        print(f"  -> Generated: {llm_response_2}")
        
        # Append final answer to memory
        self.memory.add_message("assistant", llm_response_2)
        
        print("\n  [FLAWLESS] The Agent successfully navigated a multi-step workflow. ")
        print("  Because we explicitly appended the Tool Observation to the Memory Array, ")
        print("  the LLM was able to read it during Loop 2 and output the correct answer.")


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_agent_memory():
    section_header("Agentic AI: Memory Buffers & ReAct")
    
    sim = ReActLoopSimulator()
    sim.simulate_agentic_workflow(user_goal="Multiply 245 by 13 using your calculator tool.")


def run_all_labs():
    demonstrate_agent_memory()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why does a complex Agentic task eventually crash with a `TokenLimitExceeded` error, and how do you fix it?"
   Senior Answer: "Context Window Saturation. On every iteration of the ReAct loop, the Agent appends new Thoughts, Tool Calls, and massive string Observations (e.g., reading a webpage) to the JSON Message Array. Because the LLM is stateless, the entire array is sent to the API on *every single loop*. Eventually, the array surpasses the model's physical hardware limit (e.g., $128,000$ tokens). To fix this, you must implement a 'Sliding Window Memory' or 'Summarization Buffer'. When the array hits $100,000$ tokens, a secondary LLM compresses the oldest $50,000$ tokens into a $500$-token summary, preserving the geometric context while physically freeing up space."

2. Interviewer: "In a ReAct loop, what happens if the Python environment fails to append the Tool Observation to the memory array before looping?"
   Senior Answer: "Infinite Hallucination Loops. If the LLM generates `Action: search(AAPL)`, but the Python environment executes it and forgets to append `Observation: 150` to the Context Array, the LLM is sent back into the forward pass. The LLM reads its own previous output: `Action: search(AAPL)`. Because it cannot see the result, it assumes the tool hasn't fired yet. It will probabilistically generate the exact same text again: `Action: search(AAPL)`. The system falls into an infinite, unbreakable loop, burning API credits until the max iteration limit halts the script."

3. Interviewer: "Explain the philosophical difference between 'ReAct' and 'Plan-and-Solve' agent architectures."
   Senior Answer: "Myopic Execution vs Global Strategy. ReAct (Reasoning and Acting) is an intertwined, step-by-step architecture. The Agent generates exactly one Thought, takes exactly one Action, and waits for the Observation. It is excellent for dynamic environments but suffers from myopia (it loses track of the grand objective). 'Plan-and-Solve' splits the Agent. In step 1, a 'Planner LLM' writes a massive, static markdown checklist (The Plan). In step 2, an 'Executor LLM' reads the Plan and completes it step-by-step. If the Executor gets distracted, the hardcoded Plan mathematically grounds it back to the core objective."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Agentic AI (Memory & ReAct) Completed.")

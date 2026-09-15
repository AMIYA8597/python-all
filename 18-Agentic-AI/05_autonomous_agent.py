"""
# ==============================================================================
# LABORATORY: AGENTIC AI (THE AUTONOMOUS AGENT CAPSTONE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You have reached the pinnacle of modern Artificial Intelligence architecture.
# An "Autonomous Agent" is not magic. It is the mathematical fusion of everything 
# you have learned in this Academy:
# 
# 1. The LLM (The Autoregressive Neural Network Brain).
# 2. Prompt Engineering (The System Instructions & ReAct template).
# 3. Tool Calling (The JSON Schema execution boundary).
# 4. Memory Management (The Context Window JSON Array).
# 5. The Control Flow (The deterministic `while` loop that glues it all together).
#
# A senior AI engineer builds this architectural loop, unleashes it on a massive 
# dataset, and walks away. The system autonomously reasons, acts, observes, and 
# solves problems without human intervention.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the complete End-to-End Agentic Loop.
# - Execute the final Capstone Architecture.
# - Synthesize the entire curriculum.
#
# ==============================================================================
"""

import json

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE CAPSTONE AGENT)
# ==============================================================================
class MockLLMAPI:
    """A highly realistic simulation of the OpenAI/Anthropic Tool-Calling API."""
    
    def __init__(self):
        self.call_count = 0
        
    def generate_response(self, memory_array: list) -> dict:
        self.call_count += 1
        
        # Look at the last message in the memory to determine context
        last_message = memory_array[-1]["content"]
        
        print(f"\n     [LLM API] Receiving massive Context Array ({len(memory_array)} messages)...")
        print("     [LLM API] Executing Forward Pass (Attention Matrix calculating)...")
        
        if self.call_count == 1:
            # First pass: The model sees the user prompt and decides it needs external data.
            return {
                "finish_reason": "tool_calls",
                "message": {
                    "role": "assistant",
                    "content": None, # No plain text to the user!
                    "tool_calls": [
                        {
                            "id": "call_999",
                            "type": "function",
                            "function": {
                                "name": "query_database",
                                "arguments": '{"sql": "SELECT revenue FROM q3_sales"}'
                            }
                        }
                    ]
                }
            }
            
        elif self.call_count == 2:
            # Second pass: The model sees the SQL output in the memory array!
            return {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": "I have checked the database. The total Q3 revenue is $50,000.",
                    "tool_calls": None
                }
            }


class AutonomousAgent:
    
    def __init__(self):
        self.llm = MockLLMAPI()
        self.memory = [
            {"role": "system", "content": "You are an autonomous agent with access to a SQL database."}
        ]
        
    def execute_tool(self, function_name: str, arguments: dict) -> str:
        """The deterministic execution boundary."""
        print(f"  -> [PYTHON INTERCEPT] Executing local tool: {function_name}({arguments})")
        if function_name == "query_database":
            # Simulate a real DB lookup
            return "[(50000,)]"
        return "Error: Unknown Tool."

    def run(self, user_prompt: str, max_iterations: int = 5):
        """
        [SECURE] The Capstone Loop.
        This `while` loop is the exact architectural foundation of AutoGPT, BabyAGI, 
        LangChain Agents, and LlamaIndex Agents.
        """
        print(f"  [INIT] Autonomous Agent Online. Goal: '{user_prompt}'")
        
        # 1. Append User Prompt to Memory
        self.memory.append({"role": "user", "content": user_prompt})
        
        iteration = 0
        while iteration < max_iterations:
            iteration += 1
            print(f"\n  [LOOP {iteration}]")
            
            # 2. Call the LLM with the ENTIRE Memory
            llm_response = self.llm.generate_response(self.memory)
            message = llm_response["message"]
            
            # 3. Append the LLM's raw message back to Memory (CRITICAL for tracking Tool IDs)
            self.memory.append(message)
            
            # 4. Check the Finish Reason
            if llm_response["finish_reason"] == "stop":
                print(f"\n  [FINAL ANSWER GENERATED]")
                print(f"  -> {message['content']}")
                break
                
            elif llm_response["finish_reason"] == "tool_calls":
                print("  [TOOL CALL DETECTED]")
                
                # 5. Execute every requested tool
                for tool_call in message["tool_calls"]:
                    func_name = tool_call["function"]["name"]
                    kwargs = json.loads(tool_call["function"]["arguments"])
                    
                    # Physically run the Python function!
                    observation = self.execute_tool(func_name, kwargs)
                    
                    # 6. Append the Observation to Memory
                    # The LLM MUST see this observation on the next iteration!
                    print(f"  -> Appending Observation to Context Window: '{observation}'")
                    self.memory.append({
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": observation
                    })


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_capstone():
    section_header("Agentic AI: The Capstone Autonomous Loop")
    
    agent = AutonomousAgent()
    agent.run(user_prompt="What was the total revenue for Q3? Query the database.")
    
    print("\n" + "="*60)
    print("  [ACADEMY COMPLETION]")
    print("  The Python Curriculum has reached its architectural conclusion.")
    print("  From basic variables in Phase 01 to Autonomous Multi-Agent AI in Phase 18.")
    print("  You are now ready to build production-grade Intelligence.")
    print("="*60)


def run_all_labs():
    demonstrate_capstone()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In an Autonomous Agent loop, what is the architectural significance of the `max_iterations` parameter?"
   Senior Answer: "The Halting Problem. A purely probabilistic LLM running inside a `while True:` loop has no mathematical guarantee of halting. If it encounters a bug, a missing tool, or simply hallucinates a bad reasoning path, it can autonomously generate an infinite loop of API calls, consuming thousands of dollars of compute in minutes. The `max_iterations` counter is a hardcoded, deterministic safeguard. It forces the system to abort and yield back to the human developer if the network fails to converge on a `finish_reason: 'stop'` within a mathematically defined limit."

2. Interviewer: "Why must we append the LLM's tool call (the `assistant` message) AND the tool result (the `tool` message) to the Context Array?"
   Senior Answer: "Vector Alignment. If you only append the tool result (the Observation), the LLM reads its Context Window and sees: `[User Prompt, Tool Result]`. The Attention Mechanism becomes mathematically confused because there is no logical link between the user asking a question and a random JSON object appearing in the context. By appending the LLM's own decision (`[User Prompt, Assistant Tool Request, Tool Result]`), the Attention Matrix smoothly maps the causal relationship: 'I asked for this data, and here it is.' This causal chain is strictly required for the model to synthesize the final answer."

3. Interviewer: "How do you transition a single Autonomous Agent into a production-grade enterprise system?"
   Senior Answer: "Specialization and Memory Persistence. A toy Agent holds its Context Array in local Python RAM. A production Agent serializes its state to a PostgreSQL or Redis database after every single step, allowing the execution loop to survive server crashes (Resumability). Furthermore, instead of one massive Agent with 50 tools, we deploy the Multi-Agent Supervisor pattern. We spawn 5 distinct Agents, each with their own specialized System Prompts and 3 highly specific tools. The Supervisor Agent routes the user's intent to the correct specialized node, mathematically preventing Context Window pollution and hallucination at enterprise scale."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Agentic AI (Capstone Agent) Completed.")

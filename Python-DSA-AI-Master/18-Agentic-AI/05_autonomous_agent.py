"""
## A. Concept Name
Autonomous Agent

## B. Educational Objective
Understand how memory, tools, and a reasoning loop combine to form an autonomous AI agent capable of executing multi-step tasks.

## C. Core Logic/Algorithm
1. Initialization: Set up memory and available tools.
2. Observe & Orient (Input): Take user instructions and append to memory.
3. Decide (LLM/Brain): Analyze current memory and determine the next action (tool call or final text output).
4. Act (Tool Execution): Execute the chosen tool.
5. Feedback (Observation): Append the tool's result to memory.
6. Loop: Repeat steps 3-5 until a final text output is generated or the maximum iteration limit is reached.

## D. Edge Cases & Handling
- Max Iterations: Prevent infinite loops by enforcing a strict max iteration limit.
- Unknown Tools: Gracefully handle attempts to call non-existent tools with error messages.

## E. Complexity (Time & Space)
- Time Complexity: O(I * (T + L)), where I is max iterations, T is tool execution time, and L is LLM decision time.
- Space Complexity: O(M), where M is the size of the memory list scaling with the number of interactions and tool results.

## F. Advanced Application/Extensions
- Real LLM Integration: Replace the simulated decision function with actual API calls to models like Gemini, GPT-4, or Claude.
- Async Execution: Implement asynchronous tool calls and reasoning for faster performance.
- Complex Memory Management: Use vector databases for long-term memory retrieval instead of a growing list.

## X. Project Connection
This script simulates the foundational autonomous loop used in larger agentic frameworks, providing the basis for creating complete, self-directed AI coding assistants or research agents.
"""
import time

# 1. Define Tools
def search_database(query: str) -> str:
    print(f"    -> [Tool: search_database] Searching for '{query}'...")
    return "Database result: AI Agents use reasoning loops to solve tasks."

def save_to_file(filename: str, content: str) -> str:
    print(f"    -> [Tool: save_to_file] Saving to '{filename}'...")
    return "Success: File saved."

# 2. Agent Core
class AutonomousAgent:
    def __init__(self):
        self.memory = []
        self.max_iterations = 5
        self.tools = {
            "search_database": search_database,
            "save_to_file": save_to_file
        }
        
    def run(self, user_instruction: str):
        print(f"--- Agent Started ---\nInstruction: {user_instruction}\n")
        self.memory.append({"role": "user", "content": user_instruction})
        
        # 3. Agent Loop
        for iteration in range(self.max_iterations):
            print(f"--- Iteration {iteration + 1} ---")
            
            # Simulated LLM Brain evaluating the memory
            action = self._simulated_llm_decision(iteration)
            
            if action["type"] == "text":
                # Agent provides final answer
                print(f"[Agent Speaking]: {action['content']}")
                print("\n--- Agent Finished ---")
                return
                
            elif action["type"] == "tool_call":
                # Agent calls a tool
                tool_name = action["name"]
                args = action["args"]
                print(f"[Agent Thinking]: I need to use {tool_name}.")
                
                # Execute Tool
                if tool_name in self.tools:
                    result = self.tools[tool_name](**args)
                    self.memory.append({"role": "tool", "name": tool_name, "content": result})
                    print(f"    -> [Observation]: {result}")
                else:
                    print("    -> [Error]: Unknown tool.")
            
            time.sleep(1) # Simulate processing time
            print()
            
        print("\n[System]: Agent stopped. Reached max iterations.")

    def _simulated_llm_decision(self, iteration: int) -> dict:
        """Simulates the LLM's response based on the iteration step."""
        if iteration == 0:
            return {
                "type": "tool_call",
                "name": "search_database",
                "args": {"query": "how do AI agents work"}
            }
        elif iteration == 1:
            return {
                "type": "tool_call",
                "name": "save_to_file",
                "args": {"filename": "agent_notes.txt", "content": "AI Agents use reasoning loops."}
            }
        else:
            return {
                "type": "text",
                "content": "I have completed the research and saved the notes to the file."
            }

if __name__ == "__main__":
    agent = AutonomousAgent()
    agent.run("Research how AI agents work and save the notes.")

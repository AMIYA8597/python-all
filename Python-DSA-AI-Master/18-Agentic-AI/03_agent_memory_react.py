"""
## A. Concept Name
Agent Memory and ReAct Planning

## B. Core Objective
Understand how an agent maintains memory (conversation history) and uses a ReAct (Reason + Act) loop to solve a problem.

## C. Key Components
1. Memory: Storing past interactions and thoughts.
2. Thought: Reasoning about the current state.
3. Action: Using a tool or making a move.
4. Observation: The result of the action.

## D. Prerequisites
Basic Python, understanding of functions and classes.

## E. Real-World Analogy
Solving a math problem on scratchpad. You write down intermediate steps (Memory), think about the next operation (Thought), use a calculator (Action), and write the result down (Observation).

## F. Architecture
SimpleMemory class for storing messages, calculator_tool for acting, simulate_react_agent for orchestration.

## G. Implementation Details
The ReAct loop is simulated sequentially here to demonstrate the pattern clearly.

## H. Pitfalls
Using `eval` in production without sanitization. Failing to manage context window limits in real LLMs.

## I. Best Practices
Sanitize inputs, implement robust tool error handling, use structured memory formats.

## J. Expected Output
Console output showing Thoughts, Actions, Observations, and Final Answer.

## K. Related Patterns
Chain of Thought (CoT), Plan-and-Solve, Tool Use (Function Calling).

## L. Testing
Run the script and verify the math operations match the expected final output (410).

## M. Performance
Negligible overhead; simulated sleeps added for pacing.

## N. Security
`eval` is used here purely for educational simplicity. DO NOT use in production.

## O. Deployment
Typically deployed as part of a larger LangChain or AutoGen application.

## P. Maintenance
Update the calculator to use safe parsing (e.g., AST) instead of eval.

## Q. Scalability
For complex tasks, integrate vector databases for long-term memory retrieval.

## R. Extensibility
Can be extended with more tools (web search, file read) and real LLM calls.

## S. Anti-Patterns
Hardcoding thoughts (done here for simulation only), ignoring tool errors.

## T. Metrics
Track tool success rate, tokens used, and latency in real applications.

## U. Dependencies
Python standard library only (`time`).

## V. Version Compatibility
Python 3.6+ (uses f-strings).

## W. References
ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al., 2022).

## X. Project Connection
This forms the foundational orchestration layer for all complex Agentic workflows in our AI Master project.
"""
import time

class SimpleMemory:
    def __init__(self):
        self.messages = []
        
    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        
    def get_context(self) -> str:
        return "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in self.messages])

def calculator_tool(expression: str) -> str:
    """A simple tool to evaluate mathematical expressions."""
    try:
        # Warning: eval is dangerous in production, used here for educational simplicity.
        return str(eval(expression))
    except Exception as e:
        return f"Error evaluating expression: {e}"

def simulate_react_agent(question: str):
    print("--- Starting ReAct Agent ---")
    memory = SimpleMemory()
    memory.add_message("user", question)
    
    # Simulated ReAct Loop
    print(f"Goal: {question}\n")
    
    # Step 1: Think
    thought_1 = "I need to calculate 15 * 24 first."
    memory.add_message("thought", thought_1)
    print(f"Thought: {thought_1}")
    
    # Step 1: Act
    action_1 = "15 * 24"
    print(f"Action: calculator_tool('{action_1}')")
    obs_1 = calculator_tool(action_1)
    memory.add_message("observation", f"Result is {obs_1}")
    print(f"Observation: {obs_1}\n")
    time.sleep(1)
    
    # Step 2: Think
    thought_2 = f"Now I need to add 50 to the previous result ({obs_1})."
    memory.add_message("thought", thought_2)
    print(f"Thought: {thought_2}")
    
    # Step 2: Act
    action_2 = f"{obs_1} + 50"
    print(f"Action: calculator_tool('{action_2}')")
    obs_2 = calculator_tool(action_2)
    memory.add_message("observation", f"Result is {obs_2}")
    print(f"Observation: {obs_2}\n")
    time.sleep(1)
    
    # Final Answer
    thought_3 = "I have the final answer."
    print(f"Thought: {thought_3}")
    answer = f"The final result is {obs_2}."
    memory.add_message("assistant", answer)
    print(f"Final Answer: {answer}")
    
    print("\n--- Final Agent Memory ---")
    print(memory.get_context())

if __name__ == "__main__":
    simulate_react_agent("What is 15 multiplied by 24, and then add 50?")

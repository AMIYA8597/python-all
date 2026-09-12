"""
Module: 04-agent-systems
Description: Comprehensive educational script for 04-agent-systems.

## A. Concept Name
Agent Systems (LLM Agents)

## B. Motivation
LLMs are naturally stateless text generators. Agent systems empower them with agency by providing a loop where they can plan, utilize tools, observe outcomes, and manage memory to solve complex, multi-step problems autonomously.

## C. Core Mechanics
An agent acts as a controller that decides which steps to take. It typically operates in a loop: perceive (input/observation) -> think (reason/plan) -> act (use a tool/generate output).

## D. Architecture
A typical agent architecture includes:
- LLM (the brain)
- Tools (the hands)
- Memory (the context)
- Planner (the strategy)

## E. Memory Management
Agents require short-term memory (conversation history) and long-term memory (RAG, vector databases) to retain context across steps.

## F. Planning
Agents can break down complex tasks into subtasks (e.g., Plan-and-Solve, Chain of Thought, Tree of Thoughts) to avoid hallucinating steps.

## G. Tool Execution
Agents use APIs, calculators, code interpreters, or database queries to fetch real-time information or cause side effects in the environment.

## H. ReAct Pattern
Reason + Act. A common prompt structure where the LLM is explicitly asked to output a "Thought:", followed by an "Action:", and wait for an "Observation:" before continuing.

## I. Multi-Agent Systems
Complex workflows can be distributed among specialized agents (e.g., a Researcher agent and a Writer agent) to improve quality and reduce context window overload.

## J. Frameworks
Popular frameworks include LangChain, LlamaIndex, AutoGen, and CrewAI, offering abstractions for building and orchestrating agents.

## K. Tracing
Agent logic is non-deterministic. Tracing steps, inputs, and tool outputs using tools like LangSmith or Phoenix is critical for debugging.

## L. Evaluation
Agents are evaluated on task completion rates, reasoning accuracy, tool selection correctness, and cost-efficiency, often requiring specialized LLM-as-a-judge pipelines.

## M. Security
Allowing LLMs to execute code or write to databases poses severe risks (prompt injection, unintended side effects). Sandboxing and restricted permissions are mandatory.

## N. Cost Management
Agent loops can easily blow up in token consumption. Hard limits on loop iterations and context window truncation are required.

## O. Latency Optimization
Agents are slow because each step requires a full LLM call. Parallelizing tool calls and streaming responses can help reduce perceived latency.

## P. Human-in-the-Loop
For high-stakes tasks, the agent should propose an action and wait for human approval before executing it.

## Q. Deployment
Agents are deployed as persistent services that hold state (often using WebSockets for streaming status) rather than simple stateless HTTP endpoints.

## R. Best Practices
Start with rigid workflows (state machines) and only introduce autonomous agency where flexibility is strictly required. Provide strict schemas for tool inputs.

## S. Common Pitfalls
Infinite loops (agent repeatedly failing to use a tool correctly), context window overflow, and losing track of the original goal.

## T. Anti-patterns
Giving an agent too many tools at once. It's better to use hierarchical agents where a router selects a specialized agent with a smaller subset of tools.

## U. Alternatives
Standard deterministic code or simple structured extraction pipelines are often more reliable and cheaper if the task doesn't require autonomous decision-making.

## V. Future Trends
Smaller, edge-deployed action models (LAMs), standard protocols for agents to communicate, and native tool-calling capabilities built into base models.

## W. References
- ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al.)
- LangChain Documentation
- AutoGen Documentation

## X. Project Connection
In our broader GenAI projects, agent systems allow the chatbot to perform real-world actions like looking up database records, booking appointments, or generating and executing Python code based on user requests.
"""

import sys
import time
from typing import List, Dict, Any, Callable

# Dummy LLM call for educational purposes
def dummy_llm(prompt: str) -> str:
    """Simulates an LLM response based on the prompt."""
    if "Calculate 5 + 7" in prompt:
        return "Thought: I need to use the calculator tool to add 5 and 7.\nAction: calculator(5, '+', 7)"
    elif "Observation: 12" in prompt:
        return "Thought: I have the result.\nFinal Answer: The result of 5 + 7 is 12."
    return "Final Answer: I am a dummy agent and cannot answer that."

def basic_implementation() -> None:
    """
    Basic implementation demonstrating a simple Agent reasoning step.
    """
    print("--- Basic Agent Systems ---")
    user_query = "Calculate 5 + 7"
    print(f"User Query: {user_query}")
    
    # Simple stateless agent step
    response = dummy_llm(f"User wants to: {user_query}\nWhat is your action?")
    print(f"Agent Response:\n{response}")
    print("Basic implementation completed successfully.\n")

def dummy_calculator(a: float, op: str, b: float) -> float:
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/': return a / b
    raise ValueError("Unknown operator")

def intermediate_implementation(query: str) -> str:
    """
    Intermediate implementation with a ReAct (Reasoning and Acting) loop.
    """
    print("--- Intermediate Agent Systems ---")
    memory = f"Task: {query}\n"
    max_steps = 3
    
    for step in range(max_steps):
        print(f"--- Step {step + 1} ---")
        llm_out = dummy_llm(memory)
        print(f"LLM Output:\n{llm_out}")
        
        if "Final Answer:" in llm_out:
            answer = llm_out.split("Final Answer:")[1].strip()
            print(f"Agent finished with answer: {answer}")
            print("Intermediate implementation completed.\n")
            return answer
        
        if "Action:" in llm_out:
            # Parse dummy action e.g., calculator(5, '+', 7)
            action_str = llm_out.split("Action:")[1].strip()
            print(f"Executing Tool: {action_str}")
            # Extremely naive parsing for demonstration
            if "calculator" in action_str:
                args = action_str.replace("calculator(", "").replace(")", "").split(",")
                a, op, b = float(args[0]), args[1].strip().strip("'\""), float(args[2])
                result = dummy_calculator(a, op, b)
                observation = f"Observation: {result}"
                print(observation)
                memory += llm_out + "\n" + observation + "\n"
    
    print("Agent failed to reach Final Answer within max steps.\n")
    return "Failed"

def advanced_implementation(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    """
    Advanced implementation showing tool registry and dynamic dispatch.
    """
    print("--- Advanced Agent Systems ---")
    
    tool_registry: Dict[str, Callable] = {
        "calculator": dummy_calculator,
        "search": lambda q: f"Search results for {q}"
    }
    
    print("Registered Tools:")
    for name, func in tool_registry.items():
        print(f"- {name}: {func.__name__}")
        
    # Simulating tool dispatch
    simulated_action_name = "calculator"
    simulated_action_kwargs = {"a": 10, "op": "*", "b": 5}
    
    result = None
    if simulated_action_name in tool_registry:
        tool_func = tool_registry[simulated_action_name]
        try:
            result = tool_func(**simulated_action_kwargs)
            status = "success"
        except Exception as e:
            result = str(e)
            status = "error"
    else:
        status = "tool_not_found"
        
    output = {
        "action": simulated_action_name,
        "result": result,
        "status": status
    }
    print(f"Execution Output: {output}")
    print("Advanced implementation completed.\n")
    return output

def analyze_performance_and_edge_cases() -> None:
    """
    Analyzes performance bottlenecks and discusses edge cases.
    """
    print("--- Performance Analysis & Edge Cases ---")
    print("1. Performance: Agent loops increase latency linearly with steps. Parallelize tool calls where possible.")
    print("2. Edge Case: LLM hallucinating a non-existent tool. Solution: Return a specific 'ToolNotFound' observation.")
    print("3. Edge Case: Infinite loops. Solution: Strict limit on the number of ReAct steps (e.g., max_iterations=5).\n")

def interview_challenge(tools: List[str], query: str) -> str:
    """
    Common interview challenge: Given a query and a list of tools, select the best tool.
    In a real scenario, this would use embeddings or an LLM call.
    """
    print("--- Interview Challenge for Agent Systems ---")
    # Simple keyword matching heuristic
    query_lower = query.lower()
    for tool in tools:
        if tool.lower() in query_lower:
            return tool
    return "general_llm"

def run_tests() -> None:
    """
    Simple test suite to validate the implementations.
    """
    print("--- Running Tests ---")
    try:
        assert dummy_calculator(10, '+', 5) == 15, "Calculator addition failed"
        assert interview_challenge(['calculator', 'search'], "Can you use the calculator?") == "calculator"
        print("All tests passed successfully!\n")
    except AssertionError as e:
        print(f"Test Failed: {e}\n")

if __name__ == "__main__":
    print("========== Exploring AGENT SYSTEMS ==========\n")
    
    basic_implementation()
    intermediate_implementation("Calculate 5 + 7")
    advanced_implementation()
    analyze_performance_and_edge_cases()
    
    res = interview_challenge(['Calculator', 'WeatherAPI', 'SearchEngine'], "What is the weather in Tokyo?")
    print(f"Interview Challenge Result: Selected tool -> {res}\n")
    
    run_tests()
    
    print("========== END OF AGENT SYSTEMS ==========\n")

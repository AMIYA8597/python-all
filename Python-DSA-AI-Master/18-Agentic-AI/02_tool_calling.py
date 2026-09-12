"""
## A. Concept Name
Tool Calling (Function Calling) Mechanics in LLMs

## B. Problem Space
Large Language Models (LLMs) are text generators. On their own, they cannot perform actions, access real-time data (like current weather), or interact with external systems. To bridge this gap, we need a mechanism that allows the LLM to dictate an action, which our code then executes.

## C. Solution Architecture
1. **Tool Definition**: Create a Python function that performs the action (e.g., calling an API).
2. **Schema Description**: Provide the LLM with a JSON schema describing the function's purpose and expected arguments.
3. **LLM Generation**: The LLM, based on the user prompt and schema, outputs a structured request (usually JSON) containing the tool name and arguments instead of normal conversational text.
4. **Execution**: The application code parses the LLM's JSON output, maps the requested tool name to the actual Python function, executes it, and optionally returns the result back to the LLM.

## D. Core Implementation
This script simulates the mechanics of an LLM tool call. It defines a tool, its schema, and a simulated LLM response to demonstrate parsing the arguments and executing the function dynamically.

## X. Project Connection
Understanding the underlying mechanics of tool calling is crucial for building robust Agentic AI systems. In larger projects, you will rely on frameworks (like LangChain or LlamaIndex) that abstract these steps, but knowing how the mapping and execution occur allows you to debug issues and design better schemas.
"""
import json
from typing import Dict, Any

# 1. Define the actual Python function (The Tool)
def get_weather(location: str) -> str:
    """Mock weather API."""
    print(f"[Tool Execution] Fetching weather for {location}...")
    # Simulated API response
    weather_db = {"New York": "75F and Sunny", "London": "60F and Rainy"}
    return weather_db.get(location, "Weather data not available.")

# 2. Define the schema (What we would send to the LLM)
weather_tool_schema = {
    "name": "get_weather",
    "description": "Get the current weather in a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
            }
        },
        "required": ["location"]
    }
}

# 3. Simulate the LLM's response
# In reality, the LLM generates this JSON string based on the user prompt.
simulated_llm_response = '{"name": "get_weather", "arguments": {"location": "New York"}}'

def execute_tool_call(llm_response: str) -> Any:
    print("--- Simulating Tool Calling ---")
    print(f"LLM Output: {llm_response}\n")
    
    # Parse the LLM's structured output
    call_data = json.loads(llm_response)
    tool_name = call_data.get("name")
    arguments = call_data.get("arguments", {})
    
    # Map the tool name to the actual Python function
    available_tools: Dict[str, Any] = {
        "get_weather": get_weather
    }
    
    if tool_name in available_tools:
        func = available_tools[tool_name]
        # Execute the function with the arguments provided by the LLM
        result = func(**arguments)
        print(f"\n[Tool Result] {result}")
        return result
    else:
        print(f"Unknown tool: {tool_name}")
        return None

if __name__ == "__main__":
    # User asked: "What's the weather like in New York?"
    # The LLM decided to use the weather tool.
    execute_tool_call(simulated_llm_response)

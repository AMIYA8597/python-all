"""
# ==============================================================================
# LABORATORY: ADVANCED GEN-AI (FUNCTION CALLING & AGENTS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# LLMs can generate beautiful text, but they are trapped inside their server. 
# An LLM cannot execute code, send an email, query a database, or search the web.
# 
# Unless... you give it Tools.
#
# Function Calling (Tool Use) is the foundation of Agentic AI. You provide the 
# LLM with a JSON schema describing Python functions you have written (e.g., 
# `get_weather(city)`). 
# 
# When the user asks "What is the weather in Paris?", the LLM detects that it 
# cannot answer from memory. Instead of hallucinating, it outputs a specialized 
# JSON string: `{"tool": "get_weather", "args": {"city": "Paris"}}`.
#
# Your Python script intercepts this JSON, executes the actual `get_weather` 
# Python function, and feeds the real API result back into the LLM. The LLM 
# then generates a natural language response: "The weather in Paris is 72°F."
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of Function Calling.
# - Understand how LLMs decide when to use a tool vs when to chat.
# - Construct a basic Agent Loop (ReAct paradigm).
#
# ==============================================================================
"""

import json

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE TOOLBOX (PYTHON FUNCTIONS)
# ==============================================================================
def get_weather(city: str) -> str:
    """Mock function representing an external Weather API."""
    print(f"[SYSTEM EXECUTION] Querying Weather API for {city}...")
    weather_db = {
        "Paris": "72°F, Sunny",
        "London": "60°F, Raining",
        "Tokyo": "85°F, Humid"
    }
    return weather_db.get(city, "Weather data not available.")

def get_stock_price(ticker: str) -> str:
    """Mock function representing an external Finance API."""
    print(f"[SYSTEM EXECUTION] Querying Stock API for {ticker}...")
    stock_db = {
        "AAPL": "$150.00",
        "MSFT": "$320.00"
    }
    return stock_db.get(ticker, "Stock not found.")

# This Dictionary maps the string names (that the LLM will output) to the actual 
# physical Python functions in memory.
TOOLBOX = {
    "get_weather": get_weather,
    "get_stock_price": get_stock_price
}


# ==============================================================================
# 4. SIMULATING THE LLM TOOL DECISION
# ==============================================================================
def mock_llm_api_call(user_prompt: str) -> str:
    """
    Simulates the response of an advanced LLM (like GPT-4).
    In reality, this is the `openai.chat.completions.create` API call.
    """
    print(f"User: '{user_prompt}'")
    print("LLM is " + "thinking...".rjust(30, '.'))
    
    # 1. The LLM mathematically analyzes the prompt.
    if "weather" in user_prompt.lower() and "paris" in user_prompt.lower():
        # The LLM decides it needs a tool! It halts text generation and outputs 
        # a strictly formatted JSON Tool Call.
        return '{"tool_call": {"name": "get_weather", "arguments": {"city": "Paris"}}}'
        
    elif "stock" in user_prompt.lower() and "aapl" in user_prompt.lower():
        return '{"tool_call": {"name": "get_stock_price", "arguments": {"ticker": "AAPL"}}}'
        
    else:
        # The LLM decides it DOES NOT need a tool. It just answers normally.
        return "I am an AI assistant. How can I help you today?"


def demonstrate_agentic_loop():
    section_header("The Agentic Loop (ReAct)")
    
    print("We will simulate an AI Agent receiving a user prompt, deciding to use ")
    print("a tool, pausing to let our Python script execute the tool, and then ")
    print("taking the tool's result to generate a final answer.\n")
    
    user_prompt = "What is the weather like in Paris today?"
    
    # --- STEP 1: INITIAL LLM CALL ---
    llm_response = mock_llm_api_call(user_prompt)
    
    # --- STEP 2: INTERCEPT AND PARSE ---
    # Our orchestration Python script checks if the LLM outputted standard text, 
    # or if it outputted a JSON Tool Call.
    try:
        # We attempt to parse it as JSON
        parsed_response = json.loads(llm_response)
        
        if "tool_call" in parsed_response:
            print(f"\n[ORCHESTRATOR] Detected Tool Call: {parsed_response['tool_call']['name']}")
            
            tool_name = parsed_response["tool_call"]["name"]
            tool_args = parsed_response["tool_call"]["arguments"]
            
            # --- STEP 3: PYTHON EXECUTION ---
            # We look up the actual Python function from our TOOLBOX dictionary 
            # and execute it using the exact arguments the LLM generated!
            executable_function = TOOLBOX[tool_name]
            tool_result = executable_function(**tool_args)
            
            print(f"[ORCHESTRATOR] Tool Execution Result: {tool_result}")
            
            # --- STEP 4: FINAL LLM GENERATION ---
            # In a real app, you would append the `tool_result` string to the 
            # message history and call the LLM API ONE MORE TIME. The LLM would 
            # read the result and output a natural language sentence.
            print("\n[ORCHESTRATOR] Sending result back to LLM...")
            print(f"Final LLM Output: 'Based on the latest data, it is {tool_result} in Paris.'")
            
    except json.JSONDecodeError:
        # If it wasn't JSON, the LLM just wanted to chat normally.
        print(f"Final LLM Output: {llm_response}")


def run_all_labs():
    demonstrate_agentic_loop()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. How does an LLM know exactly what arguments a Tool requires (e.g. `city` vs `location`)?
   Answer: When you initialize the LLM API, you don't just send the User Prompt. You send a massive JSON Schema array called `tools` or `functions`. This schema explicitly lists every available function name, a human-readable description of what the function does, and the exact JSON data types and keys required for the arguments (e.g., `{"type": "string", "name": "city", "description": "The city to get weather for"}`). The LLM reads this schema as part of its Context Window. If it decides to call a tool, it is mathematically constrained to generate a JSON object that perfectly matches the schema you provided.

2. What is the fundamental difference between standard LLM Generation and an Agentic Loop (ReAct)?
   Answer: Standard generation is a single-shot, open-loop process. The user asks a question, the LLM generates a response, and the execution terminates immediately. The ReAct (Reasoning and Acting) paradigm is a `while` loop. The Agent reasons about the problem, acts by calling a tool, receives the observation (the tool's output), and then reasons again based on that new information. The `while` loop continues spinning, allowing the AI to call multiple tools sequentially (e.g., search the web -> download a PDF -> read the PDF -> write a summary) until it mathematically determines it has completely solved the user's overarching goal.

3. Why is Error Handling critical in the Python execution step of an Agent architecture?
   Answer: LLMs are probabilistic models, not deterministic compilers. Despite the JSON schema, an LLM might hallucinate a tool name that doesn't exist, or generate an argument of type `Integer` when the Python function expects a `String`. If your orchestration Python code tries to execute `TOOLBOX['fake_tool']()`, the entire Python application will crash with a KeyError. You must wrap the execution step in a robust `try/except` block. If the LLM generates garbage, the `except` block catches the error and sends a message *back* to the LLM (e.g., "Error: Tool not found. Please try again with a valid tool."), allowing the Agent to recognize its mistake and self-correct on the next iteration.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced GenAI & Function Calling Completed.")

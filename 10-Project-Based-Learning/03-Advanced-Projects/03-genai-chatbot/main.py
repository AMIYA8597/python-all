"""
# ==============================================================================
# LABORATORY: PROJECT-BASED LEARNING (GENERATIVE AI & TOOL CALLING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer uses an LLM API to build a chatbot. They just pass the 
# user's prompt directly to the API (`response = llm(user_input)`). When the 
# user asks "What is the weather in Tokyo right now?", the LLM hallucinates 
# a fake temperature because it has no internet connection. When the user says 
# "What did I just say?", the LLM forgets the conversation completely.
#
# A senior AI engineer builds an "Agentic AI System". They mathematically construct 
# a rolling 'Conversation History' array, injecting it into every single API call 
# so the LLM has perfect memory. More importantly, they implement "Function Calling". 
# When the user asks for the weather, the LLM mathematically realizes it doesn't 
# know. It halts text generation, sends a structured JSON payload to the Python 
# Backend requesting the weather, the Backend executes a real API call, injects 
# the real temperature back into the LLM, and the LLM formulates a flawless, 
# mathematically proven answer.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master LLM Context Window management (Conversation History Arrays).
# - Architect Function Calling (Agentic Tool Execution).
# - Execute programmatic generation and parsing of LLM JSON payloads.
#
# ==============================================================================
"""

import json
from typing import List, Dict, Any

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE EXTERNAL TOOLS (THE PYTHON BACKEND)
# ==============================================================================
class BackendTools:
    """
    These are real Python functions running on the server.
    The LLM has absolutely no internet access. It must ask Python to run these!
    """
    @staticmethod
    def get_current_weather(location: str) -> str:
        # In a real app, this would use the OpenWeather API.
        print(f"  [PYTHON BACKEND] Executing Tool: get_current_weather(location='{location}')")
        
        if "tokyo" in location.lower():
            return '{"temperature": 22, "condition": "rainy"}'
        elif "paris" in location.lower():
            return '{"temperature": 15, "condition": "cloudy"}'
        else:
            return '{"temperature": 25, "condition": "sunny"}'

    @staticmethod
    def get_stock_price(ticker: str) -> str:
        print(f"  [PYTHON BACKEND] Executing Tool: get_stock_price(ticker='{ticker}')")
        if ticker.upper() == "AAPL":
            return '{"price": 175.50, "currency": "USD"}'
        return '{"price": 100.00, "currency": "USD"}'


# ==============================================================================
# 4. THE LLM SIMULATOR (THE MOCK API)
# ==============================================================================
class MockLLMAPI:
    """
    Simulates the OpenAI/Anthropic API to prevent the CI/CD pipeline from requiring API keys.
    It analyzes the Conversation History and decides whether to generate text or call a tool!
    """
    @staticmethod
    def chat_completion(messages: List[Dict[str, str]]) -> Dict[str, Any]:
        # We grab the absolute last message the user sent
        latest_user_message = messages[-1]["content"].lower()
        
        # 1. TOOL CALLING LOGIC
        if "weather" in latest_user_message and "tokyo" in latest_user_message:
            # The LLM halts text generation and demands a Tool Call!
            return {
                "finish_reason": "tool_calls",
                "message": {
                    "role": "assistant",
                    "content": None, # No text!
                    "tool_calls": [
                        {
                            "id": "call_abc123",
                            "function": {
                                "name": "get_current_weather",
                                "arguments": '{"location": "Tokyo, Japan"}'
                            }
                        }
                    ]
                }
            }
            
        # 2. STANDARD TEXT GENERATION LOGIC
        if "what did i just ask" in latest_user_message:
            # The LLM proves it has memory by looking backwards in the array!
            if len(messages) >= 3:
                previous_question = messages[-3]["content"]
                return {
                    "finish_reason": "stop",
                    "message": {
                        "role": "assistant",
                        "content": f"You just asked me: '{previous_question}'"
                    }
                }
                
        # 3. TOOL RESULT PROCESSING LOGIC
        if messages[-1]["role"] == "tool":
            # The LLM just received the data from the Python Backend!
            # It mathematically converts the raw JSON into conversational text.
            raw_data = json.loads(messages[-1]["content"])
            return {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": f"The weather in Tokyo is currently {raw_data['temperature']}°C and {raw_data['condition']}."
                }
            }

        # Fallback generic response
        return {
            "finish_reason": "stop",
            "message": {
                "role": "assistant",
                "content": "I am an AI assistant. How can I help you?"
            }
        }


# ==============================================================================
# 5. THE AGENTIC ARCHITECTURE (THE CHATBOT ENGINE)
# ==============================================================================
class AgenticChatbot:
    def __init__(self):
        # THE CONTEXT WINDOW
        # This array is the mathematical brain of the AI. It stores the entire history!
        self.conversation_history: List[Dict[str, str]] = [
            {"role": "system", "content": "You are a helpful AI Agent with access to tools."}
        ]
        
        # A registry mapping tool names to actual Python function pointers!
        self.available_tools = {
            "get_current_weather": BackendTools.get_current_weather,
            "get_stock_price": BackendTools.get_stock_price
        }

    def chat(self, user_input: str):
        print(f"\n[USER]: {user_input}")
        
        # 1. We mathematically append the User's message to the History Array!
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # 2. We blast the ENTIRE array to the LLM (Context Injection)
        response = MockLLMAPI.chat_completion(self.conversation_history)
        message = response["message"]
        
        # 3. If the LLM just generated standard text, we print it and append it!
        if response["finish_reason"] == "stop":
            print(f"[AI AGENT]: {message['content']}")
            self.conversation_history.append(message)
            return
            
        # 4. IF THE LLM DEMANDED A TOOL CALL! (Agentic Execution)
        if response["finish_reason"] == "tool_calls":
            print("  [SYSTEM] The LLM has halted text generation and demanded a Tool Call!")
            
            # We MUST append the Assistant's empty tool-call request to the history
            self.conversation_history.append(message)
            
            # We iterate through the requested tools (LLMs can request multiple at once!)
            for tool_call in message["tool_calls"]:
                function_name = tool_call["function"]["name"]
                # We mathematically parse the JSON arguments the LLM generated!
                arguments = json.loads(tool_call["function"]["arguments"])
                
                # We execute the real Python function!
                function_pointer = self.available_tools.get(function_name)
                if function_pointer:
                    tool_result = function_pointer(**arguments)
                    
                    # We mathematically append the raw Python result BACK into the history!
                    self.conversation_history.append({
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "name": function_name,
                        "content": tool_result
                    })
                    
            # 5. RECURSIVE INJECTION
            # We blast the array back to the LLM AGAIN, now containing the Python Data!
            print("  [SYSTEM] Injecting Python data back into the LLM Context Window...")
            final_response = MockLLMAPI.chat_completion(self.conversation_history)
            
            final_message = final_response["message"]
            print(f"[AI AGENT]: {final_message['content']}")
            
            self.conversation_history.append(final_message)


# ==============================================================================
# 6. MATHEMATICAL PROOF (THE SIMULATION)
# ==============================================================================
def demonstrate_agent():
    section_header("Project: Agentic AI Chatbot with Tool Calling")
    
    agent = AgenticChatbot()
    
    # Test 1: Tool Calling
    agent.chat("What is the weather in Tokyo right now?")
    
    # Test 2: Context Memory
    agent.chat("What did I just ask you?")


def run_all_labs():
    demonstrate_agent()


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why must we append the entire Conversation History array to every single API call? Why can't the API just remember our conversation automatically?"
   Senior Answer: "Stateless REST Architecture. The OpenAI and Anthropic APIs are mathematically 'Stateless'. When you send an HTTP POST request to their servers, their GPUs process the tokens, generate the response, and instantly annihilate all memory of your connection to free up RAM for the next user. They do not store a session cookie for you. Therefore, to simulate a continuous conversation, the Python client must mathematically maintain the entire array locally, and re-transmit the entire $2,000$-token history in every single API call, allowing the LLM to read the past and generate the present."

2. Interviewer: "What is the architectural difference between a Standard LLM Prompt and 'Tool Calling' (Function Calling)?"
   Senior Answer: "Structured JSON Constraints. In a standard prompt, the LLM outputs a raw, unstructured string of text. If you ask it to return a JSON object, it might hallucinate Markdown backticks or conversational filler ('Here is your JSON...'). With strict Tool Calling, the LLM is mathematically forced at the API level to halt standard generation and output a flawlessly structured, validated JSON object that perfectly matches a predefined JSON Schema. This guarantees that the Python Backend can safely execute `json.loads()` on the output without the application crashing due to parsing errors."

3. Interviewer: "When the Python backend finishes executing `get_current_weather`, why must we append the result using the `"role": "tool"` tag, and why must we include the `tool_call_id`?"
   Senior Answer: "Token Alignment and Hallucination Prevention. If the LLM generates a tool call with ID `call_abc123`, it mathematically expects the very next message in the Context Window to provide the exact answer to that specific ID. If we just append the weather data as a `"role": "user"` message, the LLM's architecture breaks. It doesn't realize the tool call was fulfilled, and it may aggressively hallucinate or enter an infinite loop of requesting the tool again. By strictly using the `"role": "tool"` tag and perfectly matching the `tool_call_id`, we satisfy the API's mathematical state machine, proving to the LLM that its request was successfully executed by the host."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Capstone Project (GenAI Chatbot) Completed.")

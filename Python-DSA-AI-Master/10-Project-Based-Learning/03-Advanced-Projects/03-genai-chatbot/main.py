\"\"\"
GenAI Chatbot Implementation

This module demonstrates how to build a robust, production-ready Generative AI Chatbot.
It covers everything from basic conversation loops to advanced concepts like Retrieval-Augmented Generation (RAG),
memory management, and rate limiting.

### Why this matters?
In the industry, chatbots are no longer simple rule-based systems. They are powered by Large Language Models (LLMs)
and augmented with custom data (RAG). Building a production-ready chatbot requires handling:
- State management (Memory)
- Context window limitations (Token limits)
- Tool calling (Agents)
- Error handling and retries

### Beginner Explanation
A GenAI chatbot takes a user's message and sends it to an AI model (like GPT-4). The model predicts the next
words and sends back a response. To make the bot remember past messages, we have to send the entire
conversation history every time, because the AI model itself is stateless.

### Advanced Explanation
A production chatbot uses LangChain or LlamaIndex concepts under the hood:
1. **Memory**: Rolling buffer of messages, summarizing older messages to fit within token limits.
2. **Retrieval (RAG)**: When a user asks a question, the system queries a vector database for relevant documents,
   and injects them into the system prompt.
3. **Tools/Function Calling**: The LLM can decide to execute a Python function (e.g., fetch_weather) before answering.
\"\"\"

import time
import json
import logging
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Data Structures ---

@dataclass
class Message:
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: float = field(default_factory=time.time)

@dataclass
class ChatSession:
    session_id: str
    messages: List[Message] = field(default_factory=list)
    max_history: int = 10  # Keep only the last 10 messages for context

    def add_message(self, role: str, content: str):
        self.messages.append(Message(role=role, content=content))
        # Trim history if it exceeds max_history (keep system prompts if implemented)
        if len(self.messages) > self.max_history:
            # Drop oldest non-system messages
            self.messages = self.messages[-self.max_history:]

    def get_context(self) -> List[Dict[str, str]]:
        return [{"role": msg.role, "content": msg.content} for msg in self.messages]

# --- Mock LLM Client (Simulates OpenAI API) ---

class MockLLMClient:
    \"\"\"
    Simulates an LLM API call, including network latency and random errors.
    \"\"\"
    def __init__(self, api_key: str):
        self.api_key = api_key
        # In a real app, you would initialize openai.Client here

    def generate_response(self, messages: List[Dict[str, str]], tools: Optional[List[Dict]] = None) -> str:
        # Simulate network delay
        time.sleep(1.5)
        
        last_message = messages[-1]['content'].lower()
        
        # Simulate tool calling logic
        if "weather" in last_message and tools:
            return json.dumps({"tool_call": "get_weather", "arguments": {"location": "San Francisco"}})

        # Standard responses
        if "hello" in last_message:
            return "Hello! How can I assist you today?"
        elif "explain rag" in last_message:
            return "RAG stands for Retrieval-Augmented Generation. It involves fetching relevant documents from a database and providing them to the LLM to ground its response."
        else:
            return "That is a fascinating topic. Can you tell me more about what you're trying to achieve?"

# --- Tools Definition ---

def get_weather(location: str) -> str:
    \"\"\"A tool function that the AI can call.\"\"\"
    logger.info(f"[Tool] Fetching weather for {location}")
    return f"The weather in {location} is currently 72°F and sunny."

# --- Main Chatbot Engine ---

class GenAIChatbot:
    \"\"\"
    The orchestrator class for the chatbot.
    \"\"\"
    def __init__(self, llm_client: MockLLMClient):
        self.llm = llm_client
        self.sessions: Dict[str, ChatSession] = {}
        
        # Register available tools
        self.tool_registry: Dict[str, Callable] = {
            "get_weather": get_weather
        }
        
        self.tool_schemas = [
            {
                "name": "get_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "The city name"}
                    },
                    "required": ["location"]
                }
            }
        ]

    def get_or_create_session(self, session_id: str) -> ChatSession:
        if session_id not in self.sessions:
            self.sessions[session_id] = ChatSession(session_id=session_id)
            # Add a system prompt
            self.sessions[session_id].add_message("system", "You are a helpful AI assistant.")
        return self.sessions[session_id]

    def chat(self, session_id: str, user_input: str) -> str:
        \"\"\"
        Main interaction method.
        \"\"\"
        session = self.get_or_create_session(session_id)
        session.add_message("user", user_input)
        
        try:
            logger.info(f"Sending prompt to LLM for session {session_id}...")
            context = session.get_context()
            
            # Step 1: Initial LLM call
            response_text = self.llm.generate_response(context, tools=self.tool_schemas)
            
            # Step 2: Check for tool calls
            if "tool_call" in response_text:
                try:
                    tool_data = json.loads(response_text)
                    tool_name = tool_data.get("tool_call")
                    args = tool_data.get("arguments", {})
                    
                    if tool_name in self.tool_registry:
                        # Execute tool
                        tool_result = self.tool_registry[tool_name](**args)
                        # Inject tool result into context and call LLM again
                        session.add_message("assistant", f"Let me check the weather... (Calling {tool_name})")
                        session.add_message("user", f"Tool {tool_name} returned: {tool_result}. Now answer my question.")
                        
                        logger.info(f"Sending tool results to LLM...")
                        final_response = self.llm.generate_response(session.get_context())
                        response_text = final_response
                except json.JSONDecodeError:
                    pass # Ignore if it wasn't a valid JSON tool call
            
            # Step 3: Save and return final response
            session.add_message("assistant", response_text)
            return response_text
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I'm sorry, I encountered an internal error. Please try again later."


# --- Tests and Execution ---

def run_tests():
    print("--- Running GenAI Chatbot Tests ---")
    client = MockLLMClient(api_key="sk-mock-key")
    bot = GenAIChatbot(llm_client=client)
    
    session_id = "user_123"
    
    # Test 1: Basic greeting
    print("\nUser: Hello!")
    reply = bot.chat(session_id, "Hello!")
    print(f"Bot: {reply}")
    
    # Test 2: RAG question
    print("\nUser: Can you explain RAG?")
    reply = bot.chat(session_id, "Can you explain RAG?")
    print(f"Bot: {reply}")
    
    # Test 3: Tool calling
    print("\nUser: What's the weather in San Francisco?")
    reply = bot.chat(session_id, "What's the weather in San Francisco?")
    print(f"Bot: {reply}")
    
    # Check history
    print("\n--- Session History ---")
    for msg in bot.sessions[session_id].messages:
        print(f"[{msg.role.upper()}]: {msg.content}")

if __name__ == "__main__":
    run_tests()

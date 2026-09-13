"""
# ==============================================================================
# LABORATORY: LLM ORCHESTRATION (LANGCHAIN BASICS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Hugging Face and OpenAI provide APIs to generate text. But building a real 
# AI application (like a Chatbot or an Autonomous Agent) requires massive 
# orchestration.
#
# - How do you inject user variables into complex Prompt Templates?
# - How do you force the LLM to output perfect JSON, and then parse that JSON?
# - LLMs have amnesia. How do you append previous chat history to every new 
#   API call so the model remembers the conversation?
#
# LangChain is the industry standard framework for orchestrating LLMs. It 
# abstracts Prompts, LLMs, Output Parsers, and Memory into modular blocks 
# that you can chain together using the LCEL (LangChain Expression Language).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand PromptTemplates and OutputParsers.
# - Build pipelines using LangChain Expression Language (LCEL).
# - Implement Conversation Memory to solve LLM amnesia.
#
# ==============================================================================
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# In a real environment: pip install langchain langchain-openai
try:
    from langchain.prompts import PromptTemplate, ChatPromptTemplate
    from langchain.schema import StrOutputParser
    # For demonstration, we will use a Fake LLM to avoid needing API keys!
    from langchain_community.llms.fake import FakeListLLM
    from langchain.memory import ConversationBufferMemory
    HAS_LANGCHAIN = True
except ImportError:
    HAS_LANGCHAIN = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. PROMPT TEMPLATES & LLM INTEGRATION
# ==============================================================================
def demonstrate_lcel_chain():
    section_header("LangChain Expression Language (LCEL)")
    
    if not HAS_LANGCHAIN:
        print("[WARNING] LangChain not installed.")
        return
        
    print("In LangChain, we construct a 'Chain' using the Pipe (|) operator.")
    print("Chain = PromptTemplate -> LLM -> OutputParser\n")
    
    try:
        # 1. PROMPT TEMPLATE
        # We define a template with a variable {topic}
        prompt = PromptTemplate.from_template("Tell me a 1 sentence joke about {topic}.")
        
        # 2. THE LLM
        # In reality, this would be `ChatOpenAI(temperature=0.7)` or `HuggingFaceHub()`.
        # We use a Fake LLM that just returns a hardcoded list of responses.
        fake_llm = FakeListLLM(responses=["Why did the robot cross the road? To get to the data center!"])
        
        # 3. OUTPUT PARSER
        # Extracts just the raw string from the complex LLM response object.
        parser = StrOutputParser()
        
        # 4. CONSTRUCT THE CHAIN (LCEL)
        # This pipes the output of the Prompt directly into the LLM, and the 
        # output of the LLM directly into the Parser!
        chain = prompt | fake_llm | parser
        
        # 5. EXECUTE THE CHAIN
        print("Invoking the Chain with topic='Artificial Intelligence'...")
        result = chain.invoke({"topic": "Artificial Intelligence"})
        
        print(f"\nLLM Output: {result}")
        
    except Exception as e:
        print(f"Execution skipped: {e}")


# ==============================================================================
# 4. SOLVING AMNESIA WITH MEMORY
# ==============================================================================
def demonstrate_memory():
    section_header("Conversation Memory (Solving Amnesia)")
    
    if not HAS_LANGCHAIN: return
    
    print("APIs are Stateless. If you say 'My name is John', and then make a ")
    print("second API call asking 'What is my name?', the LLM will fail.")
    print("LangChain Memory objects automatically intercept API calls, append the ")
    print("chat history to the Prompt, and save the LLM's response for next time!\n")
    
    try:
        # Initialize an empty buffer
        memory = ConversationBufferMemory(return_messages=True)
        
        print("User : 'Hello, my name is John.'")
        print("AI   : 'Nice to meet you, John.'")
        
        # We manually save the interaction to the memory buffer
        memory.save_context(
            {"input": "Hello, my name is John."}, 
            {"output": "Nice to meet you, John."}
        )
        
        print("\nUser : 'What is my favorite color? It is Blue.'")
        print("AI   : 'I will remember that your favorite color is Blue.'")
        
        memory.save_context(
            {"input": "What is my favorite color? It is Blue."}, 
            {"output": "I will remember that your favorite color is Blue."}
        )
        
        # Let's inspect what LangChain has constructed in the background!
        print("\n--- Current Raw Memory Buffer ---")
        variables = memory.load_memory_variables({})
        
        for msg in variables['history']:
            print(f"[{msg.type.upper()}]: {msg.content}")
            
        print("\nLangChain will automatically dynamically inject this entire ")
        print("buffer into the `ChatPromptTemplate` on the next API call, ")
        print("giving the illusion that the LLM 'Remembers' you!")
        
    except Exception as e:
        print(f"Execution skipped: {e}")


def run_all_labs():
    demonstrate_lcel_chain()
    demonstrate_memory()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the LangChain Expression Language (LCEL) and why do we use the Pipe (`|`) operator?
   Answer: LCEL is a declarative way to compose LangChain components. Instead of writing heavy, nested boilerplate code to pass variables from a Prompt to an LLM, and then writing a separate function to parse the LLM's output, LCEL uses the Linux-style pipe operator (`|`). The syntax `chain = prompt | model | output_parser` mathematically chains the `__call__` or `.invoke()` methods of each object. When you call `chain.invoke()`, the dictionary is injected into the Prompt, the resulting string is routed to the Model, and the Model's raw JSON response is routed to the Parser, creating a perfectly streamlined execution pipeline.

2. How does `ConversationBufferMemory` solve LLM Amnesia, and what is its fatal flaw?
   Answer: LLM APIs (like OpenAI's endpoint) are completely stateless; they retain absolutely zero memory of your previous API calls. `ConversationBufferMemory` acts as a local Python array that intercepts and stores every single User Prompt and AI Response. On the next turn, it silently concatenates the entire array into a massive string and prepends it to your new prompt. 
   **The Fatal Flaw:** The Context Window limit. If you chat for 3 hours, the memory buffer might grow to 20,000 tokens. Eventually, the buffer will exceed the LLM's hard context limit (e.g., 4096 tokens), causing a catastrophic crash, or it will cost you massive amounts of money because you are re-sending the entire 20,000-token history on every single API call.

3. How do you solve the fatal flaw of `ConversationBufferMemory`?
   Answer: You use advanced memory structures:
   - `ConversationSummaryMemory`: Instead of keeping the exact chat history, it uses the LLM in the background to continuously summarize the conversation into a dense, 200-word paragraph.
   - `ConversationBufferWindowMemory`: It acts as a queue (FIFO), keeping only the last $K$ interactions (e.g., the last 5 messages) and ruthlessly deleting older messages.
   - Vector Databases: You store every message as a mathematical Vector. When the user asks a question, you query the database for the 3 most semantically relevant past messages and inject ONLY those into the context window.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: LangChain Basics Completed.")

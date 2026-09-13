import json

# Note: In a real scenario, this script would make API calls to OpenAI, Anthropic, Gemini, etc.
# Here we simulate the LLM's response to demonstrate the *structure* of prompt engineering code.

def simulated_llm_call(prompt: str) -> str:
    """
    A mock function that simulates an LLM response based on the prompt content.
    """
    prompt_lower = prompt.lower()
    
    if "let's think step by step" in prompt_lower or "reasoning" in prompt_lower:
        return "Step 1: I need to analyze the input.\nStep 2: I apply the logic requested.\nConclusion: The result is 42."
    
    if "json" in prompt_lower and "schema" in prompt_lower:
        # Simulate returning a structured JSON string
        return '{\n  "name": "Alice",\n  "age": 30,\n  "profession": "Software Engineer"\n}'
    
    if "example:" in prompt_lower:
        # Simulate Few-Shot pattern matching
        return "Positive"
        
    return "This is a generic response to a zero-shot prompt."

def demo_zero_shot():
    print("--- Zero-Shot Prompting ---")
    prompt = "Translate 'Hello' to French."
    response = simulated_llm_call(prompt)
    print(f"Prompt:\n{prompt}\n")
    print(f"Response:\n{response}\n")

def demo_few_shot():
    print("--- Few-Shot Prompting ---")
    prompt = """Classify the text into Neutral, Negative, or Positive.
Text: I think the vacation is okay.
Sentiment: Neutral
Text: I do not like this product.
Sentiment: Negative
Text: This is the best day of my life!
Sentiment: """
    response = simulated_llm_call(prompt)
    print(f"Prompt:\n{prompt}\n")
    print(f"Response:\n{response}\n")

def demo_chain_of_thought():
    print("--- Chain-of-Thought (CoT) Prompting ---")
    prompt = """Solve the following math problem. Let's think step by step.
Problem: If a train travels at 60 mph for 2 hours, and then 80 mph for 1 hour, what is the total distance traveled?"""
    response = simulated_llm_call(prompt)
    print(f"Prompt:\n{prompt}\n")
    print(f"Response:\n{response}\n")

def demo_structured_output():
    print("--- Structured Output Prompting ---")
    prompt = """Extract the entities from the following text and return ONLY valid JSON matching this schema:
{
    "name": "string",
    "age": "integer",
    "profession": "string"
}

Text: Alice is a 30-year-old Software Engineer living in New York.
JSON Output:"""
    response = simulated_llm_call(prompt)
    print(f"Prompt:\n{prompt}\n")
    print(f"Response:\n{response}")
    
    # Demonstrate parsing the JSON
    try:
        parsed_data = json.loads(response)
        print("\nParsed Python Dictionary:")
        print(f"Name: {parsed_data.get('name')}, Age: {parsed_data.get('age')}")
    except json.JSONDecodeError:
        print("Failed to parse JSON.")
    print()

if __name__ == "__main__":
    print("Executing Prompt Engineering Demonstrations...\n")
    demo_zero_shot()
    demo_few_shot()
    demo_chain_of_thought()
    demo_structured_output()

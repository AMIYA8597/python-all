"""
# ==============================================================================
# LABORATORY: GENERATIVE AI (PROMPT ENGINEERING & REASONING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer prompts an LLM: "Solve 24 * 13." The model instantly 
# generates "302" and is mathematically wrong. The developer assumes the model 
# is stupid.
#
# A senior AI engineer understands "Chain of Thought" (CoT) and "In-Context 
# Learning". They know that LLMs cannot "pause and think" before generating a 
# token. If the very next token must be the final answer, the model guesses. 
# The engineer structures the prompt: "Solve 24 * 13. Let's think step by step." 
# This forces the model to generate intermediate tokens: "24 * 10 = 240. 
# 24 * 3 = 72. 240 + 72 = 312." By forcing the model to write its scratchpad 
# into the Context Window, the final attention matrix perfectly calculates 312.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Few-Shot Prompting Templates.
# - Execute Chain-of-Thought (CoT) Reasoning constraints.
# - Architect ReAct (Reasoning and Acting) Agentic loops.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (IN-CONTEXT LEARNING)
# ==============================================================================
class PromptSimulator:
    
    @staticmethod
    def construct_few_shot_prompt(user_input: str) -> str:
        """
        [SECURE] Few-Shot Prompting.
        LLMs are highly sensitive to pattern matching. By injecting 2-3 perfectly 
        formatted examples directly into the prompt (In-Context), we "program" 
        the LLM's attention mechanism to strictly mimic the exact output format 
        without changing any underlying weights.
        """
        print("  [INIT] Constructing Few-Shot Classification Prompt...")
        
        system_instruction = "You are a precise Sentiment Analysis API. Output exactly one word: POSITIVE, NEGATIVE, or NEUTRAL."
        
        # The "Shots" (Examples)
        shot_1 = "Input: I absolutely loved the cinematography in this film.\nOutput: POSITIVE"
        shot_2 = "Input: The food was completely raw and the service was terrible.\nOutput: NEGATIVE"
        shot_3 = "Input: The package arrived on Tuesday as scheduled.\nOutput: NEUTRAL"
        
        # The Actual Target
        target = f"Input: {user_input}\nOutput:"
        
        # Assemble the massive prompt
        final_prompt = f"{system_instruction}\n\n{shot_1}\n\n{shot_2}\n\n{shot_3}\n\n{target}"
        return final_prompt

    @staticmethod
    def construct_chain_of_thought_prompt(math_problem: str) -> str:
        """
        [SECURE] Chain of Thought (CoT).
        Forces the model to expand its compute. Every token generated is another 
        forward pass through the GPU. "Thinking step by step" literally gives the 
        model more GPU cycles to solve the problem!
        """
        print("\n  [INIT] Constructing Chain of Thought (CoT) Prompt...")
        
        prompt = (
            "You are a mathematical reasoning engine.\n"
            f"Question: {math_problem}\n\n"
            "Answer: Let's break this down step-by-step to ensure we arrive at the correct calculation.\n"
            "Step 1:"
        )
        return prompt


# ==============================================================================
# 4. THE ARCHITECTURAL PATTERN: ReAct (REASONING & ACTING)
# ==============================================================================
class ReActAgentSimulator:
    
    @staticmethod
    def simulate_react_loop():
        """
        [SECURE] ReAct (Reason + Act).
        This is how "Agentic AI" works. The LLM is trapped in a `while` loop. 
        It is forced to output a "Thought", then an "Action" (a function call), 
        then it waits for the Python environment to output an "Observation".
        """
        print("\n  [INIT] Simulating ReAct Agentic Loop...")
        
        system_prompt = """
        You run in a loop of THOUGHT, ACTION, OBSERVATION.
        Available Actions:
        - search_wikipedia(query: str)
        - calculate(expression: str)
        """
        print("  [SYSTEM PROMPT]")
        print(system_prompt)
        
        print("  [USER] Who is the current CEO of Microsoft, and what is their age multiplied by 2?")
        
        print("\n  [LLM GENERATION 1]")
        print("  Thought: I need to find out who the CEO of Microsoft is.")
        print("  Action: search_wikipedia('CEO of Microsoft')")
        
        print("\n  [PYTHON EXECUTION]")
        print("  -> Python intercepts the text, parses the function call, and hits the Wikipedia API.")
        print("  Observation: Satya Nadella is the CEO of Microsoft. He was born in 1967 (Age 57).")
        
        print("\n  [LLM GENERATION 2]")
        print("  Thought: The CEO is Satya Nadella and his age is 57. I need to multiply this by 2.")
        print("  Action: calculate('57 * 2')")
        
        print("\n  [PYTHON EXECUTION]")
        print("  -> Python executes `eval('57 * 2')`.")
        print("  Observation: 114")
        
        print("\n  [LLM GENERATION 3]")
        print("  Thought: I have the final answer.")
        print("  Final Answer: The CEO of Microsoft is Satya Nadella, and his age multiplied by 2 is 114.")
        
        print("\n  [FLAWLESS] The LLM successfully compensated for its inability to natively do math ")
        print("  or access real-time data by acting as a 'Reasoning Engine' that delegates tasks ")
        print("  to external tools via the ReAct prompt structure.")


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_prompt_engineering():
    section_header("Generative AI: Prompt Engineering Architectures")
    
    sim = PromptSimulator()
    
    # 1. Few-Shot
    few_shot = sim.construct_few_shot_prompt("I guess the movie was okay, not great but not terrible.")
    print("  -> Assembled Few-Shot Prompt:\n")
    print("-" * 40)
    print(few_shot)
    print("-" * 40)
    
    # 2. Chain of Thought
    cot = sim.construct_chain_of_thought_prompt("If John has 5 apples, eats 2, buys 10 more, and gives half to Mary, how many does he have?")
    print("\n  -> Assembled CoT Prompt:\n")
    print("-" * 40)
    print(cot)
    print("-" * 40)
    
    # 3. ReAct
    agent = ReActAgentSimulator()
    agent.simulate_react_loop()


def run_all_labs():
    demonstrate_prompt_engineering()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why does adding 'Let's think step by step' physically improve the mathematical accuracy of an LLM?"
   Senior Answer: "Compute Expansion. An LLM's architecture dictates that generating exactly ONE token requires exactly ONE forward pass through the Neural Network. If you ask a complex math problem and force the model to instantly output the final answer in token 1, it only has ONE forward pass of computational power to solve it. It fails. By prompting 'Let's think step by step', you force the model to generate $50$ tokens of intermediate 'scratchpad' reasoning. This physically grants the model $50$ consecutive forward passes through the GPU. As it generates the scratchpad, those intermediate numbers are fed back into its Context Window via the Autoregressive Loop, allowing the Self-Attention mechanism to mathematically refer back to its own intermediate calculations when predicting the final answer."

2. Interviewer: "What is 'In-Context Learning' (Few-Shot Prompting), and how does it differ from Fine-Tuning?"
   Senior Answer: "Temporary vs Permanent Weight Modification. Fine-tuning permanently modifies the actual billions of physical floating-point weights inside the model by running Backpropagation Calculus on a dataset. In-Context Learning (Few-Shot) changes zero weights. Instead, by injecting 5 examples of an input/output pair into the Prompt, you manipulate the $Q \\cdot K^T$ Self-Attention matrix. The Query vector of the new input heavily 'attends' to the patterns established by the Key/Value vectors of the examples currently sitting in the Context Window. As soon as the session ends and the Context Window is cleared, the model instantly forgets the task. In-Context learning exploits the transient activation states of the network."

3. Interviewer: "In a ReAct (Reasoning and Acting) architecture, what is the most critical failure point?"
   Senior Answer: "The Parsing Boundary. ReAct relies on the LLM generating a perfectly formatted string (e.g., `Action: search_wikipedia('query')`) so that standard Python regex or JSON parsers can intercept it, halt the LLM generation, run the tool, and append the Observation. If the LLM hallucinates the format (e.g., `Action: I will now search wikipedia for 'query'`), the Python script crashes, the loop breaks, and the Agent fails. This is why modern Agentic frameworks (like OpenAI Function Calling) fine-tune the models specifically to output strict JSON schemas, bridging the gap between probabilistic text generation and deterministic software execution."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Generative AI (Prompt Engineering) Completed.")

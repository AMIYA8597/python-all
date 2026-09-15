"""
# ==============================================================================
# LABORATORY: AGENTIC AI (WORKFLOWS VS AGENTS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer builds a tool to summarize stock reports. They write a 
# linear Python script: 1. Download PDF -> 2. Extract Text -> 3. Send to LLM 
# for summary -> 4. Email result. This is a "Workflow". If the PDF download fails, 
# the script instantly crashes. It cannot recover.
#
# A senior AI engineer builds an "Agent". They give the LLM tools: `search_web`, 
# `read_pdf`, `send_email`. They give it a goal: "Email me a summary of Apple's 
# Q3 earnings." The Agent autonomously decides to search the web for the PDF. 
# The first link is broken (404 Error). Instead of crashing, the Agent observes 
# the error, reasons that it should try a different link, searches again, finds 
# the data, summarizes it, and emails it. The Agent controls its own execution flow.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the limitations of Deterministic Workflows (Chains).
# - Architect an Autonomous Agentic Loop (ReAct).
# - Execute dynamic error recovery via LLM reasoning.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (WORKFLOW VS AGENT)
# ==============================================================================
class LLMSimulator:
    """Simulates LLM responses for the sake of the Laboratory."""
    @staticmethod
    def prompt(text: str) -> str:
        # Hardcoded simulation responses
        if "Extract text from: None" in text:
            return "ERROR: No text provided to summarize."
        return "Apple reported $81 Billion in Revenue for Q3."


class WorkflowSimulator:
    
    def __init__(self):
        self.llm = LLMSimulator()
        
    def run_workflow(self, url: str):
        """
        [SECURE] A Deterministic Chain.
        If Step 1 fails, Step 2 is doomed. There is zero reasoning.
        """
        print("  [INIT] Executing Deterministic Workflow...")
        
        # STEP 1: Scrape
        print(f"  -> Step 1: Scraping {url}...")
        scraped_text = None
        if url == "broken_link.com":
            print("     [ERROR] 404 Not Found. Scraper returned None.")
            scraped_text = None
        else:
            scraped_text = "Apple Q3 Revenue: 81 Billion."
            
        # STEP 2: Summarize
        print("  -> Step 2: Sending to LLM for summarization...")
        llm_input = f"Extract text from: {scraped_text}"
        summary = self.llm.prompt(llm_input)
        
        print(f"  [FINAL OUTPUT] {summary}")


class AgentSimulator:
    
    def __init__(self):
        self.max_loops = 5
        self.current_loop = 0
        
    def run_agent(self, goal: str):
        """
        [SECURE] An Autonomous Agentic Loop.
        The Agent encounters an error, observes the error, and dynamically 
        chooses a new action to recover.
        """
        print(f"\n  [INIT] Spawning Agent with Goal: '{goal}'")
        
        while self.current_loop < self.max_loops:
            self.current_loop += 1
            print(f"\n  [LOOP {self.current_loop}]")
            
            # Simulated LLM Reasoning Engine
            if self.current_loop == 1:
                thought = "I need to find the Q3 earnings. I will try the first link I know."
                action = "scrape('broken_link.com')"
                print(f"  -> Thought: {thought}")
                print(f"  -> Action:  {action}")
                
                # The execution of the action fails!
                observation = "ERROR 404: Page not found."
                print(f"  -> Observation: {observation}")
                
            elif self.current_loop == 2:
                # The Agent sees the ERROR in its context window and ADAPTS.
                thought = "The first link was broken. I cannot summarize a 404 error. I must search for an alternative source."
                action = "search_google('Apple Q3 Earnings PDF')"
                print(f"  -> Thought: {thought}")
                print(f"  -> Action:  {action}")
                
                observation = "Found link: valid_source.com/q3"
                print(f"  -> Observation: {observation}")
                
            elif self.current_loop == 3:
                thought = "I found a valid link. I will scrape it now."
                action = "scrape('valid_source.com/q3')"
                print(f"  -> Thought: {thought}")
                print(f"  -> Action:  {action}")
                
                observation = "Text: Apple Q3 Revenue: 81 Billion."
                print(f"  -> Observation: {observation}")
                
            elif self.current_loop == 4:
                thought = "I have the required text. I will generate the final summary."
                action = "summarize_and_finish()"
                print(f"  -> Thought: {thought}")
                print(f"  -> Action:  {action}")
                print("\n  [FINAL OUTPUT] Apple reported $81 Billion in Revenue for Q3.")
                break


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_architecture():
    section_header("Agentic AI: Workflows vs Agents")
    
    print("\n[SCENARIO] Fetching a document from a broken URL.\n")
    
    # 1. The Workflow Fails
    workflow = WorkflowSimulator()
    workflow.run_workflow(url="broken_link.com")
    
    print("\n" + "-"*60)
    
    # 2. The Agent Recovers
    agent = AgentSimulator()
    agent.run_agent(goal="Get Apple Q3 earnings and summarize.")
    
    print("\n  [FLAWLESS] The Workflow blindly executed Step 2 even though Step 1 failed, ")
    print("  resulting in a catastrophic crash. The Agent mathematically analyzed the ")
    print("  404 error during its loop, dynamically altered its execution graph, and ")
    print("  successfully recovered.")


def run_all_labs():
    demonstrate_architecture()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the architectural distinction between a 'Chain' (e.g., LangChain SequentialChain) and an 'Agent'?"
   Senior Answer: "Control Flow Ownership. In a Chain (Workflow), the human developer hardcodes the control flow using Python logic (e.g., `A() -> B() -> C()`). The LLM is merely a passive text-processing node within that pipeline. If a variable is missing, the Python code crashes. In an Agent, the LLM *owns* the control flow. The human provides a `while True:` loop and a suite of Tools. The LLM acts as the central CPU, dynamically deciding which tool to call, in what order, based on the real-time Observations it receives. An Agent writes its own execution graph at runtime."

2. Interviewer: "Why are Agents inherently more expensive and slower to run in production than Workflows?"
   Senior Answer: "The Autoregressive Feedback Loop. A Workflow might only invoke the LLM once at the very end to summarize data ($1$ API call). An Agent must invoke the LLM at every single node of its decision tree. To search, read, and summarize, an Agent might loop $5$ times. Each loop requires sending the *entire accumulated context* (Thoughts, Actions, Observations) back to the LLM. Because the LLM must mathematically re-evaluate the entire context history from scratch to generate the next action, the token usage and latency scale exponentially compared to a deterministic workflow."

3. Interviewer: "What is the mathematical risk of 'Infinite Loops' in Agentic architectures, and how do we mitigate it?"
   Senior Answer: "Hallucinated Feedback Cycles. An Agent might execute `search('data')`, receive `Error: not found`, and then hallucinate that it should try `search('data')` again, infinitely burning API credits. We mitigate this using two architectural constraints: 1. A hardcoded `max_iterations` counter that breaks the `while` loop regardless of LLM output. 2. A 'System Prompt Injection' that forces the Agent to review its past actions. If it detects consecutive identical failures, it is mathematically penalized (prompted) to change its strategy or execute a forced 'Yield/Ask Human' action."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Agentic AI (Workflows vs Agents) Completed.")

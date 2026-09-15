"""
# ==============================================================================
# LABORATORY: AGENTIC AI (MULTI-AGENT SUPERVISOR ARCHITECTURE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer tries to solve a massive software engineering task with a 
# single Agent. The Agent tries to search the web, write the code, review the 
# code, run tests, and deploy. The single Context Window becomes polluted with 
# overlapping responsibilities, the LLM hallucinates, and the system fails.
#
# A senior AI engineer uses a "Multi-Agent Topology". They spawn a "Supervisor 
# Agent" whose only job is Routing. The Supervisor analyzes the user's prompt 
# and routes it to specialized sub-agents. It sends the coding task to a "Coder 
# Agent" (with a specialized system prompt). The Coder writes the code and sends 
# it back. The Supervisor then routes it to a "Reviewer Agent". By isolating 
# responsibilities into separate, pristine Context Windows, the system achieves 
# unprecedented reliability and scales infinitely.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Supervisor / Worker topological pattern.
# - Execute message passing between isolated Agent nodes.
# - Architect Multi-Agent Debate and verification loops.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (MULTI-AGENT TOPOLOGY)
# ==============================================================================
class LLMSimulator:
    """Simulates API responses for different specialized Agents."""
    
    @staticmethod
    def prompt_supervisor(task: str) -> str:
        print("     [LLM: SUPERVISOR] Analyzing task and determining the correct routing...")
        if "code" in task.lower() or "python" in task.lower():
            return "ROUTE_TO: CODER"
        elif "verify" in task.lower() or "review" in task.lower():
            return "ROUTE_TO: REVIEWER"
        return "ROUTE_TO: FINAL_OUTPUT"

    @staticmethod
    def prompt_coder(task: str) -> str:
        print("     [LLM: CODER] Writing the Python code...")
        return "def calculate_sum(a, b):\n    return a + b"

    @staticmethod
    def prompt_reviewer(code: str) -> str:
        print("     [LLM: REVIEWER] Analyzing the code for security and syntax...")
        return "VERIFIED: The code `calculate_sum` is mathematically sound and secure."


class SupervisorArchitecture:
    
    def __init__(self):
        self.llm = LLMSimulator()
        self.memory_bus = [] # A shared message bus between agents
        
    def execute_multi_agent_workflow(self, user_request: str):
        """
        [SECURE] The Multi-Agent Orchestration Loop.
        The Supervisor is the absolute authority on control flow.
        """
        print(f"  [INIT] Multi-Agent Swarm activated for request: '{user_request}'")
        self.memory_bus.append(f"USER: {user_request}")
        
        # Step 1: Supervisor analyzes the initial request
        print("\n  [NODE: SUPERVISOR]")
        routing_decision = self.llm.prompt_supervisor(user_request)
        print(f"  -> Supervisor Decision: {routing_decision}")
        
        # Step 2: Handoff to the Coder
        if "CODER" in routing_decision:
            print("\n  [NODE: CODER]")
            # The Coder has its own isolated prompt and context window!
            code_output = self.llm.prompt_coder(user_request)
            print("  -> Coder generated the payload.")
            self.memory_bus.append(f"CODER_OUTPUT: {code_output}")
            
            # Step 3: Supervisor intercepts the Coder's output and re-evaluates
            print("\n  [NODE: SUPERVISOR]")
            print("  -> Supervisor intercepting code payload. Routing for Verification...")
            verification_decision = self.llm.prompt_supervisor("Review this code: " + code_output)
            print(f"  -> Supervisor Decision: {verification_decision}")
            
            # Step 4: Handoff to the Reviewer
            if "REVIEWER" in verification_decision:
                print("\n  [NODE: REVIEWER]")
                review_output = self.llm.prompt_reviewer(code_output)
                print(f"  -> Reviewer Output: {review_output}")
                self.memory_bus.append(f"REVIEWER_OUTPUT: {review_output}")
                
        print("\n  [FINAL AGENTIC OUTPUT]")
        print("  -> The code was successfully written by the Coder Agent and ")
        print("  independently verified by the Reviewer Agent, orchestrated by ")
        print("  the Supervisor. The pristine Context Windows prevented hallucination.")


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_supervisor_architecture():
    section_header("Agentic AI: Multi-Agent Supervisor Pattern")
    
    swarm = SupervisorArchitecture()
    swarm.execute_multi_agent_workflow(user_request="Write a python function to add two numbers.")


def run_all_labs():
    demonstrate_supervisor_architecture()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why is a Multi-Agent architecture physically superior to a single 'God Agent' for complex enterprise tasks?"
   Senior Answer: "Context Window Purity and System Prompt Specificity. A single Agent attempting to scrape the web, write SQL, and review Python code requires a massive, convoluted System Prompt defining the rules for all three tasks. As the Context Window fills with web HTML and raw SQL, the Attention Mechanism gets mathematically diluted. It loses focus on the Python rules and begins to hallucinate. In a Multi-Agent topology, the 'SQL Agent' has a pristine Context Window containing ONLY database schemas and strict SQL System Prompts. The Attention Mechanism ($Q \\cdot K^T$) is mathematically focused $100\\%$ on SQL, yielding near-perfect accuracy before handing the isolated payload back to the Supervisor."

2. Interviewer: "Explain the 'Multi-Agent Debate' pattern and how it mathematically improves final output accuracy."
   Senior Answer: "Adversarial Verification. If you ask a single LLM a complex logic puzzle, it will probabilistically generate an answer and commit to it, even if it's wrong (due to autoregressive momentum). In a Debate pattern, you spawn three isolated Agents. Agent A and Agent B are independently prompted to solve the puzzle. Agent C is the 'Judge'. Agent A and B submit their answers to C. If they differ, C generates a critique and mathematically forces A and B to read each other's reasoning and update their answers. Because the models are exposed to alternative logic paths in their Context Window, they probabilistically self-correct, dramatically increasing the final mathematical accuracy of the system."

3. Interviewer: "What is the primary failure mode of a 'Hierarchical Supervisor' architecture, and how do decentralized topologies (like Swarm) solve it?"
   Senior Answer: "The Orchestrator Bottleneck. If the Supervisor LLM hallucinates the routing logic (e.g., routing a Python task to the SQL Agent), the entire tree collapses. The Supervisor is a single point of mathematical failure. In a fully decentralized 'Swarm' or 'Graph' topology, there is no central Supervisor. Agents pass messages directly to each other peer-to-peer. The Coder Agent autonomously realizes it needs SQL data and directly pings the SQL Agent. This reduces the token load on a central node and prevents single-point failure, but vastly increases the complexity of managing infinite loops and state."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Agentic AI (Supervisor Architecture) Completed.")

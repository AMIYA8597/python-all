"""
Educational Example: Supervisor Multi-Agent Architecture

This script simulates a Supervisor agent that delegates tasks
to specialized worker agents based on the request.
"""

class WorkerAgent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        
    def execute_task(self, task: str) -> str:
        print(f"[{self.name} - {self.role}] Executing task: '{task}'...")
        # Simulated task execution
        if "research" in self.role.lower():
            return "Found relevant information on the topic."
        elif "code" in self.role.lower():
            return "def hello_world():\n    print('Hello')\n"
        return "Task completed."

class SupervisorAgent:
    def __init__(self):
        self.workers = {
            "Researcher": WorkerAgent("Alice", "Researcher"),
            "Coder": WorkerAgent("Bob", "Python Coder")
        }
        
    def manage_request(self, request: str):
        print("--- Supervisor Agent Processing Request ---")
        print(f"Original Request: {request}\n")
        
        # Simulated Supervisor Logic
        print("[Supervisor] Analyzing request to delegate tasks...")
        
        # 1. Delegate Research
        research_task = f"Research concepts for: {request}"
        print(f"[Supervisor] Delegating to Alice: {research_task}")
        research_result = self.workers["Researcher"].execute_task(research_task)
        print(f"[Supervisor] Received from Alice: {research_result}\n")
        
        # 2. Delegate Coding
        coding_task = f"Write code based on research: {research_result}"
        print(f"[Supervisor] Delegating to Bob: {coding_task}")
        code_result = self.workers["Coder"].execute_task(coding_task)
        print(f"[Supervisor] Received from Bob:\n{code_result}\n")
        
        # 3. Final Output
        print("[Supervisor] Synthesizing final response...")
        print("Task finished successfully. All workers reported back.")

if __name__ == "__main__":
    supervisor = SupervisorAgent()
    supervisor.manage_request("Find out how to write a Python function and write one.")

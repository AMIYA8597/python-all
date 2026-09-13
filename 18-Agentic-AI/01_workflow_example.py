\"\"\"
Agentic AI: Workflow Example

This module demonstrates a professional-grade implementation of a basic Agentic AI workflow.
It illustrates how an agent can be constructed to receive a task, plan a sequence of actions,
execute those actions using available tools, and synthesize a final response.

Use Cases:
- Customer support bots that need to look up order details and process refunds.
- Data analysis assistants that can query databases, run statistical models, and generate reports.
- DevOps automation agents that can monitor system health, diagnose issues, and apply patches.

Concepts Covered:
1. Agent State Management
2. Task Planning
3. Tool Execution
4. Observation Integration
5. Final Synthesis

Advanced Concepts:
- Type hinting for robust interfaces
- Modular tool registry
- Basic retry mechanism for tool failures
\"\"\"

import logging
import time
from typing import Any, Callable, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Models ---

class Tool(BaseModel):
    \"\"\"Represents a tool that the agent can use.\"\"\"
    name: str = Field(..., description=\"The name of the tool.\")
    description: str = Field(..., description=\"A description of what the tool does.\")
    func: Callable[..., Any] = Field(..., description=\"The python function to execute.\")

class Action(BaseModel):
    \"\"\"Represents an action chosen by the agent.\"\"\"
    tool_name: str
    tool_input: Dict[str, Any]

class Observation(BaseModel):
    \"\"\"Represents the result of executing a tool.\"\"\"
    action: Action
    result: Any
    error: Optional[str] = None

class AgentState(BaseModel):
    \"\"\"Tracks the state of the agent's current task.\"\"\"
    task: str
    plan: List[str] = []
    observations: List[Observation] = []
    is_complete: bool = False
    final_answer: Optional[str] = None

# --- Mock Tools ---

def search_database(query: str) -> str:
    \"\"\"Simulates searching a database for information.\"\"\"
    logger.info(f\"Executing tool 'search_database' with query: {query}\")
    time.sleep(1) # Simulate network latency
    mock_db = {
        \"order_123\": \"Status: Shipped, Date: 2026-09-10\",
        \"user_bob\": \"Email: bob@example.com, Plan: Premium\"
    }
    return mock_db.get(query, \"No results found.\")

def calculate_refund(amount: float, days_since_purchase: int) -> str:
    \"\"\"Simulates calculating a refund amount based on policy.\"\"\"
    logger.info(f\"Executing tool 'calculate_refund' with amount={amount}, days={days_since_purchase}\")
    if days_since_purchase <= 30:
        return f\"Full refund approved: ${amount}\"
    elif days_since_purchase <= 60:
        return f\"Partial refund (50%) approved: ${amount / 2}\"
    else:
        return \"Refund denied: Past 60 days.\"

# --- Agent Implementation ---

class SimpleAgent:
    \"\"\"A simple agent that plans, executes, and synthesizes.\"\"\"
    
    def __init__(self, tools: List[Tool]):
        self.tools = {tool.name: tool for tool in tools}
        
    def _create_plan(self, task: str) -> List[str]:
        \"\"\"
        Simulates the LLM planning phase. In a real scenario, an LLM
        would analyze the task and generate these steps based on available tools.
        \"\"\"
        logger.info(\"Phase 1: Planning\")
        # Mock planning logic for demonstration
        if \"order_123\" in task:
            return [
                \"Step 1: Search database for order_123\",
                \"Step 2: Synthesize findings\"
            ]
        elif \"refund\" in task:
            return [
                \"Step 1: Calculate refund for $100, 15 days ago\",
                \"Step 2: Synthesize findings\"
            ]
        else:
            return [\"Step 1: Acknowledge unknown task\"]

    def _decide_next_action(self, state: AgentState) -> Optional[Action]:
        \"\"\"
        Simulates the LLM deciding which tool to call next based on the plan and past observations.
        \"\"\"
        logger.info(\"Phase 2: Deciding Next Action\")
        
        # Mock decision logic
        if len(state.observations) == 0:
            if \"order_123\" in state.task:
                return Action(tool_name=\"search_database\", tool_input={\"query\": \"order_123\"})
            elif \"refund\" in state.task:
                 return Action(tool_name=\"calculate_refund\", tool_input={\"amount\": 100.0, \"days_since_purchase\": 15})
        return None # No more actions needed

    def _execute_action(self, action: Action, max_retries: int = 3) -> Observation:
        \"\"\"Executes a chosen action using the tool registry with retries.\"\"\"
        logger.info(f\"Phase 3: Executing Action - {action.tool_name}\")
        tool = self.tools.get(action.tool_name)
        
        if not tool:
            return Observation(action=action, result=None, error=f\"Tool '{action.tool_name}' not found.\")

        for attempt in range(max_retries):
            try:
                # Unpack dictionary as kwargs for the function
                result = tool.func(**action.tool_input)
                return Observation(action=action, result=result)
            except Exception as e:
                logger.warning(f\"Tool execution failed (Attempt {attempt + 1}/{max_retries}): {e}\")
                time.sleep(1) # wait before retry
                
        return Observation(action=action, result=None, error=\"Max retries exceeded.\")

    def _synthesize(self, state: AgentState) -> str:
        \"\"\"Simulates the LLM generating a final response based on all observations.\"\"\"
        logger.info(\"Phase 4: Synthesis\")
        
        if not state.observations:
            return \"I could not find any information to help with your task.\"
            
        summary = \"Here is what I found based on your request:\\n\"
        for obs in state.observations:
            if obs.error:
                summary += f\"- Encountered an error with {obs.action.tool_name}: {obs.error}\\n\"
            else:
                summary += f\"- Result from {obs.action.tool_name}: {obs.result}\\n\"
                
        return summary

    def run(self, task: str) -> str:
        \"\"\"The main execution loop (the 'workflow') of the agent.\"\"\"
        logger.info(f\"Starting task: {task}\")
        state = AgentState(task=task)
        
        # 1. Plan
        state.plan = self._create_plan(task)
        
        # 2. ReAct Loop (Reason & Act)
        while not state.is_complete:
            # Reason: Decide next action
            action = self._decide_next_action(state)
            
            if not action:
                # No more actions to take, exit loop
                logger.info(\"No further actions required. Proceeding to synthesis.\")
                state.is_complete = True
                break
                
            # Act: Execute tool
            observation = self._execute_action(action)
            state.observations.append(observation)
            
            # Safe-guard to prevent infinite loops in this simple mock
            if len(state.observations) >= 3:
                logger.warning(\"Max iterations reached. Force completing.\")
                state.is_complete = True
                break

        # 3. Synthesize
        state.final_answer = self._synthesize(state)
        return state.final_answer


# --- Tests & Execution ---

def test_workflow():
    \"\"\"Runs tests to demonstrate the agent workflow.\"\"\"
    
    # Register available tools
    tools = [
        Tool(
            name=\"search_database\", 
            description=\"Searches the database for a given query.\", 
            func=search_database
        ),
        Tool(
            name=\"calculate_refund\", 
            description=\"Calculates refund amount based on rules.\", 
            func=calculate_refund
        )
    ]
    
    agent = SimpleAgent(tools=tools)
    
    # Test Scenario 1: Order Lookup
    print(\"\\n--- Test Scenario 1: Order Lookup ---\")
    task1 = \"Check the status of order_123.\"
    result1 = agent.run(task1)
    print(f\"\\nFinal Output:\\n{result1}\")
    assert \"Shipped\" in result1, \"Failed to retrieve order status.\"
    
    # Test Scenario 2: Refund Calculation
    print(\"\\n--- Test Scenario 2: Refund Calculation ---\")
    task2 = \"Process a refund for $100 purchased 15 days ago.\"
    result2 = agent.run(task2)
    print(f\"\\nFinal Output:\\n{result2}\")
    assert \"Full refund approved\" in result2, \"Failed to calculate refund correctly.\"
    
    print(\"\\nAll tests passed successfully.\")

if __name__ == \"__main__\":
    test_workflow()

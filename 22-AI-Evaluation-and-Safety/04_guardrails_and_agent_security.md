# 04 - Guardrails and Agent Security

## Prerequisites
- Knowledge of AI Safety fundamentals.
- Understanding of AI Agents (LLMs with tool-use capabilities).

## Objectives
- Learn how to implement input and output guardrails.
- Understand the security implications of autonomous AI agents.
- Explore strategies for securing agentic workflows.

## Intuition / Theory

### AI Guardrails
Guardrails are programmable constraints placed around an LLM to ensure it behaves within defined ethical, safety, and operational boundaries.
- **Input Guardrails:** Intercept the user's prompt before it reaches the LLM. Checks for prompt injection, toxicity, PII, and out-of-domain topics.
- **Output Guardrails:** Intercept the LLM's response before it reaches the user. Checks for hallucinations, toxic language, formatting errors, or leaked sensitive data.
*Frameworks:* NeMo Guardrails, Llama Guard.

### Agent Security
AI Agents can use tools (e.g., APIs, databases, shell execution). This significantly expands the attack surface.
- **Confused Deputy Problem:** An agent might be tricked by a malicious user (via prompt injection) into using its permissions to delete a database or send a phishing email.
- **Over-privileged Agents:** Giving an agent more permissions than it needs (violating the Principle of Least Privilege).

*Mitigations:*
- **Human-in-the-loop (HITL):** Require explicit user approval for destructive or high-stakes actions.
- **Sandboxing:** Run agent code execution in isolated, low-privilege environments.
- **Strict API Scopes:** Limit the tools and API scopes the agent can access.

## Code Examples

### Basic Output Guardrail implementation
```python
def check_output_toxicity(output_text):
    """
    A mock function to represent an external toxicity classifier (e.g., Perspective API).
    """
    toxic_keywords = ["hate", "kill", "destroy"]
    if any(word in output_text.lower() for word in toxic_keywords):
        return True
    return False

def generate_safe_response(llm_output):
    if check_output_toxicity(llm_output):
        return "I'm sorry, I cannot fulfill this request as it violates safety guidelines."
    return llm_output

# Mock LLM outputs
output1 = "I will help you learn Python."
output2 = "I will destroy this program."

print(generate_safe_response(output1))
print(generate_safe_response(output2))
```

## Interview Questions
1. **What is the "Confused Deputy Problem" in the context of AI Agents?**
   *Answer:* It happens when a malicious user or indirect prompt injection tricks an AI agent into misusing the privileges granted to it by the system developer (e.g., executing a malicious SQL query using the agent's database access).
2. **What is the difference between an input guardrail and an output guardrail?**
   *Answer:* Input guardrails analyze the user prompt to block malicious requests or PII *before* generating. Output guardrails analyze the LLM's response to block hallucinations, formatting errors, or policy violations *before* showing it to the user.
3. **How does 'Human-in-the-loop' enhance agent security?**
   *Answer:* It ensures that autonomous agents cannot execute critical or irreversible actions (like making payments or dropping tables) without explicit human review and authorization, serving as a failsafe against injection attacks or logic errors.

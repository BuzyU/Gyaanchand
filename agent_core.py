# agent_core.py
# Core logic to handle prompts and route them to tools or LLM

from api.llm_api import query_llm
from tools.simulator import run_simulation
from tools.test_generator import generate_tests
from tools.code_executor import execute_code
  # example tools (optional)

def route_task(prompt: str) -> str:
    """
    Simple keyword-based routing logic. Later upgrade to NLP classifier or intent detection.
    """
    lower_prompt = prompt.lower()

    if "simulate" in lower_prompt:
        return simulate.run(prompt)  # assume simulate.py defines `run()`
    elif "test" in lower_prompt:
        return generate_tests.create(prompt)
    elif "code" in lower_prompt or "program" in lower_prompt:
        return code_executor.run(prompt)
    else:
        return None  # fallback to LLM

def handle_query(prompt: str) -> str:
    """
    Handles user query by routing to tool or defaulting to LLM.
    """
    try:
        result = route_task(prompt)
        if result:
            return result
        else:
            return query_llm(prompt)
    except Exception as e:
        return f"⚠️ Error while processing your request: {e}"

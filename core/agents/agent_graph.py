from agents.client import generate_text
from .memory import query_vectors

def planner(state):
    prompt = f"Break this goal into steps:\n{state['input']}"
    state["plan"] = generate_text(prompt)
    return state

def worker(state):
    # Query memory
    context = "\n".join(query_vectors(state["input"]))
    prompt = f"Plan:\n{state['plan']}\nContext:\n{context}"
    state["result"] = generate_text(prompt)
    return state

def evaluator(state):
    prompt = (
        f"Evaluate if this answer satisfies the task. Task: {state['input']}\n"
        f"Result: {state['result']}\n"
        "Return PASS or FAIL with a confidence score."
    )
    state["evaluation"] = generate_text(prompt)
    return state

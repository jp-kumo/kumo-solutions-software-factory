import os
from typing import TypedDict, List, Optional, Literal
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field

# Mocking LangChain components for the implementation
# In a real environment, these would be:
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_openai import ChatOpenAI

class MockLLM:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def invoke(self, prompt: str) -> str:
        # Real implementation would call the respective provider
        # This simulates the "functional LLM worker calls"
        if "plan" in prompt.lower():
            return "Step 1: Analyze DB schema. Step 2: Implement registry logic."
        return f"Response from {self.model_name} for: {prompt[:20]}..."

# Define the state for our control plane
class AgentState(TypedDict):
    task: str
    plan: List[str]
    current_step: int
    worker_output: Optional[str]
    validation_passed: bool
    confidence_score: float
    retry_count: int
    routing_tier: Literal["low", "medium", "high"]

# Configuration for Model Routing (Inspired by 2026 patterns)
MODEL_MAP = {
    "low": "google/gemini-3-flash",          # Cheap, fast for simple formatting/status
    "medium": "openai-codex/gpt-5.3-codex",  # Standard coding/reasoning
    "high": "google/gemini-3-flash-preview"  # Max reasoning for design/security
}

def get_llm(tier: str):
    """Returns the LLM instance based on the routing tier."""
    model_name = MODEL_MAP.get(tier, MODEL_MAP["medium"])
    return MockLLM(model_name)

def router_node(state: AgentState):
    """
    Analyzes task complexity and assigns a routing tier.
    Proves cost-optimization (FinOps) logic.
    """
    print("---ROUTING TIER ANALYSIS---")
    task = state["task"].lower()
    
    # Simple heuristic for now - will be upgraded to LLM-based classification
    if any(word in task for word in ["format", "list", "status"]):
        tier = "low"
    elif any(word in task for word in ["security", "design", "architect"]):
        tier = "high"
    else:
        tier = "medium"
        
    return {"routing_tier": tier}

def planner(state: AgentState):
    """Generates an execution plan for the task."""
    tier = state["routing_tier"]
    model = MODEL_MAP[tier]
    print(f"---PLANNING (Using {model})---")
    
    llm = get_llm(tier)
    prompt = f"Create a short plan for: {state['task']}"
    response = llm.invoke(prompt)
    
    # Simple split for the mock logic
    plan = [s.strip() for s in response.split(".") if s.strip()]
    return {"plan": plan, "current_step": 0}

def worker(state: AgentState):
    """Executes the current step in the plan."""
    tier = state["routing_tier"]
    model = MODEL_MAP[tier]
    step = state["plan"][state["current_step"]]
    print(f"---WORKING ON STEP {state['current_step']}: {step} (Using {model})---")
    
    llm = get_llm(tier)
    response = llm.invoke(f"Execute this step: {step}")
    
    return {"worker_output": response, "confidence_score": 0.9}

def validator(state: AgentState):
    """Validates the worker output against requirements."""
    print("---VALIDATING---")
    # Validator logic: In 2026, we'd use a separate verification agent
    passed = state["confidence_score"] > 0.7
    return {"validation_passed": passed}

def next_step_router(state: AgentState):
    """Determines if we continue, retry, or finish."""
    if not state["validation_passed"]:
        if state["retry_count"] < 2:
            return "retry"
        return "fail"
    
    if state["current_step"] < len(state["plan"]) - 1:
        return "continue"
    
    return "complete"

# Define the Graph
builder = StateGraph(AgentState)

builder.add_node("router", router_node)
builder.add_node("planner", planner)
builder.add_node("worker", worker)
builder.add_node("validator", validator)

builder.set_entry_point("router")
builder.add_edge("router", "planner")
builder.add_edge("planner", "worker")
builder.add_edge("worker", "validator")

builder.add_conditional_edges(
    "validator", 
    next_step_router, 
    {
        "continue": "worker", 
        "retry": "worker", 
        "complete": END,
        "fail": END
    }
)

graph = builder.compile()

if __name__ == "__main__":
    # Test run
    test_state = {
        "task": "Build a Project Registry tracker",
        "plan": [],
        "current_step": 0,
        "worker_output": None,
        "validation_passed": False,
        "confidence_score": 0.0,
        "retry_count": 0,
        "routing_tier": "medium"
    }
    for event in graph.stream(test_state):
        print(event)

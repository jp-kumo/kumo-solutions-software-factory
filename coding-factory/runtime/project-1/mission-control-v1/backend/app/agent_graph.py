from typing import TypedDict, List, Optional, Literal
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field

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
    print(f"---PLANNING (Using {MODEL_MAP[state['routing_tier']]})---")
    # In a real impl, this would call the LLM assigned to the tier
    return {"plan": ["step1", "step2"], "current_step": 0}

def worker(state: AgentState):
    """Executes the current step in the plan."""
    print(f"---WORKING ON STEP {state['current_step']} (Using {MODEL_MAP[state['routing_tier']]})---")
    # Worker logic simulation
    return {"worker_output": f"Execution of {state['plan'][state['current_step']]} successful", "confidence_score": 0.85}

def validator(state: AgentState):
    """Validates the worker output against requirements."""
    print("---VALIDATING---")
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

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
from .agent_graph import graph, AgentState

app = FastAPI(title="Kumo Solutions Mission Control API")

# Simple in-memory trace store for portfolio evidence
traces = {}

class TaskRequest(BaseModel):
    task: str

class TaskResponse(BaseModel):
    run_id: str
    status: str
    tier: str
    output: Optional[str]
    steps_completed: int

@app.get("/health")
async def health_check():
    return {"status": "online", "version": "1.1.0"}

@app.post("/agent/run", response_model=TaskResponse)
async def run_agent_task(request: TaskRequest):
    try:
        run_id = str(uuid.uuid4())
        
        # Initialize state
        initial_state: AgentState = {
            "task": request.task,
            "plan": [],
            "current_step": 0,
            "worker_output": None,
            "validation_passed": False,
            "confidence_score": 0.0,
            "retry_count": 0,
            "routing_tier": "medium" 
        }
        
        # Execute the LangGraph
        # In production, we'd use .astream or a background task, but for v1 .invoke works
        result = graph.invoke(initial_state)
        
        # Capture trace
        traces[run_id] = result
        
        return TaskResponse(
            run_id=run_id,
            status="completed" if result.get("validation_passed") else "failed",
            tier=result.get("routing_tier"),
            output=result.get("worker_output"),
            steps_completed=result.get("current_step", 0) + 1
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agent/traces/{run_id}")
async def get_trace(run_id: str):
    if run_id not in traces:
        raise HTTPException(status_code=404, detail="Run not found")
    return traces[run_id]

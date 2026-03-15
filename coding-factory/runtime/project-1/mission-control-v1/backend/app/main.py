from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from .agent_graph import graph

app = FastAPI(title="Kumo Solutions Mission Control API")

class TaskRequest(BaseModel):
    task: str

class TaskResponse(BaseModel):
    status: str
    output: Optional[str]
    steps_completed: int

@app.get("/health")
async def health_check():
    return {"status": "online", "version": "1.0.0"}

@app.post("/agent/run", response_model=TaskResponse)
async def run_agent_task(request: TaskRequest):
    try:
        # Initialize state for the graph
        initial_state = {
            "task": request.task,
            "plan": [],
            "current_step": 0,
            "worker_output": None,
            "validation_passed": False,
            "confidence_score": 0.0,
            "retry_count": 0
        }
        
        # Execute the LangGraph
        result = graph.invoke(initial_state)
        
        return TaskResponse(
            status="completed" if result.get("validation_passed") else "failed",
            output=result.get("worker_output"),
            steps_completed=result.get("current_step", 0) + 1
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

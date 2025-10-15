from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from app.agent import run_sql_agent_stream
import json
from fastapi.responses import StreamingResponse
from app.auth import get_current_user
from time import sleep
app = FastAPI(title="SQL Agent API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/health")
async def check_health():
    sleep(10)
    return {"status": "I am alive"}
    

@app.get("/")
async def root():
    return {"message": "Hello i am SQL Agent API server"}

@app.get("/ask/stream")
async def ask_sql_agent_stream(
    query: str = Query(...),
    delay_ms: int = Query(30, ge=0, le=1000, description="Delay per token in milliseconds"),
    current_user: dict = Depends(get_current_user),
):
    """
    Stream SQL agent responses incrementally.
    Returns a streaming text/event-stream format.
    """

    async def event_generator():
        delay_seconds = (delay_ms or 0) / 1000.0
        async for chunk in run_sql_agent_stream(query, typing_delay=delay_seconds):
            yield f"data: {json.dumps(chunk)}\n\n"

    
    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

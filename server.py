from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from rq_client import queue
from chat import chat_with_model
app = FastAPI(

    title="My FastAPI Service",
    version="1.0.0",
    description="Example FastAPI app with Swagger UI",
    docs_url="/docs",          # Swagger UI
)


class ChatRequest(BaseModel):
    message: str


class ChatAsyncRespone(BaseModel):
    job_id: str

class ChatSyncRespone(BaseModel):
    answer: str

@app.post("/chat/sync", response_model=ChatSyncRespone)
async def chat(request:ChatRequest):
    answer = chat_with_model(request.message)
    return {"answer": answer}


@app.post("/chat/async", response_model=ChatAsyncRespone)
async def chat(request:ChatRequest):
    job = queue.enqueue(chat_with_model, request.message)
    return {"job_id": job.id}

@app.get("/chat/jobs/{job_id}")
async def get_chat_answer(job_id: str):
    job = queue.fetch_job(job_id=job_id)
    return {"answer": job.return_value()}


if __name__ == "__main__":
    uvicorn.run("server:app", port=5000, log_level="info")
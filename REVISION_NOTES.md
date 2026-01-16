# Project Revision Notes

## Project Overview
**Name:** Python Async PDF Chat  
**Type:** FastAPI-based asynchronous chat service with Redis Queue background processing  
**Purpose:** REST API for AI chat interactions with sync/async processing patterns

---

## Architecture Pattern

**Flow:**
1. User calls API with query
2. Query enqueued in Redis (async) or processed immediately (sync)
3. RQ worker picks up job and processes via OpenAI
4. Result stored in Redis with job_id as key
5. User retrieves result using job_id

---

## Tech Stack

- **FastAPI** - Web framework with auto Swagger docs
- **Redis** - Message broker & result storage
- **RQ (Redis Queue)** - Background job processing
- **LangChain** - AI framework for chat
- **OpenAI** - GPT-5 model & text-embedding-3-large (1024 dims)
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

---

## API Endpoints

### 1. POST `/chat/sync`
- **Purpose:** Immediate synchronous response
- **Request:** `{"message": "query"}`
- **Response:** `{"answer": "AI response"}`

### 2. POST `/chat/async`
- **Purpose:** Submit for background processing
- **Request:** `{"message": "query"}`
- **Response:** `{"job_id": "unique-id"}`

### 3. GET `/chat/jobs/{job_id}`
- **Purpose:** Retrieve async job result
- **Response:** `{"answer": "AI response"}`

---

## Key Files

### `server.py`
- FastAPI app setup (port 5000)
- Route definitions for sync/async chat
- Pydantic models: ChatRequest, ChatAsyncRespone, ChatSyncRespone
- Swagger UI at `/docs`

### `chat.py`
- OpenAI integration (GPT-5 model)
- Embeddings: text-embedding-3-large (1024 dimensions)
- `chat_with_model(message)` - core chat function
- System prompt with context support (currently empty)

### `rq_client.py`
- Redis connection (localhost:6379)
- RQ Queue initialization

### `.env`
- Contains OPENAI_API_KEY (keep secure!)

### `pyproject.toml`
- Python 3.14+ required
- Dependencies: fastapi, langchain, redis, rq, openai, qdrant-client

---

## Setup Commands

```bash
# Install dependencies
uv sync

# Start Redis
redis-server

# Start FastAPI server
python server.py

# Start RQ worker (separate terminal)
rq worker
```

---

## Important Notes

- **Port:** Server runs on 5000
- **Redis:** localhost:6379
- **Model:** GPT-5 (OpenAI)
- **Embeddings:** text-embedding-3-large with 1024 dimensions
- **Context:** Currently empty string in chat.py (can be enhanced with RAG)
- **Swagger UI:** http://localhost:5000/docs

---

## Potential Enhancements

- Add PDF processing (project name suggests this feature)
- Implement vector store (Qdrant client already in dependencies)
- Add context retrieval using embeddings
- Error handling for failed jobs
- Job status endpoint
- Authentication/rate limiting

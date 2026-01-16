# Python Async PDF Chat

A FastAPI-based asynchronous chat service with RAG (Retrieval-Augmented Generation) capabilities. The system processes PDF documents, stores them in a vector database, and uses Redis Queue (RQ) for background job processing to provide intelligent, context-aware responses powered by OpenAI.

## Overview

This project provides a REST API for chat interactions with AI models that can answer questions based on PDF document content. It uses RAG to retrieve relevant context from indexed PDFs and supports both synchronous and asynchronous processing patterns. The async mode uses Redis and RQ workers to handle chat requests in the background, making it suitable for handling longer-running AI operations without blocking the API.

## Features

- **RAG (Retrieval-Augmented Generation)**: Answer questions based on PDF document content
- **PDF Processing**: Automatically load, chunk, and index PDF documents
- **Vector Search**: Uses Qdrant vector database for semantic similarity search
- **Synchronous Chat API**: Get immediate responses from the AI model
- **Asynchronous Chat API**: Submit queries and retrieve results later via job ID
- **Redis Queue Integration**: Background job processing with RQ workers
- **OpenAI Integration**: Uses GPT-5 for chat responses and text-embedding-3-large for embeddings
- **FastAPI Framework**: Modern, fast API with automatic Swagger documentation

## Architecture

1. **PDF Indexing** (one-time setup):
   - PDF documents are loaded using PyPDFLoader
   - Documents are split into chunks (1000 chars with 400 char overlap)
   - Chunks are converted to embeddings using OpenAI's text-embedding-3-large
   - Embeddings are stored in Qdrant vector database

2. **Chat Processing**:
   - User sends a chat query to the API
   - Query is converted to embeddings and similar document chunks are retrieved from Qdrant
   - Retrieved context is passed to OpenAI GPT-5 along with the user query
   - Query gets enqueued in Redis (async mode) or processed immediately (sync mode)
   - RQ worker picks up the job and processes it using the RAG pipeline
   - Result is stored in Redis with the job ID as the key
   - User retrieves the result using the job ID

## API Endpoints

### POST `/chat/sync`
Send a message and get an immediate response.

**Request Body:**
```json
{
  "message": "Your question here"
}
```

**Response:**
```json
{
  "answer": "AI response"
}
```

### POST `/chat/async`
Submit a message for asynchronous processing.

**Request Body:**
```json
{
  "message": "Your question here"
}
```

**Response:**
```json
{
  "job_id": "unique-job-id"
}
```

### GET `/chat/jobs/{job_id}`
Retrieve the result of an asynchronous chat job.

**Response:**
```json
{
  "answer": "AI response"
}
```

## Setup

1. Install dependencies using `uv`:
```bash
uv sync
```

2. Configure environment variables in `.env`:
```
OPENAI_API_KEY=your_api_key_here
```

3. Start Qdrant vector database:
```bash
docker run -p 6333:6333 qdrant/qdrant
```

4. Start Redis server:
```bash
redis-server
```

5. Index your PDF documents (one-time setup):
```bash
python rag_index.py
```

6. Start the FastAPI server:
```bash
python server.py
```

7. Start the RQ worker (in a separate terminal):
```bash
rq worker
```

## API Documentation

Once the server is running, visit `http://localhost:5000/docs` for interactive Swagger UI documentation.

## Tech Stack

- **FastAPI**: Web framework
- **Redis**: Message broker and result storage
- **RQ (Redis Queue)**: Background job processing
- **Qdrant**: Vector database for semantic search
- **LangChain**: AI framework for RAG and chat interactions
- **OpenAI**: Language model provider (GPT-5 and text-embedding-3-large)
- **PyPDFLoader**: PDF document processing
- **Pydantic**: Data validation

## Key Components

### `rag_index.py`
Handles PDF document indexing:
- Loads PDF files using PyPDFLoader
- Splits documents into chunks (1000 chars, 400 overlap)
- Generates embeddings using OpenAI's text-embedding-3-large
- Stores vectors in Qdrant collection "learning_rag"

### `chat.py`
Core RAG chat functionality:
- Connects to Qdrant vector database
- Performs similarity search to retrieve relevant document chunks
- Passes retrieved context to GPT-5 for answer generation
- Returns context-aware responses

### `server.py`
FastAPI application:
- Defines sync and async chat endpoints
- Integrates with Redis Queue for background processing
- Provides Swagger UI documentation at `/docs`

### `rq_client.py`
Redis Queue configuration:
- Establishes Redis connection (localhost:6379)
- Initializes job queue for async processing

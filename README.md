# Python Async PDF Chat

A FastAPI-based asynchronous chat service that uses Redis Queue (RQ) for background job processing and integrates with OpenAI's language models for intelligent responses.

## Overview

This project provides a REST API for chat interactions with AI models, supporting both synchronous and asynchronous processing patterns. The async mode uses Redis and RQ workers to handle chat requests in the background, making it suitable for handling longer-running AI operations without blocking the API.

## Features

- **Synchronous Chat API**: Get immediate responses from the AI model
- **Asynchronous Chat API**: Submit queries and retrieve results later via job ID
- **Redis Queue Integration**: Background job processing with RQ workers
- **OpenAI Integration**: Uses GPT-5 for chat responses and text embeddings
- **FastAPI Framework**: Modern, fast API with automatic Swagger documentation

## Architecture

1. User sends a chat query to the API
2. Query gets enqueued in Redis (async mode) or processed immediately (sync mode)
3. RQ worker picks up the job and processes it using OpenAI's language model
4. Result is stored in Redis with the job ID as the key
5. User retrieves the result using the job ID

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

3. Start Redis server:
```bash
redis-server
```

4. Start the FastAPI server:
```bash
python server.py
```

5. Start the RQ worker (in a separate terminal):
```bash
rq worker
```

## API Documentation

Once the server is running, visit `http://localhost:5000/docs` for interactive Swagger UI documentation.

## Tech Stack

- **FastAPI**: Web framework
- **Redis**: Message broker and result storage
- **RQ (Redis Queue)**: Background job processing
- **LangChain**: AI framework for chat interactions
- **OpenAI**: Language model provider (GPT-5 and embeddings)
- **Pydantic**: Data validation

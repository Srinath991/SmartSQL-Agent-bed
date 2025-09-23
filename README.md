## SQL Agent (Streaming API)

A FastAPI service that exposes a streaming SQL Agent built with LangGraph/LangChain. Responses are streamed as Server‑Sent Events (SSE).

### Key Features
- **Streaming responses (SSE)**: incremental tokens as they are generated
- **SQL tools**: agent can reason and query a database using LangChain SQL toolkit


## Requirements
- Python 3.10+
- A Google Generative AI API key
- Supabase project with JWT secret for auth

## Environment Variables
Create a `.env` (or set variables in your environment):

```bash
GOOGLE_API_KEY=your_google_genai_api_key
SUPABASE_JWT_SECRET=your_supabase_jwt_secret
SUPABASE_DB_URL=${DATABASE_URL}
```

## Installation

```bash
uv sync
```
```bash
source .venv/bin/activate #for mac
```

## Running the API Server

```bash
fastapi run app/main.py --reload
```

### Docker

```bash
docker build -t sql-agent .
docker run --env-file .env -p 8000:8000 sql-agent
```

## API

### Stream Agent Response
- **Method**: GET
- **Path**: `/ask/stream`
- **Query params**:
  - `query` (string, required): user message/question
- **Response**: `text/event-stream` (SSE). Each event is emitted as a JSON object.





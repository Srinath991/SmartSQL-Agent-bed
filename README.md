## SQL Agent (Streaming API)

A FastAPI service that exposes a streaming SQL Agent built with LangGraph/LangChain. Responses are streamed as Server‑Sent Events (SSE) with an optional per‑token delay for smooth typing effects in the frontend.

### Key Features
- **Streaming responses (SSE)**: incremental tokens as they are generated
- **Configurable per‑token delay**: control typing smoothness via `delay_ms`
- **SQL tools**: agent can reason and query a database using LangChain SQL toolkit
- **CORS enabled** for browser clients

## Requirements
- Python 3.10+
- A Google Generative AI API key

## Environment Variables
Create a `.env` (or set variables in your environment):

```bash
GOOGLE_API_KEY=your_google_genai_api_key
DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/dbname
```

## Installation

```bash
pip install -r requirements.txt
```

## Running the API

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
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
  - `delay_ms` (int, optional, default `30`, range `0`–`1000`): per‑token delay in milliseconds
- **Response**: `text/event-stream` (SSE). Each event is emitted as a JSON object prefixed by `data:`.

#### Example

```bash
curl -N "http://localhost:8000/ask/stream?query=What%20are%20the%20top%205%20customers%20by%20revenue%3F&delay_ms=25"
```

#### Event payloads

```json
{"type":"token","content":"...","run_id":"..."}
{"type":"tool_start","tool":"sql_db_query","input":{...},"run_id":"..."}
{"type":"tool_end","tool":"sql_db_query","output":"...","run_id":"..."}
```

Notes:
- The `delay_ms` is applied only after `token` events for a smoother typing effect; tool events are not delayed.
- Set `delay_ms=0` to disable backend throttling entirely.

## Development

- Main app entry: `app/main.py`
- Agent streaming logic: `app/agent.py`
- LLM setup: `app/llm.py`
- Database wiring: `app/db.py`

### Lint/Test
Use your preferred tools. Example:

```bash
python -m pip install ruff pytest
ruff check .
pytest -q
```

## Security & Operational Notes
- Restrict `allow_origins` in production.
- Do not commit secrets. Use `.env` or a secret manager.
- Validate and sanitize queries before executing against production databases.



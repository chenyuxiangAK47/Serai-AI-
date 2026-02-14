# Serai Backend Test (FastAPI)

Minimal backend service to support the frontend demo.

## Requirements
- Python 3.10+

## Setup
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

## Run

```powershell
uvicorn app.main:app --reload
```

Open:

* [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Endpoints

### GET /health

Response:

```json
{"status":"ok","version":"0.1.0"}
```

### POST /generate

Request:

```json
{"brand":"Nike","event":"Launch","context":"Hello"}
```

Response (stub):

```json
{
  "summary":"stub summary",
  "risks":["stub risk 1","stub risk 2"],
  "recommendation":"stub recommendation"
}
```

Validation error example (missing `context`):

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "invalid request body",
    "request_id": "..."
  }
}
```

## Design Notes

* FastAPI + Pydantic schema validation
* In-memory TTL cache for `/generate`: key = SHA256(brand|event|context), max 1000 entries, 10 min TTL; avoids duplicate generation and reduces cost/latency.
* Clear layering:
  * `app/api` routes
  * `app/schemas` request/response models
  * `app/services` business logic (stub generator)
  * `app/core` configuration via environment variables
* Request ID middleware: `X-Request-Id` is generated/propagated and returned in responses
* Unified error response format

## Configuration

Environment variables (see `.env.example`):

* `GENERATOR_MODE`: `mock` | `llm`
* `LLM_API_KEY`: only required for `llm` mode (not hardcoded in code)

## If I had more time

* Add real LLM client with timeout/retry/circuit breaker
* Add caching (Redis or in-memory TTL cache) keyed by request hash
* Add rate limiting + request size limits
* Add basic tests (pytest) for happy path + validation errors
* Add simple RAG with pgvector (chunking/embedding/retrieval), plus evaluation (golden set, latency/cost)

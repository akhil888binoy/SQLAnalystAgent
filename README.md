# SQL Analyst Agent

A FastAPI service that answers natural-language questions about a PostgreSQL database. A LangGraph agent inspects the schema, writes read-only SQL, runs it, and replies in plain English.

## How it works

```
POST /api/analyst/  {"question": "..."}
        │
        ▼
   llm_call ──► tool_node ──► llm_call ──► ... ──► answer
                  │
                  ├─ get_schema   tables, columns, foreign keys (via SQLAlchemy inspector)
                  └─ execute_sql  validated SELECT-only queries (via sqlglot + SQLAlchemy)
```

The model loops between calling tools and reasoning until it produces a final answer. SQL errors are returned to the model as tool output so it can correct the query and retry.

Only a single `SELECT` statement is allowed per call. Anything else is rejected before it reaches the database.

## Setup

Requires Python 3.14+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Create a `.env` file:

```
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
OPENROUTER_API_KEY=sk-or-...
DEBUG=false
```

The LLM is configured in `src/llm/llm.py`. It uses OpenRouter through the OpenAI-compatible API, so any OpenRouter model with tool-calling support works.

## Run

```bash
uv run uvicorn main:app --reload
```

Then:

```bash
curl -X POST http://localhost:8000/api/analyst/ \
  -H "Content-Type: application/json" \
  -d '{"question": "How many customers are there?"}'
```

```json
{"answer": "There are **10 customers** in the database."}
```

Interactive docs are at `http://localhost:8000/docs`.

## Layout

```
main.py                  FastAPI app
src/routers/analyst.py   POST /api/analyst/
src/agent/               LangGraph state, graph, and routing
src/llm/llm.py           model config, system prompt, llm_call and tool_node
src/tools/schema.py      get_schema tool
src/tools/database.py    execute_sql tool
src/tools/sql_validator.py  sqlglot-based SELECT-only check
src/database/database.py    SQLAlchemy engine and session
```

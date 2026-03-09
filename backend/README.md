# Jobschatbot Backend

## Architecture

```text
Scraper -> Raw CSV -> Cleaning -> Clean CSV -> Embeddings -> FAISS Index -> Retrieval -> LLM -> API
```

## Setup

```bash
py -m pip install -r backend/requirements.txt
```

Optional semantic embeddings (heavier, needs more disk/RAM):

```bash
py -m pip install -r backend/requirements-optional.txt
```

## Pipeline

```bash
py backend/scripts/run_scraper.py
py backend/scripts/run_cleaning.py
py backend/scripts/run_rag_pipeline.py
```

## Run API

```bash
py -m uvicorn app.main:app --host 127.0.0.1 --port 8002 --reload
```

## API Endpoints

- `GET /` service message
- `GET /health` health check
- `POST /api/chat` body: `{"query": "engineering jobs in chennai"}`

## Environment Variables

- `LLM_PROVIDER` optional; `openai` (default) or `huggingface`
- `OPENAI_API_KEY` optional; required when `LLM_PROVIDER=openai`
- `OPENAI_MODEL` optional; default `gpt-4o-mini`
- `HF_API_TOKEN` optional; required when `LLM_PROVIDER=huggingface`
- `HF_MODEL` optional; default `mistralai/Mistral-7B-Instruct-v0.3`
- `EMBEDDING_MODEL` optional; default `sentence-transformers/all-MiniLM-L6-v2`

## Notes

- If `sentence-transformers` is not installed, embedding/query vectors fall back to deterministic hash vectors.
- If FAISS is unavailable or index is missing, retrieval falls back to keyword ranking.
- If LLM provider credentials are missing or provider errors occur, API falls back to retrieval-only response.

## Tests

```bash
py -m pytest backend/tests -q
```

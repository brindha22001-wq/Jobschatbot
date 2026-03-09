# Tamil Nadu Job and Career Guidance Chatbot

Full-stack internship project with scraping, preprocessing, RAG retrieval, LLM integration, and chatbot UI.

## Project Structure

- `backend/` FastAPI API + RAG pipeline + datasets + tests
- `frontend/` React + Vite chatbot UI

## End-to-End Workflow

```text
Web Scraping
  -> backend/data/raw/jobs_raw.csv
Data Cleaning
  -> backend/data/cleaned/jobs_cleaned.csv
Embedding Generation
  -> backend/data/vector_db/embeddings.npy
Vector DB Build (FAISS)
  -> backend/data/vector_db/faiss_index/index.faiss
RAG Retrieval
  -> relevant job contexts
LLM Generation (OpenAI or fallback)
  -> chatbot answer
Frontend UI (React)
  -> user conversation
```

## Run Backend

```bash
py -m pip install -r backend/requirements.txt
py backend/scripts/run_scraper.py
py backend/scripts/run_cleaning.py
py backend/scripts/run_rag_pipeline.py
py -m uvicorn app.main:app --host 127.0.0.1 --port 8002 --reload
```

## Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:5173`
Backend URL: `http://127.0.0.1:8002`

## Sample Queries

- `software developer jobs in chennai`
- `nurse jobs in madurai`
- `skills for data analyst`
- `good morning`

## Submission Checklist

- Dataset: raw + cleaned CSV files present
- Source code: backend + frontend folders present
- Chatbot app: running via Vite + FastAPI
- Testing: backend tests available in `backend/tests`
- Documentation: architecture + setup + workflow included

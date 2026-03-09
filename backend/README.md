# Jobschatbot Backend

## Run API

```bash
uvicorn app.main:app --reload --app-dir backend
```

## Run pipeline scripts

```bash
python backend/scripts/run_scraper.py
python backend/scripts/run_cleaning.py
python backend/scripts/run_rag_pipeline.py
```

## Run tests

```bash
pytest backend/tests
```

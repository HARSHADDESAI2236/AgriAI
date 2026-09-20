# Farm History Backend

FastAPI + asynchronous SQLAlchemy backend for keeping a farm's history (farms → fields → seasons → crops, with
activities, expenses and harvests), plus timeline, analytics, and an AI assistant that answers
questions about your records using retrieval-augmented generation (RAG).

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # then edit SECRET_KEY and OPENAI_API_KEY for AI answers
python -m app.seed.demo_data    # optional demo data: demo@farm.test / demo12345
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs for the interactive API docs.

### Docker (Postgres)

```bash
docker compose up --build
```

## Tests

```bash
pytest -q
```

## API overview

| Area | Endpoints |
|------|-----------|
| Auth | `POST /auth/register`, `POST /auth/login` (form: username=email), `GET /auth/me` |
| Farms | `POST/GET /farms`, `GET/PATCH/DELETE /farms/{id}` |
| Fields | `POST/GET /farms/{id}/fields`, `GET/PATCH/DELETE /fields/{id}` |
| Seasons | `POST/GET /farms/{id}/seasons`, `GET/PATCH/DELETE /seasons/{id}` |
| Crops | `POST /crops`, `GET /farms/{id}/crops?season_id=`, `GET/PATCH/DELETE /crops/{id}` |
| Activities | `POST/GET /crops/{id}/activities`, `PATCH/DELETE /activities/{id}` |
| Expenses | `POST/GET /farms/{id}/expenses?season_id=&crop_id=&category=`, `PATCH/DELETE /expenses/{id}` |
| Harvests | `POST/GET /crops/{id}/harvests`, `PATCH/DELETE /harvests/{id}` |
| Timeline | `GET /farms/{id}/timeline?season_id=&crop_id=&start=&end=` |
| Analytics | `GET /farms/{id}/analytics`, `/seasons/{id}/analytics`, `/crops/{id}/analytics` |
| AI | `POST /ai/ask`, `POST /ai/farms/{id}/reindex` |

All data endpoints require `Authorization: Bearer <token>` and are scoped to the logged-in user;
other users' records return 404.

## How the AI part works

1. `record_formatter` turns each crop, activity, expense and harvest into a sentence.
2. `retrieval_service.sync_farm_index` keeps a `record_chunks` table in sync (only new/changed
   records are re-embedded). It runs automatically before every question.
3. `embedding_service` uses a dependency-free hashed bag-of-words embedding so everything works
   offline. Swap `embed()` for a real embedding model for better semantic matching
   (keep the vector size fixed, then clear old chunks and reindex).
4. `context_service` builds a prompt from farm/season/crop totals plus the top-k retrieved records.
5. `llm_service` calls OpenAI (`LLM_MODEL`, default `gpt-4o-mini`) if `OPENAI_API_KEY` is set; otherwise `/ai/ask`
   falls back to returning the most relevant records (`llm_used: false`).

## Notes / next steps

- Tables are created asynchronously on startup with `create_all()`. Add Alembic before making schema changes in production.
- With many records per farm, move embeddings to `pgvector` instead of scoring in Python.
- Analytics: crop-linked expenses automatically inherit the crop's season; farm-level expenses can
  be tagged with a `season_id` to count toward that season's cost.
- Set `CURRENCY` in `.env` to change the label used in AI context text.

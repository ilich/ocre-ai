# OCRE AI — Backend

FastAPI backend for the OCRE AI project. Provides REST endpoints for authentication, coin catalog browsing with hybrid search, AI-powered chat, and user management.

## Tech stack

- **Python 3.13**, FastAPI, Uvicorn
- **Beanie** (async ODM) + **PyMongo** over MongoDB Atlas Local
- **pydantic-ai** for the AI agent and embeddings (OpenAI-compatible)
- **Argon2** password hashing, **PyJWT** authentication
- **Loguru** structured logging, **asgi-correlation-id** request tracing
- **Ruff** (format + lint), **mypy** (strict), **pytest** test suite

## Project structure

```
app/
  main.py            # FastAPI app, lifespan, middleware, router registration
  cli.py             # CLI commands: seed and embed-coins
  core/
    settings.py      # Pydantic Settings (reads .env / env vars)
    logging.py       # Loguru setup
  routes/
    auth.py          # /auth — register, login, password reset
    catalog.py       # /catalog — list, search, filter, image describe
    chat.py          # /chat — AI expert chat
    health.py        # /health
    user.py          # /user — profile, coin collection
  services/
    authentication.py  # JWT helpers, get_current_user dependency
    catalog.py         # Coin search (vector + full-text rank fusion), filters
    chat.py            # pydantic-ai agent with tools: describe_image, search_coins, rewrite_question
    vision.py          # OpenAI vision — coin image description
    email.py           # Transactional email via SMTP
    user_repository.py # User CRUD
  models/
    domain.py        # Beanie documents: Coin, User, Geographic, Metadata
    catalog.py       # API request/response models for catalog
    chat.py          # ChatRequest / ChatResponse models
    auth.py          # Auth request/response models
    user.py          # User profile models
    fields.py        # Shared Pydantic field types
    health.py        # Health check model
tests/               # pytest suite (mirrors routes/)
support/             # Notebooks / scratch scripts
```

## Local development

### Prerequisites

- Python 3.13
- [uv](https://docs.astral.sh/uv/) package manager
- MongoDB Atlas Local running (see root `docker compose --profile dev up`)

### Setup

```bash
cp .env.example .env   # fill in your values
make install           # sync dependencies from uv.lock
make run               # start dev server at http://localhost:8000 (with reload)
```

### Commands

```bash
make install   # sync runtime + dev dependencies
make run       # start dev server (http://0.0.0.0:8000, --reload)
make seed      # load OCRE coin data from ../../datasets/ocre20251021.json
make embed     # generate embeddings for all coins (requires OPENAI_API_KEY)
make test      # format, lint, type-check, run full pytest suite with coverage
```

Targeted commands:
```bash
uv run pytest tests/test_auth.py -vv
uv run ruff check app tests
uv run mypy .
```

## Environment variables

Copy `.env.example` to `.env` and fill in the required values. Never commit secrets.

| Variable             | Required | Description                              |
|----------------------|----------|------------------------------------------|
| `MONGODB_URI`        | yes      | MongoDB connection string                |
| `MONGODB_DATABASE`   | yes      | Database name (e.g. `ocre_ai`)           |
| `SECRET_KEY`         | yes      | JWT signing secret (random string)       |
| `OPENAI_API_KEY`     | yes      | OpenAI API key                           |
| `AI_MODEL`           | yes      | LLM for chat (e.g. `gpt-4o`)            |
| `AI_EMBEDDING_MODEL` | yes      | Embedding model (e.g. `text-embedding-3-small`) |
| `PUBLIC_URL`         | yes      | Public base URL (for email links)        |
| `EMAIL_FROM`         | yes      | Sender address for transactional email   |
| `SMTP_HOST`          | yes      | SMTP host                                |
| `SMTP_PORT`          | yes      | SMTP port                                |
| `SMTP_USERNAME`      | no       | SMTP username (if auth required)         |
| `SMTP_PASSWORD`      | no       | SMTP password (if auth required)         |
| `SMTP_USE_TLS`       | no       | Enable TLS (default `False`)             |
| `CORS_ORIGINS`       | no       | Comma-separated allowed origins (default `*`) |

## API routes

| Method | Path                   | Description                                 |
|--------|------------------------|---------------------------------------------|
| GET    | `/health`              | Health check                                |
| POST   | `/auth/register`       | Create account                              |
| POST   | `/auth/login`          | Login, returns JWT                          |
| POST   | `/auth/forgot-password`| Send password reset email                   |
| POST   | `/auth/reset-password` | Reset password using token                  |
| GET    | `/user/me`             | Get current user profile                    |
| PATCH  | `/user/me`             | Update profile                              |
| GET    | `/user/collection`     | Get user's saved coin collection            |
| POST   | `/user/collection`     | Add coin to collection                      |
| DELETE | `/user/collection/{id}`| Remove coin from collection                 |
| GET    | `/catalog`             | List / search coins (filters + pagination)  |
| GET    | `/catalog/metadata`    | Distinct filter values (denomination, material, etc.) |
| GET    | `/catalog/{record_id}` | Get single coin by OCRE record ID           |
| POST   | `/catalog/image`       | Upload coin image → AI description          |
| POST   | `/chat`                | Send message to AI expert agent             |

Interactive API docs are available at `http://localhost:8000/docs` when the dev server is running.

## Search

The catalog supports two search modes, selected automatically:

- **List mode** (no `search` param): standard MongoDB filter + sort with pagination.
- **Hybrid search** (`search` param): combines vector search and full-text search using MongoDB `$rankFusion`. A query embedding is generated via the configured `AI_EMBEDDING_MODEL`, then the results from both pipelines are merged by rank and filtered/paginated.

## Search indexes

Two MongoDB Atlas Search indexes must be created on the `coins` collection before search works. Connect to MongoDB and run:

### Full-text search index

```js
db.coins.createSearchIndex(
  "coins_text_search",
  {
    mappings: {
      dynamic: false,
      fields: {
        record_id:    [{ type: "string", analyzer: "lucene.standard" }],
        title:        [{ type: "string", analyzer: "lucene.standard" }],
        description:  [{ type: "string", analyzer: "lucene.standard" }],
        authority:    [{ type: "string", analyzer: "lucene.standard" }],
        denomination: [{ type: "string", analyzer: "lucene.standard" }],
        manufacturer: [{ type: "string", analyzer: "lucene.standard" }],
        material:     [{ type: "string", analyzer: "lucene.standard" }],
        object_type:  [{ type: "string", analyzer: "lucene.standard" }],
      }
    }
  }
);
```

### Vector search index

```js
db.runCommand({
  createSearchIndexes: "coins",
  indexes: [
    {
      name: "coins_vector_search",
      type: "vectorSearch",
      definition: {
        fields: [
          {
            type: "vector",
            path: "embedding",
            numDimensions: 1536,
            similarity: "cosine"
          }
        ]
      }
    }
  ]
});
```

`numDimensions: 1536` matches `text-embedding-3-small`. If you use a different model, update this value accordingly.

## Database operations

### Seed coin data

```bash
make seed    # loads ../../datasets/ocre20251021.json into MongoDB
make embed   # generates OpenAI embeddings for each coin (slow on first run)
```

### Backup and restore

```bash
mongodump \
  --uri="mongodb://localhost:27017/?directConnection=true" \
  --db="ocre_ai" \
  --out="./backup"
```

```bash
mongorestore \
  --uri="mongodb://localhost:27017/?directConnection=true" \
  --db="ocre_ai" \
  "./backup/ocre_ai"
```

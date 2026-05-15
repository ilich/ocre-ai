# OCRE AI

AI toolkit for identifying Roman coins using the [Online Coins of the Roman Empire](https://numismatics.org/ocre/) dataset, covering 43,000+ documented coin types from Augustus (31 BC) to Zeno (AD 491).

Users can browse and filter the coin catalog, search using natural language or by uploading a coin image, and chat with an AI expert that can identify coins and answer questions about Roman numismatics.

## Architecture

```
┌──────────────────────────────────────────────────────┐
│  Browser                                             │
│  React SPA (React Router 7, MUI, TailwindCSS)        │
└──────────────────┬───────────────────────────────────┘
                   │ HTTP /api/*
┌──────────────────▼───────────────────────────────────┐
│  nginx (port 80)                                     │
│  Serves static frontend assets                       │
│  Reverse-proxies /api/* → backend:8000               │
└──────────────────┬───────────────────────────────────┘
                   │
┌──────────────────▼───────────────────────────────────┐
│  FastAPI backend (Python 3.13, pydantic-ai)          │
│  Auth · Catalog · Chat · User                        │
└──────────────────┬───────────────────────────────────┘
                   │
┌──────────────────▼───────────────────────────────────┐
│  MongoDB Atlas Local (port 27017)                    │
│  Atlas Vector Search + Atlas Full-Text Search        │
└──────────────────────────────────────────────────────┘
```

The backend is **not** exposed directly to the host — all traffic from the browser goes through the nginx reverse proxy.

## Services

| Service    | Description                         | Port(s)        |
|------------|-------------------------------------|----------------|
| `mongodb`  | MongoDB Atlas Local (vector search) | `27017`        |
| `mailpit`  | Test SMTP server + web UI           | `1025`, `8025` |
| `backend`  | FastAPI backend                     | internal only  |
| `frontend` | React SPA served via nginx          | `80`           |

## Docker Compose profiles

| Profile   | Services started                       |
|-----------|----------------------------------------|
| _(none)_  | `mongodb` only                         |
| `dev`     | `mongodb` + `mailpit`                  |
| `full`    | `mongodb` + `mailpit` + `backend` + `frontend` |

## Quick start

### 1. Configure environment

```bash
cp .env.docker.example .env.docker
```

Edit `.env.docker` and fill in your values. Required fields:

| Variable             | Description                          | Example                     |
|----------------------|--------------------------------------|-----------------------------|
| `SECRET_KEY`         | JWT signing secret                   | _(random string)_           |
| `OPENAI_API_KEY`     | OpenAI API key                       | `sk-...`                    |
| `AI_MODEL`           | LLM used for chat                    | `gpt-4o`                    |
| `AI_EMBEDDING_MODEL` | Model used to generate embeddings    | `text-embedding-3-small`    |
| `MONGODB_URI`        | MongoDB connection string            | `mongodb://mongodb:27017`   |
| `MONGODB_DATABASE`   | Database name                        | `ocre_ai`                   |
| `PUBLIC_URL`         | Public base URL of the app           | `http://localhost`          |
| `EMAIL_FROM`         | Sender address for transactional email | `noreply@example.com`     |
| `SMTP_HOST`          | SMTP host (use `mailpit` in Docker)  | `mailpit`                   |
| `SMTP_PORT`          | SMTP port                            | `1025`                      |

### 2. Start the stack

**Full stack** — frontend on [http://localhost](http://localhost):
```bash
docker compose --profile full up
```

**Development dependencies only** (MongoDB + mailpit for local dev):
```bash
docker compose --profile dev up
```

**MongoDB only**:
```bash
docker compose up
```

### 3. Seed the database

After the stack is running, seed the coin catalog and generate embeddings:

```bash
docker compose --profile full exec backend make seed
docker compose --profile full exec backend make embed
```

Then create the required MongoDB search indexes — see [apps/backend/README.md](apps/backend/README.md#search-indexes).

### 4. Rebuild after code changes

```bash
docker compose --profile full build
docker compose --profile full up
```

## Exposed ports

| Port    | Service          |
|---------|------------------|
| `80`    | Frontend (nginx) |
| `27017` | MongoDB          |
| `1025`  | Mailpit SMTP     |
| `8025`  | Mailpit web UI   |

## Local development

- Backend: [apps/backend/README.md](apps/backend/README.md)
- Frontend: [apps/frontend/README.md](apps/frontend/README.md)

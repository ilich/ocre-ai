# OCRE AI

AI toolkit for identifying Roman coins using the [Online Coins of the Roman Empire](https://numismatics.org/ocre/) dataset, covering 43,000+ documented coin types from Augustus (31 BC) to Zeno (AD 491).

## Services

| Service  | Description                         | Port(s)           |
|----------|-------------------------------------|-------------------|
| mongodb  | MongoDB Atlas Local (vector search) | `27017`           |
| mailpit  | Test SMTP server + web UI           | `1025`, `8025`    |
| backend  | FastAPI backend                     | internal only     |
| frontend | React SPA served via nginx          | `80`              |

## Docker Compose profiles

| Profile | Services started                          |
|---------|-------------------------------------------|
| _(none)_ | mongodb only                             |
| `dev`   | mongodb + mailpit                         |
| `full`  | mongodb + mailpit + backend + frontend    |

## Quick start

### 1. Configure environment

Copy the Docker env template and fill in your secrets:

```bash
cp .env.docker.example .env.docker
```

Edit `.env.docker` — at minimum set `SECRET_KEY`, `OPENAI_API_KEY`, `AI_MODEL`, and `AI_EMBEDDING_MODEL`.

### 2. Run

**Full stack** (frontend on [http://localhost](http://localhost)):
```bash
docker compose --profile full up
```

**Development dependencies only** (MongoDB + mailpit):
```bash
docker compose --profile dev up
```

**MongoDB only**:
```bash
docker compose up
```

### 3. Rebuild after code changes

```bash
docker compose --profile full build
docker compose --profile full up
```

## Exposed ports

| Port   | Service         |
|--------|-----------------|
| `80`   | Frontend (nginx)|
| `27017`| MongoDB         |
| `1025` | Mailpit SMTP    |
| `8025` | Mailpit web UI  |

The backend is **not** reachable directly from the host — frontend nginx proxies `/api/*` requests to it internally.

## Local development

See `apps/frontend/` and `apps/backend/` for local dev setup.

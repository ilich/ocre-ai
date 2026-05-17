# Performance Testing with Locust

## Setup

1. Install dependencies (Locust is included in dev dependencies):
   ```bash
   make install   # or: uv sync
   ```

2. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your test credentials
   ```

## Running Tests

### Local Development Server (direct, port 8000)
```bash
# Override the nginx-proxy default to hit the dev server directly
locust -f locustfile.py --host=http://localhost:8000
```

### Full stack via Docker / nginx proxy (default config)
```bash
# Uses the default host from locust.conf: http://localhost/api
locust -f locustfile.py
```

### Staging/Production
```bash
locust -f locustfile.py --host=https://staging.yourdomain.com
locust -f locustfile.py --host=https://api.yourdomain.com
```

### Headless Mode (No Web UI)
```bash
# Run with 100 users, spawn rate of 10/sec, for 5 minutes
locust -f locustfile.py --headless -u 100 -r 10 -t 5m --html=report.html
```

## Configuration

The `locust.conf` file contains default settings. You can override any setting via command line:

- `--users` / `-u`: Number of concurrent users
- `--spawn-rate` / `-r`: Users to spawn per second
- `--run-time` / `-t`: Stop after specified time (e.g., 5m, 1h)
- `--host`: Target host URL
- `--headless`: Run without web UI
- `--csv`: Export results to CSV
- `--html`: Generate HTML report

## Web UI

By default, Locust runs with a web interface at http://localhost:8089 where you can:
- Start/stop tests
- Adjust user count and spawn rate in real-time
- View real-time statistics and charts

## Environment Variables

Required in `.env`:
- `USERNAME`: Test user login
- `PASSWORD`: Test user password

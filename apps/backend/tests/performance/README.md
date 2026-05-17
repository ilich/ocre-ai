# Performance Testing with Locust

## Setup

1. Install Locust:
   ```bash
   uv pip install locust
   ```

2. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your test credentials
   ```

## Running Tests

### Local Development Server
```bash
# Using the default config (localhost:8000)
locust -f locustfile.py

# Or explicitly set the host
locust -f locustfile.py --host=http://localhost:8000
```

### Staging/Production
```bash
# Override the host for staging
locust -f locustfile.py --host=https://staging.yourdomain.com

# Override the host for production
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

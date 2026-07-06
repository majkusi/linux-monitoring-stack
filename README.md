# linux-monitoring-stack

A three-tier monitoring stack running on Docker Compose. A **monitor** agent collects system metrics and checks service health, a **loader** persists the data into an **Oracle** database, a **FastAPI** service exposes that data as a REST API, a **React** dashboard visualizes it, and **Tomcat** acts as the monitored application server. mTLS secures all HTTPS communication between the monitor and Tomcat.

## Architecture

![Architecture](docs/architecture.svg?v=3)

## Tech Stack

| Component          | Technology                                       |
| ------------------ | ------------------------------------------------ |
| Application server | Apache Tomcat (latest)                           |
| Monitoring agent   | Bash + curl                                      |
| Database loader    | Python 3 + python-oracledb                       |
| REST API           | Python 3 + FastAPI                               |
| Frontend           | React + Vite + TypeScript, Tailwind CSS, Chart.js |
| Database           | Oracle Database Free 23ai (`gvenzl/oracle-free`) |
| Security           | mTLS with self-signed CA                         |
| Tests / CI         | pytest + ESLint + GitHub Actions                 |
| Orchestration      | Docker Compose                                   |

## Project Structure

```
linux-monitoring-stack/
├── .github/
│   └── workflows/
│       ├── api_test.yml         # CI — pytest, runs on api/** changes
│       └── front_eslint.yml     # CI — ESLint, runs on frontend/** changes
├── api/
│   ├── dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py              # FastAPI app, endpoints, lifespan, CORS
│   │   ├── db/connect.py        # Oracle connection pool wrapper (Connect)
│   │   ├── models/              # Pydantic response models
│   │   └── sql/sql_queries.py   # query builders for the endpoints
│   └── tests/
│       ├── conftest.py          # sets test env vars, FakeDb override
│       ├── misc/fakeDb.py       # FakeDb stub (canned rows — no live Oracle)
│       └── test/test_endpoints.py
├── certs/
│   ├── generate-certs.sh        # generates CA, server, and client certs
│   └── generated/               # output dir (gitignored)
├── frontend/
│   └── monitoring-frontend/     # React + Vite + TS dashboard
│       ├── src/
│       │   ├── App.tsx
│       │   └── components/       # Header, StatCard, MetricsChart, ServiceHealth, ServiceRow
│       ├── package.json
│       └── vite.config.ts
├── loader/
│   ├── dockerfile
│   ├── requirements.txt
│   └── scripts/
│       └── loader.py            # reads logs, inserts into Oracle
├── logs/                        # shared volume (gitignored)
├── monitor/
│   ├── dockerfile
│   └── scripts/
│       ├── run_all.sh           # entrypoint — health_check.sh + daily log_cleanup.sh
│       ├── health_check.sh      # collects metrics, checks Tomcat
│       └── log_cleanup.sh       # deletes logs older than 7 days
├── sql/
│   └── queries/
│       ├── avg_ram_per_hour.sql
│       ├── http_errors_per_day.sql
│       ├── tomcat_uptime.sql
│       └── top5_cpu_pct.sql
├── tomcat/
│   ├── conf/
│   │   └── server.xml           # Tomcat config with mTLS connector
│   └── webapps/                 # deploy apps here (gitignored)
├── docker-compose.yml
└── .env                         # secrets (gitignored)
```

## Setup

### Prerequisites

- Docker + Docker Compose
- OpenSSL (for cert generation)
- Git Bash or Linux shell
- Node.js 24+ (only for the frontend)

### 1. Configure environment

Create a `.env` file in the project root:

```env
ORACLE_PASSWORD=your_oracle_sys_password
APP_USER=app_user
APP_USER_PASSWORD=your_app_user_password
```

### 2. Generate mTLS certificates

```bash
cd certs
bash generate-certs.sh
```

This creates a local CA and signs two certificates: `tomcat` (server) and `monitor` (client). Output goes to `certs/generated/`.

### 3. Start the stack

```bash
docker-compose up --build -d
```

The `loader` container waits for Oracle to pass its healthcheck before starting. First startup takes a few minutes while Oracle initializes.

### 4. Verify

```bash
# Check all containers are running
docker-compose ps

# Tail monitor logs
docker logs monitor -f

# Tail loader logs
docker logs loader -f
```

## How It Works

### monitor

`run_all.sh` is the container entrypoint. It launches `health_check.sh` in the background and then runs `log_cleanup.sh` once a day.

`health_check.sh` runs every 60 seconds. It collects RAM, CPU, and disk usage, then performs three Tomcat health checks:

1. HTTP on port 8080
2. HTTPS on port 8443 **without** a client certificate (should fail — tests mTLS enforcement)
3. HTTPS on port 8443 **with** `monitor.crt` + `monitor.key` (should succeed)

Metrics and service statuses are written to `/logs/` (shared Docker volume), and threshold breaches are appended to a daily `alerts-*.log`.

`log_cleanup.sh` deletes any `/logs/*.log` older than 7 days.

### loader

Reads the log files every 60 seconds (both today's and yesterday's, to handle the midnight rollover) and inserts any rows newer than the latest `MAX(TIME_STAMP)` in the database. Creates the `METRICS` and `STATUS` tables on first run (idempotent — checks `USER_TABLES` before issuing `CREATE TABLE`).

### api

A FastAPI service (container `api_dashboard`, port **8000**) that reads from Oracle through a `python-oracledb` connection pool and returns the data as JSON. The pool is opened and closed in the FastAPI `lifespan`, and exposed to the route handlers via a `get_db` dependency. CORS is enabled for the frontend origin `http://localhost:5173` (GET only).

| Method & path                         | Returns                                              |
| ------------------------------------- | ---------------------------------------------------- |
| `GET /metrics`                        | Today's rows from `METRICS`, newest first            |
| `GET /metrics/average/hourly/ram`     | Hourly average RAM (`RAM_PCT`, `RAM_USED`)           |
| `GET /metrics/average/hourly/cpu`     | Hourly average CPU (`CPU_PCT`)                       |
| `GET /metrics/average/hourly/disk`    | Hourly average disk (`DISK_PCT`)                     |
| `GET /metrics/average/uptime`         | Uptime % (`successes`, `total`, `uptime_pct`)        |
| `GET /metrics/status/test_results`    | Latest `STATUS` row (`http`, `mtls_no_cert`, `mtls_cert`) |

Interactive docs are auto-generated at `http://localhost:8000/docs`.

### frontend

A React + Vite + TypeScript dashboard (`frontend/monitoring-frontend/`) styled with Tailwind CSS. It polls the API every 60 seconds and renders CPU / RAM / disk / uptime stat cards, a Chart.js line chart of today's metrics, and a service-health panel. Not containerized yet — run it locally:

```bash
cd frontend/monitoring-frontend
npm install
npm run dev
```

Opens on `http://localhost:5173` (the origin whitelisted by the API's CORS config).

### mTLS

The CA (`ca.crt`) is self-signed and shared by both Tomcat and the monitor container at runtime. `ca.key` is only needed during cert generation. Tomcat's `SSLHostConfig` has `certificateVerification="required"` — connections without a valid client cert are rejected.

## Sample Output

### `logs/health-2026-06-18.log`

```
2026-06-18 09:06:08,17.28,677,3917,2,100.00
2026-06-18 09:07:08,68.73,2692,3917,2,0.00
2026-06-18 09:08:11,70.31,2754,3917,2,4.60
```

Format: `timestamp, RAM_PCT, RAM_USED_MB, RAM_TOTAL_MB, DISK_PCT, CPU_PCT`

### `logs/service-2026-06-18.log`

One line per minute, holding all three checks — HTTP, mTLS without cert, mTLS with cert:

```
2026-06-18 10:02:27,404,000,404
```

Format: `timestamp, http, mtls_no_cert, mtls_cert`. `000` = mTLS connection rejected (no client cert). `404` = Tomcat responded (no webapp deployed, which is expected).

### `logs/alerts-2026-06-18.log`

```
2026-06-18 09:06:08,CPU ALERT: 100.00% > 90.00%
2026-06-18 09:25:26,CPU ALERT: 100.00% > 90.00%
```

Thresholds: CPU > 90%, RAM >= 85%, Disk > 80%.

## SQL Queries

Connect via Oracle SQL\*Plus or any SQL client on port 1521 (service: `FREEPDB1`).

**Average RAM usage per hour:**

```sql
SELECT TO_CHAR(trunc(TIME_STAMP, 'HH24'), 'YYYY-MM-DD HH24:MI') AS hour,
       avg(RAM_PCT) AS avg_ram_pct
FROM METRICS
GROUP BY trunc(TIME_STAMP, 'HH24')
ORDER BY trunc(TIME_STAMP, 'HH24');
```

**HTTP errors per day:**

```sql
SELECT trunc(TIME_STAMP, 'DD') AS day, COUNT(HTTP_STATUS) AS error_count
FROM STATUS
WHERE HTTP_STATUS != 200
GROUP BY day
ORDER BY day;
```

**Tomcat uptime percentage:**

```sql
SELECT successes, total, ROUND(successes/total * 100, 2) AS uptime_pct
FROM (
    SELECT SUM(CASE WHEN HTTP_STATUS = 200 THEN 1 ELSE 0 END) AS successes,
           COUNT(*) AS total
    FROM STATUS
);
```

**Top 5 CPU spikes:**

```sql
SELECT TIME_STAMP, CPU_PCT
FROM METRICS
ORDER BY CPU_PCT DESC
FETCH FIRST 5 ROWS ONLY;
```

## Tests & CI

The API has unit tests (`api/tests/`) built on **pytest** and FastAPI's `TestClient`. The Oracle dependency is swapped out at test time via `app.dependency_overrides[get_db]`, which injects a `FakeDb` stub (`tests/misc/fakeDb.py`) returning canned rows — so the tests run **without a live Oracle instance**. Environment variables that `main.py` reads at import time are set in `conftest.py` before the app is imported.

Run them locally:

```bash
cd api
python -m pytest -v
```

CI runs on GitHub Actions:

- `.github/workflows/api_test.yml` — installs `api/requirements.txt` and runs `pytest` (Python 3.14) on any change under `api/**`. Because the database is stubbed, no Oracle service is required.
- `.github/workflows/front_eslint.yml` — runs `npm ci` + `npm run lint` (Node 24) on any change under `frontend/**`.

## Design Decisions

**Ephemeral database** — Oracle data is not persisted to a volume. Tables are recreated automatically on each startup via `check_if_table_exists()`. This is intentional for a dev/demo environment; adding a named volume to `docker-compose.yml` would make it persistent.

**All three checks per STATUS row** — Each service-log line records the plain HTTP check plus both mTLS checks and is stored as a single timestamped row with dedicated columns (`HTTP_STATUS`, `MTLS_NO_CERT`, `MTLS_CERT`). This keeps every minute's full health snapshot in one place rather than spread across separate rows.

**Self-signed CA** — No public CA is used. Both containers mount `certs/generated/` and trust the same `ca.crt`. The CA private key (`ca.key`) is only needed to sign certs and is not mounted at runtime.

**Secrets via `.env`** — Oracle passwords are passed through Docker Compose environment variables sourced from `.env`, which is gitignored.

## TODO

### Infrastructure

- [x] CI — GitHub Actions (pytest for the API, ESLint for the frontend)
- [x] Log cleanup — `log_cleanup.sh` deletes logs older than 7 days (compression still TODO)
- [ ] `init.sh` — single script setup (`.env`, certs, `docker-compose up`)
- [ ] Nginx reverse proxy container (SSL termination, forward to Tomcat)

### Backend

- [x] FastAPI container — `/metrics`, hourly averages (RAM / CPU / disk), uptime, and status test results
- [x] `/status`-style endpoint exposing the `STATUS` table (`/metrics/status/test_results`)
- [ ] SQL Views (`DAILY_SUMMARY`, etc.) as data layer for the API
- [ ] Alert email sender (Python `smtplib`, triggers on threshold breach)
- [ ] Daily report generator (HTML/PDF summary of metrics)

### Frontend

- [x] React dashboard — Chart.js CPU/RAM/disk chart, stat cards, uptime, service-health panel
- [ ] Dockerize the frontend and add it to `docker-compose.yml`
- [ ] Wire the ServiceHealth panel to `/metrics/status/test_results` (currently static)

### Database

- [ ] Oracle `DBMS_SCHEDULER` job for in-DB metric aggregation
- [ ] Additional analytical queries (CPU vs HTTP errors correlation, peak alert hours)

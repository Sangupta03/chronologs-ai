# 📜 ChronoLogs AI — Intelligent Log Analysis System

> Turn thousands of messy log lines into a handful of incidents you can actually read.

ChronoLogs AI is a full-stack system that ingests raw application logs, groups related events using machine learning, flags anomalies, and writes a plain-English summary of what went wrong — so you don't have to scroll through a 50,000-line log file by hand.

---

## 🤔 What is "log analysis," anyway?

If you don't come from an ops/SRE background, here's the 30-second primer:

- **Logs** are timestamped text lines that an application writes while it runs (e.g. `2026-06-01 09:00:02 ERROR payment-service Database connection timeout`).
- A real production system can generate **millions of these per day**, across dozens of services.
- When something breaks, the *symptom* (an error) is usually surrounded by hundreds of *related* error lines — same root cause, different timestamps. Reading them one by one is slow and easy to get wrong.
- **Log analysis** is the practice of automatically parsing, grouping, and scoring these lines so a human can answer "what broke, how bad is it, and why?" in seconds instead of hours.

ChronoLogs AI automates the three hardest parts of that process:

| Problem | What ChronoLogs does |
|---|---|
| 📚 Too much volume to read | Streams and parses logs without loading the whole file into memory |
| 🔀 Same error repeated 500 times | Clusters similar log lines together using ML, so 500 lines become 1 incident |
| ❓ "Is this serious?" | Scores each incident's severity automatically |
| 🗣️ Logs are cryptic | Generates a human-readable explanation of each incident using an LLM (Gemini) |
| 🔍 "Have we seen this before?" | Semantic search over past logs — search by *meaning*, not exact keyword |

---

## 🧠 Core Concepts (the ML/AI bits, explained)

These are the techniques under the hood — you don't need a data science background to follow along:

- **TF-IDF (Term Frequency–Inverse Document Frequency)** — converts each log line into a vector of numbers based on which words are distinctive to it. Common words like "the" or "service" are downweighted; rare, meaningful words (`timeout`, `refused`, `OOM`) are upweighted.
- **K-Means Clustering** — groups those vectors into clusters of "similar-sounding" log lines. This is how 500 near-identical `Database connection timeout` lines collapse into a single group instead of 500 separate alerts.
- **Rule-based anomaly detection** — simple heuristics (error rate spikes, repeated failures in a time window, unexpected severities) flag clusters worth a human's attention.
- **Incident engine** — takes flagged clusters and turns them into a single "Incident" record with a severity score and a time window, instead of a wall of raw log lines.
- **AI Storytelling (Gemini)** — feeds the incident's representative log lines to a Gemini LLM and asks it to write a short, human-readable explanation: what happened, which service, and a likely cause.
- **Semantic search (FAISS + embeddings)** — lets you search logs by *meaning* ("payment failures around 9am") rather than exact text match, using vector embeddings and a FAISS similarity index.

---

## 🏗️ Architecture

```text
┌─────────────────┐
│  React Frontend │   Upload → Analyze → View incidents
└────────┬─────────┘
         │ REST API (JWT auth)
┌────────▼─────────┐
│  Django REST API │
└────────┬─────────┘
         │
         ▼
┌───────────────────────────────────────────┐
│ Log Parser → TF-IDF → K-Means → Anomaly    │   ← runs async via Celery + Redis
│ Detection → Incident Engine → Gemini AI    │     so big uploads don't block requests
│ Storytelling → FAISS Semantic Index        │
└───────────────────────────────────────────┘
         │
         ▼
   PostgreSQL (prod) / SQLite (dev)
```

Long-running work (parsing huge files, running ML, calling the LLM) happens in **Celery background workers**, not in the request/response cycle — you upload a file, poll a status endpoint, and the UI updates once processing finishes.

---

## 🧪 Tech Stack

| Layer | Tools |
|---|---|
| **Backend** | Django, Django REST Framework, SimpleJWT, django-cors-headers |
| **Async / Queue** | Celery, Redis |
| **AI / ML** | scikit-learn (TF-IDF, K-Means), NumPy/SciPy, FAISS (semantic search), Google Gemini (storytelling) |
| **Database** | PostgreSQL (prod), SQLite (dev) |
| **Frontend** | React (Vite), Tailwind CSS, Axios, React Router |
| **Infra** | Docker, docker-compose, Render (deploy config), GitHub Actions (CI) |

---

## 📂 Project Structure

```text
backend/
  apps/
    accounts/    → registration, login, JWT auth
    logs/        → file upload, streaming parser, status polling
    ai_engine/   → TF-IDF, clustering, anomaly detection, semantic search
    ai_story/    → Gemini-powered incident summaries
    incidents/   → incident records, stats, filtering
  config/        → Django settings, root URL config

frontend/
  src/
    components/  → reusable UI (incident cards, severity badges, etc.)
    pages/       → Upload / Dashboard / Incidents views
    services/    → API client (Axios)

sample_logs/     → example .log files for trying out each feature
```

---

## ⚙️ Running Locally

### Option A — Docker (easiest, brings up everything at once)

```bash
docker-compose up --build
```

Starts Redis, the Django backend, a Celery worker, and the React frontend together. Backend at `localhost:8000`, frontend at `localhost:5173`.

### Option B — Run services manually

Create `backend/.env`:

```env
GEMINI_API_KEY=your-gemini-api-key
```

**Backend** (needs Redis running locally first)

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

**Celery worker** (in a second terminal, from `backend/`)

```bash
celery -A config worker --pool=solo -l info
```

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

---

## 🚀 Production Deployment

### Backend → Railway

1. Create a new project in [Railway](https://railway.app).
2. Add a **PostgreSQL** plugin and a **Redis** plugin from the Railway dashboard — Railway will inject the connection strings automatically.
3. Add a **new service** → "Deploy from GitHub repo" → select this repo → set **Root Directory** to `backend`. Railway picks up `railway.toml` and the Dockerfile automatically.
4. Set these environment variables in the Railway service settings:

   | Variable | Value |
   |---|---|
   | `DJANGO_SETTINGS_MODULE` | `config.settings.prod` |
   | `DJANGO_SECRET_KEY` | any long random string |
   | `DB_NAME` | from Railway PostgreSQL plugin |
   | `DB_USER` | from Railway PostgreSQL plugin |
   | `DB_PASSWORD` | from Railway PostgreSQL plugin |
   | `DB_HOST` | from Railway PostgreSQL plugin |
   | `DB_PORT` | from Railway PostgreSQL plugin |
   | `CELERY_BROKER_URL` | from Railway Redis plugin |
   | `CELERY_RESULT_BACKEND` | from Railway Redis plugin |
   | `GEMINI_API_KEY` | your Gemini API key |
   | `ALLOWED_HOSTS` | `your-project.up.railway.app` |
   | `CORS_ALLOWED_ORIGINS` | `https://your-frontend.vercel.app` |

5. **Celery worker** — add a second Railway service from the same repo, same root directory (`backend`), but override the start command to:
   ```
   celery -A config worker --pool=solo -l info
   ```
   Give it the same environment variables (no `ALLOWED_HOSTS` / `CORS_ALLOWED_ORIGINS` needed for the worker).

### Frontend → Vercel

1. Import the repo in [Vercel](https://vercel.com).
2. Set **Root Directory** to `frontend`.
3. Vercel auto-detects Vite — the default build settings work (`npm run build`, output `dist`).
4. Add one environment variable:

   | Variable | Value |
   |---|---|
   | `VITE_API_URL` | `https://your-project.up.railway.app/api` |

5. Deploy. The `vercel.json` in `frontend/` handles SPA routing (all paths → `index.html`).

---

## 🔌 API Reference

All endpoints are prefixed with `/api/`. Authenticated routes require `Authorization: Bearer <access_token>`.

### 🔐 Auth (`/api/auth/`)

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `register/` | Create a new account |
| POST | `login/` | Get JWT access + refresh tokens |
| POST | `refresh/` | Refresh an expired access token |
| POST | `logout/` | Invalidate session |

### 📤 Logs (`/api/logs/`)

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `upload/` | Upload a `.log` file for processing |
| GET | `<log_file_id>/status/` | Poll whether parsing has finished |

### 🤖 AI Engine (`/api/ai/`)

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `analyze/<log_file_id>/` | Kick off clustering + anomaly detection |
| GET | `analyze/<log_file_id>/status/` | Poll analysis progress |
| GET | `search/<log_file_id>/` | Semantic search within a log file |

### 🚨 Incidents (`/api/incidents/`)

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `` | List incidents (filterable) |
| GET | `stats/` | Aggregate incident stats (counts by severity, etc.) |

---

## 🧾 Try it with sample data

The [`sample_logs/`](sample_logs/) folder has ready-made log files for exercising different features without needing real production data:

| File | What it demonstrates |
|---|---|
| `01_basic_quickstart.log` | Minimal example — upload this first |
| `02_multi_cluster_medium.log` | Multiple distinct incident clusters |
| `03_large_scale.log` | Larger file to test streaming/performance |
| `04_bracket_format.log` | Alternate log format `[LEVEL]` parsing |
| `05_date_only_format.log` | Logs with date-only (no time) timestamps |
| `06_clean_low_severity.log` | Mostly healthy logs, low severity output |
| `07_malformed_partial.log` | Malformed/partial lines — tests parser resilience |
| `08_semantic_search_demo.log` | Good candidate for trying semantic search |

---

## 📈 Roadmap

- Real-time log streaming (Kafka)
- Isolation Forest / statistical anomaly detection alongside the rule-based engine
- Alerting (email/Slack) on new high-severity incidents
- Role-based access control
- Charting & trend dashboards

---

## 👩‍💻 Author

Sanjoli Gupta

## ⭐ License

MIT

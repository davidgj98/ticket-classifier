# IT Ticket Classifier & Translator

AI-powered IT helpdesk ticket triage using local LLMs via Ollama.
Clasificación y traducción de tickets de soporte TI mediante LLMs locales.

[![CI](https://github.com/davidgj98/ticket-classifier/actions/workflows/ci.yml/badge.svg)](https://github.com/davidgj98/ticket-classifier/actions/workflows/ci.yml)

---

## What it does

Paste any chaotic or non-technical IT support ticket and get an instant structured technical classification:

| Field | Description |
|---|---|
| **Category** | Hardware, Software, Network, Security, Access/IAM, Email, Database, Infrastructure |
| **Priority** | Critical, High, Medium, Low (calculated based on impact) |
| **Team** | Recommended support team |
| **Summary** | Converts non-technical descriptions into professional IT diagnostics |
| **Confidence** | Model certainty score |
| **Reasoning** | Step-by-step explanation behind the classification |

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Python 3.10+ |
| AI Inference | Ollama (local, no cloud APIs) |
| Frontend | Vanilla HTML/CSS/JS with cyberpunk-neon aesthetic |
| Database | SQLite (classification history) |
| Dev tools | Ruff (lint), mypy (types), pytest (tests) |
| Deployment | Docker + docker-compose |

## Quick Start

```bash
# 1. Clone
git clone https://github.com/davidgj98/ticket-classifier.git
cd ticket-classifier

# 2. Install
pip install -r requirements.txt

# 3. Pull a model
ollama pull qwen2.5

# 4. Run
uvicorn app.main:app --reload --port 8000

# 5. Open
open http://localhost:8000
```

## Docker

```bash
docker compose up --build
```

Starts both Ollama and the classifier. The app will be at `http://localhost:8000`.

## API

| Method | Path | Description |
|---|---|---|
| GET | `/` | Web interface |
| POST | `/classify` | Classify a ticket |
| GET | `/models` | List available Ollama models |
| GET | `/health` | Health check |
| GET | `/history` | Classification history |
| GET | `/history/{id}` | Get specific classification |
| DELETE | `/history/{id}` | Delete a classification |
| GET | `/export/csv` | Export history as CSV |
| GET | `/export/json` | Export history as JSON |

## Project Structure

```
ticket-classifier/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Pydantic Settings (env vars)
│   ├── models.py            # Pydantic request/response models
│   ├── routers/
│   │   ├── classify.py      # POST /classify
│   │   ├── health.py        # GET /health
│   │   ├── history.py       # CRUD /history
│   │   ├── models_router.py # GET /models
│   │   └── export.py        # GET /export/{csv,json}
│   ├── services/
│   │   ├── ollama.py        # Ollama API client
│   │   └── history.py       # SQLite history service
│   └── static/
│       └── index.html       # Cyberpunk-neon themed UI
├── tests/
│   ├── conftest.py          # Mocked Ollama + test client
│   ├── test_classify.py
│   ├── test_health.py
│   ├── test_models.py
│   ├── test_history.py
│   └── test_export.py
├── main.py                  # Backwards-compatible entry point
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml            # Ruff, mypy, pytest config
├── requirements.txt
└── .github/workflows/ci.yml # CI pipeline
```

## CI/CD

Every push runs:
1. **Ruff** — lint & format check
2. **mypy** — strict type checking
3. **pytest** — 12 tests across all endpoints (with mocked Ollama)

## Configuration

All configurable via environment variables (prefix `TICKET_`):

| Variable | Default | Description |
|---|---|---|
| `TICKET_OLLAMA_URL` | `http://localhost:11434` | Ollama base URL |
| `TICKET_DEFAULT_MODEL` | `qwen2.5:latest` | Fallback model |
| `TICKET_LOG_LEVEL` | `INFO` | Logging level |
| `TICKET_REQUEST_TIMEOUT` | `60.0` | Ollama request timeout |

## License

MIT

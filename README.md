<div align="center">

# IT Ticket Classifier

**AI-powered IT helpdesk ticket triage using local LLMs via Ollama**

[![CI](https://img.shields.io/github/actions/workflow/status/davidgj98/ticket-classifier/ci.yml?branch=main&style=flat-square&label=CI&logo=github)](https://github.com/davidgj98/ticket-classifier/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Ruff](https://img.shields.io/badge/Ruff-black?style=flat-square&logo=ruff)](https://docs.astral.sh/ruff)
[![mypy](https://img.shields.io/badge/mypy-strict-2A6DB2?style=flat-square&logo=python)](https://mypy-lang.org)

</div>

---

**English** · [Español](#español)

---

# English

## Overview

**IT Ticket Classifier** bridges the gap between chaotic user descriptions and professional IT diagnostics. Paste any support ticket and get an instant structured classification — all running **locally** via Ollama, no data leaves your network.

### Features

- **AI Classification** — Category, priority, team, summary, confidence, and reasoning
- **Ticket System** — Create support tickets with auto-generated IDs (`TCK-001`, `TCK-002`...)
- **Status Workflow** — Open → In Progress → Resolved → Closed
- **Local & Private** — All inference runs on your machine via Ollama
- **Full History** — SQLite persistence with CSV/JSON export
- **Jira-style UI** — Clean dark-mode interface with sidebar navigation
- **Docker Support** — One-command setup with `docker compose up`

### Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | [FastAPI](https://fastapi.tiangolo.com) + Python 3.10+ |
| **AI Inference** | [Ollama](https://ollama.ai) (local, no cloud APIs) |
| **Frontend** | Vanilla HTML/CSS/JS — Jira-inspired dark theme |
| **Database** | SQLite (WAL mode) |
| **Linting** | [Ruff](https://docs.astral.sh/ruff) |
| **Type Checking** | [mypy](https://mypy-lang.org) — strict mode |
| **Testing** | [pytest](https://pytest.org) + pytest-asyncio + httpx |
| **CI/CD** | [GitHub Actions](https://github.com/features/actions) |
| **Containerization** | Docker + docker-compose |

### Quick Start

```bash
# 1. Clone
git clone https://github.com/davidgj98/ticket-classifier.git
cd ticket-classifier

# 2. Install dependencies
pip install -r requirements.txt

# 3. Pull a model (example)
ollama pull phi4-mini

# 4. Start the server
uvicorn app.main:app --reload --port 8000

# 5. Open in browser
open http://localhost:8000
```

### Docker (recommended)

```bash
docker compose up --build
```

This starts both Ollama and the classifier. Visit `http://localhost:8000`.

### API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Web interface |
| `POST` | `/classify` | Analyze a ticket description |
| `POST` | `/tickets` | Create a ticket from classification |
| `GET` | `/tickets` | List all tickets |
| `GET` | `/tickets/{id}` | Get a specific ticket |
| `PATCH` | `/tickets/{id}/status` | Update ticket status |
| `DELETE` | `/tickets/{id}` | Delete a ticket |
| `GET` | `/health` | Health check (Ollama connectivity) |
| `GET` | `/models` | List available Ollama models |
| `GET` | `/export/csv` | Export tickets as CSV |
| `GET` | `/export/json` | Export tickets as JSON |

### Example

**Request:**
```bash
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"text":"The internet globe icon on my taskbar has a red cross and the floor box is flashing red"}'
```

**Response:**
```json
{
  "category": "Network",
  "priority": "High",
  "team": "Network Team",
  "summary": "Local WAN link failure / Router hardware alert status",
  "confidence": "High",
  "reasoning": "User describes a red cross on the network icon and flashing LEDs on the router, indicating a physical or link-layer connectivity issue."
}
```

### Run Tests

```bash
pytest -v
```

### Configuration

All settings via environment variables (prefix `TICKET_`):

| Variable | Default | Description |
|---|---|---|
| `TICKET_OLLAMA_URL` | `http://localhost:11434` | Ollama base URL |
| `TICKET_DEFAULT_MODEL` | `phi4-mini:latest` | Fallback model |
| `TICKET_LOG_LEVEL` | `INFO` | Logging level |
| `TICKET_REQUEST_TIMEOUT` | `60.0` | Ollama timeout in seconds |

### Project Structure

```
ticket-classifier/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Pydantic Settings (env vars)
│   ├── models.py            # Pydantic request/response models
│   ├── routers/
│   │   ├── classify.py      # POST /classify
│   │   ├── tickets.py       # CRUD /tickets + status PATCH
│   │   ├── health.py        # GET /health
│   │   ├── models_router.py # GET /models
│   │   └── export.py        # GET /export/{csv,json}
│   ├── services/
│   │   ├── ollama.py        # Ollama API client
│   │   └── tickets.py       # SQLite ticket persistence
│   └── static/
│       └── index.html       # Jira-inspired dark UI
├── tests/
│   ├── conftest.py          # Mocked Ollama + test client
│   ├── test_classify.py
│   ├── test_tickets.py
│   ├── test_health.py
│   ├── test_models.py
│   └── test_export.py
├── main.py                  # Backwards-compatible entry point
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml            # Ruff + mypy + pytest config
└── .github/workflows/ci.yml # CI pipeline
```

---

<a name="español"></a>

# Español

## Vista General

**IT Ticket Classifier** convierte descripciones caóticas de usuarios en diagnósticos profesionales de TI. Pega cualquier ticket de soporte y obtén una clasificación estructurada al instante — todo **localmente** mediante Ollama, sin que los datos salgan de tu red.

### Características

- **Clasificación IA** — Categoría, prioridad, equipo, resumen, confianza y razonamiento
- **Sistema de Tickets** — Crea tickets de soporte con IDs auto-generados (`TCK-001`, `TCK-002`...)
- **Flujo de Estados** — Abierto → En Progreso → Resuelto → Cerrado
- **Local y Privado** — Toda la inferencia se ejecuta en tu máquina vía Ollama
- **Historial Completo** — Persistencia SQLite con exportación CSV/JSON
- **UI estilo Jira** — Interfaz oscura y limpia con navegación lateral
- **Soporte Docker** — Listo para desplegar con `docker compose up`

### Stack Tecnológico

| Capa | Tecnología |
|---|---|
| **Backend** | [FastAPI](https://fastapi.tiangolo.com) + Python 3.10+ |
| **Inferencia IA** | [Ollama](https://ollama.ai) (local, sin APIs externas) |
| **Frontend** | HTML/CSS/JS nativo — Tema oscuro inspirado en Jira |
| **Base de Datos** | SQLite (modo WAL) |
| **Linting** | [Ruff](https://docs.astral.sh/ruff) |
| **Type Checking** | [mypy](https://mypy-lang.org) — modo estricto |
| **Tests** | [pytest](https://pytest.org) + pytest-asyncio + httpx |
| **CI/CD** | [GitHub Actions](https://github.com/features/actions) |
| **Contenerización** | Docker + docker-compose |

### Inicio Rápido

```bash
# 1. Clonar
git clone https://github.com/davidgj98/ticket-classifier.git
cd ticket-classifier

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Descargar un modelo (ejemplo)
ollama pull phi4-mini

# 4. Iniciar el servidor
uvicorn app.main:app --reload --port 8000

# 5. Abrir en el navegador
open http://localhost:8000
```

### Docker (recomendado)

```bash
docker compose up --build
```

Inicia tanto Ollama como el clasificador. Visita `http://localhost:8000`.

### Endpoints de la API

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/` | Interfaz web |
| `POST` | `/classify` | Analizar una descripción de ticket |
| `POST` | `/tickets` | Crear un ticket desde la clasificación |
| `GET` | `/tickets` | Listar todos los tickets |
| `GET` | `/tickets/{id}` | Obtener un ticket específico |
| `PATCH` | `/tickets/{id}/status` | Actualizar el estado de un ticket |
| `DELETE` | `/tickets/{id}` | Eliminar un ticket |
| `GET` | `/health` | Estado de la conexión con Ollama |
| `GET` | `/models` | Listar modelos disponibles en Ollama |
| `GET` | `/export/csv` | Exportar tickets como CSV |
| `GET` | `/export/json` | Exportar tickets como JSON |

### Ejemplo

**Petición:**
```bash
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"text":"El icono de Internet tiene una cruz roja y el router tiene luces rojas parpadeando"}'
```

**Respuesta:**
```json
{
  "category": "Network",
  "priority": "High",
  "team": "Network Team",
  "summary": "Pérdida de conectividad WAN / Fallo de enlace en router local",
  "confidence": "High",
  "reasoning": "El usuario describe pérdida de conectividad junto con alertas físicas en el router, lo que apunta a un problema de red o hardware."
}
```

### Ejecutar Tests

```bash
pytest -v
```

### Configuración

Todas las opciones mediante variables de entorno (prefijo `TICKET_`):

| Variable | Por Defecto | Descripción |
|---|---|---|
| `TICKET_OLLAMA_URL` | `http://localhost:11434` | URL base de Ollama |
| `TICKET_DEFAULT_MODEL` | `phi4-mini:latest` | Modelo por defecto |
| `TICKET_LOG_LEVEL` | `INFO` | Nivel de logging |
| `TICKET_REQUEST_TIMEOUT` | `60.0` | Timeout de Ollama en segundos |

### Estructura del Proyecto

```
ticket-classifier/
├── app/
│   ├── main.py              # Punto de entrada FastAPI
│   ├── config.py            # Configuración con Pydantic
│   ├── models.py            # Modelos Pydantic
│   ├── routers/             # Routers de la API
│   ├── services/            # Lógica de negocio
│   └── static/              # Frontend
├── tests/                   # Suite de tests
├── Dockerfile + docker-compose.yml
├── pyproject.toml           # Ruff + mypy + pytest
└── .github/workflows/ci.yml # Pipeline CI
```

---

## License / Licencia

MIT &mdash; David Garcia Jodar

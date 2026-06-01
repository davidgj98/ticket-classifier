# 🎫 IT Ticket Classifier

AI-powered IT helpdesk ticket triage using local LLMs via Ollama. Classifies tickets by category, priority, and responsible team — no cloud APIs, no data leaving your network.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?style=flat-square)
![Ollama](https://img.shields.io/badge/Ollama-local-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-gray?style=flat-square)

## What it does

Paste any IT support ticket and get instant structured classification:

- **Category** — Hardware, Software, Network, Security, Access/IAM, Email, Database, Infrastructure
- **Priority** — Critical / High / Medium / Low
- **Team** — Which team should handle it
- **Summary** — One-sentence ticket summary
- **Confidence** — How certain the model is
- **Reasoning** — Why it classified it this way

## Why this matters

Manual ticket triage is slow and inconsistent. This tool lets a helpdesk automatically pre-classify incoming tickets before a human reviews them, reducing triage time and routing errors — all running locally, so sensitive IT data stays on-premise.

## Stack

| Layer | Tech |
|---|---|
| Backend | FastAPI + Python |
| AI inference | Ollama (local) |
| Models | Qwen2.5, DeepSeek, or any Ollama model |
| Frontend | Vanilla HTML/CSS/JS |

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) running locally
- At least one model pulled (e.g. `qwen2.5:latest`)

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/ticket-classifier
cd ticket-classifier

# 2. Install dependencies
pip install -r requirements.txt

# 3. Make sure Ollama is running and pull a model
ollama pull qwen2.5

# 4. Start the server
uvicorn main:app --reload --port 8000

# 5. Open in browser
open http://localhost:8000
```

## API

The classifier exposes a simple REST API you can integrate anywhere:

```bash
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "User cannot login to VPN since this morning, affects 20 people"}'
```

Response:
```json
{
  "category": "Network",
  "priority": "High",
  "team": "Network Team",
  "summary": "VPN access failure affecting 20 users since this morning",
  "confidence": "High",
  "reasoning": "VPN is a network service; 20 affected users with no access raises priority to High"
}
```

### Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Web interface |
| `POST` | `/classify` | Classify a ticket |
| `GET` | `/models` | List available Ollama models |
| `GET` | `/health` | Health check |

## Switching models

The web UI shows all models you have installed in Ollama. You can also specify the model in the API:

```json
{ "text": "...", "model": "deepseek-r1:7b" }
```

## Project structure

```
ticket-classifier/
├── main.py              # FastAPI backend
├── requirements.txt
├── static/
│   └── index.html       # Web interface
└── README.md
```

## Ideas to extend this project

- [ ] Batch classification via CSV upload
- [ ] Export results to CSV / JSON
- [ ] Webhook integration (ServiceNow, Jira, etc.)
- [ ] Confidence threshold alerts
- [ ] Classification history with SQLite
- [ ] Slack / Teams bot integration

## License

MIT

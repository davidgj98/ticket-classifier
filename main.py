from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import httpx
import json
import re

app = FastAPI(title="IT Ticket Classifier")

app.mount("/static", StaticFiles(directory="static"), name="static")


class TicketRequest(BaseModel):
    text: str
    model: str = "qwen2.5:latest"


class TicketResponse(BaseModel):
    category: str
    priority: str
    team: str
    summary: str
    confidence: str
    reasoning: str


SYSTEM_PROMPT = """You are an IT helpdesk ticket classifier. Analyze the ticket and return ONLY a JSON object with no extra text.

Categories: Hardware, Software, Network, Security, Access/IAM, Email, Database, Infrastructure, Other
Priorities: Critical, High, Medium, Low
Teams: Hardware Support, Software Support, Network Team, Security Team, IAM Team, Email Team, DBA Team, Infrastructure Team, General IT

Rules:
- Critical: system down, security breach, data loss affecting business
- High: major functionality broken, many users affected
- Medium: degraded performance, single user affected, workaround exists
- Low: cosmetic issues, feature requests, minor inconveniences

Return exactly this JSON structure:
{
  "category": "...",
  "priority": "...",
  "team": "...",
  "summary": "One sentence summary of the issue",
  "confidence": "High|Medium|Low",
  "reasoning": "Brief explanation of classification"
}"""


@app.get("/")
async def root():
    return FileResponse("static/index.html")


@app.post("/classify", response_model=TicketResponse)
async def classify_ticket(request: TicketRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Ticket text cannot be empty")

    payload = {
        "model": request.model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Classify this IT ticket:\n\n{request.text}"}
        ],
        "stream": False,
        "format": "json"
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post("http://localhost:11434/api/chat", json=payload)
            response.raise_for_status()
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Cannot connect to Ollama. Make sure it's running on port 11434.")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Ollama took too long to respond. Try a smaller model.")

    result = response.json()
    content = result["message"]["content"]

    try:
        data = json.loads(content)
        return TicketResponse(**data)
    except (json.JSONDecodeError, KeyError) as e:
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            return TicketResponse(**data)
        raise HTTPException(status_code=500, detail=f"Model returned invalid JSON: {content[:200]}")


@app.get("/models")
async def list_models():
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://localhost:11434/api/tags")
            response.raise_for_status()
            data = response.json()
            models = [m["name"] for m in data.get("models", [])]
            return {"models": models}
    except Exception:
        return {"models": ["qwen2.5:latest"]}


@app.get("/health")
async def health():
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.get("http://localhost:11434/api/tags")
        return {"status": "ok", "ollama": "connected"}
    except Exception:
        return {"status": "degraded", "ollama": "disconnected"}

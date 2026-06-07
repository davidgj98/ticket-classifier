import json
import logging
import re

import httpx

from app.config import get_settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are an IT helpdesk ticket classifier. Analyze the ticket"
    " and return ONLY a JSON object with no extra text.\n"
    "\n"
    "Categories: Hardware, Software, Network, Security, Access/IAM,"
    " Email, Database, Infrastructure, Other\n"
    "Priorities: Critical, High, Medium, Low\n"
    "Teams: Hardware Support, Software Support, Network Team,"
    " Security Team, IAM Team, Email Team, DBA Team,"
    " Infrastructure Team, General IT\n"
    "\n"
    "Rules:\n"
    "- Critical: system down, security breach, data loss affecting business\n"
    "- High: major functionality broken, many users affected\n"
    "- Medium: degraded performance, single user affected, workaround exists\n"
    "- Low: cosmetic issues, feature requests, minor inconveniences\n"
    "\n"
    "Return exactly this JSON structure:\n"
    '{\n'
    '  "category": "...",\n'
    '  "priority": "...",\n'
    '  "team": "...",\n'
    '  "summary": "One sentence summary of the issue",\n'
    '  "confidence": "High|Medium|Low",\n'
    '  "reasoning": "Brief explanation of classification"\n'
    "}"
)


class OllamaError(Exception):
    pass


class OllamaConnectionError(OllamaError):
    pass


class OllamaTimeoutError(OllamaError):
    pass


class OllamaResponseError(OllamaError):
    pass


class OllamaService:
    def __init__(self) -> None:
        settings = get_settings()
        self.base_url = settings.ollama_url

    async def classify(self, text: str, model: str) -> dict[str, str]:
        settings = get_settings()
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Classify this IT ticket:\n\n{text}"},
            ],
            "stream": False,
            "format": "json",
        }

        try:
            async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/chat", json=payload
                )
                response.raise_for_status()
        except httpx.ConnectError as e:
            raise OllamaConnectionError(
                "Cannot connect to Ollama. Make sure it's running on port 11434."
            ) from e
        except httpx.TimeoutException as e:
            raise OllamaTimeoutError(
                "Ollama took too long to respond. Try a smaller model."
            ) from e

        result = response.json()
        content = result["message"]["content"]

        try:
            data: dict[str, str] = json.loads(content)
            return data
        except (json.JSONDecodeError, KeyError) as e:
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return data
            raise OllamaResponseError(
                f"Model returned invalid JSON: {content[:200]}"
            ) from e

    async def list_models(self) -> list[str]:
        settings = get_settings()
        try:
            async with httpx.AsyncClient(timeout=settings.models_timeout) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                response.raise_for_status()
                data = response.json()
                models_raw = data.get("models", [])
                return [str(m["name"]) for m in models_raw]
        except Exception as e:
            logger.warning("Failed to fetch models from Ollama: %s", e)
            return []

    async def check_health(self) -> bool:
        settings = get_settings()
        try:
            async with httpx.AsyncClient(timeout=settings.health_timeout) as client:
                await client.get(f"{self.base_url}/api/tags")
            return True
        except Exception:
            return False

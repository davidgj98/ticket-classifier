import logging

from fastapi import APIRouter, HTTPException

from app.models import ClassifyRequest, ClassifyResponse, ErrorResponse
from app.services.ollama import (
    OllamaConnectionError,
    OllamaResponseError,
    OllamaService,
    OllamaTimeoutError,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["classify"])
ollama_service = OllamaService()


@router.post(
    "/classify",
    response_model=ClassifyResponse,
    responses={
        400: {"model": ErrorResponse},
        503: {"model": ErrorResponse},
        504: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def classify_ticket(request: ClassifyRequest) -> ClassifyResponse:
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Ticket text cannot be empty")

    try:
        data = await ollama_service.classify(request.text, request.model)
    except OllamaConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except OllamaTimeoutError as e:
        raise HTTPException(status_code=504, detail=str(e)) from e
    except OllamaResponseError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return ClassifyResponse(**data)

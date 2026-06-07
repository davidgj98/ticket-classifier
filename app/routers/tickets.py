from typing import Any

from fastapi import APIRouter, HTTPException, Query

from app.models import (
    ErrorResponse,
    StatusUpdateRequest,
    TicketCreateRequest,
    TicketListResponse,
    TicketResponse,
)
from app.services.tickets import TicketService

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post(
    "",
    response_model=TicketResponse,
    status_code=201,
    responses={500: {"model": ErrorResponse}},
)
async def create_ticket(body: TicketCreateRequest) -> dict[str, Any]:
    try:
        result = await TicketService.create(
            text=body.text,
            result={
                "category": body.category,
                "priority": body.priority,
                "team": body.team,
                "summary": body.summary,
                "confidence": body.confidence,
                "reasoning": body.reasoning,
            },
            model=body.model,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("", response_model=TicketListResponse)
async def list_tickets(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> TicketListResponse:
    tickets_raw, total = await TicketService.list_tickets(
        limit=limit, offset=offset
    )
    tickets = [TicketResponse(**t) for t in tickets_raw]
    return TicketListResponse(tickets=tickets, total=total)


@router.get(
    "/{ticket_id}",
    response_model=TicketResponse,
    responses={404: {"model": ErrorResponse}},
)
async def get_ticket(ticket_id: int) -> dict[str, Any]:
    ticket = await TicketService.get_ticket(ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.patch(
    "/{ticket_id}/status",
    response_model=TicketResponse,
    responses={404: {"model": ErrorResponse}, 422: {"model": ErrorResponse}},
)
async def update_ticket_status(
    ticket_id: int, body: StatusUpdateRequest
) -> dict[str, Any]:
    valid = {"Open", "In Progress", "Resolved", "Closed"}
    if body.status not in valid:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid status. Must be one of: {', '.join(sorted(valid))}",
        )
    ticket = await TicketService.update_status(ticket_id, body.status)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.delete(
    "/{ticket_id}",
    responses={404: {"model": ErrorResponse}},
)
async def delete_ticket(ticket_id: int) -> dict[str, str]:
    deleted = await TicketService.delete_ticket(ticket_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"detail": "Ticket deleted"}

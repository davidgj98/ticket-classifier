from datetime import datetime

from pydantic import BaseModel, Field


class ClassifyRequest(BaseModel):
    text: str = Field(..., min_length=1)
    model: str = "phi4-mini:latest"


class ClassifyResponse(BaseModel):
    category: str
    priority: str
    team: str
    summary: str
    confidence: str
    reasoning: str


class TicketCreateRequest(BaseModel):
    text: str
    category: str
    priority: str
    team: str
    summary: str
    confidence: str
    reasoning: str
    model: str = "phi4-mini:latest"


class StatusUpdateRequest(BaseModel):
    status: str = Field(..., pattern=r"^(Open|In Progress|Resolved|Closed)$")


class TicketResponse(BaseModel):
    id: int
    ticket_number: str
    text: str
    category: str
    priority: str
    team: str
    summary: str
    confidence: str
    reasoning: str
    model: str
    status: str
    created_at: datetime
    updated_at: datetime


class TicketListResponse(BaseModel):
    tickets: list[TicketResponse]
    total: int


class ErrorResponse(BaseModel):
    detail: str

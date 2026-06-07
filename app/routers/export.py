from fastapi import APIRouter
from fastapi.responses import JSONResponse, PlainTextResponse

from app.services.tickets import TicketService

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/csv", response_class=PlainTextResponse)
async def export_csv() -> PlainTextResponse:
    content = await TicketService.export_csv()
    return PlainTextResponse(
        content=content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=tickets.csv"},
    )


@router.get("/json", response_class=JSONResponse)
async def export_json() -> JSONResponse:
    content = await TicketService.export_json()
    return JSONResponse(
        content=content,
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=tickets.json"},
    )

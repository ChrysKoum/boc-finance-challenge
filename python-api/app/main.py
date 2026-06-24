import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import FinanceAskRequest, FinanceAskResponse
from app.services.finance_service import FinanceService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Bank of Cyprus Finance Challenge API",
    version="1.0.0",
)

cors_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "*").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

finance_service = FinanceService()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/finance/ask", response_model=FinanceAskResponse)
async def ask_finance_question(request: FinanceAskRequest) -> FinanceAskResponse:
    logger.info(
        "Received finance question correlationId=%s",
        request.correlation_id,
    )

    response = finance_service.answer(request)

    if response.blocked:
        logger.warning(
            "Blocked unsafe finance question correlationId=%s",
            request.correlation_id,
        )
    else:
        logger.info(
            "Answered finance question correlationId=%s",
            request.correlation_id,
        )

    return response

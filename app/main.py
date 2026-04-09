from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from app.api.exception_handlers import (
    upstream_error_handler,
    upstream_invalid_payload_handler,
    upstream_unavailable_handler,
)
from app.api.middleware.logging import RequestLoggingMiddleware
from app.api.routes.journeys import router
from app.core.config import settings
from app.domain.exceptions import (
    UpstreamAPIError,
    UpstreamInvalidPayloadError,
    UpstreamUnavailableError,
)
from app.infrastructure.clients.cached_flight_events_client import CachedFlightEventsClient
from app.infrastructure.clients.flight_events_client import FlightEventsClient
from app.infrastructure.logging.logger import get_logger, setup_logging

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(level=settings.log_level, fmt=settings.log_format)
    logger.info(
        "Starting Flight Journeys API",
        extra={
            "upstream": settings.flight_events_api_url,
            "cache_ttl": settings.cache_ttl_seconds,
        },
    )

    async with httpx.AsyncClient(
        base_url=settings.flight_events_api_url,
        timeout=10.0,
    ) as http_client:
        raw_client = FlightEventsClient(http_client)
        app.state.flight_client = CachedFlightEventsClient(
            raw_client,
            ttl_seconds=settings.cache_ttl_seconds,
        )
        yield

    logger.info("Shutting down")


app = FastAPI(
    title="Flight Journeys API",
    description="Busca viajes de uno o dos vuelos entre origen y destino.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(RequestLoggingMiddleware)
app.add_exception_handler(UpstreamAPIError, upstream_error_handler)
app.add_exception_handler(UpstreamUnavailableError, upstream_unavailable_handler)
app.add_exception_handler(UpstreamInvalidPayloadError, upstream_invalid_payload_handler)
app.include_router(router)


@app.get("/health", tags=["ops"])
def health() -> dict:
    return {"status": "ok"}
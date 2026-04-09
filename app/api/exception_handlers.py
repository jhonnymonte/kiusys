from fastapi import Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    UpstreamAPIError,
    UpstreamInvalidPayloadError,
    UpstreamUnavailableError,
)
from app.infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


async def upstream_error_handler(request: Request, exc: UpstreamAPIError) -> JSONResponse:
    logger.error(
        "Upstream bad gateway",
        extra={"detail": str(exc), "path": request.url.path},
    )
    return JSONResponse(status_code=502, content={"detail": str(exc)})


async def upstream_unavailable_handler(
    request: Request,
    exc: UpstreamUnavailableError,
) -> JSONResponse:
    logger.error(
        "Upstream unavailable",
        extra={"detail": str(exc), "path": request.url.path},
    )
    return JSONResponse(status_code=503, content={"detail": str(exc)})


async def upstream_invalid_payload_handler(
    request: Request,
    exc: UpstreamInvalidPayloadError,
) -> JSONResponse:
    logger.error(
        "Upstream invalid payload",
        extra={"detail": str(exc), "path": request.url.path},
    )
    return JSONResponse(status_code=502, content={"detail": str(exc)})
import httpx
from pydantic import ValidationError

from app.domain.entities import FlightEvent
from app.domain.exceptions import (
    UpstreamAPIError,
    UpstreamInvalidPayloadError,
    UpstreamUnavailableError,
)
from app.infrastructure.logging.logger import get_logger
from app.schemas.external import FlightEventExternal

logger = get_logger(__name__)


class FlightEventsClient:
    def __init__(self, http_client: httpx.AsyncClient) -> None:
        self._client = http_client

    async def get_events(self) -> list[FlightEvent]:
        logger.debug("Fetching flight events for Upstream API")
        try:
            response = await self._client.get("/flight-events")
            response.raise_for_status()
        except httpx.TimeoutException as exc:
            logger.error("Upstream timed out", extra={"error": str(exc)})
            raise UpstreamUnavailableError("Flight-events API timed out") from exc
        except httpx.ConnectError as exc:
            logger.error("Cannot connect to upstream", extra={"error": str(exc)})
            raise UpstreamUnavailableError("Cannot connect to flight-events API") from exc
        except httpx.HTTPStatusError as exc:
            logger.warning(
                "Upstream returned error status",
                extra={"status_code": exc.response.status_code},
            )
            raise UpstreamAPIError(f"Upstream returned {exc.response.status_code}") from exc

        events = self._parse(response.json())
        logger.info("Flight events fetched", extra={"count": len(events)})
        return events

    def _parse(self, data: list[dict]) -> list[FlightEvent]:
        result = []
        for item in data:
            try:
                parsed = FlightEventExternal(**item)
                event = FlightEvent(
                    flight_number=parsed.flight_number,
                    departure_city=parsed.departure_city,
                    arrival_city=parsed.arrival_city,
                    departure_datetime=parsed.departure_datetime,
                    arrival_datetime=parsed.arrival_datetime,
                )

            except ValidationError as exc:
                logger.error("Upstream returned invalid schema", extra={"error": str(exc)})
                raise UpstreamInvalidPayloadError(f"Unexpected upstream schema: {exc}") from exc
            except ValueError as exc:
                logger.error("Upstream returned incoherent data", extra={"error": str(exc)})
                raise UpstreamInvalidPayloadError(str(exc)) from exc

            result.append(event)

        return result

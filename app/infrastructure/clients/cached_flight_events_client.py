import asyncio
import time

from app.domain.entities import FlightEvent
from app.infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class CachedFlightEventsClient:
    """
    A decorator for FlightEventsClient that adds an in-memory cache with a TTL.

    The lock prevents cache stampedes: if the cache has expired and N simultaneous requests arrive,
    only the first one fetches the data from the upstream server. The others wait
    and reuse the result.

    """

    def __init__(self, client, ttl_seconds: int = 300) -> None:
        self._client = client
        self._ttl = ttl_seconds
        self._cache: list[FlightEvent] | None = None
        self._cached_at: float = 0.0
        self._lock = asyncio.Lock()

    async def get_events(self) -> list[FlightEvent]:
        if self._is_valid():
            logger.debug("Cache hit for flight events")
            return self._cache  # type: ignore[return-value]

        async with self._lock:
            if self._is_valid():
                logger.debug("Cache hit after lock (populated by concurrent request)")
                return self._cache  # type: ignore[return-value]

            logger.info("Cache miss - fetching from upstream", extra={"ttl": self._ttl})
            self._cache = await self._client.get_events()
            self._cached_at = time.monotonic()
            return self._cache

    def _is_valid(self) -> bool:
        return self._cache is not None and (time.monotonic() - self._cached_at) < self._ttl

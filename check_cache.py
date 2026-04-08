import asyncio

from app.infrastructure.clients.cached_flight_events_client import CachedFlightEventsClient
from app.infrastructure.logging.logger import setup_logging


class FakeClient:
    def __init__(self):
        self.call_count = 0

    async def get_events(self):
        self.call_count += 1
        return ["event1", "event2"]


async def main():
    setup_logging(level="DEBUG", fmt="text")

    raw_client = FakeClient()
    cached_client = CachedFlightEventsClient(raw_client, ttl_seconds=60)

    result1 = await cached_client.get_events()
    result2 = await cached_client.get_events()

    print("first result:", result1)
    print("second result:", result2)
    print("upstream calls:", raw_client.call_count)


if __name__ == "__main__":
    asyncio.run(main())
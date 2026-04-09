import asyncio

import httpx

from app.infrastructure.clients.flight_events_client import FlightEventsClient
from app.infrastructure.logging.logger import setup_logging

MOCK_EVENTS = [
    {
        "flight_number": "XX1234",
        "departure_city": "BUE",
        "arrival_city": "MAD",
        "departure_datetime": "2025-09-12T12:00:00Z",
        "arrival_datetime": "2025-09-13T00:00:00Z",
    },
    {
        "flight_number": "XX2345",
        "departure_city": "MAD",
        "arrival_city": "PMI",
        "departure_datetime": "2025-09-13T02:00:00Z",
        "arrival_datetime": "2025-09-13T03:00:00Z",
    },
]


def handler(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/flight-events":
        return httpx.Response(200, json=MOCK_EVENTS)
    return httpx.Response(404, json={"detail": "not found"})


async def main():
    setup_logging(level="DEBUG", fmt="text")

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(
        base_url="http://testserver",
        transport=transport,
    ) as http_client:
        client = FlightEventsClient(http_client)
        events = await client.get_events()

    print(f"events fetched: {len(events)}")
    for event in events:
        print(event)


if __name__ == "__main__":
    asyncio.run(main())

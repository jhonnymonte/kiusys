import httpx
import pytest
from httpx import ASGITransport, AsyncClient

from app.infrastructure.clients.cached_flight_events_client import CachedFlightEventsClient
from app.infrastructure.clients.flight_events_client import FlightEventsClient
from app.main import app

SAMPLE_EVENTS = [
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


@pytest.fixture
async def async_client():
    async with httpx.AsyncClient(base_url="http://localhost:8001") as http_client:
        raw_client = FlightEventsClient(http_client)
        app.state.flight_client = CachedFlightEventsClient(raw_client, ttl_seconds=0)

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            yield client

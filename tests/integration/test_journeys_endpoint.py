import httpx
import respx
from httpx import Response

from tests.conftest import SAMPLE_EVENTS

BASE = "http://localhost:8001"
SEARCH = "/journeys/search"


@respx.mock
async def test_direct_journey(async_client):
    respx.get(f"{BASE}/flight-events").mock(
        return_value=Response(200, json=SAMPLE_EVENTS)
    )
    resp = await async_client.get(
        SEARCH,
        params={"date": "2025-09-12", "from": "BUE", "to": "MAD"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body[0]["connections"] == 1
    assert body[0]["path"][0]["from"] == "BUE"
    assert body[0]["path"][0]["to"] == "MAD"


@respx.mock
async def test_connecting_journey(async_client):
    respx.get(f"{BASE}/flight-events").mock(
        return_value=Response(200, json=SAMPLE_EVENTS)
    )
    resp = await async_client.get(
        SEARCH,
        params={"date": "2025-09-12", "from": "BUE", "to": "PMI"},
    )
    assert resp.status_code == 200
    assert resp.json()[0]["connections"] == 2


@respx.mock
async def test_missing_date_returns_422(async_client):
    resp = await async_client.get(SEARCH, params={"from": "BUE", "to": "MAD"})
    assert resp.status_code == 422


@respx.mock
async def test_same_origin_destination_returns_400(async_client):
    respx.get(f"{BASE}/flight-events").mock(return_value=Response(200, json=[]))
    resp = await async_client.get(
        SEARCH,
        params={"date": "2025-09-12", "from": "BUE", "to": "BUE"},
    )
    assert resp.status_code == 400


@respx.mock
async def test_upstream_500_returns_502(async_client):
    respx.get(f"{BASE}/flight-events").mock(return_value=Response(500))
    resp = await async_client.get(
        SEARCH,
        params={"date": "2025-09-12", "from": "BUE", "to": "MAD"},
    )
    assert resp.status_code == 502


@respx.mock
async def test_upstream_unreachable_returns_503(async_client):
    respx.get(f"{BASE}/flight-events").mock(
        side_effect=httpx.ConnectError("refused")
    )
    resp = await async_client.get(
        SEARCH,
        params={"date": "2025-09-12", "from": "BUE", "to": "MAD"},
    )
    assert resp.status_code == 503


@respx.mock
async def test_upstream_timeout_returns_503(async_client):
    respx.get(f"{BASE}/flight-events").mock(
        side_effect=httpx.TimeoutException("timeout")
    )
    resp = await async_client.get(
        SEARCH,
        params={"date": "2025-09-12", "from": "BUE", "to": "MAD"},
    )
    assert resp.status_code == 503
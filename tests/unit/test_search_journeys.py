from datetime import date, datetime, timezone

from app.application.use_cases.search_journeys import SearchJourneysUseCase
from app.domain.entities import FlightEvent


def dt(year, month, day, hour, minute=0):
    return datetime(year, month, day, hour, minute, tzinfo=timezone.utc)


def event(fn, dep, arr, dep_dt, arr_dt):
    return FlightEvent(fn, dep, arr, dep_dt, arr_dt)


class StubClient:
    def __init__(self, events):
        self._events = events

    async def get_events(self):
        return self._events


async def test_direct_flight_found():
    events = [event("XX1", "BUE", "MAD", dt(2025, 9, 12, 12), dt(2025, 9, 12, 20))]
    result = await SearchJourneysUseCase(StubClient(events)).execute(
        date(2025, 9, 12), "BUE", "MAD"
    )
    assert len(result) == 1
    assert result[0].connections == 1
    assert result[0].path[0].flight_number == "XX1"


async def test_connecting_flight_valid():
    events = [
        event("XX1", "BUE", "MAD", dt(2025, 9, 12, 12), dt(2025, 9, 13, 0)),
        event("XX2", "MAD", "PMI", dt(2025, 9, 13, 2), dt(2025, 9, 13, 3)),
    ]
    result = await SearchJourneysUseCase(StubClient(events)).execute(
        date(2025, 9, 12), "BUE", "PMI"
    )
    assert len(result) == 1
    assert result[0].connections == 2


async def test_connection_over_4h_discarded():
    events = [
        event("XX1", "BUE", "MAD", dt(2025, 9, 12, 12), dt(2025, 9, 13, 0)),
        event("XX2", "MAD", "PMI", dt(2025, 9, 13, 5), dt(2025, 9, 13, 6)),
    ]
    result = await SearchJourneysUseCase(StubClient(events)).execute(
        date(2025, 9, 12), "BUE", "PMI"
    )
    assert result == []


async def test_total_duration_over_24h_discarded():
    events = [
        event("XX1", "BUE", "MAD", dt(2025, 9, 12, 0), dt(2025, 9, 12, 20)),
        event("XX2", "MAD", "PMI", dt(2025, 9, 12, 22), dt(2025, 9, 13, 1)),
    ]
    result = await SearchJourneysUseCase(StubClient(events)).execute(
        date(2025, 9, 12), "BUE", "PMI"
    )
    assert result == []


async def test_no_results_unknown_route():
    events = [event("XX1", "BUE", "MAD", dt(2025, 9, 12, 12), dt(2025, 9, 12, 20))]
    result = await SearchJourneysUseCase(StubClient(events)).execute(
        date(2025, 9, 12), "BUE", "XXX"
    )
    assert result == []


async def test_wrong_date_returns_empty():
    events = [event("XX1", "BUE", "MAD", dt(2025, 9, 12, 12), dt(2025, 9, 12, 20))]
    result = await SearchJourneysUseCase(StubClient(events)).execute(
        date(2025, 9, 13), "BUE", "MAD"
    )
    assert result == []
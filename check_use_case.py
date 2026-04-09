import asyncio
from datetime import date, datetime, timezone

from app.application.use_cases.search_journeys import SearchJourneysUseCase
from app.domain.entities import FlightEvent


def dt(year, month, day, hour, minute=0):
    return datetime(year, month, day, hour, minute, tzinfo=timezone.utc)


class StubClient:
    async def get_events(self):
        return [
            FlightEvent(
                flight_number="XX1234",
                departure_city="BUE",
                arrival_city="MAD",
                departure_datetime=dt(2025, 9, 12, 12),
                arrival_datetime=dt(2025, 9, 13, 0),
            ),
            FlightEvent(
                flight_number="XX2345",
                departure_city="MAD",
                arrival_city="PMI",
                departure_datetime=dt(2025, 9, 13, 2),
                arrival_datetime=dt(2025, 9, 13, 3),
            ),
        ]


async def main():
    use_case = SearchJourneysUseCase(StubClient())

    direct = await use_case.execute(date(2025, 9, 12), "BUE", "MAD")
    connected = await use_case.execute(date(2025, 9, 12), "BUE", "PMI")

    print("direct journeys:", len(direct))
    for journey in direct:
        print(
            "  connections:", journey.connections, "path:", [f.flight_number for f in journey.path]
        )

    print("connected journeys:", len(connected))
    for journey in connected:
        print(
            "  connections:", journey.connections, "path:", [f.flight_number for f in journey.path]
        )


if __name__ == "__main__":
    asyncio.run(main())

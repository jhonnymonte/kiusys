from datetime import datetime, timezone

from app.domain.entities import FlightEvent, Journey
from app.schemas.response import JourneyResponse

event1 = FlightEvent(
    flight_number="XX1234",
    departure_city="BUE",
    arrival_city="MAD",
    departure_datetime=datetime(2025, 9, 12, 12, 0, tzinfo=timezone.utc),
    arrival_datetime=datetime(2025, 9, 13, 0, 0, tzinfo=timezone.utc),
)

event2 = FlightEvent(
    flight_number="XX2345",
    departure_city="MAD",
    arrival_city="PMI",
    departure_datetime=datetime(2025, 9, 13, 2, 0, tzinfo=timezone.utc),
    arrival_datetime=datetime(2025, 9, 13, 3, 0, tzinfo=timezone.utc),
)

journey = Journey(path=[event1, event2])

response = JourneyResponse.from_domain(journey)

print(response.model_dump())
print(response.model_dump(by_alias=True))

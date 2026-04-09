from datetime import datetime, timezone

from app.domain.entities import FlightEvent
from app.domain.rules import is_valid_connection

e1 = FlightEvent(
    flight_number="XX1234",
    departure_city="BUE",
    arrival_city="MAD",
    departure_datetime=datetime(2025, 9, 12, 12, 0, tzinfo=timezone.utc),
    arrival_datetime=datetime(2025, 9, 13, 0, 0, tzinfo=timezone.utc),
)

e2 = FlightEvent(
    flight_number="XX2345",
    departure_city="MAD",
    arrival_city="PMI",
    departure_datetime=datetime(2025, 9, 13, 2, 0, tzinfo=timezone.utc),
    arrival_datetime=datetime(2025, 9, 13, 3, 0, tzinfo=timezone.utc),
)

print("valid connection:", is_valid_connection(e1, e2, "PMI"))

try:
    bad = FlightEvent(
        flight_number="BAD1",
        departure_city="BUE",
        arrival_city="MAD",
        departure_datetime=datetime(2025, 9, 13, 5, 0, tzinfo=timezone.utc),
        arrival_datetime=datetime(2025, 9, 13, 3, 0, tzinfo=timezone.utc),
    )
except ValueError as exc:
    print("invalid flight rejected correctly:", exc)

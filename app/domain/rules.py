from datetime import timedelta

from app.domain.entities import FlightEvent

MAX_CONNECTION_WAIT = timedelta(hours=4)
MAX_JOURNEY_DURATION = timedelta(hours=24)


def is_valid_connection(e1: FlightEvent, e2: FlightEvent, destination: str) -> bool:
    if e1.arrival_city != e2.departure_city:
        return False
    if e2.arrival_city != destination:
        return False

    wait = e2.departure_datetime - e1.arrival_datetime
    if wait.total_seconds() < 0 or wait > MAX_CONNECTION_WAIT:
        return False

    if (e2.arrival_datetime - e1.departure_datetime) > MAX_JOURNEY_DURATION:
        return False

    return True

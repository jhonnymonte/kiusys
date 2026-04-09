from fastapi import FastAPI

app = FastAPI(title="Mock Flight Events API")

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
    {
        "flight_number": "IB0001",
        "departure_city": "MAD",
        "arrival_city": "BUE",
        "departure_datetime": "2021-12-31T23:59:59Z",
        "arrival_datetime": "2022-01-01T16:00:00Z",
    },
]


@app.get("/flight-events")
def get_flight_events():
    return MOCK_EVENTS

# Flight Journeys API

REST API to search journeys between cities using direct flights or a single connection, applying business rules for connection times and total duration.

---

## Overview

This service builds journeys between an origin and destination from flight events fetched from an external service (`/flight-events`).

### Key features

- Support for direct flights and one-connection journeys
- Business rules for max layover and total trip duration
- In-memory cache with TTL
- REST API built with FastAPI
- Unit + integration tests
- Docker + Docker Compose ready to run

---

## Configuration

Create a local `.env` file based on the example:

```bash
cp .env.example .env
```

Environment variables:

| Variable | Default | Description |
|---|---:|---|
| `FLIGHT_EVENTS_API_URL` | `http://localhost:8001` | Upstream base URL for flight events |
| `LOG_LEVEL` | `INFO` | Log level |
| `LOG_FORMAT` | `text` | `text` or `json` |
| `CACHE_TTL_SECONDS` | `300` | Cache TTL in seconds |

---

## Architecture

The project follows a Clean / Hexagonal Architecture approach:

```
app/
├── domain/         # Entities + business rules
├── application/    # Use cases
├── infrastructure/ # HTTP client, cache, logging
├── api/            # FastAPI (routes, middleware, handlers)
└── core/           # Configuration
```

### Applied principles

- Separation of concerns
- Low coupling
- High testability
- Framework independence

---

## Main endpoint

### `GET /journeys/search`

**Query params**

| Param | Type   | Description |
|-------|--------|-------------|
| date  | string | Departure date (YYYY-MM-DD) |
| from  | string | Origin city code |
| to    | string | Destination city code |

**Example**

```bash
curl "http://localhost:8000/journeys/search?date=2025-09-12&from=BUE&to=PMI"
```

**Response**

```json
[
  {
    "connections": 2,
    "path": [
      {
        "flight_number": "XX1234",
        "from": "BUE",
        "to": "MAD",
        "departure_time": "2025-09-12 12:00",
        "arrival_time": "2025-09-13 00:00"
      },
      {
        "flight_number": "XX2345",
        "from": "MAD",
        "to": "PMI",
        "departure_time": "2025-09-13 02:00",
        "arrival_time": "2025-09-13 03:00"
      }
    ]
  }
]
```

---

## Business rules

- Only flights departing on the requested date are considered
- Direct flights and journeys with a single connection are allowed
- Constraints:
  - Layover between flights ≤ 4 hours
  - Total journey duration ≤ 24 hours
  - Origin and destination must be different

---

## Cache

In-memory cache with TTL:

- Avoids repeated upstream calls
- Configurable TTL (`CACHE_TTL_SECONDS`)
- Protected against cache stampede with an async lock

---

## Error handling

| Upstream error | API response |
|---|---|
| 5xx | 502 Bad Gateway |
| Timeout / connection | 503 Service Unavailable |
| Invalid payload | 502 |

---

## Testing

### Unit tests

- Business-rule validation
- Edge cases

### Integration tests

- `/journeys/search` endpoint
- Upstream mocked with `respx`

```bash
pytest tests/ -v
```

---

## Docker

```bash
docker compose up --build
```

Services:

- API → http://localhost:8000
- Mock → http://localhost:8001

```bash
curl http://localhost:8000/health
```

---

## Local development

```bash
make install   # install dependencies
make run       # start API
make mock      # start mock
```

---

## Code Quality

```bash
make format    # black
make lint      # ruff
make check     # format + lint
```

---

## Design decisions

### No database

No database is used because the upstream is the source of truth, persistence is not required, and an in-memory cache is sufficient for this use case.

### Protocols (ports)

An interface (`FlightEventsProvider`) is defined to decouple the HTTP client, allow mocks in tests, and apply decorators such as caching.

### Cache as a decorator

Caching is implemented in the infrastructure layer, does not leak into the domain, and can be replaced easily (e.g., Redis).

### Domain validations

Rules live in `domain/`, avoiding duplication and keeping consistency.

### Flight event identification

A flight event is identified by its flight number and operating date. Each event is independent and no additional deduplication is required since the upstream is the source of truth.

---

## Future improvements

- Support for multiple connections (graph)
- Distributed cache (Redis)
- Circuit breaker
- Metrics (Prometheus)
- Rate limiting

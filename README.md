# Flight Journeys API

API REST para buscar viajes entre ciudades utilizando vuelos directos o con una única conexión, aplicando reglas de negocio sobre tiempos de conexión y duración total.

---

## Overview

Este servicio permite construir journeys entre un origen y destino a partir de eventos de vuelos obtenidos desde un servicio externo (`/flight-events`).

### Características principales

- Soporte para vuelos directos y vuelos con una conexión
- Reglas de negocio sobre tiempo máximo de espera y duración total del viaje
- Cache en memoria con TTL
- API REST construida con FastAPI
- Tests unitarios e integración
- Docker + Docker Compose listos para ejecutar

---

## Arquitectura

Se implementa una arquitectura basada en Clean / Hexagonal Architecture:

```
app/
├── domain/         # Entidades + reglas de negocio
├── application/    # Casos de uso
├── infrastructure/ # HTTP client, cache, logging
├── api/            # FastAPI (routes, middleware, handlers)
└── core/           # Configuración
```

### Principios aplicados

- Separación de responsabilidades
- Bajo acoplamiento
- Alta testabilidad
- Independencia del framework

---

## Endpoint principal

### `GET /journeys/search`

**Query params**

| Param | Tipo   | Descripción                    |
|-------|--------|--------------------------------|
| date  | string | Fecha de salida (YYYY-MM-DD)   |
| from  | string | Código de ciudad origen        |
| to    | string | Código de ciudad destino       |

**Ejemplo**

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

## Reglas de negocio

- Solo se consideran vuelos cuya salida ocurre en la fecha solicitada
- Se permiten vuelos directos y vuelos con una única conexión
- Restricciones:
  - Espera entre vuelos ≤ 4 horas
  - Duración total ≤ 24 horas
  - Origen y destino deben ser distintos

---

## Cache

Se implementa cache en memoria con TTL:

- Evita múltiples llamadas al upstream
- TTL configurable (`CACHE_TTL_SECONDS`)
- Protegido contra cache stampede con lock async

---

## Manejo de errores

| Error upstream        | Respuesta API         |
|-----------------------|-----------------------|
| 5xx                   | 502 Bad Gateway       |
| Timeout / conexión    | 503 Service Unavailable |
| Payload inválido      | 502                   |

---

## Testing

### Unit tests

- Validación de reglas de negocio
- Edge cases

### Integration tests

- Endpoint `/journeys/search`
- Mock del upstream con `respx`

```bash
pytest tests/ -v
```

---

## Docker

```bash
docker compose up --build
```

Servicios:

- API → http://localhost:8000
- Mock → http://localhost:8001

```bash
curl http://localhost:8000/health
```

---

## Desarrollo local

```bash
make install   # instalar dependencias
make run       # levantar API
make mock      # levantar mock
```

---

## Code Quality

```bash
make format    # black
make lint      # ruff
make check     # format + lint
```

---

## Decisiones de diseño

### Sin base de datos

No se utiliza base de datos porque el upstream es la fuente de verdad, no se requiere persistencia, y el cache en memoria es suficiente para este caso.

### Uso de Protocol (ports)

Se define una interfaz (`FlightEventsProvider`) que permite desacoplar el cliente HTTP, usar mocks en tests, y aplicar decorators como cache.

### Cache como decorator

El cache se implementa en infraestructura, no contamina el dominio, y permite reemplazo fácil (ej: Redis).

### Validaciones en dominio

Las reglas viven en `domain/`, lo que evita duplicación y mantiene consistencia.

### Identificación de eventos de vuelo

Un evento de vuelo se identifica por su número de vuelo y fecha de operación. Cada evento es independiente y no se requiere deduplicación adicional ya que el upstream es la fuente de verdad.

---

## Mejoras futuras

- Soporte para múltiples conexiones (grafo)
- Cache distribuido (Redis)
- Circuit breaker
- Métricas (Prometheus)
- Rate limiting


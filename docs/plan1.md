# Plan de trabajo — API REST FastAPI + Neon + Menú CRUD (Entrega: Domingo 8 de marzo)

Este documento define un plan **vertical** (para aprender) donde cada integrante implementa **modelos + schemas + endpoints + cliente HTTP + submenú CLI** para sus entidades, y una persona integra el menú principal y registra los routers.

Repositorio: `Nicogrih/airport-app`  
Ramas ya creadas: `dev`, `qa`, `prod`  
Estructura actual del proyecto (confirmada):

```text
app/
  crud/
  database/
  endpoints/
  models/
  schemas/
  app.py      # servidor FastAPI
  main.py     # menú CLI
```

---

## 1) Objetivo de la entrega

Construir una aplicación que:

1. Exponga una **API REST** con **FastAPI**.
2. Se ejecute con **Uvicorn**.
3. Se conecte a **PostgreSQL en Neon** usando **SQLAlchemy async + asyncpg**.
4. Tenga entre **6 y 10 entidades** (usaremos **6** para llegar a tiempo).
5. Incluya un **menú por consola** que haga CRUD **consumiendo la API por HTTP** (NO DB directa).
6. Cumpla PEP8 y docstrings relevantes.
7. Use flujo Git con PRs sobre ramas `dev`, `qa`, `prod`.

---

## 2) Entidades (6) y relaciones (definitivas)

Entidades confirmadas:

- `users`
- `airlines`
- `airports`
- `flights`
- `reservations`
- `passengers`

Relaciones (claves foráneas):

- `flights.airline_id -> airlines.id`
- `flights.origin_airport_id -> airports.id`
- `flights.destination_airport_id -> airports.id`
- `reservations.user_id -> users.id`
- `passengers.reservation_id -> reservations.id`

IDs: **UUID v4** para todas.

---

## 3) Base de datos (Neon) — `scripts/schema.sql`

> Ejecutar en Neon SQL Editor.  
> Requisito: `pgcrypto` para `gen_random_uuid()`.

```sql
-- airport-app - Demo schema (6 entidades)
-- Neon PostgreSQL - UUID v4

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ===== 1) users =====
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT NOT NULL UNIQUE,
  full_name TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'CLIENT' CHECK (role IN ('CLIENT', 'ADMIN')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ===== 2) airlines =====
CREATE TABLE IF NOT EXISTS airlines (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  code TEXT NOT NULL UNIQUE,     -- e.g. "AV"
  name TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ===== 3) airports =====
CREATE TABLE IF NOT EXISTS airports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  code TEXT NOT NULL UNIQUE,     -- IATA e.g. "BOG"
  name TEXT NOT NULL,
  country TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ===== 4) flights =====
CREATE TABLE IF NOT EXISTS flights (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  airline_id UUID NOT NULL REFERENCES airlines(id) ON DELETE RESTRICT,
  flight_number TEXT NOT NULL, -- e.g. "AV123"
  origin_airport_id UUID NOT NULL REFERENCES airports(id) ON DELETE RESTRICT,
  destination_airport_id UUID NOT NULL REFERENCES airports(id) ON DELETE RESTRICT,
  departure_at TIMESTAMPTZ NOT NULL,
  arrival_at TIMESTAMPTZ NOT NULL,
  status TEXT NOT NULL DEFAULT 'SCHEDULED'
    CHECK (status IN ('SCHEDULED', 'RESCHEDULED', 'CANCELED')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT chk_flights_airports_different CHECK (origin_airport_id <> destination_airport_id),
  CONSTRAINT chk_flights_time_order CHECK (arrival_at > departure_at),
  UNIQUE (airline_id, flight_number, departure_at)
);

CREATE INDEX IF NOT EXISTS idx_flights_origin_departure
  ON flights (origin_airport_id, departure_at);

CREATE INDEX IF NOT EXISTS idx_flights_destination_arrival
  ON flights (destination_airport_id, arrival_at);

-- ===== 5) reservations =====
CREATE TABLE IF NOT EXISTS reservations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
  status TEXT NOT NULL DEFAULT 'HOLD'
    CHECK (status IN ('HOLD', 'CONFIRMED', 'CANCELED', 'EXPIRED')),
  total_amount_cop INTEGER NOT NULL DEFAULT 0 CHECK (total_amount_cop >= 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_reservations_user_created
  ON reservations (user_id, created_at DESC);

-- ===== 6) passengers =====
CREATE TABLE IF NOT EXISTS passengers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  reservation_id UUID NOT NULL REFERENCES reservations(id) ON DELETE CASCADE,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  document_number TEXT NOT NULL,
  birth_date DATE NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_passengers_reservation
  ON passengers (reservation_id);
```

---

## 4) Contrato de API (campos mínimos por entidad)

### Users

- POST `/api/users`: `email`, `full_name`, `role?`
- PUT `/api/users/{id}`: `email?`, `full_name?`, `role?`
- Read: `id`, `email`, `full_name`, `role`, `created_at`

### Airlines

- POST `/api/airlines`: `code`, `name`
- PUT `/api/airlines/{id}`: `code?`, `name?`
- Read: `id`, `code`, `name`, `created_at`

### Airports

- POST `/api/airports`: `code`, `name`, `country`
- PUT `/api/airports/{id}`: `code?`, `name?`, `country?`
- Read: `id`, `code`, `name`, `country`, `created_at`

### Flights

- POST `/api/flights`:
  - `airline_id`, `flight_number`,
  - `origin_airport_id`, `destination_airport_id`,
  - `departure_at`, `arrival_at`,
  - `status?`
- PUT `/api/flights/{id}`: mismos campos opcionales
- Read: todos los campos + `created_at`

### Reservations

- POST `/api/reservations`: `user_id`, `status?`, `total_amount_cop?`
- PUT `/api/reservations/{id}`: `user_id?`, `status?`, `total_amount_cop?`
- Read: `id`, `user_id`, `status`, `total_amount_cop`, `created_at`

### Passengers

- POST `/api/passengers`:
  - `reservation_id`, `first_name`, `last_name`, `document_number`, `birth_date?`
- PUT `/api/passengers/{id}`: campos opcionales
- Read: todos los campos + `created_at`

---

## 5) Rutas REST obligatorias (por entidad)

Cada entidad debe tener:

- `GET /api/<resource>` (listar)
- `GET /api/<resource>/{id}` (obtener por id)
- `POST /api/<resource>` (crear)
- `PUT /api/<resource>/{id}` (actualizar)
- `DELETE /api/<resource>/{id}` (eliminar)

Recursos:

- `/api/users`
- `/api/airlines`
- `/api/airports`
- `/api/flights`
- `/api/reservations`
- `/api/passengers`

---

## 6) Menú por consola (CRUD vía HTTP, para las 6 entidades)

Reglas:

- El menú **NO** usa SQLAlchemy ni toca DB.
- El menú llama los endpoints por HTTP (ideal: `httpx`).
- Se ejecuta: `python -m app.main`
- El servidor se ejecuta aparte: `uvicorn app.app:app --reload`

Recomendación para evitar conflictos:

- Cada integrante implementa un **submenú** propio y el integrador solo “enchufa” en `main.py`.

Archivos sugeridos:

- `app/crud/menu_airlines_airports.py`
- `app/crud/menu_users_reservations.py`
- `app/crud/menu_flights_passengers.py`

---

## 7) Plan de reparto (vertical: todos aprenden)

### Integrante 1: Airlines + Airports

Implementa para ambas entidades:

- `app/models/airline.py`, `app/models/airport.py`
- `app/schemas/airlines.py`, `app/schemas/airports.py`
- `app/endpoints/airlines.py`, `app/endpoints/airports.py`
- `app/crud/airlines.py`, `app/crud/airports.py`
- `app/crud/menu_airlines_airports.py`

PR: `feat-dev/airlines-airports-vertical`

---

### Integrante 2: Users + Reservations

Implementa para ambas entidades:

- `app/models/user.py`, `app/models/reservation.py`
- `app/schemas/users.py`, `app/schemas/reservations.py`
- `app/endpoints/users.py`, `app/endpoints/reservations.py`
- `app/crud/users.py`, `app/crud/reservations.py`
- `app/crud/menu_users_reservations.py`

PR: `feat-dev/users-reservations-vertical`

---

### Integrante 3: Flights + Passengers

Implementa para ambas entidades:

- `app/models/flight.py`, `app/models/passenger.py`
- `app/schemas/flights.py`, `app/schemas/passengers.py`
- `app/endpoints/flights.py`, `app/endpoints/passengers.py`
- `app/crud/flights.py`, `app/crud/passengers.py`
- `app/crud/menu_flights_passengers.py`

PR: `feat-dev/flights-passengers-vertical`

---

## 8) Archivos compartidos (evitar conflictos)

Asignar un **integrador** (recomendado: Integrante 1) como único que edita:

- `app/app.py` (registrar routers de todas las entidades)
- `app/crud/http_client.py` (cliente base con `httpx`)
- `app/main.py` (menú principal que llama los submenús)

Los demás NO modifican esos archivos, solo crean módulos nuevos.

---

## 9) Flujo Git (obligatorio)

Ramas principales:

- `dev` (desarrollo)
- `qa` (pruebas/calidad)
- `prod` (producción/entrega)

Flujo:

1. Cada integrante crea su rama desde `dev`:
   - `feat-dev/<tema>`
2. PR siempre hacia `dev`
3. Cuando `dev` esté estable:
   - PR `dev -> qa`
4. Cuando `qa` esté OK:
   - PR `qa -> prod`

Regla: **sin merges directos** a ramas principales.

---

## 10) Checklist final de evaluación (domingo)

- [ ] FastAPI funciona y corre con Uvicorn
- [ ] Conexión Neon OK (health DB)
- [ ] 6 entidades con relaciones coherentes
- [ ] CRUD completo para las 6 entidades
- [ ] Menú por consola CRUD para las 6 entidades vía HTTP
- [ ] `.env` ignorado
- [ ] PEP8 + docstrings
- [ ] README con comandos y explicación
- [ ] Uso real de PRs y ramas dev/qa/prod, commits con autoría clara

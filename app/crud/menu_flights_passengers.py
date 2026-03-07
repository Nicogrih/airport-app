from typing import Any

import httpx
from app.crud.http_client import APIClient
from app.crud.flights import (
    create_flight,
    delete_flight,
    get_flight,
    list_flights,
    update_flight,
)
from app.crud.passengers import (
    create_passenger,
    delete_passenger,
    get_passenger,
    list_passengers,
    update_passenger,
)

def _print_json(data: Any) -> None:
    print("\n-- Respuesta ---")
    print(data)
    print("-----------------\n")

def _handle_error(exc: Exception) -> None:
    if isinstance(exc, httpx.HTTPStatusError):
        print(f"\nError HTTP {exc.response.status_code}: {exc.response.text}\n")
    else:
        print(f"\nError: {exc}\n")

def flights_menu(client: APIClient) -> None:
    while True:
        print("=== VUELOS ===")
        print("1) Listar")
        print("2) Ver uno (UUID)")
        print("3) Crear")
        print("4) Actualizar (UUID)")
        print("5) Eliminar (UUID)")
        print("0) Volver")

        op = input("Opción: ").strip()

        try:
            if op == "1":
                _print_json(list_flights(client))
            
            elif op == "2":
                fid = input("UUID vuelo: ").strip()
                _print_json(get_flight(client, fid))

            elif op == "3":
                airline_id = input("Aerolinea ID (UUID): ").strip()
                flight_number = input("Numero de vuelo: ").strip()
                origin_airport_id = input("Aeropuerto de origen ID (UUID): ").strip()
                destination_airport_id = input("Aeropuerto de destino ID (UUID): ").strip()
                departure_at = input("Fecha de despegue (YYYY-MM-DDTHH:MM:SSZ): ").strip()
                arrival_at = input("Fecha de llegada (YYYY-MM-DDTHH:MM:SSZ): ").strip()

                status = (
                    input("Estado (SCHEDULED/RESCHEDULED/CANCELED) [SCHEDULED]: ").strip()
                    or "SCHEDULED"
                )

                payload = {
                    "airline_id": airline_id,
                    "flight_number": flight_number,
                    "origin_airport_id": origin_airport_id,
                    "destination_airport_id": destination_airport_id,
                    "departure_at": departure_at,
                    "arrival_at": arrival_at,
                    "status": status,
                }

                _print_json(create_flight(client, payload))

            elif op == "4":
                fid = input("UUID vuelo: ").strip()

                print("Deja vacío para no modificar un campo.")

                flight_number = input("Número de vuelo: ").strip() or None
                departure_at = input("Fecha de despegue: ").strip() or None
                arrival_at = input("Fecha de Llegada: ").strip() or None
                status = input("Estado: ").strip() or None

                payload = {
                    k: v
                    for k, v in {
                        "flight_number": flight_number,
                        "departure_at": departure_at,
                        "arrival_at": arrival_at,
                        "status": status,
                    }.items()
                    if v is not None
                }

                _print_json(update_flight(client, fid, payload))
            
            elif op == "5":
                fid = input("UUID vuelo: ").strip()
                delete_flight(client, fid)
                print("\nEliminado.\n")
            
            elif op == "0":
                return
            
        except Exception as exc:
            _handle_error(exc)

def passengers_menu(client: APIClient) -> None:
    while True:
        print("=== PASAJEROS ===")
        print("1) Listar")
        print("2) Ver uno (UUID)")
        print("3) Crear")
        print("4) Actualizar (UUID)")
        print("5) Eliminar (UUID)")
        print("0) Volver")

        op = input("Opción: ").strip()

        try:
            if op == "1":
                _print_json(list_passengers(client))

            elif op == "2":
                pid = input("UUID pasajero: ").strip()
                _print_json(get_passenger(client, pid))

            elif op == "3":
                reservation_id = input("Reservación ID (UUID): ").strip()
                first_name = input("Nombre: ").strip()
                last_name = input("Apellido: ").strip()
                document_number = input("Número de documento: ").strip()
                birth_date = input("Fecha de nacimiento (YYYY-MM-DD): ").strip() or None

                payload = {
                    "reservation_id": reservation_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "document_number": document_number,
                    "birth_date": birth_date,
                }

                _print_json(create_passenger(client, payload))

            elif op == "4":
                pid = input("UUID pasajero: ").strip()

                print("Deja vacío para no modificar un campo.")

                first_name = input("Nombre: ").strip() or None
                last_name = input("Apellido: ").strip() or None
                document_number = input("Número de documento: ").strip() or None
                birth_date = input("Fecha de nacimiento: ").strip() or None

                payload = {
                    k: v
                    for k, v in {
                        "first_name": first_name,
                        "last_name": last_name,
                        "document_number": document_number,
                        "birth_date": birth_date,
                    }.items()
                    if v is not None
                }

                _print_json(update_passenger(client, pid, payload))

            elif op == "5":
                pid = input("UUID pasajero: ").strip()
                delete_passenger(client, pid)
                print("\nEliminado.\n")

            elif op == "0":
                return

        except Exception as exc:
            _handle_error(exc)
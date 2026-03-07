from app.crud.http_client import APIClient
from typing import Any
import httpx

from app.crud.airlines import (
    list_airlines, 
    get_airline, 
    create_airline, 
    update_airline,
    delete_airline
)
from app.crud.airports import(
    list_airports,
    get_airport,
    create_airport,
    update_airport,
    delete_airport
)

def _print_json(data: Any) -> None:
    print("\n--- Respuesta ---")
    print(data)
    print("-----------------\n")


def _handle_error(exc: Exception) -> None:
    if isinstance(exc, httpx.HTTPStatusError):
        print(f"\nError HTTP {exc.response.status_code}: {exc.response.text}\n")
    else:
        print(f"\nError: {exc}\n")

def airlines_menu(client:APIClient)->None:
    while True:
        print("=== AEROLINEAS ===")
        print("1) Listar")
        print("2) Ver Aerolínea(UUID)")
        print("3) Crear")
        print("4) Actualizar(UUID)")
        print("5) Eliminar(UUID)")
        print("0) Volver")
        op = input("Opcion: ").strip()
        try:
            if op == "1":
                _print_json(list_airlines(client))
            elif op == "2":
                airl_id = input("UUID: ").strip()
                _print_json(get_airline(client, airl_id))
            elif op == "3":
                code = input("Código: ").strip()
                name = input("Nombre de la Aerolínea: ").strip()
                _print_json(create_airline(client,{"code":code, "name": name}))
            elif op == "4":
                airl_id= input("UUID: ").strip()
                print("Deja vacío para no modificar un campo.")
                code = input("Código (IATA): ").strip() or None
                name = input("Nombre de la Aerolínea: ").strip() or None
                payload = {
                    k: v
                    for k, v in {"code": code, "name": name}.items()
                    if v is not None
                }
                _print_json(update_airline(client, airl_id, payload))
            elif op == "5":
                airl_id = input("UUID: ").strip()
                delete_airline(client, airl_id)
                print("\nEliminado.\n")
            elif op == "0":
                return
        except Exception as exc:
            _handle_error(exc)

def airports_menu(client:APIClient)->None:
    while True:
        print("=== AEROPUERTOS ===")
        print("1) Listar")
        print("2) Ver Aeropuerto(UUID)")
        print("3) Crear")
        print("4) Actualizar(UUID)")
        print("5) Eliminar(UUID)")
        print("0) Volver")
        op = input("Opcion: ").strip()
        try:
            if op == "1":
                _print_json(list_airports(client))
            elif op == "2":
                aportid = input("UUID: ").strip()
                _print_json(get_airport(client, aportid))
            elif op == "3":
                code = input("Código: ").strip()
                name = input("Nombre del Aeropuerto: ").strip()
                country = input("País/Ciudad: ").strip()
                _print_json(
                    create_airport(
                        client, {"code": code, "name": name, "country": country}
                    )
                )
            elif op == "4":
                aportid = input("UUID: ").strip()
                print("Deja vacío para no modificar un campo.")
                code = input("Código: ").strip() or None
                name = input("Nombre del Aeropuerto: ").strip() or None
                country = input("País/Ciudad: ").strip() or None
                payload = {
                    k: v
                    for k, v in {
                        "code": code,
                        "name": name,
                        "country": country,
                    }.items()
                    if v is not None
                }
                _print_json(update_airport(client, aportid, payload))
            elif op == "5":
                aportid = input("UUID: ").strip()
                _print_json(delete_airport(client, aportid))
            elif op == "0":
                return
        except Exception as exc:
            _handle_error(exc)
"""
Punto de entrada del menú CLI (en español).
"""

import os

from app.crud.http_client import APIClient
from app.crud.menu_users_reservations import users_menu, reservations_menu
from app.crud.menu_flights_passengers import flights_menu, passengers_menu


def main() -> None:
    base_url = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
    client = APIClient(base_url)

    while True:
        print("=== MENÚ PRINCIPAL ===")
        print("1) Usuarios")
        print("2) Reservas")
        print("3) Vuelos")
        print("4) Pasajeros")
        print("0) Salir")

        op = input("Opción: ").strip()

        if op == "1":
            users_menu(client)

        elif op == "2":
            reservations_menu(client)

        elif op == "3":
            flights_menu(client)

        elif op == "4":
            passengers_menu(client)

        elif op == "0":
            break


if __name__ == "__main__":
    main()
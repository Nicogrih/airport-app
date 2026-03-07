import os

from app.crud.http_client import APIClient
from app.crud.menu_airlines_airports import airlines_menu, airports_menu
from app.crud.menu_users_reservations import users_menu, reservations_menu
from app.crud.menu_flights_passengers import flights_menu, passengers_menu


def main() -> None:
    base_url = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
    client = APIClient(base_url)

    while True:
        print("=== MENÚ PRINCIPAL ===")
        print("1) Aerolíneas")
        print("2) Aeropuertos")
        print("3) Usuarios")
        print("4) Reservas")
        print("5) Vuelos")
        print("6) Pasajeros")
        print("0) Salir")

        op = input("Opción: ").strip()

        if op == "1":
            airlines_menu(client)
        elif op == "2":
            airports_menu(client)
        elif op == "3":
            users_menu(client)
        elif op == "4":
            reservations_menu(client)
        elif op == "5":
            flights_menu(client)
        elif op == "6":
            passengers_menu(client)
        elif op == "0":
            break


if __name__ == "__main__":
    main()
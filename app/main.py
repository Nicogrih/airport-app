import os

from dotenv import load_dotenv
from rich.console import Console

from app.crud.http_client import APIClient
from app.crud.menu_airlines import airlines_menu
from app.crud.menu_airports import airports_menu
from app.crud.menu_flights import flights_menu
from app.crud.menu_users import users_menu
from app.crud.menu_reservations import reservations_menu
from app.utils.cli_utils import clear_screen, pause

console = Console()


def main() -> None:
    load_dotenv()
    base_url = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

    client = APIClient(base_url)
    try:
        while True:
            clear_screen()
            console.print("=== MENÚ PRINCIPAL ===\n")
            console.print("1) Aerolíneas")
            console.print("2) Aeropuertos")
            console.print("3) Vuelos")
            console.print("4) Usuarios")
            console.print("5) Reservas")
            console.print("0) Salir")
            console.print("----------------------")

            op = input("Opción: ").strip()

            if op == "0":
                return
            if op == "1":
                airlines_menu(client)
            if op == "2":
                airports_menu(client)
            elif op == "3":
                flights_menu(client)
            elif op == "4":
                users_menu(client)
            elif op == "5":
                reservations_menu(client)
            else:
                console.print("Opción inválida.")
                pause()
    finally:
        client.close()


if __name__ == "__main__":
    main()

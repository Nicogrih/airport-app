import os

from app.crud.http_client import APIClient
from app.crud.menu_airlines_airports import airlines_menu, airports_menu

def main() -> None:
    base_url = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
    client = APIClient(base_url)

    while True:
        print("=== MENÚ PRINCIPAL ===")
        print("1) Aerolineas")
        print("2) Aeropuertos")
        print("0) Salir")
        op = input("Opción: ").strip()

        if op == "1":
            airlines_menu(client)
        elif op == "2":
            airports_menu(client)
        elif op == "0":
            break


if __name__ == "__main__":
    main()

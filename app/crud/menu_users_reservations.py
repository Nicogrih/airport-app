from typing import Any

import httpx

from app.crud.http_client import APIClient
from app.crud.users import create_user, delete_user, get_user, list_users, update_user
from app.crud.reservations import (
    create_reservation,
    delete_reservation,
    get_reservation,
    list_reservations,
    update_reservation,
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


def users_menu(client: APIClient) -> None:
    while True:
        print("=== USUARIOS ===")
        print("1) Listar")
        print("2) Ver uno (UUID)")
        print("3) Crear")
        print("4) Actualizar (UUID)")
        print("5) Eliminar (UUID)")
        print("0) Volver")
        op = input("Opción: ").strip()

        try:
            if op == "1":
                _print_json(list_users(client))
            elif op == "2":
                uid = input("UUID: ").strip()
                _print_json(get_user(client, uid))
            elif op == "3":
                email = input("Correo: ").strip()
                full_name = input("Nombre completo: ").strip()
                role = input("Rol (CLIENT/ADMIN) [CLIENT]: ").strip() or "CLIENT"
                _print_json(
                    create_user(
                        client, {"email": email, "full_name": full_name, "role": role}
                    )
                )
            elif op == "4":
                uid = input("UUID: ").strip()
                print("Deja vacío para no modificar un campo.")
                email = input("Correo: ").strip() or None
                full_name = input("Nombre completo: ").strip() or None
                role = input("Rol (CLIENT/ADMIN): ").strip() or None
                payload = {
                    k: v
                    for k, v in {
                        "email": email,
                        "full_name": full_name,
                        "role": role,
                    }.items()
                    if v is not None
                }
                _print_json(update_user(client, uid, payload))
            elif op == "5":
                uid = input("UUID: ").strip()
                delete_user(client, uid)
                print("\nEliminado.\n")
            elif op == "0":
                return
        except Exception as exc:
            _handle_error(exc)


def reservations_menu(client: APIClient) -> None:
    while True:
        print("=== RESERVAS ===")
        print("1) Listar")
        print("2) Ver una (UUID)")
        print("3) Crear")
        print("4) Actualizar (UUID)")
        print("5) Eliminar (UUID)")
        print("0) Volver")
        op = input("Opción: ").strip()

        try:
            if op == "1":
                _print_json(list_reservations(client))
            elif op == "2":
                rid = input("UUID: ").strip()
                _print_json(get_reservation(client, rid))
            elif op == "3":
                user_id = input("ID de usuario (UUID): ").strip()
                status = (
                    input("Estado (HOLD/CONFIRMED/CANCELED/EXPIRED) [HOLD]: ").strip()
                    or "HOLD"
                )
                total = input("Total (COP) [0]: ").strip()
                total_amount_cop = int(total) if total else 0
                _print_json(
                    create_reservation(
                        client,
                        {
                            "user_id": user_id,
                            "status": status,
                            "total_amount_cop": total_amount_cop,
                        },
                    )
                )
            elif op == "4":
                rid = input("UUID: ").strip()
                print("Deja vacío para no modificar un campo.")
                user_id = input("ID de usuario (UUID): ").strip() or None
                status = (
                    input("Estado (HOLD/CONFIRMED/CANCELED/EXPIRED): ").strip() or None
                )
                total = input("Total (COP): ").strip()
                total_amount_cop = int(total) if total else None
                payload = {
                    k: v
                    for k, v in {
                        "user_id": user_id,
                        "status": status,
                        "total_amount_cop": total_amount_cop,
                    }.items()
                    if v is not None
                }
                _print_json(update_reservation(client, rid, payload))
            elif op == "5":
                rid = input("UUID: ").strip()
                delete_reservation(client, rid)
                print("\nEliminado.\n")
            elif op == "0":
                return
        except Exception as exc:
            _handle_error(exc)

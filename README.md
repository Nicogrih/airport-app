# airport-app

Proyecto académico para un sistema de reservas de vuelos.

- **Backend:** Python + FastAPI  
- **Base de datos:** Neon (PostgreSQL)  
- **Frontend (futuro):** HTML/CSS/JS servido como estático desde FastAPI en `static/`  
- **Equipo:** 3 personas (Windows + VS Code)  
- **Convenciones:** commits en **español**, código/estructuras en **inglés**.

---

## Integrantes

- Ángel David Gutiérrez Ladino  
- Gerardo Andrés Jiménez Piedrahíta  
- Nicolás Josué Grijalba Huertas  

---

## Estructura del repositorio

```text
airport-app/
├── app/                  # Backend (FastAPI)
│   ├── api/              # Routes (más adelante)
│   ├── core/             # Configuration, security (más adelante)
│   ├── db/               # DB session, migrations (más adelante)
│   ├── models/           # ORM models (más adelante)
│   ├── schemas/          # Pydantic schemas (más adelante)
│   ├── services/         # Business logic (más adelante)
│   ├── utils/            # Helpers/utilities (más adelante)
│   ├── __init__.py
│   └── main.py           # FastAPI entrypoint
├── static/               # Frontend estático (vacío por ahora)
├── docs/                 # Documentación del proyecto (opcional)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Requisitos

- Python **3.14+** (recomendado)
- Git
- VS Code
- Cuenta y base de datos en **Neon** (PostgreSQL)

---

## Configuración inicial (Windows)

### 1) Clonar el repositorio
```bash
git clone https://github.com/Nicogrih/airport-app.git
cd airport-app
```

### 2) Crear y activar el entorno virtual
```bash
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

> Si PowerShell bloquea la activación, abre una terminal **Command Prompt (cmd)** en VS Code y usa:
```bat
.\.venv\Scripts\activate.bat
```

### 3) Instalar dependencias
```bash
pip install -r requirements.txt
```

---

## Variables de entorno (`.env`)

Este proyecto usa un archivo `.env` **local** (no se sube al repositorio).

1. Crea un archivo `.env` en la raíz del proyecto (al mismo nivel de `requirements.txt`).
2. Agrega al menos:

```env
DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@HOST:5432/DBNAME?sslmode=require
JWT_SECRET=change-me
```

- `DATABASE_URL`: se obtiene desde Neon.
- `JWT_SECRET`: cualquier string largo (solo para desarrollo).

---

## Ejecutar el servidor (modo desarrollo)

Con el entorno virtual activado, puedes usar cualquiera de estas opciones:

### Opción A (recomendada / estándar)
```bash
uvicorn app.main:app --reload
```

### Opción B (FastAPI CLI)
```bash
fastapi dev app/main.py
```

Luego abre:
- Swagger: http://127.0.0.1:8000/docs
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

---

## Flujo de trabajo con Git (equipo de 3)

- Ramas: `main` = estable, `dev` = integración, `feature/...` = por funcionalidad.

Pasos rápidos:
1. Partir siempre desde `dev`:
   - git checkout dev && git pull
   - Evita divergencias grandes.
2. Crear la rama de feature desde `dev`:
   - git checkout -b feature/nombre
3. Trabajar, commitear y pushear normalmente:
   - git add . && git commit -m "Mensaje en español" && git push -u origin feature/nombre
4. Mantener la rama actualizada con `dev` periódicamente:
   - git checkout dev && git pull
   - git checkout feature/nombre && git merge dev (resolver conflictos si los hay)
5. Cuando esté lista la feature → abrir PR desde `feature/...` hacia `dev` y exigir revisión.
   - Solo merge a `main` cuando `dev` esté estable y probado.

Regla clave: PRs a `dev` (nunca directo a `main`). Commits en español.

---

## Notas
- La carpeta `static/` está reservada para el frontend (HTML/CSS/JS) que se desarrollará después.
- Este repositorio prioriza simplicidad (KISS) y una estructura escalable por módulos (`api`, `db`, `services`, etc.).

---

## Licencia
Uso académico.
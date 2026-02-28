# airport-app

Proyecto académico para un sistema de reservas de vuelos.

- **Backend:** Python + FastAPI
- **Servidor:** Uvicorn
- **Base de datos:** Neon (PostgreSQL)
- **Menú por consola:** CRUD consumiendo la API por HTTP
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
├── app/
│   ├── crud/             # Cliente HTTP usado por el menú (consume la API)
│   ├── database/         # Configuración de conexión a Neon y sesión async
│   ├── endpoints/        # Routers/Endpoints FastAPI por entidad
│   ├── models/           # Modelos ORM (SQLAlchemy)
│   ├── schemas/          # Esquemas Pydantic (request/response)
│   ├── __init__.py
│   ├── app.py            # Aplicación FastAPI (registra routers)
│   └── main.py           # Menú por consola (script principal)
├── scripts/              # Scripts SQL (por ejemplo schema.sql)
├── static/               # Frontend estático (futuro)
├── docs/                 # Documentación (opcional)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Requisitos

- Python **3.11+** (recomendado)
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
DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@HOST/DBNAME?sslmode=require
```

- `DATABASE_URL`: se obtiene desde Neon.
- Importante: debe estar en formato SQLAlchemy async (**postgresql+asyncpg**) y en Neon normalmente se requiere `sslmode=require`.

> También se recomienda crear `.env.example` para documentar las variables sin credenciales.

---

## Ejecutar la API (modo desarrollo)

Con el entorno virtual activado:

```bash
uvicorn app.app:app --reload
```

Luego abre:

- Swagger: http://127.0.0.1:8000/docs
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

---

## Ejecutar el menú por consola (CRUD por HTTP)

El menú **consume la API** mediante llamadas HTTP (no accede directo a la base de datos).

1. Primero levanta el servidor:
   ```bash
   uvicorn app.app:app --reload
   ```
2. En otra terminal, ejecuta el menú:
   ```bash
   python -m app.main
   ```

---

## Base de datos (Neon)

- Los scripts para crear tablas se guardan en `scripts/` (por ejemplo `scripts/schema.sql`).
- Ejecuta el script en Neon desde el **SQL Editor**.

---

## Flujo de trabajo con Git y GitHub (equipo de 3)

Ramas principales:

- `dev`: desarrollo / integración
- `qa`: pruebas / calidad
- `prod`: producción / entrega

Flujo recomendado:

1. Crear una rama por tarea desde `dev`:
   ```bash
   git checkout dev
   git pull
   git checkout -b feat-dev/nombre-tarea
   ```
2. Commits en español:
   ```bash
   git add .
   git commit -m "Describe el cambio en español"
   git push -u origin feat-dev/nombre-tarea
   ```
3. Abrir Pull Request de `feat-dev/...` hacia `dev`.
4. Cuando `dev` esté estable, abrir PR `dev -> qa`.
5. Cuando `qa` esté validado, abrir PR `qa -> prod`.

Regla clave: **todo cambio entra por PR** (sin merges directos a ramas principales).

---

## Notas

- `static/` queda reservada para el frontend (HTML/CSS/JS) más adelante.
- Se prioriza simplicidad (KISS), PEP 8 y docstrings en funciones/módulos relevantes.

---

## Licencia

Uso académico.

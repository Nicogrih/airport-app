# Plan de Trabajo - Entrega Final (28 de Marzo)

## 1. Objetivo y Equipo

Implementar los requisitos del examen 2, distribuyendo las tareas de forma equitativa entre los tres integrantes del equipo:

- **Ángel David Gutiérrez Ladino**
- **Gerardo Andrés Jiménez Piedrahíta**
- **Nicolás Josué Grijalba Huertas**

## 2. Pipeline

El pipeline de CI/CD (con GitHub Actions). Las acciones se ejecutan en "runners" que son máquinas virtuales (normalmente basadas en Linux) que se crean solo para ejecutar el pipeline.

**La clave es:**

- **Estandarizar:** El archivo `requirements.txt` asegura que todos (y el pipeline) usen las mismas versiones de las librerías.
- **Scripts Agnósticos:** Los comandos en el archivo YML deben ser compatibles con el entorno del runner (ej. `python -m pip install -r requirements.txt` funciona en ambos).
- **Variables de Entorno:** La base de datos se conecta usando secretos (secrets) de GitHub, no con un archivo `.env` local.

Si el pipeline se ejecuta correctamente en GitHub, significa que la configuración del proyecto es portable y no depende del Windows local.

## 3. División de Tareas por Integrante

Para optimizar el tiempo, las tareas se dividen en tres grandes bloques que pueden trabajarse en paralelo.

---

### **Tarea Principal 1: Base de Datos: Migraciones y Seeder**

- **Responsable:** Ángel David Gutiérrez Ladino
- **Rama Git:** `feat/db-migrations-seeder`

El objetivo es reemplazar la creación manual de tablas (`schema.sql`) por un sistema de migraciones automatizado y un poblado inicial de datos (seeder).

**Pasos detallados:**

1.  **Investigar e Instalar Alembic:** Alembic es el estándar para migraciones con SQLAlchemy.
    - Añadir `alembic` al archivo `requirements.txt`.
    - Instalarlo: `pip install alembic`.
    - Inicializar Alembic en el proyecto: `alembic init alembic`. Esto creará una carpeta `alembic/` y un archivo `alembic.ini`.

2.  **Configurar Alembic:**
    - En `alembic/env.py`, importar los modelos de `app/models` y configurar el `target_metadata`.
    - En `alembic.ini`, configurar la URL de la base de datos para que la lea desde las variables de entorno (similar a como ya lo hacen).

3.  **Crear la Primera Migración:**
    - Generar automáticamente la migración inicial basada en los modelos existentes: `alembic revision --autogenerate -m "Crear tablas iniciales"`.
    - Revisar el archivo de migración generado en `alembic/versions/`. Este archivo contiene el código Python para crear todas las tablas.

4.  **Crear el Script Seeder (`seeder.py`):**
    - Crear un nuevo archivo `app/database/seeder.py`.
    - Este script debe ser **idempotente**: si los datos ya existen, no debe fallar ni duplicarlos.
      - Ejemplo: "Si no existe un usuario admin, créalo".
    - Poblar datos iniciales como catálogos (aerolíneas, aeropuertos si aplica) y un usuario por defecto.

5.  **Crear Scripts de Ejecución:**
    - Modificar el `README.md` para añadir los nuevos comandos para la base de datos:
      - `alembic upgrade head` (Aplica todas las migraciones).
      - `python -m app.database.seeder` (Ejecuta el poblado de datos).

---

### **Tarea Principal 2: Carpeta `core` y Manejo Centralizado de Errores**

- **Responsable:** Nicolás Josué Grijalba Huertas
- **Rama Git:** `feat/core-error-handling`

El objetivo es estandarizar las respuestas de error de la API para que sean consistentes y manejadas desde un lugar central.

**Pasos detallados:**

1.  **Crear la Estructura:**
    - Crear una nueva carpeta: `app/core/`.
    - Dentro, crear dos archivos: `app/core/exceptions.py` y `app/core/handlers.py`.

2.  **Definir Excepciones Personalizadas (`exceptions.py`):**
    - En `app/core/exceptions.py`, crear clases de excepción que hereden de `Exception`. Esto hace el código más legible.
    - Ejemplos:

      ```python
      class NotFoundError(Exception):
          pass

      class ConflictError(Exception):
          pass
      ```

3.  **Crear Manejadores Globales (`handlers.py`):**
    - En `app/core/handlers.py`, crear funciones que capturen tus excepciones personalizadas y devuelvan una `JSONResponse` de FastAPI con el código de estado y mensaje correctos.

      ```python
      from fastapi import Request
      from fastapi.responses import JSONResponse
      from .exceptions import NotFoundError

      async def not_found_exception_handler(request: Request, exc: NotFoundError):
          return JSONResponse(
              status_code=404,
              content={"message": str(exc)},
          )
      ```

    - Hacer lo mismo para `ConflictError` (409), `ValueError` (400), etc.

4.  **Integrar en la App de FastAPI:**
    - En `app/app.py`, importar los manejadores y las excepciones, y registrarlos en la aplicación FastAPI.

      ```python
      from app.core.exceptions import NotFoundError, ConflictError
      from app.core.handlers import not_found_exception_handler, conflict_exception_handler

      app = FastAPI(...)

      app.add_exception_handler(NotFoundError, not_found_exception_handler)
      app.add_exception_handler(ConflictError, conflict_exception_handler)
      ```

5.  **Refactorizar Endpoints:**
    - Ir a los archivos en `app/endpoints/` y reemplazar la lógica de error actual (ej. `raise HTTPException`) por las nuevas excepciones.
      - **Antes:** `raise HTTPException(status_code=404, detail="...")`
      - **Ahora:** `raise NotFoundError("...")`

---

### **Tarea Principal 3: Pipeline CI/CD con GitHub Actions**

- **Responsable:** Gerardo Andrés Jiménez Piedrahíta
- **Rama Git:** `feat/ci-cd-pipeline`

El objetivo es automatizar la verificación de calidad, pruebas, y la sincronización con la base de datos cada vez que se integra código en la rama `dev`.

**Pasos detallados:**

1.  **Crear Estructura para Workflow:**
    - Crear la ruta de carpetas: `.github/workflows/`.
    - Dentro, crear un archivo: `ci.yml`.

2.  **Definir el Disparador (Trigger):**
    - En `ci.yml`, configurar el pipeline para que se ejecute solo en `push` o `pull_request` a la rama `dev`.

      ```yaml
      name: CI Pipeline

      on:
        push:
          branches: [dev]
        pull_request:
          branches: [dev]
      ```

3.  **Configurar los Pasos (Jobs):**
    - Definir un `job` llamado `build` que se ejecute en un `ubuntu-latest`.
    - Añadir los siguientes `steps`:
      a. **Checkout:** `actions/checkout@v3` para obtener el código.
      b. **Setup Python:** `actions/setup-python@v4` para instalar la versión correcta de Python.
      c. **Install Dependencies:** `pip install -r requirements.txt`.
      d. **Linting:** `pip install ruff && ruff check .` para verificar el formato del código.
      e. **Database Sync:** - **Ejecutar Migraciones:** `alembic upgrade head`. Para esto, necesitas la variable de entorno `DATABASE_URL`. - **Ejecutar Seeder:** `python -m app.database.seeder`. - **Importante:** Configurar la variable `DATABASE_URL` como un **secret** en la configuración del repositorio de GitHub (`Settings > Secrets and variables > Actions`) para que el pipeline pueda conectarse a la base de datos de Neon de forma segura.

    - **Ejemplo del paso de migración en `ci.yml`:**
      ```yaml
      - name: Run Database Migrations
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: alembic upgrade head
      ```

---

## 4. Integración, Video y Entrega

- **Fecha Límite:** Viernes 27 de Marzo (para tener margen antes de la entrega final el Sábado 28).

**Plan de Integración:**

1.  **Pull Requests Individuales:** Cada integrante debe crear un Pull Request (PR) de su rama de funcionalidad (`feat/...`) hacia la rama `dev`.
2.  **Revisión Cruzada:** Revisen los PRs de sus compañeros. Es una buena práctica y parte de la evaluación.
3.  **Merge a `dev`:** Una vez que los PRs estén aprobados, hacer merge. El pipeline de Gerardo debería ejecutarse automáticamente. Si falla, arréglenlo en equipo.
4.  **Grabación del Video:** Con el pipeline funcionando, graben el video mostrando:
    - El código del archivo `ci-cd-pipeline.yml`.
    - La ejecución exitosa del pipeline en la pestaña "Actions" de GitHub, explicando cada paso (linting, migraciones, seeder).
    - Una prueba de que los cambios en la BD se aplicaron (ej. mostrando los datos del seeder en la consola de Neon).
5.  **Actualizar `README.md`:** Añadir el enlace al video y cualquier nueva instrucción.
6.  **PR Final:** Crear el PR final `dev -> qa -> prod` como lo indica su flujo de trabajo.

from fastapi import FastAPI

app = FastAPI(title="Sistema de reservas de vuelos")


@app.get("/")
def hola():
    return {"mensaje": "hola mundo"}

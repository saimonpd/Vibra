from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime
from pathlib import Path
import json

app = FastAPI(
    title="Vibra API",
    description="Backend de la app de Vibra",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS es un mecanismo de seguridad de los navegadores que bloquea peticiones HTTP cuando el frontend intenta conectarse al
# backend que esta en una direccion o puerto diferentes 
app.add_middleware( # añade un middleware a mi web: capa intermedia que intercepta y procesa todas las peticiones
    CORSMiddleware, # componente encargado de inspeccionar cabeceras de peticiones HTTP y responder con los permisos adecuados
    allow_origins=["*"], # permite a cualquier dominio hacerme peticiones
    allow_methods=["*"], # define los metodos HTTP permitidos ( GET, POST, PUT...) que te pueden hacer
    allow_headers=["*"], # controla que cabeceras HTTP custom pueden enviarme (Authorization, Content-Type...)
)

DATA_DIR = Path(__file__).parent / "datos"
DATA_DIR.mkdir(exist_ok=True)
FICHERO = DATA_DIR / "palabras.jsonl"

class Entrada(BaseModel):
    palabra: str = Field(..., min_length=1, max_length=30)

class EntradaGuardada(Entrada):
    fecha: str


@app.post("/palabras", response_model=EntradaGuardada)
def anadir_palabra(entrada: Entrada):
    """Recoge las palabra recibida, le añade la fecha y lo guarda en BD"""
    registro = EntradaGuardada(
        palabra = entrada.palabra.strip().lower(),
        fecha = datetime.now().isoformat(timespec="seconds"),
    )

    with open(FICHERO, "a", encoding="utf-8") as f:
        f.write(registro.model_dump_json() + "\n")

    return registro


@app.get("/listapalabras", response_model=list[EntradaGuardada])
def obtener_palabras(dia: str | None = None):
    """Recoge todos los datos del dia solicitado de la BD y lo muestra"""
    if not FICHERO.exists():
        return ["El fichero no existe."]

    resultado = []
    with open(FICHERO, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            registro = json.loads(linea)
            if dia is None or registro["fecha"].startswith(dia):
                resultado.append(registro)
    return resultado

@app.get("/salud")
def salud():
    total = sum(1 for _ in open(FICHERO)) if FICHERO.exists else 0
    return {"estado": "ok", "total_registros": total}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime
from pathlib import Path
from database.repository.palabras_repository import RepositorioPalabras
from utils.analizador import clasificar

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

FICHERO = Path(__file__).parent / "database" / "palabras.jsonl"

repo = RepositorioPalabras(FICHERO)

class Entrada(BaseModel):
    palabra: str = Field(..., min_length=1, max_length=30)

class EntradaGuardada(Entrada):
    palabra: str
    sentimiento: str
    fecha: str


@app.post("/palabras", response_model=EntradaGuardada)
def anadir_palabra(entrada: Entrada):
    """Recibe una palabra, calcula su sentimiento y la guarda."""
    palabra = entrada.palabra.strip().lower()
    return repo.guardar(
        palabra=palabra,
        sentimiento=clasificar(palabra),
        fecha=datetime.now().isoformat(timespec="seconds"),
    )

@app.get("/listapalabras", response_model=list[EntradaGuardada])
def obtener_palabras(dia: str | None = None):
    """Devuelve las palabras guardadas, opcionalmente de un día (AAAA-MM-DD)."""
    return repo.obtener_por_dia(dia)

@app.get("/salud")
def salud():
    return {"estado": "ok", "total_registros": repo.contar_registros()}

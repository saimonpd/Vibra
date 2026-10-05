# Vibra 🌡️

Termómetro emocional del aula: cada alumno resume en una palabra cómo se siente, y la aplicación analiza esas palabras para ver el ambiente general de la clase.

> Proyecto de aprendizaje: backend con **FastAPI**, frontend con **Streamlit** y, próximamente, análisis de sentimiento con IA.

---

## ¿Qué hace?

1. El alumno escribe una palabra en el cuestionario (Streamlit).
2. El frontend envía la palabra al backend mediante una petición HTTP (JSON).
3. El backend (FastAPI) valida los datos con Pydantic, le añade la fecha y la guarda en un fichero.
4. *(Próximamente)* Un modelo de IA clasifica si la palabra es positiva, neutra o negativa.
5. *(Próximamente)* La página de estadísticas muestra cómo está la clase.

🔒 **Privacidad:** las palabras son anónimas. No se guarda quién las escribe.

## Arquitectura

```text
Navegador ──► Streamlit (frontend, :8501) ──HTTP/JSON──► FastAPI (backend, :8000)
                                                              │
                                                              ├──► backend/datos/palabras.jsonl
                                                              └──► (futuro) servicio de IA
```

Regla de diseño: el frontend **solo** habla con la API. Nunca accede directamente a los datos ni a la IA.

## Estructura del proyecto

```text
Vibra/
├── backend/
│   ├── main.py              # API FastAPI
│   ├── requirements.txt     # Dependencias del backend
│   └── datos/
│       └── palabras.jsonl   # Respuestas guardadas (se genera solo)
├── frontend/
│   ├── app.py               # Punto de entrada y navegación de Streamlit
│   ├── views/
│   │   ├── inicio.py        # Portada: explicación de la app
│   │   ├── registro.py      # Cuestionario: envía la palabra a la API
│   │   └── estadisticas.py  # Estadísticas de la clase (en construcción)
│   └── requirements.txt     # Dependencias del frontend
├── .env.example             # Plantilla de configuración
├── .gitignore
└── README.md
```

Cada módulo tiene su **propio entorno virtual** (`venv/`) para mantener las dependencias aisladas.

## Requisitos

- Python 3.10 o superior
- Git
- Windows con PowerShell (los comandos de abajo están pensados para él)

## Instalación y ejecución

Necesitas **dos terminales**, una para el backend y otra para el frontend.

### 1. Backend

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

La API queda disponible en http://127.0.0.1:8000 y su documentación interactiva en http://127.0.0.1:8000/docs.

### 2. Frontend

```powershell
cd frontend
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Antes de arrancar, crea tu archivo de configuración a partir de la plantilla:

```powershell
copy .env.example .env
```

Abre `.env` y escribe la dirección de tu API. En local:

```text
API_URL=http://127.0.0.1:8000
```

Y ya puedes arrancar la interfaz:

```powershell
python -m streamlit run app.py
```

Se abre en http://localhost:8501.

> ⚠️ El archivo `.env` **nunca se sube a Git** (está en `.gitignore`). Lo que se comparte es `.env.example`, que solo lista los nombres de las variables, sin valores.

### Problemas frecuentes

| Problema | Solución |
|---|---|
| PowerShell bloquea `Activate.ps1` | `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` (solo afecta a esa terminal) |
| `pip.exe` bloqueado por Windows Defender | Usar siempre `python -m pip ...` |
| `No module named '...'` | Falta instalar dependencias: activa el venv y ejecuta `python -m pip install -r requirements.txt` |
| El cuestionario dice que el servicio no está disponible | Comprueba que el backend está arrancado y que `API_URL` en `.env` es correcta |

## Endpoints de la API

| Método | Ruta | Descripción | Cuerpo de la petición |
|---|---|---|---|
| POST | `/palabras` | Guarda una palabra y le añade la fecha | `{ "palabra": "motivado" }` |
| GET | `/listapalabras` | Devuelve todas las palabras guardadas. Opcional: `?dia=2026-10-05` filtra por día | — |
| GET | `/salud` | Comprueba que la API está viva y cuenta los registros | — |

**Ejemplo de respuesta de `POST /palabras`:**

```json
{ "palabra": "motivado", "fecha": "2026-10-05T11:19:07" }
```

## Almacenamiento de datos

Las respuestas se guardan en `backend/datos/palabras.jsonl` (formato **JSON Lines**): cada línea es un objeto JSON independiente, así que añadir una respuesta es solo escribir una línea al final del fichero.

```text
{"palabra": "motivado", "fecha": "2026-10-05T11:19:07"}
{"palabra": "cansado", "fecha": "2026-10-05T11:20:31"}
```

## Hoja de ruta

- [x] Estructura modular backend / frontend
- [x] Comunicación Streamlit ↔ FastAPI
- [x] Cuestionario conectado con la API
- [x] Persistencia en fichero JSON Lines
- [ ] Página de estadísticas
- [ ] Análisis de sentimiento con IA
- [ ] Despliegue público

## Autor

Saimon — proyecto de aprendizaje guiado por mi profesora.
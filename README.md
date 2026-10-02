# Vibra 🌡️

Termómetro emocional del aula: cada alumno resume en una palabra cómo se siente, y la aplicación analiza esas palabras para ver el ambiente general de la clase.

> Proyecto de aprendizaje: backend con **FastAPI**, frontend con **Streamlit** y, próximamente, análisis de sentimiento con IA.

---

## ¿Qué hace?

1. El alumno escribe una palabra en la interfaz web (Streamlit).
2. El frontend envía la palabra al backend mediante una petición HTTP (JSON).
3. El backend (FastAPI) valida los datos con Pydantic y los procesa.
4. *(Próximamente)* Un modelo de IA clasifica si la palabra es positiva, neutra o negativa.

## Arquitectura

```text
Navegador ──► Streamlit (frontend, :8501) ──HTTP/JSON──► FastAPI (backend, :8000)
                                                              │
                                                              └──► (futuro) servicio de IA
```

Regla de diseño: el frontend **solo** habla con la API. Nunca accede directamente a los datos ni a la IA.

## Estructura del proyecto

```text
Vibra/
├── backend/
│   ├── main.py             # API FastAPI
│   └── requirements.txt    # Dependencias del backend
├── frontend/
│   ├── app.py              # Interfaz Streamlit
│   └── requirements.txt    # Dependencias del frontend
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
python -m streamlit run app.py
```

La interfaz se abre en http://localhost:8501.

### Problemas frecuentes en Windows

| Problema | Solución |
|---|---|
| PowerShell bloquea `Activate.ps1` | `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` (solo afecta a esa terminal) |
| `pip.exe` bloqueado por Windows Defender | Usar siempre `python -m pip ...` |

## Endpoints de la API

| Método | Ruta | Descripción | Cuerpo de la petición |
|---|---|---|---|
| POST | `/...` | ... | `{ ... }` |
| GET | `/...` | ... | — |

## Hoja de ruta

- [x] Estructura modular backend / frontend
- [x] Comunicación Streamlit ↔ FastAPI
- [ ] Análisis de sentimiento con IA
- [ ] Persistencia de las respuestas
- [ ] Despliegue público

## Autor

Saimon — proyecto de aprendizaje guiado por mi profesora.

# Vibra

**Vibra es un termómetro emocional para el aula.** Cada alumno resume en una palabra cómo se siente, la aplicación clasifica esa palabra como positiva, neutra o negativa, y la clase entera se ve reflejada en una nube de palabras coloreada.

Está pensada para que un grupo detecte a tiempo cuándo conviene parar y hablar de cómo está, sin que nadie tenga que exponerse: las respuestas son anónimas.

```text
Alumno escribe "motivado" ──► Vibra la clasifica (positivo) ──► aparece en la nube de la clase
```

## Índice

- [Funcionalidades](#funcionalidades)
- [Tecnologías](#tecnologías)
- [Inicio rápido](#inicio-rápido)
- [Uso](#uso)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Documentación adicional](#documentación-adicional)
- [Solución de problemas](#solución-de-problemas)
- [Privacidad](#privacidad)
- [Hoja de ruta](#hoja-de-ruta)
- [Autoría](#autoría)

## Funcionalidades

- **Cuestionario anónimo:** elige una de las 10 emociones predefinidas o escribe tu propia palabra.
- **Clasificación automática:** las emociones conocidas se clasifican al instante; las desconocidas se guardan como `pendiente`.
- **Nube de palabras:** cuanto más se repite una palabra, más grande se dibuja. El color indica el sentimiento: verde (positivo), gris (neutro) y rojo (negativo).
- **API documentada:** FastAPI genera una documentación interactiva en `/docs`.
- **Aviso si el servicio falla:** si el backend no responde, el alumno ve un mensaje claro en lugar de un error técnico.

## Tecnologías

| Capa | Tecnología | Para qué se usa |
|---|---|---|
| Backend | [FastAPI](https://fastapi.tiangolo.com/) + Uvicorn | API REST y servidor |
| Backend | [Pydantic](https://docs.pydantic.dev/) | Validación de los datos de entrada |
| Frontend | [Streamlit](https://streamlit.io/) | Interfaz web (navegación con `st.navigation`) |
| Frontend | [wordcloud](https://github.com/amueller/word_cloud) + matplotlib + numpy | Generación de la nube |
| Frontend | requests + python-dotenv | Llamadas a la API y lectura de `.env` |
| Datos | Fichero JSON Lines | Persistencia sencilla, sin base de datos |

## Inicio rápido

### Requisitos

- Python 3.10 o superior
- Git
- Windows con PowerShell (los comandos están pensados para él)
- Una versión reciente de Streamlit (el código usa `st.navigation` y `st.pills`)

### Instalación y arranque

Necesitas **dos terminales**: una para el backend y otra para el frontend.

1. Clona el repositorio y entra en la carpeta:

   ```powershell
   git clone <URL-del-repositorio>
   cd Vibra
   ```

2. En la **primera terminal**, arranca el backend:

   ```powershell
   cd backend
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   python -m uvicorn main:app --reload --port 8000
   ```

3. Comprueba que funciona: abre <http://127.0.0.1:8000/salud>. Debes ver `{"estado":"ok","total_registros":...}`.

4. En la **segunda terminal**, prepara el frontend:

   ```powershell
   cd frontend
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   copy .env.example .env
   ```

5. Abre `.env` y escribe la dirección de tu API:

   ```text
   API_URL=http://127.0.0.1:8000
   ```

6. Arranca la interfaz:

   ```powershell
   python -m streamlit run app.py
   ```

7. Abre <http://localhost:8501>. Si todo ha ido bien, verás la portada de Vibra.

> **Importante:** `.env` nunca se sube a Git (está en `.gitignore`). Lo que se comparte es `.env.example`, que solo lista los nombres de las variables.

## Uso

### Enviar una palabra

1. Entra en **Cuestionario**.
2. Elige una emoción de la lista **o** escribe otra palabra en el campo "Otra". Si escribes algo ahí, tiene prioridad sobre lo seleccionado.
3. Pulsa **Enviar**.

### Ver la nube de la clase

1. Entra en **Nube**.
2. Consulta el resultado. Si hay menos de 5 respuestas, la página lo avisa: la nube mejora cuando hay más.

### Probar la API directamente

Si quieres enviar una palabra sin usar la interfaz, ejecuta en PowerShell:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/palabras `
  -ContentType "application/json" `
  -Body '{"palabra": "motivado"}'
```

Respuesta:

```json
{ "palabra": "motivado", "sentimiento": "positivo", "fecha": "2026-11-23T09:26:19" }
```

También puedes probar todas las rutas desde <http://127.0.0.1:8000/docs>.

## Estructura del proyecto

```text
Vibra/
├── backend/
│   ├── main.py                          # Rutas de la API
│   ├── database/
│   │   ├── palabras.jsonl               # Respuestas guardadas (se genera solo)
│   │   └── repository/palabras_repository.py   # Único acceso al fichero
│   └── utils/
│       ├── analizador.py                # Clasifica cada palabra
│       └── conteo_palabras.py           # Cuenta palabras por sentimiento
├── frontend/
│   ├── app.py                           # Navegación entre páginas
│   ├── views/                           # inicio.py, registro.py, nube.py
│   └── utils/                           # grafico_nube.py, lista_emociones.py
├── docs/                                # Documentación detallada
├── .env.example
└── README.md
```

Cada módulo (`backend/` y `frontend/`) tiene su propio entorno virtual `venv/` para aislar las dependencias.

## Documentación adicional

- [Referencia de la API](docs/referencia-api.md): rutas, parámetros, respuestas y errores.
- [Arquitectura y decisiones de diseño](docs/arquitectura.md): cómo se conectan las piezas y por qué se hicieron así.

## Solución de problemas

| Problema | Solución |
|---|---|
| PowerShell bloquea `Activate.ps1` | Ejecuta `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`. Solo afecta a esa terminal. |
| `pip.exe` bloqueado por Windows Defender | Usa siempre `python -m pip ...`. |
| `No module named '...'` | Activa el venv y ejecuta `python -m pip install -r requirements.txt`. |
| `cannot import name 'load_dotenv'` | Está instalado el paquete equivocado. Desinstala `dotenv` e instala `python-dotenv`. |
| El cuestionario dice que no puede cargar el formulario | Comprueba que el backend está arrancado, que `API_URL` en `.env` es correcta y que <http://127.0.0.1:8000/salud> responde. |
| La página Nube dice que el servicio no está disponible | Aplica el mismo diagnóstico y prueba <http://127.0.0.1:8000/conteo>. |
| Una palabra aparece en negro en la nube | Es una palabra `pendiente`: aún no está clasificada. Ver [Arquitectura](docs/arquitectura.md#palabras-pendientes). |

## Privacidad

Las palabras son anónimas: la aplicación **no guarda quién las escribe**. Solo se almacenan la palabra, su sentimiento y la fecha.

## Hoja de ruta

- [x] Estructura modular backend / frontend
- [x] Comunicación Streamlit ↔ FastAPI
- [x] Cuestionario con emociones predefinidas y palabra libre
- [x] Persistencia en JSON Lines con capa de repositorio
- [x] Clasificación con diccionario de emociones conocidas
- [x] Nube de palabras coloreada por sentimiento
- [ ] Clasificar con IA las palabras `pendiente`
- [ ] Guardar la respuesta en local si la API no está disponible y reenviarla después
- [ ] Despliegue público

## Autoría

Saimon: proyecto de aprendizaje guiado por mi profesora.

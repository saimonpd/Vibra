# Arquitectura y decisiones de diseño

Documento de **explicación**: cuenta cómo encajan las piezas y por qué se tomaron ciertas decisiones. Para consultar rutas y formatos, ve a la [Referencia de la API](referencia-api.md).

## Visión general

```text
Navegador ──► Streamlit (frontend, :8501) ──HTTP/JSON──► FastAPI (backend, :8000)
                                                              │
                                                              ├──► utils/analizador.py (clasifica)
                                                              ├──► repository ──► database/palabras.jsonl
                                                              └──► (futuro) servicio de IA
```

## Qué pasa cuando un alumno envía una palabra

1. El alumno elige una emoción o escribe una palabra en `views/registro.py`.
2. El frontend hace `POST /palabras` con `{"palabra": "..."}`.
3. FastAPI valida el cuerpo con Pydantic (1 a 30 caracteres).
4. `main.py` limpia la palabra (`strip` y `lower`) y llama a `clasificar()`.
5. `clasificar()` normaliza la palabra y la busca en el diccionario de emociones conocidas.
6. `RepositorioPalabras.guardar()` añade una línea al final de `palabras.jsonl`.
7. La API responde con el registro guardado.

Cuando alguien abre la página **Nube**, el recorrido es el inverso: `GET /conteo` agrupa los registros y `generar_nube()` dibuja el resultado.

## Responsabilidades por capa

| Capa | Fichero | Responsabilidad | No debe hacer |
|---|---|---|---|
| API | `main.py` | Definir rutas y orquestar | Leer o escribir ficheros directamente |
| Repositorio | `palabras_repository.py` | Leer y escribir `palabras.jsonl` | Decidir sentimientos o contar |
| Lógica | `analizador.py` | Normalizar y clasificar | Conocer HTTP ni ficheros |
| Lógica | `conteo_palabras.py` | Agrupar y contar registros | Acceder al fichero (pide los datos al repositorio) |

## Decisiones de diseño

### El frontend solo habla con la API

Streamlit nunca abre `palabras.jsonl`. Así, si algún día el fichero se sustituye por una base de datos, solo cambia el repositorio; la interfaz ni se entera.

### Capa de repositorio

Todo el acceso al fichero vive en una clase. Si mañana cambia el formato de almacenamiento, hay un único sitio que modificar, y `conteo_palabras.py` se puede probar con datos de ejemplo sin tocar disco.

### JSON Lines en lugar de un array JSON

Con un array JSON habría que leer el fichero entero, añadir el elemento y reescribirlo en cada envío. Con JSON Lines basta con abrir el fichero en modo `"a"` (añadir) y escribir una línea. Es más rápido y más seguro cuando dos alumnos envían a la vez.

### El servidor pone el sentimiento y la fecha

El cliente solo envía la palabra. Así nadie puede falsear la hora ni elegir el sentimiento que quiere que se muestre.

### Normalizar antes de comparar

`normalizar()` pasa a minúsculas, quita espacios y elimina tildes, y las claves del diccionario pasan por la misma función. Sin esto, `"Tranquilo"` y `"tranquilo "` serían palabras distintas y se contarían por separado.

### La nube agrupa por palabra

`WordCloud` necesita **una** frecuencia y **un** color por palabra. Si la misma palabra aparece con dos sentimientos distintos, `generar_nube()` suma las cantidades y pinta la palabra con el sentimiento más repetido.

## Palabras pendientes

Si una palabra no está en el diccionario, se guarda con sentimiento `pendiente` y se dibuja en negro en la nube. Esto es una limitación temporal: la hoja de ruta incluye clasificarlas con IA.

Dos preguntas abiertas para esa mejora:

- El modo `"a"` solo añade líneas. Para corregir el sentimiento de un registro antiguo habrá que decidir cómo reescribir el fichero.
- Conviene decidir si el servidor clasifica al guardar o en un proceso aparte.

## Limitaciones conocidas

- **Persistencia en producción:** un fichero local no sobrevive en plataformas *serverless* (como Vercel) y puede perderse en planes gratuitos que reinician el servicio. Antes del despliegue público hay que elegir un alojamiento con disco persistente o cambiar a una base de datos.
- **Cuestionario sin conexión:** si la API no responde, la respuesta se pierde. Está en la hoja de ruta guardarla en local y reenviarla después.
- **Escritura concurrente:** añadir líneas es seguro para pocos usuarios a la vez, pero no hay bloqueo explícito del fichero.

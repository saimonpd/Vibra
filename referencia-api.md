# Referencia de la API

Documento de **consulta**: describe qué hace cada ruta, sin explicar por qué se diseñó así (eso está en [Arquitectura](arquitectura.md)). Para probar las rutas de forma interactiva, abre `/docs` con el backend arrancado.

- **URL base en local:** `http://127.0.0.1:8000`
- **Formato:** JSON
- **Autenticación:** ninguna

## Resumen de rutas

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/palabras` | Guarda una palabra, calculando su sentimiento y su fecha |
| GET | `/listapalabras` | Lista los registros guardados |
| GET | `/conteo` | Cuenta las repeticiones por palabra y sentimiento |
| GET | `/salud` | Comprueba que la API está viva |

## Modelo de datos

Cada registro guardado tiene tres campos:

| Campo | Tipo | Descripción |
|---|---|---|
| `palabra` | texto | Palabra normalizada a minúsculas y sin espacios sobrantes |
| `sentimiento` | texto | `positivo`, `neutro`, `negativo` o `pendiente` |
| `fecha` | texto (ISO 8601) | Fecha y hora del envío, sin zona horaria. La pone siempre el servidor |

## POST /palabras

Guarda una palabra. El cliente solo envía la palabra: el sentimiento y la fecha los calcula el servidor.

**Cuerpo de la petición**

| Campo | Tipo | Obligatorio | Restricciones |
|---|---|---|---|
| `palabra` | texto | Sí | Entre 1 y 30 caracteres |

```json
{ "palabra": "motivado" }
```

**Respuesta 200**

```json
{ "palabra": "motivado", "sentimiento": "positivo", "fecha": "2026-11-23T09:26:19" }
```

**Errores**

| Código | Cuándo ocurre |
|---|---|
| 422 | El cuerpo no cumple las restricciones (por ejemplo, `palabra` vacía o de más de 30 caracteres) |

## GET /listapalabras

Devuelve los registros guardados, en el orden en que se escribieron.

**Parámetros de consulta**

| Parámetro | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `dia` | texto `AAAA-MM-DD` | No | Devuelve solo los registros de ese día |

**Respuesta 200**

```json
[
  { "palabra": "alegre", "sentimiento": "positivo", "fecha": "2026-11-08T11:59:04" },
  { "palabra": "futbol", "sentimiento": "pendiente", "fecha": "2026-11-08T12:47:48" }
]
```

Si el fichero no existe todavía, devuelve una lista vacía (`[]`).

## GET /conteo

Agrupa los registros por pareja (`palabra`, `sentimiento`) y ordena el resultado de más a menos repetida.

**Parámetros de consulta**

| Parámetro | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `dia` | texto `AAAA-MM-DD` | No | Cuenta solo los registros de ese día |

**Respuesta 200**

| Campo | Tipo | Descripción |
|---|---|---|
| `palabra` | texto | La palabra |
| `sentimiento` | texto | Su sentimiento |
| `cantidad` | entero | Cuántas veces se ha registrado esa pareja |
| `fecha` | texto | Fecha del último registro de esa pareja |

```json
[
  { "palabra": "motivado", "sentimiento": "positivo", "cantidad": 8, "fecha": "2026-11-23T09:26:21" },
  { "palabra": "tranquilo", "sentimiento": "positivo", "cantidad": 3, "fecha": "2026-11-23T09:30:35" }
]
```

## GET /salud

Comprueba que la API responde y cuenta los registros guardados. El cuestionario la consulta antes de mostrar el formulario.

**Respuesta 200**

```json
{ "estado": "ok", "total_registros": 18 }
```

## Emociones conocidas

Estas palabras se clasifican al instante. Cualquier otra se guarda como `pendiente`.

| Sentimiento | Palabras |
|---|---|
| `positivo` | alegre, tranquilo, motivado, orgulloso |
| `neutro` | indiferente, chill |
| `negativo` | agobiado, triste, cansado, enfadado |

La comparación ignora mayúsculas, espacios sobrantes y tildes (la `ñ` se respeta). Por ejemplo, `" Tranquilo "` se reconoce como `tranquilo`.

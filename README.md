# AsissBot — Bot de Telegram con LM Studio

Pequeño bot de Telegram que conversa usando un servidor local/remoto de **LM Studio** y, además, puede enviar al azar **fotos**, **videos** y **audios** cuando detecta esas palabras en el mensaje del usuario.

> Este README describe y acompaña al script `asissbot.py`. Asegúrate de haber revisado el código para ajustar los valores marcados con `...`.


## Características
- Conversación con un LLM (vía endpoint HTTP configurable).
- Envío de **foto/video/audio** aleatorios desde carpetas locales al detectar las palabras: `foto`, `video`/`vídeo`, `audio`.
- **Control de acceso** por `MY_USER_ID` (solo responde al usuario autorizado).
- Indicador de “escribiendo…” mientras el bot genera respuesta.
- Manejo básico de errores y logs.

## Requisitos
- **Python 3.10+** (recomendado 3.10 o superior).
- Un bot creado con **@BotFather** (obtendrás el `TELEGRAM_BOT_TOKEN`).
- Un endpoint compatible con **LM Studio** que acepte una solicitud `POST` con los campos usados en el script (`model`, `prompt`, `max_tokens`, `stop`).  
  - Ejemplo (ajústalo a tu entorno): `http://localhost:1234/v1/completions`

Instala dependencias:

```bash
python -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración
Edita los valores **marcados con `...`** en `asissbot.py`:

- `MY_USER_ID`: tu ID numérico de usuario de Telegram (el bot solo te responderá a ti).
- `TELEGRAM_BOT_TOKEN`: token de tu bot.
- `LM_STUDIO_SERVER_URL`: URL de tu servidor LM Studio (p. ej. `http://localhost:1234/v1/completions`).
- `SYSTEM_PROMPT`: prompt del sistema para guiar el estilo del asistente.
- Directorios de medios:
  - `PHOTO_DIRECTORY`: carpeta con imágenes (`.png`, `.jpg`, `.jpeg`).
  - `VIDEO_DIRECTORY`: carpeta con vídeos (`.mp4`, `.mov`, `.avi`, `.mkv`).
  - `AUDIO_DIRECTORY`: carpeta con audios (`.ogg`).

Sugerencia de estructura de carpetas:

```
media/
  photos/
  videos/
  audios/
```

Y en el script:

```python
PHOTO_DIRECTORY = "media/photos"
VIDEO_DIRECTORY = "media/videos"
AUDIO_DIRECTORY = "media/audios"
```

## Ejecución
Con el entorno activado y el script configurado, ejecuta:

```bash
python asissbot.py
```

Verás en la consola algo como “El bot está corriendo…”. Abre tu chat con el bot en Telegram y:

- Envía `/start` para el mensaje de bienvenida.
- Envía un texto normal para conversar con el modelo.
- Incluye las palabras clave:
  - `foto` → el bot enviará una foto aleatoria.
  - `video` / `vídeo` → enviará un vídeo aleatorio.
  - `audio` → enviará un audio aleatorio (`.ogg`).

## ¿Cómo funciona la llamada al LLM?
Cuando envías un mensaje de texto, el bot compone un *prompt* con tu `SYSTEM_PROMPT` y el texto del usuario, y hace una solicitud `POST` a `LM_STUDIO_SERVER_URL`, con un `json` parecido a:

```json
{
  "model": "...",
  "prompt": "…prompt completo…",
  "max_tokens": 200,
  "stop": ["Usuario:", "Asistente:"]
}
```

> Adapta los campos según la API exacta de tu servidor LM Studio (modelo, ruta, formato de petición, etc.).

## Consejos y solución de problemas
- **No responde a mis mensajes**: confirma que `MY_USER_ID` es tu usuario numérico real de Telegram y que el bot está en línea (token correcto).
- **“No puedo comunicarme con el servidor de IA.”**: revisa que `LM_STUDIO_SERVER_URL` sea accesible y que LM Studio esté ejecutándose y escuchando en esa URL.
- **“No hay fotos/videos/audios disponibles.”**: llena las carpetas configuradas con archivos válidos y con extensiones permitidas.
- **Tiempos de respuesta altos**: el bot simula pequeñas esperas (`asyncio.sleep`) y el modelo puede tardar; puedes ajustar tiempos o parámetros del modelo.

## Seguridad
- Conserva privado tu `TELEGRAM_BOT_TOKEN` y tu `MY_USER_ID`.
- Revisa el contenido de los medios que compartes para evitar datos sensibles.
- Si vas a exponer el servidor de LM Studio, protégelo con autenticación y red segura.

## Licencia
Este proyecto se distribuye “tal cual”. Úsalo, modifícalo y adáptalo según tus necesidades internas.

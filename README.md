# AsissBot — Bot de Telegram + LM Studio 🤖💬

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Telegram Bot](https://img.shields.io/badge/Telegram%20Bot-API-26A5E4?logo=telegram&logoColor=white)](https://core.telegram.org/bots)
[![Requests](https://img.shields.io/badge/requests-%E2%89%A52.31-000000?logo=python&logoColor=white)](https://docs.python-requests.org/)
[![License](https://img.shields.io/badge/license-MIT-informational)](#licencia)

Pequeño bot de **Telegram** que conversa usando un servidor local/remoto de **LM Studio** y, además, puede enviar al azar **fotos**, **videos** y **audios** cuando detecta esas palabras en el mensaje del usuario.

> Este repositorio contiene el script `asissbot.py`. Ajusta en el código todos los valores marcados con `...` antes de ejecutar.


## 🗂️ Tabla de contenidos
- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalación rápida](#-instalación-rápida)
- [Configuración](#-configuración)
- [Ejecución](#-ejecución)
- [Cómo funciona la llamada al LLM](#-cómo-funciona-la-llamada-al-llm)
- [Estructura sugerida](#-estructura-sugerida)
- [Personalización](#-personalización)
- [Solución de problemas](#-solución-de-problemas)
- [Seguridad](#-seguridad)
- [Hoja de ruta](#-hoja-de-ruta)
- [Licencia](#-licencia)


## ✨ Características
- 💬 **Chat** con un LLM (endpoint HTTP configurable).
- 🖼️/🎬/🎧 **Medios aleatorios**: envía **foto**, **video**/**vídeo** o **audio** si detecta esas palabras en el mensaje.
- 🔒 **Control de acceso** por `MY_USER_ID` (solo responde al usuario autorizado).
- ⌨️ **Indicador de escritura** (“escribiendo…”) mientras genera respuesta.
- 🧰 **Logs y errores** con mensajes claros para el usuario.


## 📦 Requisitos
- **Python 3.10+** (recomendado 3.10 o superior).
- Un bot creado con **@BotFather** → obtendrás el `TELEGRAM_BOT_TOKEN`.
- Un endpoint compatible con **LM Studio** que acepte `POST` con campos como `model`, `prompt`, `max_tokens` y `stop`.  
  Ejemplo de URL: `http://localhost:1234/v1/completions`


## ⚡ Instalación rápida

```bash
git clone <tu-repo> asissbot
cd asissbot

python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows (PowerShell)
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
```


## 🔧 Configuración
Edita en `asissbot.py` los valores **marcados con `...`**:

- `MY_USER_ID`: tu ID numérico de Telegram (el bot solo te responderá a ti).
- `TELEGRAM_BOT_TOKEN`: token de tu bot.
- `LM_STUDIO_SERVER_URL`: URL del servidor LM Studio (p. ej. `http://localhost:1234/v1/completions`).
- `SYSTEM_PROMPT`: prompt del sistema para guiar el estilo del asistente.
- Directorios de medios:
  - `PHOTO_DIRECTORY`: carpeta con imágenes (`.png`, `.jpg`, `.jpeg`).
  - `VIDEO_DIRECTORY`: carpeta con vídeos (`.mp4`, `.mov`, `.avi`, `.mkv`).
  - `AUDIO_DIRECTORY`: carpeta con audios (`.ogg`).

> 💡 **Sugerencia**: si prefieres no “quemar” credenciales en el código, puedes refactorizar el script para leer de variables de entorno (`os.getenv`) o un `.env` con [python-dotenv](https://pypi.org/project/python-dotenv/).


## ▶️ Ejecución

```bash
python asissbot.py
```

En la consola verás algo como “El bot está corriendo…”. En tu chat de Telegram:

- Envía **`/start`** para el mensaje de bienvenida.
- Envía texto normal para conversar con el modelo.
- Usa palabras clave:
  - **`foto`** → envía una foto aleatoria.
  - **`video`**/**`vídeo`** → envía un vídeo aleatorio.
  - **`audio`** → envía un audio (`.ogg`).


## 🧠 ¿Cómo funciona la llamada al LLM?
Cuando envías un mensaje, el bot compone un *prompt* con `SYSTEM_PROMPT` + el texto del usuario y hace `POST` a `LM_STUDIO_SERVER_URL` con un JSON como:

```json
{
  "model": "llama-3-8b-lexi-uncensored@q4_k_m",
  "prompt": "…PROMPT COMPLETO…",
  "max_tokens": 200,
  "stop": ["Usuario:", "Asistente:"]
}
```

> Ajusta los campos según la API exacta que exponga tu instancia de LM Studio.


## 🗃️ Estructura sugerida

```
asissbot/
├─ asissbot.py
├─ requirements.txt
├─ README.md
└─ media/
   ├─ photos/
   ├─ videos/
   └─ audios/
```

Y en el script:
```python
PHOTO_DIRECTORY = "media/photos"
VIDEO_DIRECTORY = "media/videos"
AUDIO_DIRECTORY = "media/audios"
```


## 🧩 Personalización

- **Palabras clave**: amplía o cambia las palabras que disparan el envío de medios (p. ej. *imagen*, *clip*, *música*).
- **Modelo/parámetros**: experimenta con `model`, `max_tokens`, `stop`, etc.
- **Retrasos**: el script usa `asyncio.sleep` para simular tiempos humanos; puedes ajustarlos.
- **Mensajes**: modifica textos de ayuda, errores y el saludo de `/start`.


## 🧯 Solución de problemas

- **No responde a mis mensajes**  
  - Verifica que `MY_USER_ID` es tu ID numérico real (puedes usar @userinfobot en Telegram) y que el bot está en línea.
- **“No puedo comunicarme con el servidor de IA.”**  
  - Comprueba que `LM_STUDIO_SERVER_URL` es accesible y que LM Studio está corriendo en esa URL.
- **“No hay fotos/videos/audios disponibles.”**  
  - Asegúrate de que las carpetas de medios existen y contienen archivos con extensiones válidas.
- **Responde muy lento**  
  - Reduce los `sleep`, ajusta el modelo o baja `max_tokens`.


## 🔐 Seguridad
- Mantén **privados** tu `TELEGRAM_BOT_TOKEN` y `MY_USER_ID`.
- Revisa los medios que compartes para evitar información sensible.
- Si expones LM Studio fuera de tu red local, **protege la API** (autenticación, firewall, TLS).


## 🛣️ Hoja de ruta
- [ ] Comandos para enviar medios bajo demanda (`/foto`, `/video`, `/audio`).
- [ ] Soporte para más formatos de audio (MP3/OPUS) y transcodificación.
- [ ] Persistencia de conversación (contexto) y memoria breve.
- [ ] Dockerfile y `docker-compose.yml`.
- [ ] Tests básicos y CI.


## 📄 Licencia
Este proyecto se distribuye “tal cual”. Úsalo, modifícalo y adáptalo según tus necesidades internas. Si necesitas una licencia formal, puedes marcarlo como **MIT** o **Apache-2.0** en tu fork.

---

<p align="center">
Desarrollado con ❤️ — ¡Feliz hacking!
</p>


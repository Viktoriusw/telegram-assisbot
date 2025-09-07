import os
import random
import logging
import requests
import asyncio
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# CONFIGURACIÓN
MY_USER_ID = ...  # Reemplaza esto con tu verdadero user_id
TELEGRAM_BOT_TOKEN = '...'
LM_STUDIO_SERVER_URL = '...'

SYSTEM_PROMPT = "Asume el rol de ..."

PHOTO_DIRECTORY = "..."
VIDEO_DIRECTORY = "..."
AUDIO_DIRECTORY = "..."

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Verificación de acceso
def is_authorized(user_id: int) -> bool:
    return user_id == MY_USER_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update.effective_user.id):
        return
    await update.message.reply_text(
        "¡Hola! Soy un bot con inteligencia artificial. "
        "Envíame un mensaje para conversar, menciona 'foto', 'video' o 'audio' para recibir medios."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update.effective_user.id):
        return

    user_message = update.message.text.lower()
    logging.info(f"Mensaje recibido: {user_message}")

    if "foto" in user_message:
        await send_random_photo(update, context)
        return
    if "video" in user_message or "vídeo" in user_message:
        await send_random_video(update, context)
        return
    if "audio" in user_message:
        await send_random_audio(update, context)
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    full_prompt = f"{SYSTEM_PROMPT}\n\nUsuario: {user_message}\nAsistente:"
    try:
        await asyncio.sleep(2)
        response = requests.post(LM_STUDIO_SERVER_URL, json={
            "model": "...",
            "prompt": full_prompt,
            "max_tokens": 200,
            "stop": ["Usuario:", "Asistente:"]
        })

        if response.status_code == 200:
            ai_response = response.json().get("choices", [{}])[0].get("text", "").strip()
        else:
            ai_response = f"Error en la solicitud: {response.status_code}."

        await update.message.reply_text(ai_response)
    except requests.exceptions.RequestException as e:
        await update.message.reply_text("No puedo comunicarme con el servidor de IA.")
        logging.error(f"Error en la comunicación con LM Studio: {e}")
    except Exception as e:
        await update.message.reply_text("Ocurrió un error inesperado.")
        logging.error(f"Error inesperado: {e}")

async def send_random_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photos = [f for f in os.listdir(PHOTO_DIRECTORY) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not photos:
            await update.message.reply_text("No hay fotos disponibles.")
            return
        photo_path = os.path.join(PHOTO_DIRECTORY, random.choice(photos))
        await asyncio.sleep(2)
        with open(photo_path, 'rb') as photo:
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
    except Exception as e:
        logging.error(f"Error al enviar foto: {e}")

async def send_random_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        videos = [f for f in os.listdir(VIDEO_DIRECTORY) if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]
        if not videos:
            await update.message.reply_text("No hay videos disponibles.")
            return
        video_path = os.path.join(VIDEO_DIRECTORY, random.choice(videos))
        await asyncio.sleep(3)
        with open(video_path, 'rb') as video:
            await context.bot.send_video(chat_id=update.effective_chat.id, video=video)
    except Exception as e:
        logging.error(f"Error al enviar video: {e}")

async def send_random_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        audios = [f for f in os.listdir(AUDIO_DIRECTORY) if f.lower().endswith('.ogg')]
        if not audios:
            await update.message.reply_text("No hay audios disponibles.")
            return
        audio_path = os.path.join(AUDIO_DIRECTORY, random.choice(audios))
        await asyncio.sleep(2)
        with open(audio_path, 'rb') as audio:
            await context.bot.send_audio(chat_id=update.effective_chat.id, audio=audio)
    except Exception as e:
        logging.error(f"Error al enviar audio: {e}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logging.info("El bot está corriendo...")
    app.run_polling()


if __name__ == "__main__":
    main()

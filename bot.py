import logging
import os
import threading
import time
import requests
from threading import Thread
from flask import Flask
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.utils import executor

# Переменные окружения
API_TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Flask для Render
app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ====== AUTOPING ======
def keep_alive():
    url = f"https://{os.getenv('RENDER_EXTERNAL_URL', '')}"
    if not url:
        url = "https://<твой-домен>.onrender.com/"
    while True:
        try:
            requests.get(url)
        except Exception as e:
            print(f"Ping error: {e}")
        time.sleep(300)  # каждые 5 минут
# =======================

# Пересылка сообщений админу
@dp.message_handler(content_types=ContentType.ANY)
async def forward_to_admin(message: types.Message):
    if message.text:
        await bot.send_message(ADMIN_ID, f"Сообщение от анонимного пользователя:\n{message.text}")
    elif message.photo:
        photo = message.photo[-1].file_id
        caption = message.caption if message.caption else "Фото без подписи"
        await bot.send_photo(ADMIN_ID, photo, caption=f"Аноним прислал фото:\n{caption}")
    elif message.document:
        await bot.send_document(ADMIN_ID, message.document.file_id, caption="Аноним прислал документ")
    elif message.voice:
        await bot.send_voice(ADMIN_ID, message.voice.file_id, caption="Аноним прислал голосовое сообщение")
    elif message.video:
        await bot.send_video(ADMIN_ID, message.video.file_id, caption="Аноним прислал видео")
    else:
        await bot.send_message(ADMIN_ID, "Аноним прислал сообщение неизвестного формата.")
    await message.answer("Сообщение отправлено админу анонимно ✅")

def run_bot():
    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    threading.Thread(target=keep_alive, daemon=True).start()  # запуск автопинга
    Thread(target=run_flask).start()
    run_bot()



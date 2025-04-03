import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from datetime import datetime
import base64
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Расшифровка Google Credentials
creds_b64 = os.getenv("GOOGLE_CREDS_BASE64")
with open("google-credentials.json", "wb") as f:
    f.write(base64.b64decode(creds_b64))

# Подключение к Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("google-credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Трекер Даниила").sheet1

# Telegram Bot
API_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Я твой трекер. В 20:00 буду присылать вопросы по дню ✍️")

@dp.message_handler(commands=['track'])
async def track(message: types.Message):
    await bot.send_message(message.chat.id, "1. Во сколько встал?\n2. Была ли тренировка?\n3. Сколько часов фокусной работы?\n4. Что сделал по боту?\n5. Что мешало?\n6. Достижение дня?")

@dp.message_handler()
async def save(message: types.Message):
    data = message.text.split('\n')
    now = datetime.now().strftime("%Y-%m-%d")
    row = [now] + data[:6]
    sheet.append_row(row)
    await message.reply("Записал ✅")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

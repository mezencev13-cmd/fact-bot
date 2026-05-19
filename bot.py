import asyncio
import random
import httpx
from datetime import datetime, timedelta
import pytz
from telegram import Bot

TOKEN = "8683591887:AAEpfRYIKTodu00K5bJCjBmKlWc_GiB7FU4"
CHAT_ID = 104815136

async def get_fact():
    async with httpx.AsyncClient() as client:
        # Получаем факт
        response = await client.get(
            "https://uselessfacts.jsph.pl/api/v2/facts/random",
            params={"language": "en"}
        )
        fact = response.json()["text"]
        
        # Переводим на русский
        translate = await client.get(
            "https://api.mymemory.translated.net/get",
            params={"q": fact, "langpair": "en|ru"}
        )
        translated = translate.json()["responseData"]["translatedText"]
        return translated

async def send_daily_fact():
    bot = Bot(token=TOKEN)
    
    # Отправляем факт сразу при запуске
    fact = await get_fact()
    await bot.send_message(
        chat_id=CHAT_ID,
        text=f"🧠 Факт дня:\n\n{fact}"

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
        response = await client.get(
            "https://uselessfacts.jsph.pl/api/v2/facts/random",
            params={"language": "en"}
        )
        data = response.json()
        return data["text"]

async def send_daily_fact():
    bot = Bot(token=TOKEN)
    while True:
        now = datetime.now(pytz.timezone("Europe/Moscow"))
        
        random_hour = random.randint(9, 23)
        random_minute = random.randint(0, 59)
        
        target = now.replace(hour=random_hour, minute=random_minute, second=0, microsecond=0)
        if target <= now:
            target = target + timedelta(days=1)
        
        wait_seconds = (target - now).total_seconds()
        await asyncio.sleep(wait_seconds)
        
        fact = await get_fact()
        await bot.send_message(
            chat_id=CHAT_ID,
            text=f"🧠 Факт дня:\n\n{fact}"
        )

if __name__ == "__main__":
    asyncio.run(send_daily_fact())

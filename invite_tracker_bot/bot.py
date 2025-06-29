import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from db import init_db
from handlers import router

async def main():
    await init_db()
    bot = Bot(BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

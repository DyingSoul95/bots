import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis

from handlers import users, mess

redis = Redis(host="localhost")
storage = RedisStorage(redis=redis)


async def main():
    bot = Bot(token="6638585663:AAGuCjCfFHhRyTnE8-CLaasCeR-UXWHnR3I")

    dp = Dispatcher(storage=storage)

    dp.include_routers(users.router, mess.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

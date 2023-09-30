import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis

from handlers import users, mess
from config import Config, load_config

config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token

redis = Redis(host="localhost")
storage = RedisStorage(redis=redis)


async def main():
    bot = Bot(BOT_TOKEN)

    dp = Dispatcher(storage=storage)

    dp.include_routers(users.router, mess.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

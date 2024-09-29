import asyncio
import logging
import sys
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import config
from handlers import common_handlers


async def on_startup(bot: Bot) -> None:
    logging.info("🚀 Бот запущен.")


async def main() -> None:
    dp = Dispatcher()
    dp.startup.register(on_startup)

    dp.include_router(common_handlers.router)

    # Информация о системе и чате
    dp["system_info"] = {}
    dp["system_info"]["started_at"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    dp["chat_info"] = {}
    dp["chat_info"]["web_id"] = {}

    bot = Bot(
        token=config.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging._nameToLevel[config.level], stream=sys.stdout)
    try:
        web_users = asyncio.run(main())
    except KeyboardInterrupt:
        pass
    finally:
        logging.info("❎ Бот остановлен.")

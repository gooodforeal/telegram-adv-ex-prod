import asyncio
import logging
from logs.config import configure_logging
from config import settings
from aiogram import Bot, Dispatcher
from handlers.referral_handler import router as referral_router
from handlers.startup_handler import router as startup_router
from handlers.admin_handler import router as admin_router


logger = logging.getLogger(__name__)
configure_logging()


async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_routers(startup_router, referral_router, admin_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.info("Starting bot!")
    asyncio.run(main())

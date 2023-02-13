import asyncio
from datetime import datetime
from pytz import timezone
import logging
import sentry_sdk

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.config import load_config, Config, I18N_DOMAIN, LOCALES_DIR
from tgbot.filters.admin import AdminFilter
from tgbot.filters.is_digit import IsDigitFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.echo import register_echo
from tgbot.handlers.user import register_user
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.middlewares.language_middleware import ACLMiddleware
from tgbot.middlewares.scheduler import SchedulerMiddleware
from tgbot.models.models import create_db

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config, scheduler):
    dp.setup_middleware(EnvironmentMiddleware(config=config))
    dp.setup_middleware(ACLMiddleware(I18N_DOMAIN, LOCALES_DIR))
    dp.setup_middleware(SchedulerMiddleware(scheduler))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsDigitFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)

    # debug
    # register_echo(dp)


async def send_message_to_admin(bot: Bot, config: Config):
    for admin_id in config.tg_bot.admin_ids:
        await bot.send_message(text="Bugungi excel faylni tashlang!", chat_id=admin_id)


def scheduled_jobs(scheduler, bot, config):
    date = datetime.now(timezone("Asia/Tashkent")).hour
    if date == 10:
        scheduler.add_job(send_message_to_admin, "interval", args=(bot, config), minutes=10, id="job")

    else:
        if len(scheduler.get_jobs()) == 2:
            scheduler.remove_job("job")
        else:
            pass


def set_scheduled_jobs(scheduler, bot, config):
    scheduler.add_job(scheduled_jobs, "cron", args=(scheduler, bot, config), hour="10-22", timezone="Asia/Tashkent")


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config: Config = load_config(".env")
    sentry_sdk.init(
        dsn=config.misc.sentry_sdk,

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
    )

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    scheduler = AsyncIOScheduler()
    bot['config'] = config
    register_all_middlewares(dp, config, scheduler)
    register_all_filters(dp)
    register_all_handlers(dp)

    set_scheduled_jobs(scheduler, bot, config)
    await create_db()

    try:
        scheduler.start()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")

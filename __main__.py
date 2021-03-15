import logging
import os

from telegram.ext import Updater

from handlers import add_handlers

updater = Updater(token=os.getenv("TELEGRAM_TOKEN"), use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

add_handlers(dispatcher)

updater.start_polling()

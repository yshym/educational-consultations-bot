from telegram import Update
from telegram.ext import CallbackQueryHandler, CallbackContext

from models.category import Category


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    query.edit_message_text(text=Category(query.data).value)


button_handler = CallbackQueryHandler(button)

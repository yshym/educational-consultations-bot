from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CallbackContext

from models.category import Category, Subcategory
from utils.iterable import batch


def reply_markup_from_categories(categories):
    keyboard = batch(
        [
            InlineKeyboardButton(c.value, callback_data=c.value)
            for c in categories
        ],
        3,
    )
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data.startswith("yes|"):
        _, category = query.data.split("|")
        reply_markup = reply_markup_from_categories(
            Category(category).subcategories
        )

        query.edit_message_reply_markup(reply_markup=reply_markup)
    elif query.data in Subcategory.values():
        query.edit_message_text(text=Subcategory(query.data).link)
    elif query.data in Category.values():
        category = query.data
        reply_markup = reply_markup_from_categories(
            Category(category).subcategories
        )

        query.edit_message_text(text=Category(query.data).value)
        query.edit_message_reply_markup(reply_markup=reply_markup)


button_handler = CallbackQueryHandler(button)

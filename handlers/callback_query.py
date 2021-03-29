from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CallbackContext

from models import predict
from models.category import Category, Subcategory
from utils.iterable import batch
from utils.telegram import reply_markup_from_categories


def button_wrapper(nlp, models):
    def button(update: Update, _context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()

        yes, category, subcategory, text = query.data.split("|")
        if yes:
            if subcategory:
                query.edit_message_reply_markup(reply_markup=None)
            else:
                subcategory = predict(nlp, models[Category(category)], text)
                reply_markup = reply_markup_from_categories(
                    Category(category).subcategories,
                    category,
                    subcategory,
                    text,
                )
                query.edit_message_text(text=Subcategory(subcategory).link)
                query.edit_message_reply_markup(reply_markup=reply_markup)
        elif subcategory:
            query.edit_message_text(text=Subcategory(subcategory).link)
        else:
            subcategory = predict(nlp, models[Category(category)], text)
            reply_markup = reply_markup_from_categories(
                Category(category).subcategories, category, subcategory, text
            )

            query.edit_message_text(text=Subcategory(subcategory).link)
            query.edit_message_reply_markup(reply_markup=reply_markup)

    return button


button_handler_wrapper = lambda nlp, models: CallbackQueryHandler(
    button_wrapper(nlp, models)
)

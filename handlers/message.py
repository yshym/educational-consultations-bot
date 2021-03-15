from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import MessageHandler, Filters

from models import predict
from models.category import Category


def category_wrapper(nlp, model):
    def category(update, context):
        category = predict(nlp, model, update.message.text)
        keyboard = [
            [
                InlineKeyboardButton(c.value, callback_data=c.value)
                for c in Category
                if c.value != category
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=category,
            reply_markup=reply_markup,
        )

    return category


category_handler_wrapper = lambda nlp, model: MessageHandler(
    Filters.text & (~Filters.command), category_wrapper(nlp, model)
)

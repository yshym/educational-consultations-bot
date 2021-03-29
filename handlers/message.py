from telegram.ext import MessageHandler, Filters

from models import predict
from models.category import Category
from utils.telegram import reply_markup_from_categories


def category_wrapper(nlp, model):
    def category(update, context):
        text = update.message.text
        category = predict(nlp, model, text)
        reply_markup = reply_markup_from_categories(
            Category, category, "", text
        )

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=category,
            reply_markup=reply_markup,
        )

    return category


category_handler_wrapper = lambda nlp, model: MessageHandler(
    Filters.text & (~Filters.command), category_wrapper(nlp, model)
)

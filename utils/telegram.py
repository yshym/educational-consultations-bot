from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .iterable import batch
from models.category import Subcategory


def reply_markup_from_categories(
    categories, category="", subcategory="", text=""
):
    sub = isinstance(list(categories)[0], Subcategory)
    buttons = [
        InlineKeyboardButton(
            "yes", callback_data=f"yes|{category}|{subcategory}|{text}"
        )
    ]
    for c in categories:
        if c.value != (subcategory if sub else category):
            category_value = category if sub else c.value
            subcategory_value = c.value if sub else subcategory
            button = InlineKeyboardButton(
                c.value,
                callback_data=f"|{category_value}|{subcategory_value}|{text}",
            )
            buttons.append(button)

    keyboard = batch(buttons, 3)
    reply_markup = InlineKeyboardMarkup(keyboard)

    return reply_markup

import spacy

import models
from .callback_query import button_handler
from .command import start_handler
from .message import category_handler_wrapper


def add_handlers(dispatcher):
    model = models.load()
    nlp = models.load_nlp()

    dispatcher.add_handler(category_handler_wrapper(nlp, model))
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(button_handler)

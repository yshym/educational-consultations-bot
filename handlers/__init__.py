import logging
import os

import models
from models import Category
from .callback_query import button_handler_wrapper
from .command import start_handler
from .message import category_handler_wrapper


def add_handlers(dispatcher):
    nlp = models.load_nlp()
    category_model = models.load(os.getenv("CATEGORY_MODEL_FILE_PATH"))
    frontend_subcategory_model = models.load(
        os.getenv("FRONTEND_SUBCATEGORY_MODEL_FILE_PATH")
    )
    backend_subcategory_model = models.load(
        os.getenv("BACKEND_SUBCATEGORY_MODEL_FILE_PATH")
    )

    dispatcher.add_handler(category_handler_wrapper(nlp, category_model))
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(
        button_handler_wrapper(
            nlp,
            {
                Category.FRONTEND: frontend_subcategory_model,
                Category.BACKEND: backend_subcategory_model,
            },
        )
    )

    logging.info("Handlers were added")

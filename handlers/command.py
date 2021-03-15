from telegram import Update
from telegram.ext import CommandHandler, CallbackQueryHandler, CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello, I'm educational consultations bot. Ask me, what you want to know",
    )


start_handler = CommandHandler("start", start)

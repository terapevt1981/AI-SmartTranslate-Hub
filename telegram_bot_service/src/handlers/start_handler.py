from telegram import Update
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger(__name__)

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /start
    """
    try:
        user = update.effective_user
        logger.info(f"User {user.id} ({user.username}) started the bot")
        
        await update.message.reply_text(
            f"Привет, {user.first_name}! Я бот-переводчик. "
            "Просто отправь мне текст, и я переведу его."
        )
    except Exception as e:
        logger.error(f"Error in start_handler: {e}", exc_info=True)
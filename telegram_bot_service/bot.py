from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from handlers.message_handler import handle_message
from handlers.error_handler import error_handler
from config import TELEGRAM_BOT_TOKEN
import logging

def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Регистрация обработчиков
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dispatcher.add_error_handler(error_handler)

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main() 
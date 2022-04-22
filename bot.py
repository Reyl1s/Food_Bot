import os
import logging

from dotenv import load_dotenv, dotenv_values
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from handlers.error_handler import error
from handlers.start_handler import start

# load config
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    config = dotenv_values(".env")

# create bot updater and dispatcher
updater = Updater(token=config['BOT_TOKEN'])
dispatcher = updater.dispatcher

# logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# start handler
def start(update: Update, context: CallbackContext):
    start(update, context)

# errors handler
def error_handler(update, context: CallbackContext):
    error(update, context)

if __name__ == '__main__':
    # add commands handlers
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # add errors handler
    dispatcher.add_error_handler(error_handler)

    # start bot
    updater.start_polling()
    updater.idle()

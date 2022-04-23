import logging

from telegram.ext import Updater, CommandHandler
from handlers.error_handler import error_command
from handlers.start_handler import start_command
from handlers.register_handler import register_command
from database import init_database
from config import get_config, init_config

# logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# inits
init_config()
init_database()

config = get_config()

# create bot updater and dispatcher
updater = Updater(token=config['BOT_TOKEN'])
dispatcher = updater.dispatcher

# start command
def start_handler(update, context):
    start_command(update, context)

# errors command
def error_handler(update, context):
    error_command(update, context)

def register_handler(update, _):
    register_command(update)

if __name__ == '__main__':
    # add commands handlers
    start_command_handler = CommandHandler('start', start_handler)
    dispatcher.add_handler(start_command_handler)

    register_command_handler = CommandHandler('register', register_handler)
    dispatcher.add_handler(register_command_handler)

    # add errors handler
    dispatcher.add_error_handler(error_handler)

    # start bot
    updater.start_polling()
    updater.idle()

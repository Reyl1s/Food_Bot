import logging
import pytz

from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, Defaults
from handlers.error_handler import error_handler
from handlers.register_handler import delete_handler
from handlers.callback_query_handler import conv_handler
from config import Config

# logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    config = Config()

    # create bot updater and dispatcher
    defaults = Defaults(parse_mode=ParseMode.HTML, tzinfo=pytz.timezone('Europe/Moscow'))
    updater = Updater(config.data['BOT_TOKEN'], use_context=True, defaults=defaults)
    dispatcher = updater.dispatcher

    # add handlers
    dispatcher.add_handler(CommandHandler('d', delete_handler))
    dispatcher.add_handler(conv_handler())

    # add errors handler
    dispatcher.add_error_handler(error_handler)

    # start bot
    updater.start_polling()
    updater.idle()

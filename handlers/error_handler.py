import sys
import traceback
import vars

from config import Config
from telegram import ParseMode, Update
from telegram.ext import CallbackContext
from telegram.utils.helpers import mention_html

def error_handler(update: Update, context: CallbackContext):
    config = Config()
    devs = [config.data['ROOT_CHAT_ID']]

    if update.effective_message:
        text = vars.user_error_message
        update.effective_message.reply_text(text)
    
    trace = ''.join(traceback.format_tb(sys.exc_info()[2]))
    payload = []
    
    # user
    if update.effective_user:
        bad_user = mention_html(update.effective_user.id, update.effective_user.first_name)
        payload.append(f' с пользователем {bad_user}')
    
    # chat
    if update.effective_chat:
        payload.append(f' внутри чата <i>{update.effective_chat.title}</i>')
        if update.effective_chat.username:
            payload.append(f' (@{update.effective_chat.username})')
    
    # pool
    if update.poll:
        payload.append(f' с id опроса {update.poll.id}.')
    
    text = f"Ошибка <code>{context.error}</code> случилась{''.join(payload)}. " \
        f"Полная трассировка:\n\n<code>{trace}</code>" \
        "\n#error"
    
    for dev_id in devs:
        context.bot.send_message(dev_id, text, parse_mode=ParseMode.HTML)
    
    raise

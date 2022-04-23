from telegram import Update
from telegram.ext import CallbackContext
from database import check_user

def start_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_is_created = check_user(user_id)

    if user_is_created:
        update.effective_message.reply_text('User is created')
    else:
        update.effective_message.reply_text('Сначала нужно зарегестрироваться. Введите команду /register')

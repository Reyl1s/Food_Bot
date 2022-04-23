from telegram import Update
from database import check_user, create_user, delete_user

def register_command(update: Update):
    user_id = update.effective_user.id
    user_is_created = check_user(user_id)

    if user_is_created:
        update.effective_message.reply_text('Вы уже зарегестрированы')
    else:
        create_user(user_id, update.effective_user.username)
        update.effective_message.reply_text('Вы успешно зарегестрировались')
    
def delete_command(update: Update):
    delete_user(update.effective_user.id)

from telegram import ReplyKeyboardRemove, Update
from config import Config
from database.users_db import Users_DB
from handlers.start_handler import start_by_created_user_handler

def register_handler(update: Update, context):
    user = update.effective_user
    user_id = user.id
    users_db = Users_DB()

    user_is_created = users_db.check_user(user_id)

    remove_markup = ReplyKeyboardRemove(True)

    if user_is_created:
        update.effective_message.reply_text('Вы уже зарегестрированы ✅', reply_markup = remove_markup)
    else:
        contact = update.effective_message.contact
        nickname = user.username
        user_name = contact.first_name
        phone = contact.phone_number

        users_db.create_user(user_id, nickname, user_name, phone)
        update.effective_message.reply_text('Вы успешно зарегестрировались ✅', reply_markup = remove_markup)

    users_db.close()
    
    return start_by_created_user_handler(update, context)

def delete_handler(update: Update, _):
    user_id = str(update.effective_user.id)
    config = Config()
    users_db = Users_DB()

    root_id = config.data['ROOT_CHAT_ID']
    user_is_root = user_id == root_id

    if user_is_root:
        user_nickname = update.message.text.replace('/d', '').strip()
        user_id_to_delete = users_db.get_user_id_by_nickname(user_nickname)

        if user_id_to_delete is None:
            update.effective_message.reply_text('Пользователь уже удален ✅')
        else:
            users_db.delete_user(user_id_to_delete)
            update.effective_message.reply_text('Пользователь успешно удален ✅')
    else:
        update.effective_message.reply_text('У Вас нет для этого прав! ❌')
    
    users_db.close()

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import ConversationHandler
from database.users_db import Users_DB
from states import *

def start_handler(update: Update, context):
    user_id = update.effective_user.id
    users_db = Users_DB()

    user_is_created = users_db.check_user(user_id)

    if user_is_created:
        users_db.close()
        return start_by_created_user_handler(update, context)
    else:
        user_is_deleted = users_db.check_user_is_deleted(user_id)

        if user_is_deleted:
            update.effective_message.reply_text('Доступ запрещен! Вы в бане ❌')
            return ConversationHandler.END
        else:
            keyboard = [
                [
                    KeyboardButton('Передать контакты 📩', request_contact=True)
                ]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            
            update.message.reply_text(
                text = 'Зарегестрируйтесь, передав свои контакты 📩', reply_markup=reply_markup
            )

            users_db.close()
            return REGISTER

def start_by_created_user_handler(update: Update, _):
    keyboard = [
        [
            InlineKeyboardButton("Новый заказ 📝", callback_data=str(START_ORDER_HANDLER)),
            InlineKeyboardButton("Редактировать ✏️", callback_data=str(EDIT_PROFILE_HANDLER)),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.effective_message.reply_text(
        text="С чего начнем?", reply_markup=reply_markup
    )

    return START

def start_over_handler(update: Update, _):
    query = update.callback_query

    keyboard = [
        [
            InlineKeyboardButton("Новый заказ 📝", callback_data=str(START_ORDER_HANDLER)),
            InlineKeyboardButton("Редактировать ✏️", callback_data=str(EDIT_PROFILE_HANDLER)),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="С чего начнем?", reply_markup=reply_markup
    )

    return START

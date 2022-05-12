from telegram import Update, ParseMode
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database.users_db import Users_DB
from handlers.start_handler import start_handler, start_by_created_user_handler, start_over_handler
from handlers.register_handler import register_handler
from states import *

def conv_handler():
    start_over = CallbackQueryHandler(start_over_handler, pattern='^' + str(START_OVER) + '$')
    return ConversationHandler(
        entry_points=[CommandHandler('start', start_handler)],
        states={
            REGISTER: [MessageHandler(Filters.contact, register_handler)],
            START: [
                CallbackQueryHandler(start_order_handler, pattern='^' + str(START_ORDER_HANDLER) + '$'),
                CallbackQueryHandler(edit_profile_handler, pattern='^' + str(EDIT_PROFILE_HANDLER) + '$')
            ],
            START_ORDER: [
                start_over
            ],
            EDIT_PROFILE: [
                start_over,
                CallbackQueryHandler(edit_requisites_handler, pattern='^' + str(EDIT_REQUISITES_HANDLER) + '$'),
                CallbackQueryHandler(edit_user_name_handler, pattern='^' + str(EDIT_NAME_HANDLER) + '$')
            ],
            EDIT_REQUISITES: [MessageHandler(Filters.text, apply_requisites_handler)],
            EDIT_NAME: [MessageHandler(Filters.text, apply_user_name_handler)]
        },
        fallbacks=[CommandHandler('start', start_handler)]
    )

def start_order_handler(update: Update, _):
    query = update.callback_query
    
    keyboard = [
        [
            InlineKeyboardButton("⏪ В начало", callback_data=str(START_OVER))
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Начало заказа 📝", reply_markup=reply_markup
    )

    return START_ORDER

def edit_profile_handler(update: Update, _):
    query = update.callback_query
    
    keyboard = [
        [
            InlineKeyboardButton("Реквизиты 💰", callback_data=str(EDIT_REQUISITES_HANDLER)),
            InlineKeyboardButton("Имя 📛", callback_data=str(EDIT_NAME_HANDLER))
            
        ],
        [
            InlineKeyboardButton("⏪ В начало", callback_data=str(START_OVER))
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard,)
    query.edit_message_text(
        text="Редактирование профиля ✏️", reply_markup=reply_markup
    )

    return EDIT_PROFILE

def edit_requisites_handler(update: Update, _):
    query = update.callback_query
    user_id = update.effective_user.id

    user_db = Users_DB()
    user_phone = user_db.get_user_phone_by_id(user_id)
    user_db.close()

    query.edit_message_text(f'Отправьте свои реквизиты (например <code>+{user_phone}, Тинькофф</code>)', parse_mode=ParseMode.HTML)

    return EDIT_REQUISITES

def apply_requisites_handler(update: Update, context):
    user_id = update.effective_user.id
    requisites = update.message.text
    users_db = Users_DB()

    users_db.apply_user_requisites(user_id, requisites)
    users_db.close()

    update.message.reply_text('Реквизиты успешно сохранены ✅')

    return start_by_created_user_handler(update, context)

def edit_user_name_handler(update: Update, _):
    query = update.callback_query
    query.edit_message_text('Напишите свое имя')

    return EDIT_NAME

def apply_user_name_handler(update: Update, context):
    user_id = update.effective_user.id
    user_name = update.message.text
    users_db = Users_DB()

    users_db.apply_user_name(user_id, user_name)
    users_db.close()

    update.message.reply_text('Имя успешно сохранено ✅')

    return start_by_created_user_handler(update, context)

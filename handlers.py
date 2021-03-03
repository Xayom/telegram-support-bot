import os
from telegram.ext import CommandHandler, MessageHandler, Filters
import time
import requests

from settings import WELCOME_MESSAGE, TELEGRAM_SUPPORT_CHAT_ID

title = None
image = None

def start(update, context):
    update.message.reply_text(WELCOME_MESSAGE)

#     user_info = update.message.from_user.to_dict()

#     context.bot.send_message(
#         chat_id=TELEGRAM_SUPPORT_CHAT_ID,
#         text=f"""
# 📞 Connected {user_info}.
#         """,
#     )

def forward_to_chat(update, context):
    """{ 
        'message_id': 5, 
        'date': 1605106546, 
        'chat': {'id': 49820636, 'type': 'private', 'username': 'danokhlopkov', 'first_name': 'Daniil', 'last_name': 'Okhlopkov'}, 
        'text': 'TEST QOO', 'entities': [], 'caption_entities': [], 'photo': [], 'new_chat_members': [], 'new_chat_photo': [], 'delete_chat_photo': False, 'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False, 
        'from': {'id': 49820636, 'first_name': 'Daniil', 'is_bot': False, 'last_name': 'Okhlopkov', 'username': 'danokhlopkov', 'language_code': 'en'}
    }"""
    update.message.forward(chat_id=TELEGRAM_SUPPORT_CHAT_ID)


def forward_to_user(update, context):
    """{
        'message_id': 10, 'date': 1605106662, 
        'chat': {'id': -484179205, 'type': 'group', 'title': '☎️ SUPPORT CHAT', 'all_members_are_administrators': True}, 
        'reply_to_message': {
            'message_id': 9, 'date': 1605106659, 
            'chat': {'id': -484179205, 'type': 'group', 'title': '☎️ SUPPORT CHAT', 'all_members_are_administrators': True}, 
            'forward_from': {'id': 49820636, 'first_name': 'Daniil', 'is_bot': False, 'last_name': 'Okhlopkov', 'danokhlopkov': 'okhlopkov', 'language_code': 'en'}, 
            'forward_date': 1605106658, 
            'text': 'g', 'entities': [], 'caption_entities': [], 'photo': [], 'new_chat_members': [], 'new_chat_photo': [], 
            'delete_chat_photo': False, 'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False, 
            'from': {'id': 1440913096, 'first_name': 'SUPPORT', 'is_bot': True, 'username': 'lolkek'}
        }, 
        'text': 'ggg', 'entities': [], 'caption_entities': [], 'photo': [], 'new_chat_members': [], 'new_chat_photo': [], 'delete_chat_photo': False, 
        'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False, 
        'from': {'id': 49820636, 'first_name': 'Daniil', 'is_bot': False, 'last_name': 'Okhlopkov', 'username': 'danokhlopkov', 'language_code': 'en'}
    }"""
    user_id = update.message.reply_to_message.forward_from.id
    context.bot.copy_message(
        message_id=update.message.message_id,
        chat_id=user_id,
        from_chat_id=update.message.chat_id
    )

def post_data(update, context):
    global title, image
#     context.bot.send_message(
#         chat_id=TELEGRAM_SUPPORT_CHAT_ID,
#         text='Загрузка...',
#     )
    update.message.reply_text('Загрузка...')
    url = 'http://gamer.pythonanywhere.com/api/v1/posts/'
    myobj = {'description': title, 'img_url': image}

    x = requests.post(url, data = myobj)
#     context.bot.send_message(
#         chat_id=TELEGRAM_SUPPORT_CHAT_ID,
#         text='http://gamer.pythonanywhere.com/media/out.png?{}'.format(time.time() * 1000),
#     )
    update.message.reply_text('http://gamer.pythonanywhere.com/media/out.png?{}'.format(time.time() * 1000))
    title = image = None
    

def get_title(update, context):
    global title
    title = update.message.text
    if image:
        post_data(update, context)
    else:
        update.message.reply_text('Добавьте фото')
#         context.bot.send_message(
#             chat_id=TELEGRAM_SUPPORT_CHAT_ID,
#             text=f"""
#                 Добавьте фото
#                 """,
#         )

def get_photo(update, context):
    global image
#     context.bot.send_message(
#         chat_id=TELEGRAM_SUPPORT_CHAT_ID,
#         text=f"""
#             message: {update.message.to_dict()}
#             """,
#     )
    file_info = context.bot.get_file(update.message.photo[-1].file_id)
    image = file_info.file_path
    if title:
        post_data(update, context)
    else:
        update.message.reply_text('Добавьте заголовок')
#         user_id = update.message.reply_to_message.forward_from.id
#         context.bot.send_message(
#             chat_id=user_id,
#             text=f"""
#                 Добавьте заголовок
#                 """,
#         )
        


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.photo | Filters.document.category("image"), get_photo))
    dp.add_handler(MessageHandler(Filters.text, get_title))
#     dp.add_handler(MessageHandler(Filters.chat_type.private, forward_to_chat))
#     dp.add_handler(MessageHandler(Filters.chat(TELEGRAM_SUPPORT_CHAT_ID) & Filters.reply, forward_to_user))
    return dp

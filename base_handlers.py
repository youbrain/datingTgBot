#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)

from base_functions import keyboards, texts
from database import *
# from main import *
from registration import start_registration
from states import *


''' Base bot's functionality (/start, /info handlers) here '''


''' COMMANDS HANDLERS '''


def info(update, context):
    update.message.reply_text(texts['info_c'])


def start(update, context):
    if not User.select().where(User.chat_id == update.message.chat.id).execute():
        User.create(chat_id=update.message.chat.id,
                    first_name=update.message.chat.first_name,
                    last_name=update.message.chat.last_name,
                    username=update.message.chat.username,
                    first_name_dating=update.message.chat.first_name,
                    language_code=update.effective_user.language_code).save()
        update.message.reply_text(texts['welcome'])

    if User.get(User.chat_id == update.message.chat.id).status_registration_dating == False:
        return start_registration(update, context)

    elif User.get(User.chat_id == update.message.chat.id).status_registration_dating:
        return to_main(update, context)


def to_main(update, context):
    keyboard_button = keyboards['main']['buttons']
    if User.get(User.chat_id == update.effective_chat.id).gender_dating:
        keyboard_button[0][0] = keyboards['main']['search_button'][0][1]
    else:
        keyboard_button[0][0] = keyboards['main']['search_button'][0][0]

    try:
        update.message.reply_text(texts['to_main'], reply_markup=ReplyKeyboardMarkup(keyboard_button, resize_keyboard=True))
    except AttributeError:
        update.callback_query.message.delete()
        context.bot.send_message(update.callback_query.message.chat.id,
                                 texts['to_main'], reply_markup=ReplyKeyboardMarkup(keyboard_button, resize_keyboard=True))

    return MAIN_MENU


def cancel(update, context):
    None

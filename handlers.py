#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base_functions import *
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)

''' Custom handlers for custom menus, commands, navigation here '''


def finaances_btn(update, context):
    print(1)
    keyb = InlineKeyboardMarkup([[InlineKeyboardButton(keyboards['send_cash'], callback_data='to_cfdhatsfd')],
                                 [InlineKeyboardButton(keyboards['change_plan'], callback_data='to_chats')]])

    update.message.reply_sticker(texts['stickers']['finaances'])
    update.message.reply_text(texts['finaances'], reply_markup=keyb)
    # return to_main(update, context)


def info_btn(update, context):
    update.message.reply_sticker(texts['stickers']['info'])
    update.message.reply_text(texts['info'], )
    # return to_main(update, context)


def settings_btn(update, context):
    update.message.reply_sticker(texts['stickers']['settings'])
    update.message.reply_text(texts['settings'], )
    # return to_main(update, context)

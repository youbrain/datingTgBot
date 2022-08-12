#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)

from base_handlers import *
from base_functions import *
from database import *
from states import *
from functions import *

''' CHATS HANDLERS '''


def to_chats(update, context):
    out = Chat.select().where(((Chat.chat_id == update._effective_chat.id) & (Chat.blocked == 0)) | ((Chat.with_chat_id == update._effective_chat.id)
                                                                                                     & (Chat.blocked == 0))).order_by(Chat.last_msg_time.desc()).execute()
    chats = set_chats_keyb(out, update._effective_chat.id)

    if len(chats) > 1:
        update.message.reply_text(texts['chats']['active_chats'], reply_markup=InlineKeyboardMarkup(chats))
        return CHATS
    else:
        ''' for test use only! remove "#" on last 2 lines of this function and delate all code lower'''
        usrs = User.select().where(User.chat_id != update._effective_chat.id).execute()
        keyb = []
        for user in usrs:
            keyb.append((InlineKeyboardButton(user.first_name, callback_data=f'chat_new_{user.chat_id}'), ))

        update.message.reply_text(texts['chats']['no_chats'], reply_markup=InlineKeyboardMarkup(keyb))
        return CHATS
        ''' remove all ^^^ this code '''

        ''' В твоих подборках должно быть инлайн кнопка с колбеком "chat_new_тут_чат_айди" для запроса на переписку'''
        # update.message.reply_text(text=texts['chats']['no_chats'])
        # return to_main(update, context)


def chat_get(update, context):
    idi = update['callback_query']['data'].split('_')[2]
    # back_btn = InlineKeyboardMarkup([[InlineKeyboardButton(keyboards['to_chats'], callback_data='to_chats')]])
    context.user_data['msg4bot2chat'] = {idi: []}

    context.bot.delete_message(chat_id=update._effective_chat.id, message_id=update.callback_query.message.message_id)
    context.bot.send_message(update._effective_chat.id, texts['chats']['chat_info'],
                             reply_markup=ReplyKeyboardMarkup([[keyboards['to_chats']]], resize_keyboard=True))

    lis = Message.select().where(Message.inside_chat_id == idi).limit(config['chat_preview']).order_by(Message.send_time.desc())
    for msg in lis[::-1]:
        i = 0
        if msg.from_chat_id == update._effective_chat.id:
            prefix = texts['chat_prefix']
            i = msg.to_chat_id

        else:
            user = User.get(User.chat_id == msg.from_chat_id)
            prefix = f"<b>{user.first_name_dating}</b>: "
            i = msg.from_chat_id

        if not i:
            break

        msg = send_msg(msg, prefix, context, update._effective_chat.id)
        context.user_data['msg4bot2chat'][idi].append(msg.message_id)

    # print(context.user_data['msg4bot2chat'])
    context.user_data['active_chat'] = {'id': idi, '4m_id': update._effective_chat.id, '2id': i}
    return CHATS


def chat_del(update, context):
    context.user_data['active_chat'] = []
    if update['callback_query']:
        if not update['callback_query']['data'] == 'to_chats':
            chat = Chat.get(Chat.id == update['callback_query']['data'].split('_')[2])
            chat.blocked = True
            chat.save()

    out = Chat.select().where(((Chat.chat_id == update._effective_chat.id) & (Chat.blocked == 0)) | ((Chat.with_chat_id == update._effective_chat.id)
                                                                                                     & (Chat.blocked == 0))).order_by(Chat.last_msg_time).execute()
    chats = set_chats_keyb(out, update._effective_chat.id)

    if update.callback_query:
        if len(chats) > 1:
            update.callback_query.edit_message_text(texts['chats']['active_chats'], reply_markup=InlineKeyboardMarkup(chats))
            return CHATS
        else:
            update.callback_query.edit_message_text(texts['chats']['no_chats'])
            return to_main(update, context)
    else:
        if len(chats) > 1:
            context.bot.send_message(update._effective_chat.id, texts['chats']['active_chats'], reply_markup=InlineKeyboardMarkup(chats))
            return CHATS
        else:
            context.bot.send_message(update._effective_chat.id, texts['chats']['no_chats'])
            return to_main(update, context)


def chat_new(update, context):
    context.bot.delete_message(chat_id=update._effective_chat.id, message_id=update.callback_query.message.message_id)
    context.bot.send_message(update._effective_chat.id, texts['chats']['send_1st_mag'],
                             reply_markup=ReplyKeyboardMarkup([[keyboards['to_chats']]], resize_keyboard=True))

    # update.callback_query.edit_message_text(texts['chats']['send_1st_mag'], reply_markup=InlineKeyboardMarkup([[
    #                                         InlineKeyboardButton(keyboards['to_chats'], callback_data='to_chats')]]))
    context.user_data['new_chat'] = update['callback_query']['data'].split('_')[2]
    return SEND_1ST_MSG


def send_1st_txt(update, context):
    txt = update.message.text

    if len(txt) > config['msg_preview_chars']:
        txt = txt[:config['msg_preview_chars']] + '...'

    txt = f"<b>{User.get(User.chat_id == update._effective_chat.id).first_name_dating}</b>: {txt}"

    keyb = InlineKeyboardMarkup([[InlineKeyboardButton(keyboards['new_cancel_btn'], callback_data=f'chat_block_{update._effective_chat.id}'),
                                  InlineKeyboardButton(keyboards['new_replay_btn'], callback_data=f'new_replay_{update._effective_chat.id}_{context.user_data["new_chat"]}')]])

    msg = context.bot.send_message(context.user_data['new_chat'], txt, reply_markup=keyb)
    update.message.reply_text(texts['chats']['1stmsg_sent'])
    chat = Chat(chat_id=update._effective_chat.id, with_chat_id=context.user_data['new_chat'])
    chat.save()

    Message(from_chat_id=update._effective_chat.id,
            to_chat_id=context.user_data['new_chat'], message_id=msg.message_id, msg_type='text', text=update.message.text, inside_chat_id=chat.id).save()
    return to_main(update, context)


def block(update, context):
    update.callback_query.edit_message_text(texts['chats']['user_blocked'])
    return to_main(update, context)


def new_replay(update, context):
    to_ch_id = update['callback_query']['data'].split('_')[2]
    f_ch_id = update['callback_query']['data'].split('_')[3]
    chat = Chat.get(((Chat.chat_id == to_ch_id) | (Chat.with_chat_id == to_ch_id)) & (
        (Chat.chat_id == f_ch_id) | (Chat.with_chat_id == f_ch_id)))  # .execute()
    chat.blocked = 0
    chat.save()
    update.callback_query.edit_message_text(texts['chats']['user_added'])


def send_new_msg(update, context):
    try:
        m = save_msg(update, context.user_data['active_chat']['id'], context.user_data['active_chat']
                     ['4m_id'], context.user_data['active_chat']['2id'], all=True)

        prefix = f"<b>{User.get(User.chat_id == update._effective_chat.id).first_name_dating}</b>: "
        send_msg(m, prefix, context, context.user_data['active_chat']['2id'])
    except:
        return to_main(update, context)

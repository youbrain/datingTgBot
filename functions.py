#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)

from base_functions import texts, keyboards, config
from database import *


''' Custom function for specific bot (scrapers, api wrappers, etc) here '''


def send_msg(msg, prefix, context, to_id):
    if msg.msg_type == 'text':
        return context.bot.send_message(to_id, f"{prefix}{msg.text}")
    else:
        context.bot.send_message(to_id, prefix)
        if msg.msg_type == 'document':
            return context.bot.send_document(to_id, msg.file_id, caption=msg.caption)
        if msg.msg_type == 'photo':
            return context.bot.send_photo(to_id, msg.file_id, caption=msg.caption)
        if msg.msg_type == 'video':
            return context.bot.send_video(to_id, msg.file_id, caption=msg.caption)
        if msg.msg_type == 'voice':
            return context.bot.send_voice(to_id, msg.file_id)
        if msg.msg_type == 'video_note':
            return context.bot.send_video_note(to_id, msg.file_id)
        if msg.msg_type == 'audio':
            return context.bot.send_audio(to_id, msg.file_id, caption=msg.caption)
        if msg.msg_type == 'sticker':
            return context.bot.send_sticker(to_id, msg.file_id)


def set_chats_keyb(out, u_id):
    chats = []
    for chat in out:
        with_chat_id = None
        if chat.with_chat_id == u_id:
            with_chat_id = User.select().where(User.chat_id == chat.chat_id).execute()[0]
        elif chat.chat_id == u_id:
            with_chat_id = User.select().where(User.chat_id == chat.with_chat_id).execute()[0]
        else:
            print('bug: ', chat.with_chat_id, u_id, chat.chat_id)

        if not with_chat_id:
            break
        chats.append((InlineKeyboardButton(with_chat_id.first_name_dating, callback_data=f'chat_get_{chat.id}'),
                      InlineKeyboardButton(keyboards['del'], callback_data=f'chat_del_{chat.id}')))

    chats.append((InlineKeyboardButton(keyboards['to_main_inline'], callback_data='to_main'), ))
    return chats


def save_msg(update, inside_chat_id, from_chat_id, to_chat_id, **kwargs):
    msg = update.message

    if kwargs.get('all'):
        kwargs['text'] = True
        kwargs['document'] = True
        kwargs['photo'] = True
        kwargs['video'] = True
        kwargs['voice'] = True
        kwargs['video_note'] = True
        kwargs['location'] = True
        kwargs['audio'] = True
        kwargs['sticker'] = True
        kwargs['poll'] = True
        kwargs['contact'] = True

    if msg.text and kwargs.get('text'):
        m = Message(inside_chat_id=inside_chat_id, from_chat_id=from_chat_id, to_chat_id=to_chat_id,
                    message_id=msg.message_id, msg_type='text', text=msg.text)
        m.save()
        return m

    elif msg.document and kwargs.get('document'):
        m = Message(inside_chat_id=inside_chat_id, from_chat_id=from_chat_id, to_chat_id=to_chat_id,
                    message_id=msg.message_id, msg_type='document', caption=msg.caption, file_id=msg.document.file_id)
        m.save()
        return m

    elif msg.photo and kwargs.get('photo'):
        m = Message(inside_chat_id=inside_chat_id, from_chat_id=from_chat_id, to_chat_id=to_chat_id,
                    message_id=msg.message_id, msg_type='photo', caption=msg.caption, file_id=msg.photo[-1].file_id)
        m.save()
        return m

    elif msg.video and kwargs.get('video'):
        m = Message(inside_chat_id=inside_chat_id, from_chat_id=from_chat_id, to_chat_id=to_chat_id,
                    message_id=msg.message_id, msg_type='video', caption=msg.caption, file_id=msg.video.file_id)
        m.save()
        return m

    elif msg.voice and kwargs.get('voice'):
        m = Message(inside_chat_id=inside_chat_id, from_chat_id=from_chat_id, to_chat_id=to_chat_id,
                    message_id=msg.message_id, msg_type='voice', file_id=msg.voice.file_id)
        m.save()
        return m

    elif msg.video_note and kwargs.get('video_note'):
        m = Message(inside_chat_id=inside_chat_id, from_chat_id=from_chat_id, to_chat_id=to_chat_id,
                    message_id=msg.message_id, msg_type='video_note', file_id=msg.video_note.file_id)
        m.save()
        return m

    elif msg.audio and kwargs.get('audio'):
        m = Message(inside_chat_id=inside_chat_id, from_chat_id=from_chat_id, to_chat_id=to_chat_id,
                    message_id=msg.message_id, msg_type='audio', caption=msg.caption, file_id=msg.audio.file_id)
        m.save()
        return m

    elif msg.sticker and kwargs.get('sticker'):
        m = Message(inside_chat_id=inside_chat_id, from_chat_id=from_chat_id, to_chat_id=to_chat_id,
                    message_id=msg.message_id, msg_type='sticker', file_id=msg.sticker.file_id)
        m.save()
        return m

    else:
        return True

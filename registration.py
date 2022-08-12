#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode)

from base_functions import keyboards, texts, config, jso
from database import *
from main import *
import base_handlers
from states import *
from geocoder import geonames

from functions import *
from handlers import *


''' FUNCTIONAL REGISTRATION '''


REGISTRATION_FIRST_NAME, REGISTRATION_GENDER, REGISTRATION_PHOTO, REGISTRATION_LOCATION, \
    MAIN_MENU, REGISTRATION_LOCATION_CONTINUATION, CHATS, SEND_1ST_MSG, AGE_REGISTRATION, INVITE_REGISTRATION, \
    MENU_PROFILE, EDIT_PROFILE, EDIT_NAME, EDIT_LAST_NAME, EDIT_AGE, EDIT_LOCATION, EDIT_LOCATION_CONTINUATION, \
    EDIT_PHOTO, EDIT_GENDER, EDIT_ABOUT_ME, EDIT_SEARCH, EDIT_HAIR, DELETE_PROFILE, RESTORE_PROFILE, GALLERY_MENU,\
    LANGUAGE_SELECTION = range(26)


def start_registration(update, context):
    return language_selection(update, context)


def language_selection(update, context):
    if User.get(User.chat_id == update.message.chat.id).language_code:
        update.message.reply_text(texts['registration']['language_is'] + texts['registration'][User.get(User.chat_id == update.message.chat.id).language_code],
                                  reply_markup=ReplyKeyboardMarkup(keyboards['yes_not'], resize_keyboard=True))
    else:
        keyboard = []
        for i in jso:
            keyboard.append([i])
        update.message.reply_text(
            texts['registration']['language_selection'],
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

    return LANGUAGE_SELECTION


def continuation_language_selection(update, context):
    keyboard = []
    for i in jso:
        keyboard.append([i])
    update.message.reply_text(
        texts['registration']['language_selection'],
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

    return LANGUAGE_SELECTION


def finish_language_selection(update, context):
    User.update(language_code=update.message.text).where(User.chat_id == update.message.chat.id).execute()
    update.message.reply_text(texts['registration']['language_ok'])

    return gender_registration(update, context)


def registration_first_name(update, context):
    if User.get(User.chat_id == update.message.chat.id).first_name_dating:
        update.message.reply_text(texts['registration']['is first name'] + '<b>' +
                                  str(User.get(User.chat_id == update.message.chat.id).first_name_dating) + ' </b>' +
                                  texts['registration']['your first name'], parse_mode=ParseMode.HTML,
                                  reply_markup=ReplyKeyboardMarkup(keyboards['yes'], resize_keyboard=True))

    else:
        update.message.reply_text(texts['registration']['send_first_name'],
                                  reply_markup=ReplyKeyboardRemove())

    return REGISTRATION_FIRST_NAME


def finish_registration_first_name(update, context):
    User.update(first_name_dating=update.message.text).where(User.chat_id == update.message.chat.id).execute()
    context.bot.send_message(update.effective_chat.id, text=texts['registration']['successfully'])

    return location_registration(update, context)


def gender_registration(update, context):
    update.message.reply_text(texts['registration']['gender'],
                              reply_markup=ReplyKeyboardMarkup(keyboards['gender'], resize_keyboard=True))

    return REGISTRATION_GENDER


def finish_registration_gender(update, context):
    if update.message.text == keyboards['gender'][0][0]:
        User.update(gender_dating=True).where(User.chat_id == update.message.chat.id).execute()
        update.message.reply_text(texts['registration']['gender_successfully_man'])
    elif update.message.text == keyboards['gender'][0][1]:
        User.update(gender_dating=False).where(User.chat_id == update.message.chat.id).execute()
        update.message.reply_text(texts['registration']['gender_successfully_girl'])

    context.bot.send_video(update.message.chat.id, video=texts['registration']['gender_gif']) # ОТПРАВКА ВАЖНОЙ ГИФКИ

    return age_registration(update, context)


def location_registration(update, context):
    update.message.reply_text(texts['registration']['location_send'],
                              reply_markup=ReplyKeyboardMarkup(keyboards['location'], resize_keyboard=True))

    return REGISTRATION_LOCATION


def finish_location_registration(update, context):
    if update.callback_query:
        data = update.callback_query.data
        arr_data = data.split('_')
        User.update(location_latitude_dating=arr_data[1]).where(
            User.chat_id == update.effective_chat.id).execute()
        User.update(location_longitude_dating=arr_data[2]).where(
            User.chat_id == update.effective_chat.id).execute()

    elif update.message.location:
        User.update(location_latitude_dating=update.message.location.latitude).where(
            User.chat_id == update.effective_chat.id).execute()
        User.update(location_longitude_dating=update.message.location.longitude).where(
            User.chat_id == update.effective_chat.id).execute()

    context.bot.send_message(update.effective_chat.id, text=texts['registration']['successfully'])

    return photo_registration(update, context)


def continuation_location_registration(update, context):
    g = geonames(update.message.text,  maxRows=int(config['maxRows_location']), key=str(config['key_location']),
                 lang=User.get(User.chat_id == update.message.chat.id).language_code)
    text_button = []
    for i in g:
        text_button.append([InlineKeyboardButton(i.address + ', ' + i.province + ', ' + i.country,
                                                 callback_data=texts['registration']['callback_location'] +
                                                 '_' + i.lat + '_' + i.lng)])
    update.message.reply_text(text=texts['registration']['location_check'], reply_markup=InlineKeyboardMarkup(text_button), resize_keyboard=True)

    return REGISTRATION_LOCATION_CONTINUATION


def photo_registration(update, context):
    if context.bot.get_user_profile_photos(update.effective_chat.id, limit=1):
        photos=context.bot.get_user_profile_photos(update.effective_chat.id, limit=1).photos
        if len(photos) > 0:
            context.bot.send_photo(update.effective_chat.id, photo=photos[0][len(photos[0])-1].file_id)
        context.bot.send_message(update.effective_chat.id, text=texts['registration']['this is your photo'],
                                  reply_markup=ReplyKeyboardMarkup(keyboards['yes'], resize_keyboard=True))

    else:
        context.bot.send_message(update.effective_chat.id, text=texts['registration']['send photo'],
                                 reply_markup=ReplyKeyboardRemove())

    return REGISTRATION_PHOTO


def continuation_photo_registration(update, context):
    User.update(photo_profile_dating=update.message.photo[0].file_id).where(
            User.chat_id == update.message.chat.id).execute()
    context.bot.send_message(update.effective_chat.id, text=texts['registration']['successfully'])

    return invite_code(update, context)


def finish_photo_registration(update, context):
    photos=context.bot.get_user_profile_photos(update.message.chat.id, limit=1).photos
    if len(photos) > 0:
        User.update(photo_profile_dating=photos[0][len(photos[0])-1].file_id).where(
            User.chat_id == update.message.chat.id).execute()
    context.bot.send_message(update.effective_chat.id, text=texts['registration']['successfully'])

    with open('video.mp4', mode='rb') as video_file:
        context.bot.send_video(update.effective_chat.id, video_file)

    return invite_code(update, context)


def age_registration(update, context):
    context.bot.send_message(update.effective_chat.id, text=texts['registration']['age_print'] +
                                                            config['age_min'] + ' - ' + config['age_max'],
                             reply_markup=ReplyKeyboardRemove())

    return AGE_REGISTRATION


def finish_age_registration(update, context):
    if update.message.text.isdigit():
        if int(config['age_min']) <= int(update.message.text) and int(config['age_max']) >= int(update.message.text):
            User.update(age_dating=int(update.message.text)).where(
                User.chat_id == update.message.chat.id).execute()

            context.bot.send_message(update.effective_chat.id, text=texts['registration']['successfully'])

            return registration_first_name(update, context)
        else:
            return age_registration(update, context)
    else:
        return age_registration(update, context)


def invite_code(update, context):
    context.bot.send_message(update.effective_chat.id, text=texts['registration']['invite_code'],
                             reply_markup=ReplyKeyboardMarkup(keyboards['skip'], resize_keyboard=True))

    return INVITE_REGISTRATION


def finish_invite_code(update, context):
    if User.select().where(User.chat_id == update.message.text):
        if User.get(User.chat_id == update.message.text).chat_id != update.message.text:
            User.update(invite_code_dating=update.message.text).where(
                User.chat_id == update.message.chat.id).execute()
            context.bot.send_message(update.effective_chat.id, text=texts['registration']['successfully'])
            return finish_registration(update, context)
        else:
            return invite_code(update, context)
    else:
        return invite_code(update, context)


def finish_registration(update, context):
    User.update(status_registration_dating=True).where(
        User.chat_id == update.message.chat.id).execute()
    context.bot.send_message(update.effective_chat.id, text=texts['registration']['invite_gold'])
    return base_handlers.to_main(update, context)

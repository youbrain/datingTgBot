# my_profile(update, context):#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)

from base_functions import keyboards, texts, config
from database import *
from main import *
import base_handlers

from geocoder import geonames

from functions import *
from handlers import *


''' FUNCTIONAL PROFILE '''


def menu_profile(update, context):
    if update.callback_query:
        update.callback_query.message.delete()
    context.bot.send_message(update.effective_chat.id, text=texts['profile']['welcome_profile'],
                             reply_markup=ReplyKeyboardMarkup(keyboards['profile']['main_profile'], resize_keyboard=True))

    return MENU_PROFILE


def print_profile(update, context):
    if User.get(User.chat_id == update.effective_chat.id).gender_dating:
        gender = texts['profile']['print_profile']['man']
    else:
        gender = texts['profile']['print_profile']['girl']
    text = ''
    if User.get(User.chat_id == update.effective_chat.id).first_name_dating:
        text += texts['profile']['print_profile']['name'] + str(User.get(User.chat_id == update.effective_chat.id).first_name_dating) + '\n'
    if User.get(User.chat_id == update.effective_chat.id).last_name_dating:
        text += texts['profile']['print_profile']['last_name'] + str(User.get(User.chat_id == update.effective_chat.id).last_name_dating) + '\n'
    text +=texts['profile']['print_profile']['age'] + str(User.get(User.chat_id == update.effective_chat.id).age_dating) +\
           '\n' + texts['profile']['print_profile']['gender'] + gender + '\n'
    if User.get(User.chat_id == update.effective_chat.id).about_me_dating:
        text += texts['profile']['print_profile']['adout_me'] + str(User.get(User.chat_id == update.effective_chat.id).about_me_dating) + '\n'
    if User.get(User.chat_id == update.effective_chat.id).target_search_dating:
        text +=texts['profile']['print_profile']['search'] + str(User.get(User.chat_id == update.effective_chat.id).target_search_dating) + '\n'
    if User.get(User.chat_id == update.effective_chat.id).color_hair_dating:
        text += texts['profile']['print_profile']['color_hair'] + str(User.get(User.chat_id == update.effective_chat.id).color_hair_dating) + '\n'
    if User.get(User.chat_id == update.effective_chat.id).photo_profile_dating:
        context.bot.send_photo(update.effective_chat.id,
                                   photo=User.get(User.chat_id == update.effective_chat.id).photo_profile_dating,
                                   caption=text)
    else:
        context.bot.send_message(update.effective_chat.id, text=text)

    return MENU_PROFILE


def gallery_menu(update, context):
    context.bot.send_message(update.effective_chat.id, text= texts['profile']['gallery_menu'],
                             reply_markup=ReplyKeyboardMarkup(keyboards['gallery_menu'],
                                                              resize_keyboard=True))

    return GALLERY_MENU


def set_video_photo_gallery(update, context):
    if update.message.photo:
        Gallery.create(
            chat_id = update.effective_chat.id,
            file_id = update.message.photo[-1].file_id,
            photo_file = True
        ).save()
    elif update.message.video:
        Gallery.create(
            chat_id = update.effective_chat.id,
            file_id = update.message.video.file_id,
            video_file = True
        ).save()


def gallery_print_photo(update, context):
    list = Gallery.select().where(Gallery.chat_id == update.effective_chat.id, Gallery.photo_file == True).execute()
    for i in list:
        context.bot.send_photo(update.effective_chat.id, photo=i.file_id)


def gallery_print_video(update, context):
    list = Gallery.select().where(Gallery.chat_id == update.effective_chat.id, Gallery.video_file == True).execute()
    for i in list:
        context.bot.send_video(update.effective_chat.id, video=i.file_id)



def delete_profile(update, context):
    context.bot.send_message(update.effective_chat.id, text= texts['profile']['delete_profile'],
                             reply_markup=ReplyKeyboardMarkup(keyboards['yes_not'],
                                                              resize_keyboard=True))

    return DELETE_PROFILE


def restore_profile(update, context):
    context.bot.send_message(update.effective_chat.id, text= texts['profile']['restore_profile'],
                             reply_markup=ReplyKeyboardMarkup(keyboards['go_restore_profile'],
                                                              resize_keyboard=True))

    return RESTORE_PROFILE


def edit_profile(update, context):
    edit_profile_keyboard = [[InlineKeyboardButton(text=keyboards['profile']['profile_edit_inline']['name'][0], callback_data=keyboards['profile']['profile_edit_inline']['name'][1]),
                              InlineKeyboardButton(text=keyboards['profile']['profile_edit_inline']['lastname'][0], callback_data=keyboards['profile']['profile_edit_inline']['lastname'][1]),
                              InlineKeyboardButton(text=keyboards['profile']['profile_edit_inline']['age'][0], callback_data=keyboards['profile']['profile_edit_inline']['age'][1])],
                             [InlineKeyboardButton(text=keyboards['profile']['profile_edit_inline']['location'][0], callback_data=keyboards['profile']['profile_edit_inline']['location'][1]),
                              InlineKeyboardButton(text=keyboards['profile']['profile_edit_inline']['photo'][0], callback_data=keyboards['profile']['profile_edit_inline']['photo'][1]),
                              InlineKeyboardButton(text=keyboards['profile']['profile_edit_inline']['gender'][0], callback_data=keyboards['profile']['profile_edit_inline']['gender'][1])],
                             [InlineKeyboardButton(text=keyboards['profile']['profile_edit_inline']['aboutme'][0], callback_data=keyboards['profile']['profile_edit_inline']['aboutme'][1]),
                              InlineKeyboardButton(text=keyboards['profile']['profile_edit_inline']['search'][0], callback_data=keyboards['profile']['profile_edit_inline']['search'][1]),
                              InlineKeyboardButton(text=keyboards['profile']['profile_edit_inline']['hair'][0], callback_data=keyboards['profile']['profile_edit_inline']['hair'][1])],
                             [InlineKeyboardButton(text=keyboards['profile']['profile_edit_inline']['backprofile'][0], callback_data=keyboards['profile']['profile_edit_inline']['backprofile'][1])],
                             [InlineKeyboardButton(text=keyboards['profile']['profile_edit_inline']['main_menu'][0],callback_data=keyboards['profile']['profile_edit_inline']['main_menu'][1])]]
    context.bot.send_message(update.effective_chat.id, text='1', reply_markup=ReplyKeyboardRemove())
    if update.callback_query:
        update.callback_query.message.delete()
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.callback_query.message.message_id + 1)
    else:
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id+1)
    context.bot.send_message(update.effective_chat.id, text=texts['profile']['edit_profile'],
                             reply_markup=InlineKeyboardMarkup(edit_profile_keyboard,
                                                              resize_keyboard=True))

    return EDIT_PROFILE


def edit_name(update, context):
    if update.callback_query:
        update.callback_query.message.delete()
    context.bot.send_message(update.effective_chat.id, text=texts['profile']['edit_name_is'] + ' ' +
                             User.get(User.chat_id == update.effective_chat.id).first_name_dating + '\n' +
                             texts['profile']['edit_name'],
                             reply_markup=ReplyKeyboardMarkup(keyboards['profile']['back'],
                                                              resize_keyboard=True))

    return EDIT_NAME


def finish_edit_name(update, context):
    User.update(first_name_dating=update.message.text).where(User.chat_id == update.message.chat.id).execute()

    return edit_profile(update, context)


def edit_last_name(update, context):
    if update.callback_query:
        update.callback_query.message.delete()
    if User.get(User.chat_id == update.effective_chat.id).last_name_dating:
        context.bot.send_message(update.effective_chat.id, text=texts['profile']['edit_last_name_is'] + ' ' +
                                 User.get(User.chat_id == update.effective_chat.id).last_name_dating + '\n' +
                                 texts['profile']['edit_last_name'],
                                 reply_markup=ReplyKeyboardMarkup(keyboards['profile']['back'],
                                                                  resize_keyboard=True))
    else:
        context.bot.send_message(update.effective_chat.id, text=texts['profile']['edit_last_name'],
                                 reply_markup=ReplyKeyboardMarkup(keyboards['profile']['back'],
                                                                  resize_keyboard=True))

    return EDIT_LAST_NAME


def finish_edit_last_name(update, context):
    User.update(last_name_dating=update.message.text).where(User.chat_id == update.message.chat.id).execute()

    return edit_profile(update, context)


def edit_age(update, context):
    if update.callback_query:
        update.callback_query.message.delete()
    context.bot.send_message(update.effective_chat.id, text=texts['profile']['edit_age_is'] + ' ' +
                             str(User.get(User.chat_id == update.effective_chat.id).age_dating) + '\n' +
                             texts['profile']['edit_age'] + '\n' + config['age_min'] + ' - ' + config['age_max'],
                             reply_markup=ReplyKeyboardMarkup(keyboards['profile']['back'],
                                                              resize_keyboard=True))

    return EDIT_AGE


def finish_edit_age(update, context):
    if update.message.text.isdigit():
        if int(config['age_min']) <= int(update.message.text) and int(config['age_max']) >= int(update.message.text):
            User.update(age_dating=int(update.message.text)).where(
                User.chat_id == update.message.chat.id).execute()

            return edit_profile(update, context)
        else:
            return edit_age(update, context)
    else:
        return edit_age(update, context)


def edit_location(update, context):
    if update.callback_query:
        update.callback_query.message.delete()
    context.bot.send_message(update.effective_chat.id, texts['registration']['location_send'],
                              reply_markup=ReplyKeyboardMarkup(keyboards['location'], resize_keyboard=True))

    return EDIT_LOCATION


def finish_location_edit(update, context):
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

    return edit_profile(update, context)


def continuation_location_edit(update, context):
    g = geonames(update.message.text,  maxRows=int(config['maxRows_location']), key=str(config['key_location']),
                 lang=User.get(User.chat_id == update.message.chat.id).language_code)
    text_button = []
    for i in g:
        text_button.append([InlineKeyboardButton(i.address + ', ' + i.province + ', ' + i.country,
                                                 callback_data=texts['registration']['callback_location'] +
                                                 '_' + i.lat + '_' + i.lng)])
    update.message.reply_text(text=texts['registration']['location_check'], reply_markup=InlineKeyboardMarkup(text_button), resize_keyboard=True)

    return EDIT_LOCATION_CONTINUATION


def edit_photo(update, context):
    if update.callback_query:
        update.callback_query.message.delete()
    if User.get(User.chat_id == update.effective_chat.id).photo_profile_dating:
        context.bot.send_photo(update.effective_chat.id, photo=User.get(User.chat_id == update.effective_chat.id).photo_profile_dating)
    context.bot.send_message(update.effective_chat.id, text=texts['profile']['edit_photo'],
                            reply_markup=ReplyKeyboardMarkup(keyboards['profile']['back'],
                                                            resize_keyboard=True))

    return EDIT_PHOTO


def finish_edit_photo(update, context):
    User.update(photo_profile_dating=update.message.photo[0].file_id).where(
        User.chat_id == update.message.chat.id).execute()

    return edit_profile(update, context)


def edit_gender(update, context):
    if update.callback_query:
        update.callback_query.message.delete()
    context.bot.send_message(update.effective_chat.id, texts['registration']['gender'],
                              reply_markup=ReplyKeyboardMarkup(keyboards['gender'], resize_keyboard=True))
    return EDIT_GENDER


def finish_edit_gender(update, context):
    if update.message.text == keyboards['gender'][0][0]:
        User.update(gender_dating=True).where(User.chat_id == update.message.chat.id).execute()
    elif update.message.text == keyboards['gender'][0][1]:
        User.update(gender_dating=False).where(User.chat_id == update.message.chat.id).execute()

    return edit_profile(update, context)


def edit_about_me(update, context):
    if update.callback_query:
        update.callback_query.message.delete()
    if User.get(User.chat_id == update.effective_chat.id).about_me_dating:
        context.bot.send_message(update.effective_chat.id, texts['profile']['edit_adout_me_is'] + '\n' +
                                 User.get(User.chat_id == update.effective_chat.id).about_me_dating + '\n\n' +
                                 texts['profile']['edit_adout_me'],
                                 reply_markup=ReplyKeyboardMarkup(keyboards['profile']['back'],
                                                                  resize_keyboard=True))
    else:
        context.bot.send_message(update.effective_chat.id,
                                 texts['profile']['edit_adout_me'],
                                 reply_markup=ReplyKeyboardMarkup(keyboards['profile']['back'],
                                                                  resize_keyboard=True))

    return EDIT_ABOUT_ME


def finish_edit_about_me(update, context):
    User.update(about_me_dating=update.message.text).where(User.chat_id == update.message.chat.id).execute()

    return edit_profile(update, context)


def edit_search(update, context):
    if update.callback_query:
        update.callback_query.message.delete()
    keyboard = []
    for i in keyboards['profile']['target_search']:
        keyboard.append([InlineKeyboardButton(text=i, callback_data=i)])
    context.bot.send_message(update.effective_chat.id,
                             texts['profile']['edit_search'],
                             reply_markup=InlineKeyboardMarkup(keyboard,
                                                              resize_keyboard=True))

    return EDIT_SEARCH


def finish_edit_search(update, context):
    User.update(target_search_dating=update.callback_query.data).where(User.chat_id == update.effective_chat.id).execute()

    return edit_profile(update, context)


def edit_hair(update, context):
    if update.callback_query:
        update.callback_query.message.delete()
    context.bot.send_message(update.effective_chat.id,
                             texts['profile']['edit_color_hair'],
                             reply_markup=ReplyKeyboardMarkup(keyboards['profile']['back'],
                                                              resize_keyboard=True))
    return EDIT_HAIR


def finish_edit_hair(update, context):
    User.update(color_hair_dating=update.message.text).where(User.chat_id == update.effective_chat.id).execute()
    return edit_profile(update, context)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
DEFAULT TEMPLATE

STRUCTURE:
    - main.py               ~ (entry point) Settings all handlers/controllers, etc (current file)
    - base_functions.py     ~ Base functions, reading config.ini. (function wrappers, values.json)
    - base_handlers.py      ~ Base bot's functionality (/start, /info handlers)

    - database.py           ~ peewee classes for communication with database.db 
    - functions.py          ~ Custom function for specific bot (scrapers, api wrappers, etc)
    - handlers.py           ~ Custom handlers for custom menus, commands, navigation

    - database.db           ~ SQLite database for dev process (Postgresql on production)
    - config.json            ~ All projects configs, api keys, tokens, etc
    - values.json           ~ All bot's texts and keyboards, for different languages

Developer: Alexander Machek [@youbrain]
Repository: https://github.com/s404s/bot_ecosystem/tree/dev/organaizer

TODO:
    - all dev tasks here
'''
import logging
from telegram import ParseMode
from telegram.ext import (Updater, Filters, Defaults)
from telegram.ext import (CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler)

from send_handler import *
from database import *
from base_functions import *
from base_handlers import *
from states import *

from functions import *
from handlers import *

from profile import *
from registration import *

import search

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


REGISTRATION_FIRST_NAME, REGISTRATION_GENDER, REGISTRATION_PHOTO, REGISTRATION_LOCATION, \
    MAIN_MENU, REGISTRATION_LOCATION_CONTINUATION, CHATS, SEND_1ST_MSG, AGE_REGISTRATION, INVITE_REGISTRATION, \
    MENU_PROFILE, EDIT_PROFILE, EDIT_NAME, EDIT_LAST_NAME, EDIT_AGE, EDIT_LOCATION, EDIT_LOCATION_CONTINUATION, \
    EDIT_PHOTO, EDIT_GENDER, EDIT_ABOUT_ME, EDIT_SEARCH, EDIT_HAIR, DELETE_PROFILE, RESTORE_PROFILE, GALLERY_MENU,\
    LANGUAGE_SELECTION = range(26)


def main():
    '''ENTRY POINT'''
    defaults = Defaults(parse_mode=ParseMode.HTML)
    updater = Updater(config['bot_token'], use_context=True, defaults=defaults)
    dp = updater.dispatcher

    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), MessageHandler(Filters.all, to_main),
                      CallbackQueryHandler(callback=chat_new, pattern="chat_new")],

        states={

            REGISTRATION_FIRST_NAME: [MessageHandler(Filters.regex(f"^({keyboards['yes'][0][0]})$"), location_registration),
                                      MessageHandler(Filters.text, finish_registration_first_name)],

            LANGUAGE_SELECTION: [MessageHandler(Filters.regex(f"^({keyboards['yes_not'][0][0]})$"), gender_registration),
                                 MessageHandler(Filters.regex(f"^({keyboards['yes_not'][0][1]})$"), continuation_language_selection),
                                 MessageHandler(Filters.text, finish_language_selection)],

            REGISTRATION_GENDER: [MessageHandler(Filters.regex(f"^({keyboards['gender'][0][0]})$"), finish_registration_gender),
                                  MessageHandler(Filters.regex(f"^({keyboards['gender'][0][1]})$"), finish_registration_gender)],

            REGISTRATION_LOCATION: [MessageHandler(Filters.location, finish_location_registration),
                                    MessageHandler(Filters.text, continuation_location_registration)],

            REGISTRATION_LOCATION_CONTINUATION: [MessageHandler(Filters.regex(f"^({keyboards['skip_cancel'][0][0]})$"), photo_registration),
                                                 MessageHandler(Filters.regex(f"^({keyboards['skip_cancel'][0][1]})$"), location_registration),
                                                 CallbackQueryHandler(callback=finish_location_registration,
                                                                      pattern=texts['registration']['callback_location']),
                                                 MessageHandler(Filters.text, continuation_location_registration)],

            REGISTRATION_PHOTO: [MessageHandler(Filters.regex(f"^({keyboards['yes'][0][0]})$"), finish_photo_registration),
                                 MessageHandler(Filters.photo, continuation_photo_registration)],

            AGE_REGISTRATION: [MessageHandler(Filters.text, finish_age_registration)],

            INVITE_REGISTRATION: [MessageHandler(Filters.regex(f"^({keyboards['skip'][0][0]})$"), finish_registration),
                                  MessageHandler(Filters.text, finish_invite_code)],

            MAIN_MENU: [MessageHandler(Filters.regex(f"^({keyboards['main']['buttons'][0][1]})$"), to_chats),  # Чаты
                        MessageHandler(Filters.regex(f"^({keyboards['main']['buttons'][1][1]})$"), finaances_btn),  # Банк
                        MessageHandler(Filters.regex(f"^({keyboards['main']['buttons'][1][0]})$"), menu_profile),  # Профиль
                        MessageHandler(Filters.regex(f"^({keyboards['main']['buttons'][2][0]})$"), info_btn),  # Информация
                        MessageHandler(Filters.regex(f"^({keyboards['main']['buttons'][2][1]})$"), settings_btn),  # Настройки
                        MessageHandler(Filters.text(keyboards['main']['search_button'][0][1]) or
                                       Filters.text(keyboards['main']['search_button'][0][0]), search.start_search_handler)  # Поиск (парни, девушки)
                        ],

            MENU_PROFILE: [MessageHandler(Filters.regex(f"^({keyboards['profile']['main_profile'][0][0]})$"), print_profile),  # моя анкета
                           MessageHandler(Filters.regex(f"^({keyboards['profile']['main_profile'][0][1]})$"), edit_profile),  # редактировать
                           MessageHandler(Filters.regex(f"^({keyboards['profile']['main_profile'][1][0]})$"), gallery_menu),  # галерея
                           MessageHandler(Filters.regex(f"^({keyboards['profile']['main_profile'][1][1]})$"), to_main),  # контакты
                           MessageHandler(Filters.regex(f"^({keyboards['profile']['main_profile'][2][0]})$"), to_main),  # тесты
                           MessageHandler(Filters.regex(f"^({keyboards['profile']['main_profile'][2][1]})$"), delete_profile),  # удалить профиль
                           MessageHandler(Filters.regex(f"^({keyboards['profile']['main_profile'][3][0]})$"), to_main)],  # возращаемся в главное меню

            EDIT_PROFILE: [CallbackQueryHandler(callback=menu_profile,
                                                pattern=keyboards['profile']['profile_edit_inline']['backprofile'][1]),  # назад в меню профиля
                           CallbackQueryHandler(callback=edit_name,
                                                pattern=keyboards['profile']['profile_edit_inline']['name'][1]),  # редактировать имя
                           CallbackQueryHandler(callback=edit_last_name,
                                                pattern=keyboards['profile']['profile_edit_inline']['lastname'][1]),  # редактировать фамилию
                           CallbackQueryHandler(callback=edit_age,
                                                pattern=keyboards['profile']['profile_edit_inline']['age'][1]),  # редактировать возраст
                           CallbackQueryHandler(callback=edit_location,
                                                pattern=keyboards['profile']['profile_edit_inline']['location'][1]),  # редактировать местоположение
                           CallbackQueryHandler(callback=edit_photo,
                                                pattern=keyboards['profile']['profile_edit_inline']['photo'][1]),  # редактировать фото
                           CallbackQueryHandler(callback=edit_gender,
                                                pattern=keyboards['profile']['profile_edit_inline']['gender'][1]),  # редактировать пол
                           CallbackQueryHandler(callback=edit_about_me,
                                                pattern=keyboards['profile']['profile_edit_inline']['aboutme'][1]),  # редактировать инфу о себе
                           CallbackQueryHandler(callback=edit_search,
                                                pattern=keyboards['profile']['profile_edit_inline']['search'][1]),  # редактировать для каких целей ищет парнера
                           CallbackQueryHandler(callback=edit_hair,
                                                pattern=keyboards['profile']['profile_edit_inline']['hair'][1]),  # цвет волос
                           CallbackQueryHandler(callback=to_main,
                                                pattern=keyboards['profile']['profile_edit_inline']['main_menu'][1])
                           ],

            EDIT_NAME: [MessageHandler(Filters.regex(f"^({keyboards['profile']['back'][0][0]})$"), edit_profile),
                        MessageHandler(Filters.text, finish_edit_name)],

            EDIT_LAST_NAME: [MessageHandler(Filters.regex(f"^({keyboards['profile']['back'][0][0]})$"), edit_profile),
                             MessageHandler(Filters.text, finish_edit_last_name)],

            EDIT_AGE: [MessageHandler(Filters.regex(f"^({keyboards['profile']['back'][0][0]})$"), edit_profile),
                       MessageHandler(Filters.text, finish_edit_age)],

            EDIT_LOCATION: [MessageHandler(Filters.location, finish_location_edit),
                            # MessageHandler(Filters.regex(f"^({keyboards['location'][1][0]})$"), edit_profile), :)
                            MessageHandler(Filters.text, continuation_location_edit)],

            EDIT_LOCATION_CONTINUATION: [MessageHandler(Filters.regex(f"^({keyboards['skip_cancel'][0][0]})$"), edit_profile),
                                         MessageHandler(Filters.regex(f"^({keyboards['skip_cancel'][0][1]})$"), edit_location),
                                         CallbackQueryHandler(callback=finish_location_edit,
                                                              pattern=texts['registration']['callback_location']),
                                         MessageHandler(Filters.text, continuation_location_edit)],

            EDIT_PHOTO: [MessageHandler(Filters.regex(f"^({keyboards['profile']['back'][0][0]})$"), edit_profile),
                         MessageHandler(Filters.photo, finish_edit_photo)],

            EDIT_GENDER: [MessageHandler(Filters.regex(f"^({keyboards['profile']['back'][0][0]})$"), edit_profile),
                          MessageHandler(Filters.text, finish_edit_gender)],

            EDIT_ABOUT_ME: [MessageHandler(Filters.regex(f"^({keyboards['profile']['back'][0][0]})$"), edit_profile),
                            MessageHandler(Filters.text, finish_edit_about_me)],

            EDIT_SEARCH: [MessageHandler(Filters.regex(f"^({keyboards['profile']['back'][0][0]})$"), edit_profile),
                          CallbackQueryHandler(callback=finish_edit_search)],

            EDIT_HAIR: [MessageHandler(Filters.regex(f"^({keyboards['profile']['back'][0][0]})$"), edit_profile),
                        MessageHandler(Filters.text, finish_edit_hair)],

            DELETE_PROFILE: [MessageHandler(Filters.regex(f"^({keyboards['yes_not'][0][0]})$"), restore_profile),
                             MessageHandler(Filters.regex(f"^({keyboards['yes_not'][0][1]})$"), menu_profile)],

            RESTORE_PROFILE: [MessageHandler(Filters.regex(f"^({keyboards['yes'][0][0]})$"), menu_profile)],

            GALLERY_MENU: [MessageHandler(Filters.regex(f"^({keyboards['gallery_menu'][0][0]})$"), gallery_print_photo),
                           MessageHandler(Filters.regex(f"^({keyboards['gallery_menu'][0][1]})$"), gallery_print_video),
                           MessageHandler(Filters.regex(f"^({keyboards['gallery_menu'][1][0]})$"), menu_profile),
                           MessageHandler(Filters.photo, set_video_photo_gallery),
                           MessageHandler(Filters.video, set_video_photo_gallery)],


            CHATS: [CallbackQueryHandler(callback=chat_get, pattern="chat_get"),
                    CallbackQueryHandler(callback=chat_del, pattern="chat_del"),
                    CallbackQueryHandler(callback=chat_new, pattern="chat_new"),
                    CallbackQueryHandler(callback=to_main, pattern="to_main"),
                    CallbackQueryHandler(callback=chat_del, pattern="to_chats"),
                    MessageHandler(Filters.regex(f"^({keyboards['to_chats']})$"), chat_del),
                    MessageHandler(Filters.all, send_new_msg)],

            SEND_1ST_MSG: [MessageHandler(Filters.text, send_1st_txt),
                           CallbackQueryHandler(callback=chat_del, pattern="to_chats")]  # other content types have to be heare

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CallbackQueryHandler(callback=block, pattern="chat_block"))
    dp.add_handler(CallbackQueryHandler(callback=new_replay, pattern="new_replay"))

    # errors
    # dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

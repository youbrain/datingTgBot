import database
import telegram


def start_search_handler(update: telegram.Update, context: telegram.ext.CallbackContext):
    user = database.User.select().where(database.User.chat_id ==
                                        update.message.from_user.id).get()

    suggested_user = database.User.select().where(
        database.User.gender_dating != user.gender_dating).get()

    history_data = database.SearchHistory(
        chat_id=user.chat_id, suggested_chat_id=suggested_user.chat_id)
    history_data.save()

    search_markup = [
        [
            telegram.InlineKeyboardButton('⬅️', callback_data='abc'),
            telegram.InlineKeyboardButton('💖', callback_data='abc'),
            telegram.InlineKeyboardButton('➡️', callback_data='abc'),
        ],
        [
            telegram.InlineKeyboardButton(
                '💬 Написать', callback_data=f'chat_new_{suggested_user.chat_id}'),
            telegram.InlineKeyboardButton(
                '🎚️ Настроить фильтры', callback_data='abc'),
        ],
    ]

    context.bot.send_photo(user.chat_id, suggested_user.photo_profile_dating,
                           caption=f'<b>{suggested_user.first_name_dating}</b>, {suggested_user.age_dating}\n{suggested_user.about_me_dating}',
                           reply_markup=telegram.InlineKeyboardMarkup(
                               search_markup)
                           )

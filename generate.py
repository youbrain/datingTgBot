import peewee
import database

database.User(
    chat_id = 9999,
    first_name='Алина',
    gender_dating=0,
    first_name_dating='Алина',
    age_dating=17,
    about_me_dating='Ищу большой любви и денег',
    status_registration_dating=True,
    status_verification_dating=True
).save()
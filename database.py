#!/usr/bin/env python
# -*- coding: utf-8 -*-

import peewee
import datetime

''' Class for communication with database.db here '''

db = peewee.SqliteDatabase('database.db')


class User(peewee.Model):
    id = peewee.AutoField()

    chat_id = peewee.IntegerField(null=True)
    first_name = peewee.CharField(null=True)
    last_name = peewee.CharField(null=True)
    username = peewee.CharField(null=True, unique=True)
    language_code = peewee.CharField(null=True)

    start_time = peewee.DateTimeField(default=datetime.datetime.now)

    first_name_dating = peewee.CharField(null=True)
    last_name_dating = peewee.CharField(null=True)
    gender_dating = peewee.BooleanField(default=False)  # True - man
    age_dating = peewee.IntegerField(null=True)

    about_me_dating = peewee.CharField(null=True)
    target_search_dating = peewee.CharField(null=True)
    color_hair_dating = peewee.CharField(null=True)

    location_latitude_dating = peewee.DoubleField(null=True)
    location_longitude_dating = peewee.DoubleField(null=True)

    status_registration_dating = peewee.BooleanField(default=False)
    status_verification_dating = peewee.BooleanField(default=False)
    invite_code_dating = peewee.CharField(null=True)

    photo_profile_dating = peewee.CharField(null=True)

    class Meta:
        database = db
        db_table = 'users'


User.create_table()


class Gallery(peewee.Model):
    id = peewee.AutoField()
    chat_id = peewee.IntegerField(null=True)
    file_id = peewee.CharField(null=True)

    photo_file = peewee.BooleanField(default=False)
    video_file = peewee.BooleanField(default=False)

    class Meta:
        database = db
        db_table = 'gallery'


class Chat(peewee.Model):
    id = peewee.AutoField()
    last_msg_time = peewee.DateTimeField(default=datetime.datetime.now)

    chat_id = peewee.IntegerField()
    with_chat_id = peewee.IntegerField()
    blocked = peewee.BooleanField(default=True)

    class Meta:
        database = db
        db_table = 'chats'


class Message(peewee.Model):
    id = peewee.AutoField()
    inside_chat_id = peewee.IntegerField()
    is_checked = peewee.BooleanField(default=False)

    from_chat_id = peewee.IntegerField()
    to_chat_id = peewee.IntegerField()
    message_id = peewee.IntegerField()

    msg_type = peewee.CharField()
    caption = peewee.TextField(null=True)
    text = peewee.TextField(null=True)
    file_id = peewee.CharField(null=True)

    send_time = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        db_table = 'messages'


class SearchHistory(peewee.Model):
    id = peewee.AutoField()
    chat_id = peewee.IntegerField()
    suggested_chat_id = peewee.IntegerField()
    date = peewee.DateField(default=datetime.date.today())

    class Meta:
        database = db
        db_table = 'search_history'


db.create_tables([Chat, Message, User, Gallery, SearchHistory])

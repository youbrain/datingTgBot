import json


'''Base functions, reading config.json. (function wrappers, values.json) here '''

file = open('config.json', encoding='utf-8')
config = json.loads(file.read())

with open(config['texts_file'], encoding='utf-8') as file:
    jso = json.loads(file.read())
    texts = jso['ru']['texts']
    keyboards = jso['ru']['keyboards']

from database import *

from telegram import InlineKeyboardButton


def get_n_column_keyb(data, prefix, n):
    flag = []
    btns = []

    if len(data) <= n:
        btns = [InlineKeyboardButton(d[0], callback_data=f"{prefix}_{d[1]}") for d in data]
        return [btns]

    for d in data:
        if len(flag) + 1 < n:
            flag.append(InlineKeyboardButton(d[0], callback_data=f"{prefix}_{d[1]}"))
        else:
            flag.append(InlineKeyboardButton(d[0], callback_data=f"{prefix}_{d[1]}"))
            btns.append(flag)
            # btns.append([])
            flag = []
    if flag:
        btns.append(flag)
    return btns

import telegram
import configparser
import redis
from telegram.ext import Updater, CommandHandler
from telegram.ext import Updater

import pandas as pd
from datetime import date
import re

config = configparser.ConfigParser()
config.read_file(open('config.ini'))
updater = Updater(token=config['DEFAULT']['token'])
dispatcher = updater.dispatcher

def start(bot, update):
    me = bot.get_me()

    msg = "Fala!\n"
    msg += "Aqui é o {0} e eu posso te dizer o almoço ou o jantar de hoje.\n".format(me.first_name)
    msg += "/lunch para o almoço e /dinner para a janta\n"


    main_menu_keyboard = [[telegram.KeyboardButton('/lunch')],
                          [telegram.KeyboardButton('/dinner')]]
    reply_kb_markup = telegram.ReplyKeyboardMarkup(main_menu_keyboard,
                                                   resize_keyboard=True,
                                                   one_time_keyboard=True)

    bot.send_message(chat_id=update.message.chat_id,
                     text=msg,
                     reply_markup=reply_kb_markup)
def lunch(bot, update):
    df = pd.read_html('http://ru.ufpa.br/index.php?option=com_content&view=article&id=7')
    cardapio = df[4].fillna(value='SEM REFEIÇÃO')
    lunch = pd.DataFrame(cardapio[1])

    me = bot.get_me()

    today = str(date.today()).split('-')[-1]
    msg = ''
    for i in range(1, 6):
        if re.split("[- ]", cardapio[0][i])[-2] == today:
            msg = cardapio[1][i]


    bot.send_message(chat_id=update.message.chat_id, text=msg)

def dinner(bot, update):
    df = pd.read_html('http://ru.ufpa.br/index.php?option=com_content&view=article&id=7')
    cardapio = df[4].fillna(value='SEM REFEIÇÃO')
    dinner = pd.DataFrame(cardapio[2])

    me = bot.get_me()

    today = str(date.today()).split('-')[-1]
    msg = ''
    for i in range(1, 6):
        if re.split("[- ]", cardapio[0][i])[-2] == today:
            msg = cardapio[2][i]
    bot.send_message(chat_id=update.message.chat_id, text=msg)


db = redis.StrictRedis(host=config['DB']['host'],
                       port=config['DB']['port'],
                       db=config['DB']['db'])

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
lunch_handler = CommandHandler('lunch', lunch)
dispatcher.add_handler(lunch_handler)
dinner_handler = CommandHandler('dinner', dinner)
dispatcher.add_handler(dinner_handler)



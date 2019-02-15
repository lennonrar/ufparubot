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
erro = '--------------------------------------------------'
def start(bot, update):
    me = bot.get_me()

    msg = "Fala manx!\n"
    msg += "Aqui é o {0} e eu posso te dizer quais as brocas de hoje.\n".format(me.first_name)
    msg += "/almoco para o almoço e /jantar para a janta\n"
    #msg += "Código: https://github.com/lennonalmeida/ufparubot\n"


    main_menu_keyboard = [[telegram.KeyboardButton('/almoco')],
                          [telegram.KeyboardButton('/jantar')]]
    reply_kb_markup = telegram.ReplyKeyboardMarkup(main_menu_keyboard,
                                                   resize_keyboard=True,
                                                   one_time_keyboard=True)

    bot.send_message(chat_id=update.message.chat_id,
                     text=msg,
                     reply_markup=reply_kb_markup)
def almoco(bot, update):
    df = pd.read_html('http://ru.ufpa.br/index.php?option=com_content&view=article&id=7')
    cardapio = df[4].fillna(value='SEM REFEIÇÃO')
    

    for i in range(1, 6):
        if erro in cardapio[1][i]:
            cardapio[1][i] = 'SEM REFEIÇÃO'
 
    lunch = pd.DataFrame(cardapio[1])
    me = bot.get_me()

    today = str(date.today()).split('-')[-1]
    msg = ''

    for i in range(1, 6):
        if re.split("[- ]", cardapio[0][i])[-2] == today:
            msg = cardapio[1][i]
    a,b = treat(msg)

    bot.send_message(chat_id=update.message.chat_id, text=a)
    bot.send_message(chat_id=update.message.chat_id, text=b)


def jantar(bot, update):
    df = pd.read_html('http://ru.ufpa.br/index.php?option=com_content&view=article&id=7')
    cardapio = df[4].fillna(value='SEM REFEIÇÃO')
        
    for i in range(1, 6):
        if erro in cardapio[2][i]:
            cardapio[2][i] = 'SEM REFEIÇÃO'
    
    dinner = pd.DataFrame(cardapio[2])
    me = bot.get_me() 

    today = str(date.today()).split('-')[-1]
    msg = ''
    for i in range(1, 6):
        if re.split("[- ]", cardapio[0][i])[-2] == today:
            msg = cardapio[2][i]
       
    c,d = treat(msg)
    
    bot.send_message(chat_id=update.message.chat_id, text=c)
    bot.send_message(chat_id=update.message.chat_id, text=d)

def treat(msg):
    if 'ARROZ CARRETEIRO' in msg or 'RISOTO DE FRANGO' in msg:        
        msg = msg.split('FEIJÃO')[0]
    else:
        msg = msg.split('ARROZ')[0]
    
    if msg == 'SEM REFEIÇÃO':
        a, b = msg, '😢'
    else:
        a = msg.split('VEGETARIANO:')[0].lower().capitalize()
        b = msg.split('VEGETARIANO:')[1].lower().strip().capitalize()
    return a, b


db = redis.StrictRedis(host=config['DB']['host'],
                       port=config['DB']['port'],
                       db=config['DB']['db'])

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
almoco_handler = CommandHandler('almoco', almoco)
dispatcher.add_handler(almoco_handler)
jantar_handler = CommandHandler('jantar', jantar)
dispatcher.add_handler(jantar_handler)


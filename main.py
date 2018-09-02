#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pprint import pprint

import requests
import telebot
from telebot import types

import backend

bot = telebot.TeleBot('620840940:AAF5VN_qQJoSZh0eVlN07hFcE8Aye2VRmjo')
chekFunction = True



@bot.message_handler(commands=["start"])
def start_command_handler(message):
    bot.send_message(message.chat.id, "Бот контролирует ваш листинг по ASIN'у и реагирует на количественные изменения отзывов, фото, кол-ва продавцов и т.д.")
    keyboard = types.InlineKeyboardMarkup()
    #keyboard.add(types.InlineKeyboardButton(text="Яндекс Деньги", callback_data="1" + str(message.from_user.first_name) + ' ' + str(message.from_user.last_name)))
    #keyboard.add(types.InlineKeyboardButton(text="Банковская карта", callback_data="2" + str(message.from_user.first_name) + ' ' + str(message.from_user.last_name)))
    #bot.send_message(message.chat.id, 'Для использования данного бота необходимо оплатить 5$' + '\n' + "После оплаты мы вышлем вам ключ для активации", reply_markup=keyboard)
    #bot.send_message(message.chat.id, "Введите ключ:")
    bot.send_message(message.chat.id, "Привет, введи ASIN товара" + '\n' + 'P.S. Один аккаунт - один ASIN' + '\n' + 'P.S. По всем вопросам, предложениям писать в Telegram: @Out_In либо @logan7034 :)')
'''
@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
    if call.data[0] == "1":
        page = requests.post("https://money.yandex.ru/quickpay/confirm.xml",
                             data={"receiver": "410012790144094", "quickpay-form": "donate",
                                   "targets": "Telegram Bot (Amazon Checker)", "sum": "350", "paymentType": "PC",
                                   "comment": call.data[1:]})
    else:
        page = requests.post("https://money.yandex.ru/quickpay/confirm.xml",
                             data={"receiver": "410012790144094", "quickpay-form": "donate",
                                   "targets": "Telegram Bot (Amazon Checker)", "sum": "350", "paymentType": "AC",
                                   "comment": call.data[1:]})
    bot.send_message(call.message.chat.id, page.url)
'''
@bot.message_handler()
def repeat_all_messages(message, flag=True):
    #global missed
    print("Принял сообщение: " + message.text)
    #if chekFunction:
    #    missed = checkKey(message)
    if True:
        # Читка из ФАЙЛ
        users = json.loads(requests.get('http://OutIin.pythonanywhere.com/read/').text)
    
        index = 0
        if len(users['Users']) == 0:
            users['Users'].append({})
            users['Users'][len(users['Users']) - 1]['id'] = str(message.chat.id)
            users['Users'][len(users['Users']) - 1]['asins'] = []
            users['Users'][len(users['Users']) - 1]['asins'].append({})
            users['Users'][len(users['Users']) - 1]['asins'][0]['asin'] = str(message.text)
            users['Users'][len(users['Users']) - 1]['name'] = str(message.from_user.first_name)
            users['Users'][len(users['Users']) - 1]['surname'] = str(message.from_user.last_name)
            users['Users'][len(users['Users']) - 1]['login'] = '@' + str(message.from_user.username)
        for i in range(len(users['Users'])):
            print("I: ", i)
            print("len(users['Users']) - 1: ", len(users['Users']) - 1)
            if int(users['Users'][i]['id']) == message.chat.id:
                users['Users'][i]['asins'].append({})
                users['Users'][i]['asins'][len(users['Users'][i]['asins']) - 1]['asin'] = message.text
                index = i
                break
            elif i == (len(users['Users']) - 1):
                users['Users'].append({})
                users['Users'][i + 1]['id'] = str(message.chat.id)
                users['Users'][i + 1]['asins'] = []
                users['Users'][i + 1]['asins'].append({})
                users['Users'][i + 1]['asins'][len(users['Users'][i + 1]['asins']) - 1]['asin'] = str(message.text)
                users['Users'][i + 1]['name'] = str(message.from_user.first_name)
                users['Users'][i + 1]['surname'] = str(message.from_user.last_name)
                users['Users'][i + 1]['login'] = '@' + str(message.from_user.username)
                index = i + 1
        #====
        answer = backend.product(message.text, index, flag, users)
        if answer == None:
            bot.send_message(message.chat.id, "Введите адекватный ASIN")
        else:
            infoPerson = str(message.from_user.first_name) + ' ' + str(message.from_user.last_name) + ' (' + '@' + str(
                message.from_user.username) + ')' + 'ASIN: ' + str(message.text)
            bot.send_message(308367462, infoPerson)
            #bot.send_message(92711413, infoPerson)
            #bot.send_message(321174190, infoPerson)
            reviews = answer[0]
            img = answer[1]
            buyer = answer[2]
            price = answer[3]
            bot.send_message(message.chat.id, "Количество отзывов: " + str(reviews) + '\n' + "Количество картинок: " + str(img) + '\n' + "Количество продавцов: " + str(buyer) + '\n' "Цена: " + str(price))
            bot.send_message(message.chat.id, 'Ваш ASIN принят и уже обрабатывается нашим сервером.' + '\n' + 'Если будут какие-либо изменения по вышепреведенным показателям - вам придет в чат уведомление :)')

def checkKey(key):
    global chekFunction
    with open('key.json') as data_file:
        keys = json.load(data_file)
    array = keys['key']
    if key.text in array:
        bot.send_message(key.chat.id, "Ваш ключ активирован!" + '\n' + "Сейчас вы можете ввести свой ASIN :)")
        array.remove(key.text)
    else:
        bot.send_message(key.chat.id, "Неверный ключ")
        return False
    newKey = {}
    newKey['key'] = array
    with open('key.json', 'w') as file:
        json.dump(newKey, file, ensure_ascii=False)
    chekFunction = False
    return True


if __name__ == '__main__':
     bot.polling(none_stop=True)
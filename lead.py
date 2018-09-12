#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pprint import pprint

import requests
import telebot
from bs4 import BeautifulSoup
from telebot import types

import backend

header = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15"
}

zag = {'Content-type': 'application/json',  # Определение типа данных
           'Accept': 'text/plain',
           'Content-Encoding': 'utf-8'}

bot = telebot.TeleBot('620840940:AAF5VN_qQJoSZh0eVlN07hFcE8Aye2VRmjo')
chekFunction = True



@bot.message_handler(commands=["start"])
def start_command_handler(message):
    bot.send_message(message.chat.id, "Бот контролирует ваш листинг по ASIN'у и реагирует на количественные изменения отзывов, фото, кол-ва продавцов, изменение цены и главного фото")
    keyboard = types.InlineKeyboardMarkup()
    #keyboard.add(types.InlineKeyboardButton(text="Яндекс Деньги", callback_data="1" + str(message.from_user.first_name) + ' ' + str(message.from_user.last_name)))
    #keyboard.add(types.InlineKeyboardButton(text="Банковская карта", callback_data="2" + str(message.from_user.first_name) + ' ' + str(message.from_user.last_name)))
    #bot.send_message(message.chat.id, 'Для использования данного бота необходимо оплатить 5$' + '\n' + "После оплаты мы вышлем вам ключ для активации", reply_markup=keyboard)
    #bot.send_message(message.chat.id, "Введите ключ:")
    bot.send_message(message.chat.id,
                     "Обновления бота (version 2.0)\n1) Добавлена команда /asin, показывающая асины, контролируемые ботом.\n2) Добавлена команда /delete [ваш ASIN], позволяющая удалить ASIN из бота.\n3) Сейчас при изменении показателей так же генерируется ссылка на ваш товар с данными изменениями.")
    bot.send_message(message.chat.id,
                     "Обновления бота (version 2.1)\n1) Исправлен баг с командой /asin, сейчас работает на отлично\n2) При вводе команды /asin, добавлена возможность кликнуть по ASIN'у, тем самым увидев данные по листингу\n3) При начальном вводе ASIN'a так же отображается и наименование товара\n4) Исправлены небольшие недочеты в коде, которые затрудняли работу бота.")
    bot.send_message(message.chat.id, "Привет, введи ASIN товара" + '\n' + 'P.S. По всем вопросам, предложениям писать в Telegram: @Out_In либо @logan7034 :)')
'''
@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):2
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

@bot.message_handler(commands=["asin"])
def callback_inline(message):
    data = json.loads(requests.get('http://OutIin.pythonanywhere.com/read/').text)
    bot.send_message(message.chat.id, "Ваши Асины:")
    for i in range(len(data['Users'])):
        if data['Users'][i]['id'] == str(message.chat.id):
            for j in range(len(data['Users'][i]['asins'])):
                bot.send_message(message.chat.id,
                                 str(j + 1) + ') ' + '/' + data['Users'][i]['asins'][j]['asin'] + '\n' +
                                 data['Users'][i]['asins'][j]['name'])

@bot.message_handler(commands=["delete"])
def callback_inlin(message):
    asin = str(message.text)[8:]
    data = json.loads(requests.get('http://OutIin.pythonanywhere.com/read/').text)
    for i in range(len(data['Users'])):
        if data['Users'][i]['id'] == str(message.chat.id):
            print(len(data['Users'][i]['asins']))
            for j in range(len(data['Users'][i]['asins'])):
                if data['Users'][i]['asins'][j]['asin'] == asin:
                    print(data['Users'][i]['asins'][j]['asin'] == asin)
                    del data['Users'][i]['asins'][j]
                    bot.send_message(message.chat.id, "ASIN: " + str(message.text)[7:] + " удален")
                    break
                if j == len(data['Users'][i]['asins']) - 1 and data['Users'][i]['asins'][j]['asin'] != asin:
                    bot.send_message(message.chat.id, "Данного ASIN'a нет в вашем списке")
    requests.post('http://OutIin.pythonanywhere.com/write/', data=json.dumps(data), headers=zag)

@bot.message_handler()
def repeat_all_messages(message, flag=True):
    if message.text[0] == '/':
        try:
            url = requests.get("https://www.amazon.com/dp/" + message.text[1:], headers=header)
            page = BeautifulSoup(url.text, "html.parser")
            with open("file.html", "w") as file:
                file.write(str(page))
            productTitle = page.find("span", {"id": "productTitle"}).text.replace('\n', '').replace(
                '                                                                                                                                                        ',
                '').replace(
                '                                                                                                                        ',
                '')
        except Exception as ex:
            bot.send_message(message.chat.id, " Неправильный ASIN")
            return None
        try:
            line = page.find("span", {"id": "acrCustomerReviewText"}).text
            line = line.replace(',', '')
            reviews = [int(s) for s in line.split() if s.isdigit()]
            reviews = int(reviews[0])
        except:
            reviews = 0
        img = page.find("div", {"id": "altImages"}).findAll("img")
        url = requests.get(
            "https://www.amazon.com/gp/offer-listing/" + message.text[1:] + "/ref=dp_olp_new_mbc?ie=UTF8&condition=new",
            headers=header)
        page = BeautifulSoup(url.text, "html.parser")
        with open("file.html", "w") as file:
            file.write(str(page))
        allbuyer = str(page).count("a-row a-spacing-mini olpOffer")
        page = BeautifulSoup(str(page).replace('\n', ''), "html.parser")
        try:
            price = page.find("div", {"class": "a-row a-spacing-mini olpOffer"}).find("span").text.replace(
                "                ", '')
        except:
            price = 0
        try:
            a = page.find("ul", {"class": "a-pagination"}).findAll("li")
            lastPage = BeautifulSoup(
                (requests.get("https://www.amazon.com" + a[len(a) - 2].find("a")['href'], headers=header)).text,
                "html.parser")
            a = int(a[len(a) - 2].text[4:])
            allbuyer += (a - 2) * 10
            allbuyer += str(lastPage).count("a-row a-spacing-mini olpOffer")
        except:
            print("1 Старница")
        bot.send_message(message.chat.id,
                         "Наименование: " + str(productTitle) + '\n' + "Количество отзывов: " + str(
                             reviews) + '\n' + "Количество картинок: " + str(len(img)
                                                                             ) + '\n' + "Количество продавцов: " + str(
                             allbuyer) + '\n' "Цена: " + str(
                             price))
    else:
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
                bot.send_message(92711413, infoPerson)
                bot.send_message(321174190, infoPerson)
                reviews = answer[0]
                img = answer[1]
                buyer = answer[2]
                price = answer[3]
                name = answer[5]
                bot.send_message(message.chat.id, "Наименование: " + str(name) + '\n' + "Количество отзывов: " + str(reviews) + '\n' + "Количество картинок: " + str(img) + '\n' + "Количество продавцов: " + str(buyer) + '\n' "Цена: " + str(price))
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
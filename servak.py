#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
from pprint import pprint

import requests
from bs4 import BeautifulSoup

from lead import bot

header = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15"
}

zag = {'Content-type': 'application/json',  # Определение типа данных
           'Accept': 'text/plain',
           'Content-Encoding': 'utf-8'}

fromaddr = "quality.busko@gmail.com"
mypass = "idinaxui"
toaddrPAVEL = "busko-007@yandex.ru"
toaddrYauheni = "busko-007@mail.ru"



#bot.send_message(int(data['Users'][0]['id']), "Введите адекватный ASIN :)")




def product(dat):
    #EMAIL
    global new1
    for i in range(len(dat['Users'])):
        for j in range(len(dat['Users'][i]['asins'])):
            print("Я ТУТ")
            url = requests.get("https://www.amazon.com/dp/" + dat['Users'][i]['asins'][j]['asin'], headers=header)
            page = BeautifulSoup(url.text, "html.parser")
            with open("file.html", "w") as file:
                file.write(str(page))
            try:
                mainImage = page.find("div", {"id": "imgTagWrapperId"}).find("img")['data-a-dynamic-image']
                productTitle = page.find("span", {"id": "productTitle"}).text.replace('\n', '').replace(
                    '                                                                                                                                                        ',
                    '').replace(
                    '                                                                                                                        ',
                    '')
            except:
                mainImage = dat['Users'][i]['asins'][j]['img']
                continue
            try:
                line = page.find("span", {"id": "acrCustomerReviewText"}).text
                line = line.replace(',', '')
                reviews = [int(s) for s in line.split() if s.isdigit()]
                reviews = int(reviews[0])
            except:
                reviews = 0
            img = page.find("div", {"id": "altImages"}).findAll("img")
            url = requests.get("https://www.amazon.com/gp/offer-listing/" + dat['Users'][i]['asins'][j]['asin'] + "/ref=dp_olp_new_mbc?ie=UTF8&condition=new", headers=header)
            page = BeautifulSoup(url.text, "html.parser")
            with open("file.html", "w") as file:
                file.write(str(page))
            allbuyer = str(page).count("a-row a-spacing-mini olpOffer")
            page = BeautifulSoup(str(page).replace('\n', ''), "html.parser")
            try:
                price = page.find("div", {"class": "a-row a-spacing-mini olpOffer"}).find("span").text.replace("                ", '')
            except:
                price = 0
            # page.find("li", attrs={"class": "a-last"}) != None
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
            print("Количество отзывов: ", reviews)
            print("Количество фото: ", len(img))
            print("Количество продавцов: ", allbuyer)
            print("Цена: ", price)
            print("Main IMAGE: ", mainImage)
            answer = [reviews, len(img), allbuyer, price, mainImage]
            new1 = change(answer, i, j, dat)
    return new1


def change(newCheck, index, j, dat):
    try:
        #info['Users'][user]['asins'][len(info['Users'][user]['asins']) - 1]['reviews']
        if str(dat['Users'][index]['asins'][j]['reviews']) != str(newCheck[0]):
            bot.send_message(int(dat['Users'][index]['id']), "По ASIN'у: " + str(
                dat['Users'][index]['asins'][j]['asin']) + " изменилось количество отзывов c " + str(
                dat['Users'][index]['asins'][j]['reviews']) + " на " + str(newCheck[0]))
            bot.send_message(int(dat['Users'][index]['id']),
                             'https://www.amazon.com/dp/' +
                             dat['Users'][index]['asins'][j]['asin'])
            dat['Users'][index]['asins'][j]['reviews'] = newCheck[0]
        if str(dat['Users'][index]['asins'][j]['img']) != str(newCheck[1]):
            bot.send_message(int(dat['Users'][index]['id']), "По ASIN'у: " + str(
                dat['Users'][index]['asins'][j]['asin']) + " изменилось количество картинок c " + str(
                dat['Users'][index]['asins'][j]['img']) + " на " + str(newCheck[1]))
            bot.send_message(int(dat['Users'][index]['id']),
                             'https://www.amazon.com/dp/' +
                             dat['Users'][index]['asins'][j]['asin'])
            dat['Users'][index]['asins'][j]['img'] = newCheck[1]
        if str(dat['Users'][index]['asins'][j]['allbuyer']) != str(newCheck[2]):
            bot.send_message(int(dat['Users'][index]['id']), "По ASIN'у: " + str(
                dat['Users'][index]['asins'][j]['asin']) + " изменилось количество продавцов c " + str(
                dat['Users'][index]['asins'][j]['allbuyer']) + " на " + str(newCheck[2]))
            bot.send_message(int(dat['Users'][index]['id']),
                             'https://www.amazon.com/dp/' +
                             dat['Users'][index]['asins'][j]['asin'])
            dat['Users'][index]['asins'][j]['allbuyer'] = newCheck[2]
        if str(dat['Users'][index]['asins'][j]['price']) != str(newCheck[3]):
            bot.send_message(int(dat['Users'][index]['id']), "По ASIN'у: " + str(
                dat['Users'][index]['asins'][j]['asin']) + " изменилась цена c " + str(
                dat['Users'][index]['asins'][j]['price']) + " на " + str(newCheck[3]))
            bot.send_message(int(dat['Users'][index]['id']),
                             'https://www.amazon.com/dp/' +
                             dat['Users'][index]['asins'][j]['asin'])
            dat['Users'][index]['asins'][j]['price'] = newCheck[3]
        if str(dat['Users'][index]['asins'][j]['mainImage']) != str(newCheck[4]):
            bot.send_message(int(dat['Users'][index]['id']), "По ASIN'у: " + str(
                dat['Users'][index]['asins'][j]['asin']) + " изменилось главное фото")
            bot.send_message(int(dat['Users'][index]['id']),
                             'https://www.amazon.com/dp/' +
                             dat['Users'][index]['asins'][j]['asin'])
            dat['Users'][index]['asins'][j]['mainImage'] = newCheck[4]
            print("КОНЕЦ ПРОВЕРКИ")
    except:
        bot.send_message(308367462, 'Чел с ' + str(int(dat['Users'][index]['id'])) + ' заблочен')
    return dat


def python():
    write = requests.get('http://127.0.0.1:8000/write/', params={'name': json.dumps(data)})
    read = json.loads(requests.get('http://127.0.0.1:8000/read/').text)
    pprint(type(read))

if __name__ == '__main__':
    #python()
    print("ПРОВЕРКА 2 ПОТОКА")
    while True:
        data = json.loads(requests.get('http://OutIin.pythonanywhere.com/read/').text)
        new = product(data)
        requests.post('http://OutIin.pythonanywhere.com/write/', data=json.dumps(new), headers=zag)
        time.sleep(1800)

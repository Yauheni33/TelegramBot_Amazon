import json
import time
from pprint import pprint
import telebot
import threading
import requests
from bs4 import BeautifulSoup


header = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15"
}

bot = telebot.TeleBot('620840940:AAFzqNAmhrpz-RV-qMPa2Q2KLuR62pnb3Sg')
fromaddr = "quality.busko@gmail.com"
mypass = "idinaxui"
toaddrPAVEL = "busko-007@yandex.ru"
toaddrYauheni = "busko-007@mail.ru"



#bot.send_message(int(data['Users'][0]['id']), "Введите адекватный ASIN :)")

with open('/Users/yauheni/PycharmProjects/OPTICATCH/users.json') as data_file:
    data = json.load(data_file)


def product():
    #EMAIL
    for i in range(len(data['Users'])):
        print("Я ТУТ")
        url = requests.get("https://www.amazon.com/Nacome-Cotton-Breathable-Panties-Underwear/dp/" + data['Users'][i]['asin'], headers=header)
        page = BeautifulSoup(url.text, "html.parser")
        with open("file.html", "w") as file:
            file.write(str(page))
        mainImage = page.find("div", {"id": "imgTagWrapperId"}).find("img")['data-a-dynamic-image']
        try:
            line = page.find("span", {"id": "acrCustomerReviewText"}).text
            line = line.replace(',', '')
            reviews = [int(s) for s in line.split() if s.isdigit()]
            reviews = int(reviews[0])
        except:
            reviews = 0
        img = page.find("div", {"id": "altImages"}).findAll("img")
        url = requests.get("https://www.amazon.com/gp/offer-listing/" + data['Users'][i]['asin'] + "/ref=dp_olp_new_mbc?ie=UTF8&condition=new", headers=header)
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
        change(answer, i)


def change(newCheck, index):
    if data['Users'][index]['reviews'] != newCheck[0]:
        bot.send_message(int(data['Users'][index]['id']), "Изменилось количество Отзывов")
        data['Users'][index]['reviews'] = newCheck[0]
    if data['Users'][index]['img'] != newCheck[1]:
        bot.send_message(int(data['Users'][index]['id']), "Изменилось количество картинок")
        data['Users'][index]['img'] = newCheck[1]
    if data['Users'][index]['allbuyer'] != newCheck[2]:
        bot.send_message(int(data['Users'][index]['id']), "Изменилось количество продавцов")
        data['Users'][index]['allbuyer'] = newCheck[2]
    if data['Users'][index]['price'] != newCheck[3]:
        bot.send_message(int(data['Users'][index]['id']), "Изменилась цена")
        data['Users'][index]['price'] = newCheck[3]
    if data['Users'][index]['mainImage'] != newCheck[4]:
        bot.send_message(int(data['Users'][index]['id']), "Изменилось главное фото")
        data['Users'][index]['mainImage'] = newCheck[4]
    print("КОНЕЦ ПРОВЕРКИ")


if __name__ == '__main__':
    while True:
        product()
        time.sleep(60)

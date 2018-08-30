#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from bs4 import BeautifulSoup

header = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15"
}

fromaddr = "quality.busko@gmail.com"
mypass = "idinaxui"
toaddrPAVEL = "busko-007@yandex.ru"
toaddrYauheni = "busko-007@mail.ru"



def product(asin, user, flag, info):
    #EMAIL
    if flag:
        #bot.send_message(308367462, asin)
        '''
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddrPAVEL
        msg['Subject'] = "Amazon ASIN"

        mymsg = MIMEMultipart()
        mymsg['From'] = fromaddr
        mymsg['To'] = toaddrYauheni
        mymsg['Subject'] = "Amazon ASIN"

        body = user[0] + ' ' + user[1] + ' (' + user[2] + ') ' + 'ASIN: ' + asin
        msg.attach(MIMEText(body, 'plain'))
        mymsg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, mypass)
        text = msg.as_string()
        textMy = mymsg.as_string()
        server.sendmail(fromaddr, toaddrPAVEL, text)
        server.sendmail(fromaddr, toaddrYauheni, textMy)
        server.quit()
        '''
    #-----
    try:
        url = requests.get("https://www.amazon.com/Nacome-Cotton-Breathable-Panties-Underwear/dp/" + asin, headers=header)
        page = BeautifulSoup(url.text, "html.parser")
        with open("file.html", "w") as file:
            file.write(str(page))
        mainImage = page.find("div", {"id": "imgTagWrapperId"}).find("img")['data-a-dynamic-image']
    except Exception as ex:
        print(ex)
        return None
    try:
        line = page.find("span", {"id": "acrCustomerReviewText"}).text
        line = line.replace(',', '')
        reviews = [int(s) for s in line.split() if s.isdigit()]
        reviews = int(reviews[0])
    except:
        reviews = 0
    img = page.find("div", {"id": "altImages"}).findAll("img")
    url = requests.get("https://www.amazon.com/gp/offer-listing/" + asin + "/ref=dp_olp_new_mbc?ie=UTF8&condition=new", headers=header)
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
    info['Users'][user]['reviews'] = reviews
    info['Users'][user]['img'] = len(img)
    info['Users'][user]['allbuyer'] = allbuyer
    info['Users'][user]['price'] = price
    info['Users'][user]['mainImage'] = mainImage
    with open('users.json', 'w') as file:
        json.dump(info, file, ensure_ascii=False)
    return answer


#product("B0000CFN0Y", [], False)
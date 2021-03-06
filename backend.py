#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup

header = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
}

zag = {'Content-type': 'application/json',  # Определение типа данных
           'Accept': 'text/plain',
           'Content-Encoding': 'utf-8'}

fromaddr = "###"
mypass = "###"
toaddrPAVEL = "###"
toaddrYauheni = "###"



def product(asin, user, flag, info):
    #EMAIL
    if flag:
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
        url = requests.get("https://www.amazon.com/dp/" + asin, headers=header)
        page = BeautifulSoup(url.text, "html.parser")
        with open("file.html", "w") as file:
            file.write(str(page))
        mainImage = page.find("div", {"id": "imgTagWrapperId"}).find("img")['data-a-dynamic-image']
        productTitle = page.find("span", {"id": "productTitle"}).text.replace('\n', '').replace(
            '                                                                                                                                                        ',
            '').replace(
            '                                                                                                                        ',
            '')
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
    img = page.find("div", {"id": "altImages"}).findAll("li", {"class": "a-spacing-small item"})
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
    ad = requests.get('https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=' +
                      dat['Users'][i]['asins'][j]['name'] + ' ' + dat['Users'][i]['asins'][j]['asin'])
    pg = BeautifulSoup(ad.text, 'html.parser')
    if pg.find("h1", {"id": "noResultsTitle"}) == None:
        index = False
    else:
        index = True
    print("Количество отзывов: ", reviews)
    print("Количество фото: ", len(img))
    print("Количество продавцов: ", allbuyer)
    print("Цена: ", price)
    print("Main IMAGE: ", mainImage)
    answer = [reviews, len(img), allbuyer, price, mainImage, productTitle]
    info['Users'][user]['asins'][len(info['Users'][user]['asins']) - 1]['name'] = str(productTitle)
    info['Users'][user]['asins'][len(info['Users'][user]['asins']) - 1]['reviews'] = str(reviews)
    info['Users'][user]['asins'][len(info['Users'][user]['asins']) - 1]['img'] = len(img)
    info['Users'][user]['asins'][len(info['Users'][user]['asins']) - 1]['allbuyer'] = str(allbuyer)
    info['Users'][user]['asins'][len(info['Users'][user]['asins']) - 1]['price'] = str(price)
    info['Users'][user]['asins'][len(info['Users'][user]['asins']) - 1]['mainImage'] = str(mainImage)
    info['Users'][user]['asins'][len(info['Users'][user]['asins']) - 1]['date'] = str(datetime.datetime.now())
    info['Users'][user]['asins'][len(info['Users'][user]['asins']) - 1]['index'] = str(index)
    #ask = requests.get('http://OutIin.pythonanywhere.com/write/', params={'name': json.dumps(info)})
    #pprint(type(json.dumps(info)))
    #print(type(json.dumps(info)))
    requests.post('http://OutIin.pythonanywhere.com/write/', data=json.dumps(info), headers=zag)
    return answer


#product("B0000CFN0Y", [], False)

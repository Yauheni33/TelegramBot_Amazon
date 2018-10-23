import datetime
import time
from pprint import pprint

import requests
import json
from dateutil.parser import parse


zag = {'Content-type': 'application/json',  # Определение типа данных
           'Accept': 'text/plain',
           'Content-Encoding': 'utf-8'}

x = 0
def main():
    print('Начал проверку подписок')
    data = json.loads(requests.get('http://OutIin.pythonanywhere.com/read/').text)
    for i in range(len(data['Users'])):
        for j in data['Users'][i]['asins']:
            if int((datetime.datetime.now() - parse(j['date'])).days) > 30:
                del data['Users'][i]['asins'][x]
            x += 1
        x = 0
    requests.post('http://OutIin.pythonanywhere.com/write/', data=json.dumps(data), headers=zag)
    print('Закончил проверку подписок')

def p():
    keys = json.loads(requests.get('http://OutIin.pythonanywhere.com/key/').text)
    keys['from'] = str(int(keys['from']) + 4)
    requests.post('http://OutIin.pythonanywhere.com/key/', data=json.dumps(keys))
    pprint(keys['from'])


if __name__ == '__main__':
    while True:
        main()
        time.sleep(86400)
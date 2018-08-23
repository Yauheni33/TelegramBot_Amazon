import json
import time
import telebot
import backend

bot = telebot.TeleBot('620840940:AAFzqNAmhrpz-RV-qMPa2Q2KLuR62pnb3Sg')



@bot.message_handler(commands=["start"])
def start_command_handler(message):
    bot.send_message(message.chat.id, "Привет, введи ASIN товара" + '\n' + 'P.S. Один аккаунт - один ASIN' + '\n' + 'P.S. По всем вопросам, предложениям писать в Telegram: @Out_In либо @logan7034 :)')

@bot.message_handler()
def repeat_all_messages(message, flag=True):
    print("Принял сообщение: " + message.text)
    # Читка из ФАЙЛ
    with open('users.json') as data_file:
        users = json.load(data_file)

    users['Users'].append({})
    users['Users'][len(users['Users']) - 1]['id'] = str(message.chat.id)
    users['Users'][len(users['Users']) - 1]['asin'] = str(message.text)
    users['Users'][len(users['Users']) - 1]['name'] = str(message.from_user.first_name)
    users['Users'][len(users['Users']) - 1]['surname'] = str(message.from_user.last_name)
    users['Users'][len(users['Users']) - 1]['login'] = '@' + str(message.from_user.username)
    #====
    answer = backend.product(message.text, [str(message.from_user.first_name), str(message.from_user.last_name), '@' + str(message.from_user.username)], flag, users)
    if answer == None:
        bot.send_message(message.chat.id, "Введите адекватный ASIN :)")
        exit()
    reviews = answer[0]
    img = answer[1]
    buyer = answer[2]
    price = answer[3]
    bot.send_message(message.chat.id, "Количество отзывов: " + str(reviews) + '\n' + "Количество картинок: " + str(img) + '\n' + "Количество продавцов: " + str(buyer) + '\n' "Цена: " + str(price))
    bot.send_message(message.chat.id, 'Ваш ASIN принят и уже обрабатывается нашим сервером.' + '\n' + 'Если будут какие-либо изменения по вышепреведенным показателям - вам придет в чат уведомление :)')


if __name__ == '__main__':
     bot.polling(none_stop=True)
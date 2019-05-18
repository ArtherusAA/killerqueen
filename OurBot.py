import requests
import datetime
import random
from telegram import ParseMode

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update


greet_bot = BotHandler('881754483:AAHPO5YANDlNtAhWK0bYq4BwSW1Om_kpqlM')
greetings = ('здравствуй', 'привет', 'ку', 'здорово')
now = datetime.datetime.now()


def hello(last_chat_id, last_chat_name, last_chat_text, hour):
    if last_chat_text.lower() and 6 <= hour < 12:
        greet_bot.send_message(last_chat_id, 'Доброе утро, {}'.format(last_chat_name))
        #today += 1

    elif last_chat_text.lower() and 12 <= hour < 17:
        greet_bot.send_message(last_chat_id, 'Добрый день, {}'.format(last_chat_name))
        #today += 1

    elif last_chat_text.lower() and 17 <= hour < 23:
        greet_bot.send_message(last_chat_id, 'Добрый вечер, {}'.format(last_chat_name))
        #today += 1

def last_mess():
    f = open('/Users/jonathan/Documents/PromProg/FInal_proj/killergame/lastmes.txt', 'r')
    ans = f.read()
    greet_bot.send_message(last_chat_id, ans[len(ans) - 100:])
    f.close()

def make_game():
    ans = ''
    for i in range(12):
        if i % 3 == 0 and i != 0:
            ans += '-'
        ans += chr(random.randint(66, 122))
    ans = ans.upper()
    return ans

def main():
    new_offset = None
    today = now.day
    hour = now.hour

    print('Запуск успешен')

    while True:
        try:
            greet_bot.get_updates(new_offset)

            last_update = greet_bot.get_last_update()

            last_update_id = last_update['update_id']
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
            last_chat_name = last_update['message']['chat']['first_name']

            if (abs(now.hour - hour) >= 1):
                hour = hour.now
                hello(last_chat_id, last_chat_name, last_chat_text, hour)

            text = list(last_chat_text.lower().split())

            if last_chat_name == 'Jonathan⚡️' and text[0] == '/last_mess':
                last_mess()

            elif (text[0] == '/make_game'):
                try:
                    str = make_game()
                    greet_bot.send_message(last_chat_id, 'Отлично твоя игра создана, её уникальный номер: ' + str) #надо создать лоби с номером str
                #и проверить играет ли уже парень
                except:
                    greet_bot.send_message(last_chat_id, 'Я такое не умею, может в следующий раз')


            elif (text[0] == '/join'): # проверить существует ли такое лобби и не играют ли уже там
                try:

                    greet_bot.send_message(last_chat_id, 'Отлично сейчас я добавлю тебя в лобби: ' + text[len(text) - 1])
                except:
                    greet_bot.send_message(last_chat_id, 'Я такое не умею, может в следующий раз')

            elif last_chat_text.lower():
                try:
                    if str(text[0]) == 'add':
                        text = map(int, text[1:])
                        greet_bot.send_message(last_chat_id, 'Сумма чисел, {}'.format(sum(text)))

                    elif str(text[0]).lower() == 'jesus':
                        f = open('/Users/jonathan/Documents/PromProg/FInal_proj/killergame/Jesus.txt', 'r')
                        jesus = f.read()
                        f.close()
                        greet_bot.send_message(last_chat_id, 'пока не робит соре')
                except:
                    greet_bot.send_message(last_chat_id, 'Ой ОЙ оЙ, за такое положен бан')

            file = open('/Users/jonathan/Documents/PromProg/FInal_proj/killergame/lastmes.txt', 'a')
            file.write(last_chat_name + ' ' + last_chat_text + '\n')
            file.close()
            print(last_chat_name, last_chat_text)# View who is write && what
            #print(last_update['message'])
            new_offset = last_update_id + 1
        except:
            print('Error')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()

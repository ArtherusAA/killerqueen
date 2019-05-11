import requests
import datetime
import random
from telegram import ParseMode
import dbrequests as dbr

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=40):
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

def last_mess(last_chat_id):
    f = open('/Users/jonathan/Documents/PromProg/FInal_proj/killerqueen/lastmes.txt', 'r')
    ans = f.read()
    greet_bot.send_message(last_chat_id, ans[len(ans) - 100:])
    f.close()

def make_game():
    ans = ''
    for i in range(12):
        if i % 3 == 0 and i != 0:
            ans += '-'
        ans += chr(random.randint(65, 90))
    return ans

def get_victim(game):

    random.shuffle(game)
    for i in range(0, len(game) - 1):
        dbr.set_target_to_user(game[i], game[i + 1])
    dbr.set_target_to_user(game[len(game) - 1], game[0])

def main():
    new_offset = None
    today = now.day
    hour = now.hour

    print('Запуск успешен')

    while True:
        try:
            #print('Запуск успешен')
            greet_bot.get_updates(new_offset)
            last_update = greet_bot.get_last_update()
            last_update_id = last_update['update_id']
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
            last_chat_name = last_update['message']['chat']['first_name']
            dbr.registration(str(last_chat_id), '@' + last_update['message']['chat']['username'])
            #print(last_update)
    ###########################################################################
            text = list(last_chat_text.lower().split())
            #print(text)
    ###########################################################################
            if last_chat_name == 'Jonathan ⚡️' and text[0] == '/last_mess':
                last_mess(last_chat_id)
    ###########################################################################
            elif (text[0] == '/make_game'):
                try:
                    if dbr.get_players_condition(str(last_chat_id) != 'playing'): # what target?
                        name_of_game = make_game()
                        print(dbr.create_game(name_of_game))
                        print(dbr.change_games_condition(name_of_game, 'wait'))
                        print(dbr.join_game(str(last_chat_id), name_of_game))
                        print(dbr.change_players_condition(str(last_chat_id), 'playing'))
                        greet_bot.send_message(last_chat_id, 'Отлично твоя игра создана, её уникальный номер: ' + name_of_game)
                    else:
                        greet_bot.send_message(last_chat_id, 'Ты не можешь этого сделать, т.к. находишься в другой игре. Доиграй или покинь её')
                except:
                    greet_bot.send_message(last_chat_id, 'Я такое не умею, может в следующий раз')
    ###########################################################################
            elif (text[0] == '/join'): # проверить существует ли такое лобби и не играют ли уже там
                try:
                    game = text[len(text) - 1].upper()
                    if dbr.get_players_condition(str(last_chat_id) != 'playing') and dbr.get_games_condition(game) == 'wait': #what target?
                        greet_bot.send_message(last_chat_id, 'Отлично сейчас я добавлю тебя в лобби: ' + game)
                        dbr.join_game(str(last_chat_id), game)
                        dbr.change_players_condition(str(last_chat_id), 'playing') #what target?
                    else:
                        greet_bot.send_message(last_chat_id, 'Ты не можешь этого сделать, т.к. находишься в другой игре. Доиграй или покинь её')
                    # else:
                    #     greet_bot.send_message(last_chat_id, 'Ты не можешь этого сделать, т.к. такой игры нет или она уже идёт(((')
                except:
                    greet_bot.send_message(last_chat_id, 'Я такое не умею, может в следующий раз')

            elif text[0] == '/start_game' and dbr.get_games_condition(dbr.get_game(str(last_chat_id)).upper()) == 'wait':
                #try:
                get_victim(dbr.get_players(dbr.get_game(str(last_chat_id))))
                dbr.change_games_condition(dbr.get_game(str(last_chat_id)), 'going')
                for i in dbr.get_players(dbr.get_game(str(last_chat_id))):
                    print(i)
                    greet_bot.send_message(i, 'Игра начинается! Отдай этот код своему убийце, если конечно тебя убили!')
                    code = make_game() # just generate a symbols
                    greet_bot.send_message(i, code)




            #except:
            #        print('Error')
            elif text[0] == '/leave' and dbr.get_players_condition(str(last_chat_id)) == 'playing':

                if dbr.get_games_condition(dbr.get_game(str(last_chat_id)).upper()) == 'wait':
                    dbr.change_players_condition(str(last_chat_id), 'free')
                    dbr.leave_game(str(last_chat_id))

                elif dbr.get_games_condition(dbr.get_game(str(last_chat_id)).upper()) == 'going':  # you need make function find_killer
                    dbr.change_players_condition(str(last_chat_id), 'free')
                    dbr.set_target_to_user(dbr.get_user_killer(str(last_chat_id)), dbr.get_user_target(str(last_chat_id)))
                    dbr.set_target_to_user(str(last_chat_id), '')
                    dbr.leave_game(str(last_chat_id))
                else:
                    greet_bot.send_message(last_chat_id, 'Ты не можешь этого сделать, т.к. не играешь')

            elif text[0] == '/jesus':
                try:
                    f = open('/Users/jonathan/Documents/PromProg/FInal_proj/killergame/Jesus.txt', 'r')
                    jesus = f.read()
                    greet_bot.send_message(last_chat_id, jesus)
                    f.close()
                except:
                    greet_bot.send_message(last_chat_id, 'Ой ОЙ оЙ, за такое положен бан')
    ###########################################################################

            file = open('/Users/jonathan/Documents/PromProg/FInal_proj/killerqueen/lastmes.txt', 'a')
            file.write(last_chat_name + ' ' + last_chat_text + '\n')
            file.close()
            print(last_chat_name, last_chat_id, last_chat_text)# View who is write && what
            #print(last_update['message'])
            new_offset = last_update_id + 1
        except:
            print('Error')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('я вышел')
        exit()

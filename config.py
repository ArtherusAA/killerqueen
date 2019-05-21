import random
import dbrequests as dbr
# -*- coding: utf-8 -*-

token = '881754483:AAHPO5YANDlNtAhWK0bYq4BwSW1Om_kpqlM'
def make_game():
    ans = ''
    for i in range(12):
        if i % 3 == 0 and i != 0:
            ans += '-'
        ans += chr(random.randint(65, 90))
    return ans
def last_mess(last_chat_id):
    f = open('/Users/jonathan/Documents/PromProg/FInal_proj/killerqueen/lastmes.txt', 'r')
    ans = f.read()
    greet_bot.send_message(last_chat_id, ans[len(ans) - 100:])
    f.close()

def get_victim(game):

    random.shuffle(game)
    for i in range(0, len(game) - 1):
        dbr.set_target_to_user(game[i], game[i + 1])
    dbr.set_target_to_user(game[len(game) - 1], game[0])

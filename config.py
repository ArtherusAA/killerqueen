import random
# -*- coding: utf-8 -*-

token = '881754483:AAHPO5YANDlNtAhWK0bYq4BwSW1Om_kpqlM'
def make_game():
    ans = ''
    for i in range(12):
        if i % 3 == 0 and i != 0:
            ans += '-'
        ans += chr(random.randint(65, 90))
    return ans

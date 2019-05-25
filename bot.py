# -*- coding: utf-8 -*-
import config
import telebot
import requests
import datetime
import random
import dbrequests as dbr
from telebot import types

greet_bot = telebot.TeleBot(config.token)
def winner(last_chat_id):
    dbr.establish_winner(last_chat_id, dbr.get_game(last_chat_id))
    greet_bot.send_message(last_chat_id, 'Поздравляю! Обыграв остальных участиков, ты ПОБЕДИЛ!')
    dbr.count_wins(last_chat_id)
    greet_bot.send_message(last_chat_id, 'Колличество твоих убийств на данный момент: ' + str(dbr.get_amount_kills(last_chat_id)))
    greet_bot.send_message(last_chat_id, 'Колличество твоих побед на данный момент: ' + str(dbr.get_amount_wins(last_chat_id)))
    dbr.set_target_to_user(last_chat_id, '')
    dbr.set_user_identifier(last_chat_id, '')
    dbr.change_players_condition(last_chat_id, 'free')
    dbr.change_games_condition(dbr.get_game(last_chat_id), 'finish')
    dbr.leave_game(last_chat_id)
    markup = types.ReplyKeyboardMarkup()
    markup.row('создать игру')
    greet_bot.send_message(last_chat_id, "выбирай", reply_markup=markup)

def kill(died):
    greet_bot.send_message(died, 'Тебя убили! Но ничего, в следующей игре тебе обязательно повезёт!')
    greet_bot.send_message(died, 'Можешь искать другую игру!')
    dbr.leave_game(died)
    dbr.set_target_to_user(died, '')
    dbr.set_user_identifier(died, '')
    dbr.change_players_condition(died, 'free')
    markup = types.ReplyKeyboardMarkup()
    markup.row('создать игру')
    greet_bot.send_message(died, "выбирай", reply_markup=markup)

@greet_bot.message_handler(commands=['join'])      # join game
def handle_start(message):
    last_chat_id = str(message.chat.id)
    game = message.text.split()
    #print(game)
    game = game[len(game) - 1]
    #print(game)
    if dbr.get_players_condition(last_chat_id != 'playing') and dbr.get_games_condition(game) == 'wait':
        greet_bot.send_message(last_chat_id, 'Отлично сейчас я добавлю тебя в лобби: ' + game)
        dbr.join_game(last_chat_id, game)
        dbr.change_players_condition(last_chat_id, 'playing')

        for i in dbr.get_players(dbr.get_game(last_chat_id)):
            print( last_chat_id, i, dbr.get_nickname(last_chat_id))
            if last_chat_id != i:
                greet_bot.send_message(i, 'К игре подключился: ' + dbr.get_nickname(last_chat_id))

        markup = types.ReplyKeyboardMarkup()
        markup.row('пригласить')
        markup.row('покинуть')
        greet_bot.send_message(last_chat_id, "Меню игры", reply_markup=markup)
    else:
        greet_bot.send_message(last_chat_id, 'Ты не можешь этого сделать, т.к. находишься в другой игре. Доиграй или покинь её')

@greet_bot.message_handler(commands=['start'])        # start menu
def handle_start(message):
    last_chat_id = str(message.chat.id)
    print(last_chat_id)
    print(str(message.chat.username))
    print(dbr.registration(last_chat_id, '@' + str(message.chat.username)))
    greet_bot.send_message(message.chat.id, 'Если ты первый раз, жми /help')
    markup = types.ReplyKeyboardMarkup()
    markup.row('создать игру')
    greet_bot.send_message(message.chat.id, "выбирай", reply_markup=markup)

@greet_bot.message_handler(func = lambda query: query.text == 'создать игру')      # create game
def handle_start(message):
    last_chat_id = str(message.chat.id)
    if dbr.get_players_condition(last_chat_id != 'playing'): # what target?
        name_of_game = config.make_game()
        print(dbr.create_game(name_of_game))
        print(dbr.change_games_condition(name_of_game, 'wait'))
        print(dbr.join_game(last_chat_id, name_of_game))
        print(dbr.change_players_condition(last_chat_id, 'playing'))
        #print(type(last_chat_id))
        markup = types.ReplyKeyboardMarkup()
        markup.row('начать')
        markup.row('пригласить')
        markup.row('покинуть')
        greet_bot.send_message(last_chat_id, 'Отлично твоя игра создана, её уникальный номер: ' + name_of_game)
        greet_bot.send_message(last_chat_id, "Меню игры", reply_markup=markup)
    else:
        greet_bot.send_message(last_chat_id, 'Ты не можешь этого сделать, т.к. находишься в другой игре. Доиграй или покинь её')

@greet_bot.message_handler(func = lambda query: query.text == 'покинуть')      # leave game
def handle_start(message):
    last_chat_id = str(message.chat.id)
    if dbr.get_players_condition(last_chat_id) == 'playing':

        if dbr.get_games_condition(dbr.get_game(last_chat_id).upper()) == 'wait':
            dbr.change_players_condition(last_chat_id, 'free')
            dbr.leave_game(last_chat_id)
            greet_bot.send_message(last_chat_id, 'Ты покинул игру')

        elif dbr.get_games_condition(dbr.get_game(last_chat_id).upper()) == 'going':
            dbr.change_players_condition(last_chat_id, 'free')
            dbr.set_target_to_user(dbr.get_user_killer(last_chat_id), dbr.get_user_target(last_chat_id))
            dbr.set_target_to_user(last_chat_id, '')
            dbr.leave_game(last_chat_id)
            greet_bot.send_message(last_chat_id, 'Ты покинул игру')

        markup = types.ReplyKeyboardMarkup()
        markup.row('создать игру')
        greet_bot.send_message(message.chat.id, "выбирай", reply_markup=markup)

    else:
        greet_bot.send_message(last_chat_id, 'Ты не можешь этого сделать, т.к. не играешь')

@greet_bot.message_handler(func = lambda query: query.text == 'пригласить')      # leave game
def handle_start(message):
    last_chat_id = str(message.chat.id)
    if dbr.get_players_condition(last_chat_id) == 'playing':
        greet_bot.send_message(last_chat_id, 'перешли приглашение своим друзьям')
        greet_bot.send_message(last_chat_id, '/join ' + dbr.get_game(last_chat_id))
    else:
        greet_bot.send_message(last_chat_id, 'Ты не можешь этого сделать, т.к. не находишься в лобби')

@greet_bot.message_handler(func = lambda query: query.text == 'начать')      # start game
def handle_start(message):
    last_chat_id = str(message.chat.id)
    if dbr.get_games_condition(dbr.get_game(last_chat_id).upper()) == 'wait':
        if len(dbr.get_players(dbr.get_game(last_chat_id))) > 2:

            config.get_victim(dbr.get_players(dbr.get_game(last_chat_id)))
            dbr.change_games_condition(dbr.get_game(last_chat_id), 'going')
            for i in dbr.get_players(dbr.get_game(last_chat_id)):
                greet_bot.send_message(i, 'Игра начинается! Вот твоя жертва: ' + dbr.get_nickname(dbr.get_user_target(i)))
                markup = types.ReplyKeyboardMarkup()
                markup.row('покинуть')
                greet_bot.send_message(i, "Удачи!", reply_markup=markup)
                greet_bot.send_message(i, 'А этот код отдай своему убийце, если конечно тебя убили!')
                code = config.make_game()
                dbr.set_user_identifier(i, code) # just generate a symbols
                greet_bot.send_message(i, code)
        else:
            greet_bot.send_message(last_chat_id, 'Ты не можешь этого сделать, слишком мало игроков!')

    else:
        greet_bot.send_message(last_chat_id, 'Ты не можешь этого сделать, игра уже началась!')

@greet_bot.message_handler(commands=['kill'])      # join game
def handle_start(message):
    last_chat_id = str(message.chat.id)
    if dbr.get_games_condition(dbr.get_game(last_chat_id).upper()) == 'going':
        code = message.text.split()[-1].upper()
        print(code, dbr.get_user_identifier(dbr.get_user_target(last_chat_id)).upper())
        print(dbr.get_user_target(last_chat_id))
        if dbr.get_user_identifier(dbr.get_user_target(last_chat_id)).upper() == code:
            died = dbr.get_user_target(last_chat_id)
            print(dbr.get_nickname(died))
            dbr.count_kill(last_chat_id)

            dbr.set_target_to_user(last_chat_id, dbr.get_user_target(died))

            print(dbr.get_user_killer(last_chat_id), dbr.get_user_target(last_chat_id))
            if dbr.get_user_target(dbr.get_user_killer(last_chat_id) == dbr.get_user_target(last_chat_id)):

                if (dbr.get_amount_kills(last_chat_id) > dbr.get_amount_kills(dbr.get_user_target(died))):
                    winner(last_chat_id)
                    kill(dbr.get_user_killer(last_chat_id))
                    kill(died)

                if (dbr.get_amount_kills(last_chat_id) == dbr.get_amount_kills(dbr.get_user_target(died))):
                    winner(last_chat_id)
                    winner(dbr.get_user_killer(last_chat_id))
                    kill(died)

                if (dbr.get_amount_kills(last_chat_id) < dbr.get_amount_kills(died)):
                    winner(dbr.get_user_killer(last_chat_id))
                    kill(last_chat_id)
                    kill(died)
            else:
                greet_bot.send_message(last_chat_id, 'Отлично! Ты убил очередную жертву, вот тебе следущая: ' + dbr.get_nickname(dbr.get_user_target(died))) # plus +1 kill
                # print(dbr.set_target_to_user(died, ''))
                # print(dbr.set_user_identifier(died, ''))
                # print(dbr.change_players_condition(died, 'free'))
                kill(died)
        else:
            greet_bot.send_message(last_chat_id, 'Неверный код, проверь ещё раз')
    else:
        greet_bot.send_message(last_chat_id, 'Ты не можешь этого сейчас сделать')

@greet_bot.message_handler(commands=['help'])      # join game
def handle_start(message):
    last_chat_id = str(message.chat.id)
    greet_bot.send_message(last_chat_id, 'Вот тебе правила!')
    greet_bot.send_message(last_chat_id, config.rules)
    greet_bot.send_message(last_chat_id, config.end_game)





if __name__ == '__main__':
     greet_bot.polling(none_stop=True)





# {'content_type': 'text', 'message_id': 2324, 'from_user': {'id': 380302100, 'is_bot': False, 'first_name': 'Jonathan', 'username': 'Longa_Bonga', 'last_name': '⚡️', 'language_code': 'ru'}, 'date': 1557783972, 'chat': {'type': 'private', 'last_name': '⚡️', 'first_name': 'Jonathan', 'username': 'Longa_Bonga', 'id': 380302100, 'title': None, 'all_members_are_administrators': None, 'photo': None, 'description': None, 'invite_link': None, 'pinned_message': None, 'sticker_set_name': None, 'can_set_sticker_set': None}, 'forward_from_chat': None, 'forward_from': {'id': 602833219, 'is_bot': True, 'first_name': 'ФENIX', 'username': 'AmberCWbot', 'last_name': None, 'language_code': None}, 'forward_date': 1557778172, 'reply_to_message': None, 'edit_date': None, 'media_group_id': None, 'author_signature': None, 'text': '⚔️🍁 ФД!\n🛡🍁 ФД!\nТактика: /tactics_oplot\n\nГотовим свои зелья и свои булки для разворотов!', 'entities': [<telebot.types.MessageEntity object at 0x104d0ad30>], 'caption_entities': None, 'audio': None, 'document': None, 'photo': None, 'sticker': None, 'video': None, 'video_note': None, 'voice': None, 'caption': None, 'contact': None, 'location': None, 'venue': None, 'new_chat_member': None, 'new_chat_members': None, 'left_chat_member': None, 'new_chat_title': None, 'new_chat_photo': None, 'delete_chat_photo': None, 'group_chat_created': None, 'supergroup_chat_created': None, 'channel_chat_created': None, 'migrate_to_chat_id': None, 'migrate_from_chat_id': None, 'pinned_message': None, 'invoice': None, 'successful_payment': None, 'connected_website': None, 'json': {'message_id': 2324, 'from': {'id': 380302100, 'is_bot': False, 'first_name': 'Jonathan', 'last_name': '⚡️', 'username': 'Longa_Bonga', 'language_code': 'ru'}, 'chat': {'id': 380302100, 'first_name': 'Jonathan', 'last_name': '⚡️', 'username': 'Longa_Bonga', 'type': 'private'}, 'date': 1557783972, 'forward_from': {'id': 602833219, 'is_bot': True, 'first_name': 'ФENIX', 'username': 'AmberCWbot'}, 'forward_date': 1557778172, 'text': '⚔️🍁 ФД!\n🛡🍁 ФД!\nТактика: /tactics_oplot\n\nГотовим свои зелья и свои булки для разворотов!', 'entities': [{'offset': 27, 'length': 14, 'type': 'bot_command'}]}}

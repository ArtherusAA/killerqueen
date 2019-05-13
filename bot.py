# -*- coding: utf-8 -*-
import config
import telebot
import requests
import datetime
import random
import dbrequests as dbr
from telebot import types

greet_bot = telebot.TeleBot(config.token)

@greet_bot.message_handler(commands=['join'])      # join game
def handle_start(message):
    last_chat_id = str(message.chat.id)
    if (message.from_user.username != message.chat.username):
        game = message.text.split()
        print(game)
        game = game[len(game) - 1]
        print(game)
        if dbr.get_players_condition(last_chat_id != 'playing') and dbr.get_games_condition(game) == 'wait':
            greet_bot.send_message(last_chat_id, 'Отлично сейчас я добавлю тебя в лобби: ' + game)
            dbr.join_game(last_chat_id, game)
            dbr.change_players_condition(last_chat_id, 'playing')
            markup = types.ReplyKeyboardMarkup()
            markup.row('начать')
            markup.row('пригласить')
            markup.row('покинуть')
            greet_bot.send_message(last_chat_id, "Меню игры", reply_markup=markup)
        else:
            greet_bot.send_message(last_chat_id, 'Ты не можешь этого сделать, т.к. находишься в другой игре. Доиграй или покинь её')
    else:
            greet_bot.send_message(last_chat_id, 'Ты переслал его сам себе!')

@greet_bot.message_handler(commands=['start'])        # start menu
def handle_start(message):
    last_chat_id = str(message.chat.id)
    print(last_chat_id)
    print(str(message.chat.username))
    print(dbr.registration(last_chat_id, '@' + str(message.chat.username)))
    greet_bot.send_message(message.chat.id, 'тут будут праила игры')
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
        markup.row('присоединиться к игре')
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
    if dbr.get_games_condition(dbr.get_game(str(last_chat_id)).upper()) == 'wait':
        get_victim(dbr.get_players(dbr.get_game(last_chat_id)))
        dbr.change_games_condition(dbr.get_game(last_chat_id), 'going')
        for i in dbr.get_players(dbr.get_game(last_chat_id)):
            print(i)
            greet_bot.send_message(i, 'Игра начинается! Вот твоя жертва: ' + dbr.get_nickname(dbr.get_user_target(i)))
            greet_bot.send_message(i, 'А этот код отдай своему убийце, если конечно тебя убили!')
            code = make_game()
            dbr.set_user_identifier(i, code) # just generate a symbols
            greet_bot.send_message(i, code)


if __name__ == '__main__':
     greet_bot.polling(none_stop=True)





# {'content_type': 'text', 'message_id': 2324, 'from_user': {'id': 380302100, 'is_bot': False, 'first_name': 'Jonathan', 'username': 'Longa_Bonga', 'last_name': '⚡️', 'language_code': 'ru'}, 'date': 1557783972, 'chat': {'type': 'private', 'last_name': '⚡️', 'first_name': 'Jonathan', 'username': 'Longa_Bonga', 'id': 380302100, 'title': None, 'all_members_are_administrators': None, 'photo': None, 'description': None, 'invite_link': None, 'pinned_message': None, 'sticker_set_name': None, 'can_set_sticker_set': None}, 'forward_from_chat': None, 'forward_from': {'id': 602833219, 'is_bot': True, 'first_name': 'ФENIX', 'username': 'AmberCWbot', 'last_name': None, 'language_code': None}, 'forward_date': 1557778172, 'reply_to_message': None, 'edit_date': None, 'media_group_id': None, 'author_signature': None, 'text': '⚔️🍁 ФД!\n🛡🍁 ФД!\nТактика: /tactics_oplot\n\nГотовим свои зелья и свои булки для разворотов!', 'entities': [<telebot.types.MessageEntity object at 0x104d0ad30>], 'caption_entities': None, 'audio': None, 'document': None, 'photo': None, 'sticker': None, 'video': None, 'video_note': None, 'voice': None, 'caption': None, 'contact': None, 'location': None, 'venue': None, 'new_chat_member': None, 'new_chat_members': None, 'left_chat_member': None, 'new_chat_title': None, 'new_chat_photo': None, 'delete_chat_photo': None, 'group_chat_created': None, 'supergroup_chat_created': None, 'channel_chat_created': None, 'migrate_to_chat_id': None, 'migrate_from_chat_id': None, 'pinned_message': None, 'invoice': None, 'successful_payment': None, 'connected_website': None, 'json': {'message_id': 2324, 'from': {'id': 380302100, 'is_bot': False, 'first_name': 'Jonathan', 'last_name': '⚡️', 'username': 'Longa_Bonga', 'language_code': 'ru'}, 'chat': {'id': 380302100, 'first_name': 'Jonathan', 'last_name': '⚡️', 'username': 'Longa_Bonga', 'type': 'private'}, 'date': 1557783972, 'forward_from': {'id': 602833219, 'is_bot': True, 'first_name': 'ФENIX', 'username': 'AmberCWbot'}, 'forward_date': 1557778172, 'text': '⚔️🍁 ФД!\n🛡🍁 ФД!\nТактика: /tactics_oplot\n\nГотовим свои зелья и свои булки для разворотов!', 'entities': [{'offset': 27, 'length': 14, 'type': 'bot_command'}]}}

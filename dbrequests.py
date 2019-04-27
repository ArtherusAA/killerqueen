import json
import requests


url = 'http://127.0.0.1:8000/bot_request/'


def get_players(game):
    params = {
        'action': 'get_players',
        'game': game,
    }
    users = json.loads(requests.post(url, params))
    if users['error'] == 'ok':
        players = []
        for key in users.keys():
            if key[:4] == 'user':
                players.append(users[key])
        return players
    return users['error']

def get_game(user):
    params = {
        'action': 'get_game',
        'user': user,
    }
    game = json.loads(requests.post(url, params))
    if game['error'] == 'ok':
        return game['game']
    return game['error']

def join_game(user, game, target, user_identifier, condition, nickname):
    params = {
        'action': 'join_game',
        'user': user,
        'game': game,
        'target': target,
        'user_identifier': user_identifier,
        'condition': condition,
        'nickname': nickname,
    }
    response = requests.post(url, params)
    return response.status_code

def create_game(game, condition, winner):
    params = {
        'action': 'create_game',
        'game': game,
        'condition': condition,
        'winner': winner,
    }
    response = requests.post(url, params)
    return response.status_code

def remove_player_from_game(game, user):
    params = {
        'action': 'remove_player_from_game',
        'game': game,
        'user': user,
    }
    response = requests.post(url, params)
    return response.status_code

def set_target_to_user(user, target):
    params = {
        'action': 'set_target_to_user',
        'user': user,
        'target': target,
    }
    response = requests.post(url, params)
    return response.status_code

def get_user_target(user):
    params = {
        'action': 'get_user_target',
        'user': user,
    }
    target = json.loads(requests.post(url, params).content.decode('utf-8'))
    if target['error'] == 'ok':
        return target['target']
    return target['error']

def registration(user, nickname):
    params = {
        'action': 'registration',
        'user': user,
        'nickname': nickname,
    }
    response = requests.post(url, params)
    return response.status_code

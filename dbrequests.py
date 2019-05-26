import json
import requests


url = 'http://127.0.0.1:1488/bot_request/'


def get_players(game):
    params = {
        'action': 'get_players',
        'game': game,
    }
    users = json.loads(requests.post(url, params).content.decode('utf-8'))
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
    game = json.loads(requests.post(url, params).content.decode('utf-8'))
    if game['error'] == 'ok':
        return game['game']
    return game['error']


def join_game(user, game):
    params = {
        'action': 'join_game',
        'user': user,
        'game': game,
    }
    response = requests.post(url, params)
    return response.status_code


def create_game(game):
    params = {
        'action': 'create_game',
        'game': game,
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


def leave_game(user):
    params = {
        'action': 'leave_game',
        'user': user,
    }
    response = requests.post(url, params)
    return response.status_code


def establish_winner(user, game):
    params = {
        'action': 'establish_winner',
        'user': user,
        'game': game
    }
    response = requests.post(url, params)
    return response.status_code


def change_games_condition(game, condition):
    params = {
        'action': 'change_games_condition',
        'game': game,
        'condition': condition,
    }
    response = requests.post(url, params)
    return response.status_code


def get_games_condition(game):
    params = {
        'action': 'get_games_condition',
        'game': game,
    }
    condition = json.loads(requests.post(url, params).content.decode('utf-8'))
    if condition['error'] == 'ok':
        return condition['condition']
    return condition['error']


def change_players_condition(user, condition):
    params = {
        'action': 'change_players_condition',
        'user': user,
        'condition': condition,
    }
    response = requests.post(url, params)
    return response.status_code


def get_players_condition(user):
    params = {
        'action': 'get_players_condition',
        'user': user,
    }
    condition = json.loads(requests.post(url, params).content.decode('utf-8'))
    if condition['error'] == 'ok':
        return condition['condition']
    return condition['error']


def get_user_killer(user):
    params = {
        'action': 'get_user_killer',
        'user': user,
    }
    response = json.loads(requests.post(url, params).content.decode('utf-8'))
    if response['error'] == 'ok':
        return response['killer']
    return response['error']


def get_nickname(user):
    params = {
        'action': 'get_nickname',
        'user': user,
    }
    response = json.loads(requests.post(url, params).content.decode('utf-8'))
    if response['error'] == 'ok':
        return response['nickname']
    return response['error']


def set_user_identifier(user, user_identifier):
    params = {
        'action': 'set_user_identifier',
        'user': user,
        'user_identifier': user_identifier,
    }
    response = requests.post(url, params)
    return response.status_code


def get_user_identifier(user):
    params = {
        'action': 'get_user_identifier',
        'user': user,
    }
    response = json.loads(requests.post(url, params).content.decode('utf-8'))
    if response['error'] == 'ok':
        return response['user_identifier']
    return response['error']


def count_kill(user):
    params = {
        'action': 'count_kill',
        'user': user,
    }
    response = requests.post(url, params)
    return response.status_code


def get_amount_kills(user):
    params = {
        'action': 'get_amount_kills',
        'user': user,
    }
    response = json.loads(requests.post(url, params).content.decode('utf-8'))
    if response['error'] == 'ok':
        return response['kills']
    return response['error']


def count_wins(user):
    params = {
        'action': 'count_wins',
        'user': user,
    }
    response = requests.post(url, params)
    return response.status_code


def get_amount_wins(user):
    params = {
        'action': 'get_amount_wins',
        'user': user,
    }
    response = json.loads(requests.post(url, params).content.decode('utf-8'))
    if response['error'] == 'ok':
        return response['wins']
    return response['error']

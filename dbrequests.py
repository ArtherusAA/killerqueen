import requests

url = 'http://127.0.0.1:8000/bot_request/'

class GameDB:

    '''def __init__(self):
        self.connection = None
        self.cursor = None

    def establish_connection(self, db_file):
        try:
            self.connection = sqlite3.connect(db_file)
            self.cursor = self.connection.cursor()
            return True
        except ValueError:
            return False

    def close_connection(self):
        try:
            self.connection.close()
            return True
        except ValueError:
            return False'''

    def get_players(self, game):
        params = {
            'action': 'get_players',
            'game': game,
        }
        users = requests.post(url, params).data
        return users

    def get_game(self, user):
        params = {
            'action': 'get_game',
            'user': user,
        }
        game = requests.post(url, params).data
        return game

    def join_game(self, user, game, target, user_identifier, condition, nickname):
        params = {
            'action': 'join_game',
            'user': user,
            'game': game,
            'target': target,
            'user_identifier': user_identifier,
            'condition': condition,
            'nickname': nickname,
        }
        return requests.post(url, params).data

    def create_game(self, game, condition, winner = None):
        params = {
            'action': 'create_game',
            'game': game,
            'condition': condition,
            'winner': winner,
        }
        return requests.post(url, params).data

    def remove_player_from_game(self, game, user):
        params = {
            'action': 'remove_player_from_game',
            'game': game,
            'user': user,
        }
        return requests.post(url, params).data

    def set_target_to_user(self, user, target):
        params = {
            'action': 'set_target_to_user',
            'user': user,
            'target': target,
        }
        return requests.post(url, params).data

    def get_user_target(self, user):
        params = {
            'action': 'get_user_target',
            'user': user,
        }
        target = requests.post(url, params).data
        return target

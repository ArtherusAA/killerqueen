from django.test import TestCase, Client
import json

class BotRequestTest(TestCase):

    # registration()
    def test_correct_registration(self):
        client = Client()
        params = {
            'action': 'registration',
            'user': 'artem1',
            'nickname': '@sobaka1'
        }
        response = client.post('/bot_request/', params)
        self.assertEqual(response.status_code, 200)

    def test_incorrect_registration_nickname(self):
        client = Client()
        params = {
            'action': 'registration',
            'user': 'artem2',
            'nickname': 'sobaka2'
        }
        response = client.post('/bot_request/', params)
        self.assertEqual(response.status_code, 228)

    def test_registration_without_user(self):
        client = Client()
        params = {
            'action': 'registration',
            'user': '',
            'nickname': '@sobaka3'
        }
        response = client.post('/bot_request/', params)
        self.assertEqual(response.status_code, 401)

    def test_registration_without_nickname(self):
        client = Client()
        params = {
            'action': 'registration',
            'user': 'artem4',
            'nickname': ''
        }
        response = client.post('/bot_request/', params)
        self.assertEqual(response.status_code, 402)

    def test_incorrect_nickname(self):
        client = Client()
        params = {
            'action': 'registration',
            'user': 'artem5',
            'nickname': '@'
        }
        response = client.post('/bot_request/', params)
        self.assertEqual(response.status_code, 403)

    def test_repeated_registration(self):
        client = Client()
        params = {
            'action': 'registration',
            'user': 'artem228',
            'nickname': '@sobaka1488'
        }
        response = client.post('/bot_request/', params)
        self.assertEqual(response.status_code, 200)
        params = {
            'action': 'registration',
            'user': 'artem228',
            'nickname': '@sobaka1488'
        }
        response = client.post('/bot_request/', params)
        self.assertEqual(response.status_code, 400)

    # create_game()
    def test_correct_creating_game(self):
        client = Client()
        params = {
            'action': 'create_game',
            'game': 'game1',
        }
        response = client.post('/bot_request/', params)
        self.assertEqual(response.status_code, 200)

    def test_repeated_creating_game(self):
        client = Client()
        params = {
            'action': 'create_game',
            'game': 'game1',
        }
        response = client.post('/bot_request/', params)
        self.assertEqual(response.status_code, 400)

    def test_creating_game_without_game(self):
        client = Client()
        params = {
            'action': 'create_game',
            'game': '',
        }
        response = client.post('/bot_request/', params)
        self.assertEqual(response.status_code, 401)

    # join_game()
    def test_correct_joining_game(self):
        client = Client()
        params = {
            'action': 'join_game',
            'user': 'artem1',
            'game': 'game1',
        }
        response = client.post('/bot_request/', params)
        self.assertEqual(response.status_code, 200)

    def test_joining_game_with_nonexistent_user(self):
        client = Client()
        params = {
            'action': 'join_game',
            'user': 'artur',
            'game': 'game1',
        }
        response = client.post('/bot_request/', params)
        self.assertEqual(response.status_code, 400)

    def test_joining_to_nonexistent_game(self):
        client = Client()
        params = {
            'action': 'registration',
            'user': 'artem6',
            'nickname': '@sobaka6'
        }
        response = client.post('/bot_request/', params)
        self.assertEqual(response.status_code, 200)
        params = {
            'action': 'join_game',
            'user': 'artem6',
            'game': 'game228',
        }
        response = client.post('/bot_request/', params)
        self.assertEqual(response.status_code, 403)

    def test_join_game_while_playing(self):
        client = Client()
        params = {
            'action': 'create_game',
            'game': 'game3',
        }
        response = client.post('/bot_request/', params)
        self.assertEqual(response.status_code, 200)
        params = {
            'action': 'join_game',
            'user': 'artem1',
            'game': 'game3',
        }
        response = client.post('/bot_request/', params)
        self.assertEqual(response.status_code, 401)

    # get_game()
    def test_get_correct_game(self):
        client = Client()
        params = {
            'action': 'get_game',
            'user': 'artem1',
        }
        response = json.loads(client.post('/bot_request/', params).content.decode('utf-8'))
        self.assertEqual(response['error'], 'ok')
        self.assertEqual(response['game'], 'game1')

    def test_get_nonexistent_user_game(self):
        client = Client()
        params = {
            'action': 'get_game',
            'user': 'omg',
        }
        response = json.loads(client.post('/bot_request/', params).content.decode('utf-8'))
        self.assertEqual(response['error'], 'no_such_user')

    # get_players()

    def test_correct_get_players(self):
        client = Client()
        params = {
            'action': 'create_game',
            'game': 'gameTest',
        }
        response = client.post('/bot_request/', params)
        self.assertEqual(response.status_code, 200)
        for i in range(3):
            user = 'art' + str(i)
            params = {
                'action': 'registration',
                'user': user,
                'nickname': '@dog' + str(i),
            }
            response = client.post('/bot_request/', params)
            self.assertEqual(response.status_code, 200)
            params = {
                'action': 'join_game',
                'user': user,
                'game': 'gameTest',
            }
            response = client.post('/bot_request/', params)
            self.assertEqual(response.status_code, 200)
        params = {
            'action': 'get_players',
            'game': 'gameTest',
        }
        users = json.loads(client.post('/bot_request/', params).content.decode('utf-8'))
        self.assertEqual(users['error'], 'ok')
        players = []
        for key in users.keys():
            if key[:4] == 'user':
                players.append(users[key])
        players.sort()
        self.assertEqual(players, ['art0', 'art1', 'art2'])

from django.test import TestCase, Client

Url = 'http://127.0.0.1:8000/bot_request/'

class BotRequestTest(TestCase):

    # registration()
    def test_correct_registration(self):
        client = Client()
        params = {
            'action': 'registration',
            'user': 'artem1',
            'nickname': '@sobaka1'
        }
        response = client.post(Url, params)
        self.assertEqual(response.status_code, 200)

    def test_incorrect_registration_nickname(self):
        client = Client()
        params = {
            'action': 'registration',
            'user': 'artem2',
            'nickname': 'sobaka2'
        }
        response = client.post(Url, params)
        self.assertEqual(response.status_code, 403)

    def test_registration_without_user(self):
        client = Client()
        params = {
            'action': 'registration',
            'user': '',
            'nickname': '@sobaka3'
        }
        response = client.post(Url, params)
        self.assertEqual(response.status_code, 403)

    def test_registration_without_nickname(self):
        client = Client()
        params = {
            'action': 'registration',
            'user': 'artem4',
            'nickname': ''
        }
        response = client.post(Url, params)
        self.assertEqual(response.status_code, 403)

    def test_incorrect_nickname(self):
        client = Client()
        params = {
            'action': 'registration',
            'user': 'artem5',
            'nickname': '@'
        }
        response = client.post(Url, params)
        self.assertEqual(response.status_code, 403)

    def test_repeated_registration(self):
        client = Client()
        params = {
            'action': 'registration',
            'user': 'artem1',
            'nickname': '@sobaka1'
        }
        response = client.post(Url, params)
        self.assertEqual(response.status_code, 400)

    # create_game()
    def test_correct_creating_game(self):
        client = Client()
        params = {
            'action': 'create_game',
            'game': 'game1',
        }
        response = client.post(Url, params)
        self.assertEqual(response.status_code, 200)

    def test_repeated_creating_game(self):
        client = Client()
        params = {
            'action': 'create_game',
            'game': 'game1',
        }
        response = client.post(Url, params)
        self.assertEqual(response.status_code, 400)

    def test_creating_game_without_game(self):
        client = Client()
        params = {
            'action': 'create_game',
            'game': '',
        }
        response = client.post(Url, params)
        self.assertEqual(response.status_code, 403)

    # join_game()
    def test_correct_joining_game(self):
        client = Client()
        params = {
            'action': 'join_game',
            'user': 'artem1',
            'game': 'game1',
        }
        response = client.post(Url, params)
        self.assertEqual(response.status_code, 200)

    def test_joining_game_with_nonexistent_user(self):
        client = Client()
        params = {
            'action': 'join_game',
            'user': 'artur',
            'game': 'game1',
        }
        response = client.post(Url, params)
        self.assertEqual(response.status_code, 400)

    def test_joining_to_nonexistent_game(self):
        client = Client()
        params = {
            'action': 'registration',
            'user': 'artem6',
            'nickname': '@sobaka6'
        }
        response = client.post(Url, params)
        self.assertEqual(response.status_code, 200)
        params = {
            'action': 'join_game',
            'user': 'artem6',
            'game': 'game228',
        }
        response = client.post(Url, params)
        self.assertEqual(response.status_code, 403)

    def test_join_game_while_playing(self):
        client = Client()
        params = {
            'action': 'create_game',
            'game': 'game3',
        }
        response = client.post(Url, params)
        self.assertEqual(response.status_code, 200)
        params = {
            'action': 'join_game',
            'user': 'artem1',
            'game': 'game3',
        }
        response = client.post(Url, params)
        self.assertEqual(response.status_code, 401)

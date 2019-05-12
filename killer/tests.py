import json
from django.test import TestCase, Client

class BotRequestTest(TestCase):

    def setup_registration(self, user, nickname):
        client = Client()
        params = {
            'action': 'registration',
            'user': user,
            'nickname': nickname,
        }
        response = client.post('/bot_request/', params)
        return response

    def setup_create_game(self, game):
        client = Client()
        params = {
            'action': 'create_game',
            'game': game,
        }
        response = client.post('/bot_request/', params)
        return response

    def setup_join_game(self, user, game):
        client = Client()
        params = {
            'action': 'join_game',
            'user': user,
            'game': game,
        }
        response = client.post('/bot_request/', params)
        return response

    def setup_get_game(self, user):
        client = Client()
        params = {
            'action': 'get_game',
            'user': user,
        }
        response = json.loads(client.post('/bot_request/', params).content.decode('utf-8'))
        return response

    def setup_get_players(self, game):
        client = Client()
        params = {
            'action': 'get_players',
            'game': game,
        }
        users = json.loads(client.post('/bot_request/', params).content.decode('utf-8'))
        return users

    def setup_leave_game(self, user):
        client = Client()
        params = {
            'action': 'leave_game',
            'user': user,
        }
        response = client.post('/bot_request/', params)
        return response

    def setup_establish_winner(self, user, game):
        client = Client()
        params = {
            'action': 'establish_winner',
            'user': user,
            'game': game,
        }
        response = client.post('/bot_request/', params)
        return response

    def setup_set_target_to_user(self, user, target):
        client = Client()
        params = {
            'action': 'set_target_to_user',
            'user': user,
            'target': target,
        }
        response = client.post('/bot_request/', params)
        return response

    # registration()
    def test_correct_registration(self):
        response = self.setup_registration('artem1', '@sobaka1')
        self.assertEqual(response.status_code, 200)

    def test_incorrect_registration_nickname(self):
        response = self.setup_registration('artem2', 'sobaka2')
        self.assertEqual(response.status_code, 228)

    def test_registration_without_user(self):
        response = self.setup_registration('', '@sobaka3')
        self.assertEqual(response.status_code, 401)

    def test_registration_without_nickname(self):
        response = self.setup_registration('artem4', '')
        self.assertEqual(response.status_code, 402)

    def test_incorrect_nickname(self):
        response = self.setup_registration('artem5', '@')
        self.assertEqual(response.status_code, 228)

    def test_repeated_registration(self):
        response = self.setup_registration('artem228', '@sobaka1488')
        self.assertEqual(response.status_code, 200)
        response = self.setup_registration('artem228', '@sobaka1488')
        self.assertEqual(response.status_code, 400)

    # create_game()
    def test_correct_creating_game(self):
        response = self.setup_create_game('game1')
        self.assertEqual(response.status_code, 200)

    def test_repeated_creating_game(self):
        response = self.setup_create_game('aaa')
        self.assertEqual(response.status_code, 200)
        response = self.setup_create_game('aaa')
        self.assertEqual(response.status_code, 400)

    def test_creating_game_without_game(self):
        response = self.setup_create_game('')
        self.assertEqual(response.status_code, 401)

    # join_game()
    def test_correct_joining_game(self):
        response = self.setup_registration('artem10', '@sobaka10')
        self.assertEqual(response.status_code, 200)
        response = self.setup_create_game('game10')
        self.assertEqual(response.status_code, 200)
        response = self.setup_join_game('artem10', 'game10')
        self.assertEqual(response.status_code, 200)

    def test_joining_game_with_nonexistent_user(self):
        response = self.setup_join_game('artur', 'game1')
        self.assertEqual(response.status_code, 400)

    def test_joining_to_nonexistent_game(self):
        response = self.setup_registration('artem6', '@sobaka6')
        self.assertEqual(response.status_code, 200)
        response = self.setup_join_game('artem6', 'game228')
        self.assertEqual(response.status_code, 402)

    def test_join_game_while_playing(self):
        response = self.setup_registration('artem8', '@sobaka8')
        self.assertEqual(response.status_code, 200)
        response = self.setup_create_game('game3')
        self.assertEqual(response.status_code, 200)
        response = self.setup_create_game('game8')
        self.assertEqual(response.status_code, 200)
        response = self.setup_join_game('artem8', 'game3')
        self.assertEqual(response.status_code, 200)
        response = self.setup_join_game('artem8', 'game8')
        self.assertEqual(response.status_code, 401)

    # get_game()
    def test_get_correct_game(self):
        response = self.setup_registration('artem9', '@sobaka9')
        self.assertEqual(response.status_code, 200)
        response = self.setup_create_game('game9')
        self.assertEqual(response.status_code, 200)
        response = self.setup_join_game('artem9', 'game9')
        self.assertEqual(response.status_code, 200)
        response = self.setup_get_game('artem9')
        self.assertEqual(response['error'], 'ok')
        self.assertEqual(response['game'], 'game9')

    def test_get_nonexistent_user_game(self):
        response = self.setup_get_game('omg')
        self.assertEqual(response['error'], 'no_such_user')

    def test_get_game_nonPlaying_user(self):
        response = self.setup_registration('artem11', '@sobaka11')
        self.assertEqual(response.status_code, 200)
        response = self.setup_get_game('artem11')
        self.assertEqual(response['error'], 'no_such_game')

    # get_players()

    def test_correct_get_players(self):
        response = self.setup_create_game('gameTest')
        self.assertEqual(response.status_code, 200)
        for i in range(3):
            user = 'art' + str(i)
            response = self.setup_registration(user, '@dog' + str(i))
            self.assertEqual(response.status_code, 200)
            response = self.setup_join_game(user, 'gameTest')
            self.assertEqual(response.status_code, 200)
        users = self.setup_get_players('gameTest')
        self.assertEqual(users['error'], 'ok')
        players = []
        for key in users.keys():
            if key[:4] == 'user':
                players.append(users[key])
        players.sort()
        self.assertEqual(players, ['art0', 'art1', 'art2'])

    def test_get_no_players(self):
        response = self.setup_create_game('gameTest1')
        self.assertEqual(response.status_code, 200)
        response = self.setup_get_players('gameTest1')
        self.assertEqual(response['error'], 'no_such_users')

    def test_get_players_nonexistent_game(self):
        response = self.setup_get_players('gameTest2')
        self.assertEqual(response['error'], 'no_such_game')

    #leave_game()
    def test_correct_leave_game(self):
        response = self.setup_registration('artem12', '@sobaka12')
        self.assertEqual(response.status_code, 200)
        response = self.setup_create_game('gameTest3')
        self.assertEqual(response.status_code, 200)
        response = self.setup_join_game('artem12', 'gameTest3')
        self.assertEqual(response.status_code, 200)
        response = self.setup_leave_game('artem12')
        self.assertEqual(response.status_code, 200)

    def test_leave_game_nonexistant_user(self):
        response = self.setup_leave_game('artem13')
        self.assertEqual(response.status_code, 400)

    def test_leave_nonexistant_game(self):
        response = self.setup_registration('artem14', '@sobaka14')
        self.assertEqual(response.status_code, 200)
        response = self.setup_leave_game('artem14')
        self.assertEqual(response.status_code, 403)

    #establish_winner()
    def test_correct_establish_winner(self):
        response = self.setup_registration('artem15', '@sobaka15')
        self.assertEqual(response.status_code, 200)
        response = self.setup_create_game('gameTest4')
        self.assertEqual(response.status_code, 200)
        response = self.setup_join_game('artem15', 'gameTest4')
        self.assertEqual(response.status_code, 200)
        response = self.setup_establish_winner('artem15', 'gameTest4')
        self.assertEqual(response.status_code, 200)

    def test_establish_winner_nonexitant_game(self):
        response = self.setup_registration('artem16', '@sobaka16')
        self.assertEqual(response.status_code, 200)
        response = self.setup_establish_winner('artem16', 'gameTest5')
        self.assertEqual(response.status_code, 400)

    def test_establish_winner_nonPlaying_user(self):
        response = self.setup_registration('artem17', '@sobaka17')
        self.assertEqual(response.status_code, 200)
        response = self.setup_create_game('gameTest6')
        self.assertEqual(response.status_code, 200)
        response = self.setup_establish_winner('artem17', 'gameTest6')
        self.assertEqual(response.status_code, 403)

    def test_establish_winner_nonexitant_user(self):
        response = self.setup_create_game('gameTest7')
        self.assertEqual(response.status_code, 200)
        response = self.setup_establish_winner('artem18', 'gameTest7')
        self.assertEqual(response.status_code, 403)

    #set_target_to_user()
    def test_set_correct_target_to_user(self):
        response = self.setup_registration('artem19', '@sobaka19')
        self.assertEqual(response.status_code, 200)
        response = self.setup_registration('artem20', '@sobaka20')
        self.assertEqual(response.status_code, 200)
        response = self.setup_create_game('gameTest8')
        self.assertEqual(response.status_code, 200)
        response = self.setup_join_game('artem19', 'gameTest8')
        self.assertEqual(response.status_code, 200)
        response = self.setup_join_game('artem20', 'gameTest8')
        self.assertEqual(response.status_code, 200)
        response = self.setup_set_target_to_user('artem19', 'artem20')
        self.assertEqual(response.status_code, 200)
        response = self.setup_set_target_to_user('artem20', 'artem19')
        self.assertEqual(response.status_code, 200)

    def test_set_target_to_nonexitant_user(self):
        response = self.setup_registration('artem21', '@sobaka21')
        self.assertEqual(response.status_code, 200)
        response = self.setup_create_game('gameTest9')
        self.assertEqual(response.status_code, 200)
        response = self.setup_join_game('artem21', 'gameTest9')
        self.assertEqual(response.status_code, 200)
        response = self.setup_set_target_to_user('archy228', 'artem21')
        self.assertEqual(response.status_code, 400)

    def test_set_nonexitant_target_to_user(self):
        response = self.setup_registration('artem22', '@sobaka22')
        self.assertEqual(response.status_code, 200)
        response = self.setup_create_game('gameTest10')
        self.assertEqual(response.status_code, 200)
        response = self.setup_join_game('artem22', 'gameTest10')
        self.assertEqual(response.status_code, 200)
        response = self.setup_set_target_to_user('artem22', 'archy228')
        self.assertEqual(response.status_code, 403)

    def test_set_outsider_target_to_user(self):
        response = self.setup_registration('artem23', '@sobaka23')
        self.assertEqual(response.status_code, 200)
        response = self.setup_registration('artem24', '@sobaka24')
        self.assertEqual(response.status_code, 200)
        response = self.setup_create_game('gameTest11')
        self.assertEqual(response.status_code, 200)
        response = self.setup_create_game('gameTest12')
        self.assertEqual(response.status_code, 200)
        response = self.setup_join_game('artem23', 'gameTest11')
        self.assertEqual(response.status_code, 200)
        response = self.setup_join_game('artem24', 'gameTest12')
        self.assertEqual(response.status_code, 200)
        response = self.setup_set_target_to_user('artem23', 'archy24')
        self.assertEqual(response.status_code, 403)
        response = self.setup_set_target_to_user('artem24', 'archy23')
        self.assertEqual(response.status_code, 403)

    def test_set_target_to_nonPlaying_user(self):
        response = self.setup_registration('artem25', '@sobaka25')
        self.assertEqual(response.status_code, 200)
        response = self.setup_registration('artem26', '@sobaka26')
        self.assertEqual(response.status_code, 200)
        response = self.setup_create_game('gameTest13')
        self.assertEqual(response.status_code, 200)
        response = self.setup_join_game('artem26', 'gameTest13')
        self.assertEqual(response.status_code, 200)
        response = self.setup_set_target_to_user('artem25', 'archy26')
        self.assertEqual(response.status_code, 403)

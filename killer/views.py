from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from killer.models import GameModel, User
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def bot_request(request):
    if request.method == 'POST':
        print(request.POST)
        if 'action' in request.POST.keys():
            print(request.POST['action'])
            if request.POST['action'] == 'create_game':
                requirements = ['game']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    games_with_same_id = GameModel.objects.all().filter(game=request.POST['game'])
                    if len(games_with_same_id) > 0:
                        return HttpResponse(status=400)
                    if request.POST['game'] == '':
                        return HttpResponse(status=401)
                    game = GameModel(game=request.POST['game'], condition='',
                                     winner='')
                    game.save()
                    return HttpResponse(status=200)
            elif request.POST['action'] == 'get_game':
                requirements = ['user']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    user = User.objects.all().filter(user=request.POST['user'])
                    if len(user) == 0:
                        return JsonResponse({'error': 'no_such_user'})
                    return JsonResponse({'error': 'ok', 'game': user[0].game})
            elif request.POST['action'] == 'join_game':
                requirements = ['game', 'user']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    player = User.objects.all().filter(user=request.POST['user'])
                    if len(player) == 0:
                        return HttpResponse(status=400)
                    if player[0].game != '':
                        return HttpResponse(status=401)
                    User.objects.all().filter(user=request.POST['user']).update(
                                                                    game=request.POST['game'],
                                                                    target='',
                                                                    user_identifier='',
                                                                    condition='')
                    return HttpResponse(status=200)
            elif request.POST['action'] == 'get_players':
                requirements = ['game']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    users = User.objects.all().filter(game=request.POST['game'])
                    if len(users) == 0:
                        return JsonResponse({'error': 'no_such_users'})
                    response = {'error': 'ok'}
                    for i in range(len(users)):
                        response['user' + str(i)] = users[i].user
                    return JsonResponse(response)
            elif request.POST['action'] == 'remove_player_from_game':
                requirements = ['game', 'user']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    player = User.objects.all().filter(user=request.POST['user'])
                    if len(player) == 0:
                        return HttpResponse(status=400)
                    if player[0]['game'] != request.POST['game']:
                        return HttpResponse(401)
                    User.objects.all().filter(user=request.POST['user']).update(game='')
                    return HttpResponse(status=200)
            elif request.POST['action'] == 'set_target_to_user':
                requirements = ['target', 'user']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    player = User.objects.all().filter(user=request.POST['user'])
                    if len(player) == 0:
                        return HttpResponse(status=400)
                    User.objects.all().filter(user=request.POST['user']).update(target=request.POST['target'])
                    return HttpResponse(status=200)
            elif request.POST['action'] == 'get_user_target':
                requirements = ['user']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    user = User.objects.all().filter(user=request.POST['user'])
                    if len(user) == 0:
                        return JsonResponse({'error': 'no_such_user'})
                    return JsonResponse({'error': 'ok', 'target': user[0].target})
            elif request.POST['action'] == 'registration':
                print(22847)
                requirements = ['user', 'nickname']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    print(22847)
                    user = User.objects.all().filter(user=request.POST['user'])
                    print(22847)
                    if len(user) > 0:
                        return HttpResponse(status=400)
                    user = User(user=request.POST['user'], nickname=request.POST['nickname'], game='', target='',
                                user_identifier='', condition='')
                    user.save()
                    return HttpResponse(status=200)
            elif request.POST['action'] == 'leave_game':
                requirements = ['user']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    player = User.objects.all().filter(user=request.POST['user'])
                    if len(player) == 0:
                        return HttpResponse(status=400)
                    User.objects.all().filter(user=request.POST['user']).update(game='')
                    return HttpResponse(status=200)
            elif request.POST['action'] == 'establish_winner':
                requirements = ['user', 'game']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    game = GameModel.objects.all().filter(user=request.POST['game'])
                    if len(game) == 0:
                        return HttpResponse(status=400)
                    GameModel.objects.all().filter(game=request.POST['game']).update(winner=request.POST['user'])
                    return HttpResponse(status=200)
            elif request.POST['action'] == 'change_games_condition':
                requirements = ['condition', 'game']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    game = GameModel.objects.all().filter(user=request.POST['game'])
                    if len(game) == 0:
                        return HttpResponse(status=400)
                    GameModel.objects.all().filter(game=request.POST['game']).update(
                        condition=request.POST['condition'])
                    return HttpResponse(status=200)
            elif request.POST['action'] == 'get_games_condition':
                requirements = ['game']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    game = GameModel.objects.all().filter(game=request.POST['game'])
                    if len(game) == 0:
                        return JsonResponse({'error': 'no_such_game'})
                    return JsonResponse({'error': 'ok', 'condition': game[0].condition})
            elif request.POST['action'] == 'get_players_condition':
                requirements = ['user']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    user = User.objects.all().filter(game=request.POST['user'])
                    if len(user) == 0:
                        return JsonResponse({'error': 'no_such_user'})
                    return JsonResponse({'error': 'ok', 'condition': user[0].condition})
            elif request.POST['action'] == 'change_players_condition':
                requirements = ['condition', 'user']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    user = User.objects.all().filter(user=request.POST['game'])
                    if len(user) == 0:
                        return HttpResponse(status=400)
                    User.objects.all().filter(game=request.POST['game']).update(
                        condition=request.POST['condition'])
                    return HttpResponse(status=200)
    return HttpResponse(status=403)

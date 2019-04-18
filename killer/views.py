from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from killer.models import GameModel, User


def bot_request(request):
    if request.method == 'POST':
        if 'action' in request.POST.keys():
            if request.POST['action'] == 'create_game':
                requirements = ['game', 'condition', 'winner']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    games_with_same_id = GameModel.objects.get(game=request.POST['game'])
                    if len(games_with_same_id) > 0:
                        return HttpResponse(status=400)
                    game = GameModel(game=request.POST['game'], condition=request.POST['condition'],
                                     winner=request.POST['winner'])
                    game.save()
                    return HttpResponse(status=200)
            elif request.POST['action'] == 'get_game':
                requirements = ['user']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    user = User.objects.get(request.POST['user'])
                    if len(user) == 0:
                        return JsonResponse({'error': 'no_such_user'})
                    return JsonResponse({'error': 'ok', 'game': user[0]['game']})
            elif request.POST['action'] == 'join_game':
                requirements = ['game', 'user', 'target', 'user_identifier', 'condition', 'nickname']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    player = User.objects.get(user=request.POST['user'])
                    if len(player) == 0:
                        return HttpResponse(status=400)
                    if player[0]['game'] != '':
                        return HttpResponse(401)
                    User.objects.all().filter(user=request.POST['user']).update(
                                                                    game=request.POST['game'],
                                                                    target=request.POST['target'],
                                                                    user_identifier=request.POST['user_identifier'],
                                                                    condition=request.POST['condition'],
                                                                    nickname=request.POST['nickname'])
                    return HttpResponse(status=200)
            elif request.POST['action'] == 'get_players':
                requirements = ['game']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    users = User.objects.get(request.POST['game'])
                    if len(users) == 0:
                        return JsonResponse({'error': 'no_such_users'})
                    response = {'error': 'ok'}
                    for i in range(len(users)):
                        response['user' + str(i)] = users[i]['user']
                    return JsonResponse(response)
            elif request.POST['action'] == 'remove_player_from_game':
                requirements = ['game', 'user']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    player = User.objects.get(user=request.POST['user'])
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
                    player = User.objects.get(user=request.POST['user'])
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
                    user = User.objects.get(request.POST['user'])
                    if len(user) == 0:
                        return JsonResponse({'error': 'no_such_user'})
                    return JsonResponse({'error': 'ok', 'target': user[0]['target']})
    return HttpResponse(status=403)

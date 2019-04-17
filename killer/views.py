from django.shortcuts import render
from django.http import HttpResponse
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
                pass
            elif request.POST['action'] == 'join_game':
                pass
            elif request.POST['action'] == 'get_players':
                pass
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
                pass
            elif request.POST['action'] == 'get_user_target':
                pass
    return HttpResponse(status=403)

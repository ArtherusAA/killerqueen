from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from killer.models import GameModel, User
from django.views.decorators.csrf import csrf_exempt


"""
Imports
"""
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from killer.models import GameModel, User
from killer.forms import AddForm, ChangeKillsForm, ChangeWinsForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
import killer.data_base_control as dbc
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required(login_url='/login')
def exit(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/login')
def input_error(request):
    """
    Error-view
    """
    return render(request, "inputerror.html")


def score(request):
    """
    Score-view
    """
    context = {}
    users = User.objects.all()
    current_user = request.user
    context['username'] = current_user
    context['users'] = users
    return render(request, "scoreboard.html", context)


@user_passes_test(lambda u: u.is_superuser)
def change_kills(request):
    """
    change_kills-view
    """
    kills_form = ChangeKillsForm(request.POST)
    if kills_form.is_valid():
        name = kills_form.cleaned_data['name']
        kills = kills_form.cleaned_data['kills']
        if not kills.isdecimal():
            return redirect('input_error')
        dbc.set_kills(name, kills)
    return redirect('admin')


@user_passes_test(lambda u: u.is_superuser)
def change_wins(request):
    """
    change_wins-view
    """
    wins_form = ChangeWinsForm(request.POST)
    if wins_form.is_valid():
        name = wins_form.cleaned_data['name']
        wins = wins_form.cleaned_data['wins']
        if not wins.isdecimal():
            return redirect('input_error')
        dbc.set_wins(name, wins)
    return redirect('admin')


@user_passes_test(lambda u: u.is_superuser)
def add_user(request):
    """
    add_user-view
    """
    add_form = AddForm(request.POST)
    if add_form.is_valid():
        name = add_form.cleaned_data['name']
        dbc.add_user(name)
    return redirect('admin')


@user_passes_test(lambda u: u.is_superuser)
def score_admin(request):
    """
    control-view
    """
    context = {}
    users = User.objects.all()
    context['users'] = users
    add_form = AddForm
    kills_form = ChangeKillsForm
    wins_form = ChangeWinsForm
    context['add_form'] = add_form
    context['kills_form'] = kills_form
    context['wins_form'] = wins_form
    current_user = request.user
    context['username'] = current_user
    return render(request, "score_admin.html", context)



@csrf_exempt
def bot_request(request):
    if request.method == 'POST':
        if 'action' in request.POST.keys():
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
                    game = GameModel.objects.all().filter(game=request.POST['game'])
                    if len(player) == 0:
                        return HttpResponse(status=400)
                    if player[0].game != '':
                        return HttpResponse(status=401)
                    if len(game) == 0:
                        return HttpResponse(status=402)
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
                    User.objects.all().filter(user=request.POST['user']).update(game='', target='', condition='')
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
                requirements = ['user', 'nickname']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    user = User.objects.all().filter(user=request.POST['user'])
                    if len(user) > 0:
                        return HttpResponse(status=400)
                    if request.POST['user'] == '':
                        return HttpResponse(status=401)
                    if request.POST['nickname'] == '':
                        return HttpResponse(status=402)
                    checker_for_nickname = True
                    if len(request.POST['nickname']) < 2:
                        checker_for_nickname = False
                    if request.POST['nickname'][0] != '@':
                        checker_for_nickname = False
                    for i in range(1, len(request.POST['nickname'])):
                        if not (ord('a') <= ord(request.POST['nickname'][i]) <= ord('z') or
                                ord('A') <= ord(request.POST['nickname'][i]) <= ord('Z') or
                                ord('0') <= ord(request.POST['nickname'][i]) <= ord('9') or
                                ord(request.POST['nickname'][i]) == ord('_')):
                            checker_for_nickname = False
                    if not checker_for_nickname:
                        return HttpResponse(status=228)
                    user = User(user=request.POST['user'], nickname=request.POST['nickname'], game='', target='',
                                user_identifier='', condition='', kills=0)
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
                    User.objects.all().filter(user=request.POST['user']).update(game='', target='', condition='')
                    return HttpResponse(status=200)
            elif request.POST['action'] == 'establish_winner':
                requirements = ['user', 'game']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    game = GameModel.objects.all().filter(game=request.POST['game'])
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
                    game = GameModel.objects.all().filter(game=request.POST['game'])
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
                    user = User.objects.all().filter(user=request.POST['user'])
                    if len(user) == 0:
                        return JsonResponse({'error': 'no_such_user'})
                    return JsonResponse({'error': 'ok', 'condition': user[0].condition})
            elif request.POST['action'] == 'change_players_condition':
                requirements = ['condition', 'user']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    user = User.objects.all().filter(user=request.POST['user'])
                    if len(user) == 0:
                        return HttpResponse(status=400)
                    User.objects.all().filter(user=request.POST['user']).update(
                        condition=request.POST['condition'])
                    return HttpResponse(status=200)
            elif request.POST['action'] == 'get_user_killer':
                requirements = ['user']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    user = User.objects.all().filter(target=request.POST['user'])
                    user1 = User.objects.all().filter(user=request.POST['user'])
                    if len(user1) == 0:
                        return JsonResponse({'error': 'no_such_user'})
                    if len(user) == 0:
                        return JsonResponse({'error': 'no_such_killer'})
                    return JsonResponse({'error': 'ok', 'killer': user[0].user})
            elif request.POST['action'] == 'get_nickname':
                requirements = ['user']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    user = User.objects.all().filter(user=request.POST['user'])
                    if len(user) == 0:
                        return JsonResponse({'error': 'no_such_user'})
                    return JsonResponse({'error': 'ok', 'nickname': user[0].nickname})
            elif request.POST['action'] == 'get_user_identifier':
                requirements = ['user']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    user = User.objects.all().filter(user=request.POST['user'])
                    if len(user) == 0:
                        return JsonResponse({'error': 'no_such_user'})
                    return JsonResponse({'error': 'ok', 'user_identifier': user[0].user_identifier})
            elif request.POST['action'] == 'set_user_identifier':
                requirements = ['user_identifier', 'user']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    user = User.objects.all().filter(user=request.POST['user'])
                    if len(user) == 0:
                        return HttpResponse(status=400)
                    User.objects.all().filter(user=request.POST['user']).update(
                        user_identifier=request.POST['user_identifier'])
                    return HttpResponse(status=200)
            elif request.POST['action'] == 'count_kill':
                requirements = ['user']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    user = User.objects.all().filter(user=request.POST['user'])
                    if len(user) == 0:
                        return HttpResponse(status=400)
                    new_kills = user[0].kills + 1
                    User.objects.all().filter(user=request.POST['user']).update(
                        kills=new_kills)
                    return HttpResponse(status=200)
            elif request.POST['action'] == 'get_amount_kills':
                requirements = ['user']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    user = User.objects.all().filter(user=request.POST['user'])
                    if len(user) == 0:
                        return JsonResponse({'error': 'no_such_user'})
                    return JsonResponse({'error': 'ok', 'kills': str(user[0].kills)})
            elif request.POST['action'] == 'count_wins':
                requirements = ['user']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    user = User.objects.all().filter(user=request.POST['user'])
                    if len(user) == 0:
                        return HttpResponse(status=400)
                    new_wins = user[0].wins + 1
                    User.objects.all().filter(user=request.POST['user']).update(
                        kills=new_wins)
                    return HttpResponse(status=200)
            elif request.POST['action'] == 'get_amount_wins':
                requirements = ['user']
                checker = True
                for req in requirements:
                    checker = (checker and req in request.POST.keys())
                if checker:
                    user = User.objects.all().filter(user=request.POST['user'])
                    if len(user) == 0:
                        return JsonResponse({'error': 'no_such_user'})
                    return JsonResponse({'error': 'ok', 'wins': str(user[0].wins)})
    return HttpResponse(status=403)

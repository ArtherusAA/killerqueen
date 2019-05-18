"""
Imports
"""
from django.shortcuts import render
from django.shortcuts import redirect
from killer.models import User
from killer.forms import AddForm, ChangeKillsForm, ChangeWinsForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
import killer.data_base_control as dbc


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


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
    context['users'] = users
    return render(request, "scoreboard.html", context)


@login_required(login_url='/login')
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


@login_required(login_url='/login')
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


@login_required(login_url='/login')
def add_user(request):
    """
    add_user-view
    """
    add_form = AddForm(request.POST)
    if add_form.is_valid():
        name = add_form.cleaned_data['name']
        dbc.add_user(name)
    return redirect('admin')


@login_required(login_url='/login')
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
    return render(request, "score_admin.html", context)

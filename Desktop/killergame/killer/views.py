from django.shortcuts import render
import killer.DataBaseControl as dbc
from killer.models import User
from killer.forms import *
from django.shortcuts import redirect
import sqlite3


def score(request):
    context = {}
    users = User.objects.all()
    context['users'] = users
    return render(request, "scoreboard.html", context)


def change_kills(request):
    killsform = ChangeKillsForm(request.POST)
    if killsform.is_valid():
        name = killsform.cleaned_data['name']
        kills = killsform.cleaned_data['kills']
        dbc.set_kills(name, kills)
    return redirect('admin')


def change_wins(request):
    winsform = ChangeWinsForm(request.POST)
    if winsform.is_valid():
        name = winsform.cleaned_data['name']
        wins = winsform.cleaned_data['wins']
        dbc.set_wins(name, wins)
    return redirect('admin')


def add_user(request):
    addform = AddForm(request.POST)
    if addform.is_valid():
        name = addform.cleaned_data['name']
        dbc.add_user(name)
    return redirect('admin')


def score_admin(request):
    context = {}
    users = User.objects.all()
    context['users'] = users
    addform = AddForm
    killsform = ChangeKillsForm
    winsform = ChangeWinsForm
    context['add_form'] = addform
    context['kills_form'] = killsform
    context['wins_form'] = winsform
    return render(request, "score_admin.html", context)

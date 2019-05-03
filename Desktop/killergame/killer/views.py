from django.shortcuts import render
from killer.DataBaseControl import Control as dbc
from killer.models import User
from killer.forms import AddForm
import sqlite3
# Create your views here.

def score(request):
    context = {}
    users = User.objects.all()
    context['users'] = users
    return render(request, "scoreboard.html", context)
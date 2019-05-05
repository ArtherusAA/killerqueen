from django.db import models
from killer.models import User
from django import db
import sqlite3


def add_user(name):
    user = User(name=name, kills=0, wins=0)
    user.save()


def set_kills(name, kills):
    user = User.objects.get(name=name)
    user.kills = kills
    user.save(False, True)


def set_wins(name, wins):
    print(name, wins)
    user = User.objects.get(name=name)
    user.wins = wins
    user.save(False, True)

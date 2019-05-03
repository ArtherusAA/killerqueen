from django.db import models
from killer.models import User
from django import db
import sqlite3


class Control:
    def add_user(name):
        user = User(name=name, kills=0, wins=0)
        user.save()


    def set_kills(name, kills):
        user = Entry.objects.filter(name=name)
        user.kills = kills
        user.save()


    def set_wins(name, wins):
        user = Entry.objects.filter(name=name)
        user.wins = wins
        user.save()

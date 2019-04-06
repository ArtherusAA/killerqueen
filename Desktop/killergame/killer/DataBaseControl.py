from django.db import models
from killer.models import User


def add_user(name):
    user = User(name=name, kills=0, wins=0)
    user.save(using='ScoreBoard')


def set_kills(name):
    user = User(name=name, kills=0, wins=0)
    user.save(using='ScoreBoard')


def set_wins(name):
    user = User(name=name, kills=0, wins=0)
    user.save(using='ScoreBoard')


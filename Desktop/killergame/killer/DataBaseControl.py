from django.db import models
from killer.models import User


def add_user(name):
    user = User(name=name, kills=0, wins=0)
    user.save(using='ScoreBoard')


def set_kills(name, kills):
    user = User(name=name, kills=kills, wins=0)
    user.save(using='ScoreBoard')


def set_wins(name, wins):
    user = User(name=name, kills=0, wins=wins)
    user.save(using='ScoreBoard')


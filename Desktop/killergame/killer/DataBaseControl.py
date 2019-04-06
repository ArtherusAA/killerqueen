from django.db import models
from killer.models import User


def add_user(name):
    user = User(name=name, score=0)
    user.save(using='ScoreBoard')


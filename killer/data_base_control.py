"""
User-model
"""
from killer.models import User


def add_user(name):
    """
    User-adding function
    """
    if not User.objects.filter(name=name):
        user = User(name=name, kills=0, wins=0)
        user.save()


def set_kills(name, kills):
    """
    Setting kills
    """
    user = User.objects.filter(name=name)
    if user.exists():
        user = User.objects.get(name=name)
        user.kills = kills
        user.save(False, True)


def set_wins(name, wins):
    """
    Setting wins
    """
    user = User.objects.filter(name=name)
    if user.exists():
        user = User.objects.get(name=name)
        user.wins = wins
        user.save(False, True)

"""
User-model
"""
from killer.models import User


def add_user(name):
    """
    User-adding function
    """
    if not User.objects.filter(nickname=name):
        user = User(user=name, nickname='@'+name, kills=0)
        user.save()


def set_kills(name, kills):
    """
    Setting kills
    """
    user = User.objects.filter(nickname=name)
    if user.exists():
        user = User.objects.get(nickname=name)
        user.kills = kills
        user.save(False, True)


def set_wins(name, wins):
    """
    Setting wins
    """
    user = User.objects.filter(nickname=name)
    if user.exists():
        user = User.objects.get(nickname=name)
        user.wins = wins
        user.save(False, True)

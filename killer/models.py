"""
standart django models
"""
from django.db import models


class GameModel(models.Model):
    """
    model of game
    """
    game = models.CharField(max_length=1024)
    condition = models.CharField(max_length=1024)
    winner = models.CharField(max_length=1024)


class User(models.Model):
    """
    player model
    """
    user = models.CharField(max_length=1024)
    game = models.CharField(max_length=1024)
    target = models.CharField(max_length=1024)
    user_identifier = models.CharField(max_length=1024)
    condition = models.CharField(max_length=1024)
    nickname = models.CharField(max_length=1024)
    kills = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)

    class Meta:
        ordering = ['-kills']

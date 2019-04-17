from django.db import models


class GameModel(models.Model):
    game = models.CharField()
    condition = models.IntegerField()
    winner = models.CharField()


class User(models.Model):
    user = models.CharField()
    game = models.CharField()
    target = models.CharField()
    user_identifier = models.CharField()
    condition = models.CharField()
    nickname = models.CharField()

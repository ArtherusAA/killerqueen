from django.db import models


class User(models.Model):
    name = models.CharField(max_length=21)
    kills = models.IntegerField()
    wins = models.IntegerField()

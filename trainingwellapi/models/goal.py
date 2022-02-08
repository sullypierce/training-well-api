from django.db import models
from .account import Account

class Goal(models.Model):

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    goal_achieved = models.BooleanField()
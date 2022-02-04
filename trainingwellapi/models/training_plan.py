from django.db import models
from .account import Account

class TrainingPlan(models.Model):

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
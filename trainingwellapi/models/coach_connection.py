from tkinter import CASCADE
from django.db import models
from .account import Account


class CoachConnection(models.Model):

    trainee = models.ForeignKey(Account, on_delete=models.CASCADE)
    coach = models.ForeignKey(Account, related_name="coach", on_delete=models.CASCADE)
    is_coaching_request = models.BooleanField(default=True)
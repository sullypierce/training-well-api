from django.db import models

from .exercise import Exercise
from .account import Account

class Benchmark(models.Model):


    notes = models.CharField(max_length=100)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    reps = models.CharField(max_length=50)
    weight = models.CharField(max_length=50)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    date = models.DateField()
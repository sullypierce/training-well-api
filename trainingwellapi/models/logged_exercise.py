from django.db import models
from .session import Session
from .exercise import Exercise

class LoggedExercise(models.Model):

    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    notes = models.CharField(max_length=250)
    completed = models.BooleanField()
    sets = models.IntegerField(null = True)
    reps = models.IntegerField(null = True)
    weight_used = models.IntegerField(null=True)
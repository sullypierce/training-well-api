from django.db import models

from .exercise_type import ExerciseType

class Exercise(models.Model):

    name = models.CharField(max_length=15)
    description = models.CharField(max_length=50)
    exercise_type = models.ForeignKey(ExerciseType, on_delete=models.CASCADE)
    url = models.CharField(max_length=50)
from django.db import models


class ExerciseType(models.Model):

    name = models.CharField(max_length=31)
    
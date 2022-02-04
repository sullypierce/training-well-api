from django.db import models
from .training_plan import TrainingPlan

class Goal(models.Model):

    training_plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    goal_achieved = models.BooleanField()
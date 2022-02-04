from django.db import models
from .training_plan import TrainingPlan

class Session(models.Model):

    training_plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE)
    assigned_date = models.DateField()
    time_completed = models.TimeField(null=True)
    notes = models.CharField(max_length=250)
    sleep_hours = models.IntegerField(null=True)
    energy_level = models.IntegerField(null=True)
    quality = models.IntegerField(null=True)
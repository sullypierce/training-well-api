from django.db import models
from .training_plan import TrainingPlan
from .account import Account

class Session(models.Model):

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    assigned_date = models.DateField()
    time_completed = models.TimeField(null=True)
    notes = models.CharField(max_length=250)
    sleep_hours = models.IntegerField(null=True)
    energy_level = models.IntegerField(null=True)
    quality = models.IntegerField(null=True)
    
    @property
    def next_scheduled(self):
        return self.__next_scheduled

    @next_scheduled.setter
    def next_scheduled(self, value):
        self.__next_scheduled = value
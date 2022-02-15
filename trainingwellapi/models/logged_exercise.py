from django.db import models
from django.db.models import F
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
    order = models.IntegerField(default=1)
    
    def move(self, exercise, new_order):
        
        qs = self.get_queryset()
        
        if exercise.order > int(new_order):
            qs.filter(
                session = exercise.session,
                order__lt = exercise.order,
                order__gte= new_order
            ).exclude(
                pk= exercise.pk
            ).update(
                order = F('order') + 1
            )
        else: 
            qs.filter(
                session = exercise.session,
                order__lte = new_order,
                order__gt= exercise.order
            ).exclude(
                pk= exercise.pk
            ).update(
                order = F('order') - 1
            )
        
        exercise.order = new_order
        exercise.save()
from django.db import models, transaction
from django.db.models import F

class LoggedExerciseManager(models.Manager):
    
    
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
"""trainingwell URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from trainingwellapi.views import register_user, login_user, ExerciseTypes, Exercises, Benchmarks, TrainingPlans, Goals, Sessions, LoggedExercises, CoachConnections, Coachs





router = routers.DefaultRouter(trailing_slash=False)
router.register(r'exercisetypes', ExerciseTypes, 'exercise_type')
router.register(r'exercises', Exercises, 'exercise')
router.register(r'benchmarks', Benchmarks, 'benchmark')
router.register(r'trainingplans', TrainingPlans, 'training_plan')
router.register(r'goals', Goals, 'goal')
router.register(r'sessions', Sessions, 'session')
router.register(r'loggedexercises', LoggedExercises, 'logged_exercise')
router.register(r'coachconnections', CoachConnections, 'coach_connection')
router.register(r'coachs', Coachs, 'coachs')


urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]

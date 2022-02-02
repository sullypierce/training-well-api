"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from trainingwellapi.models import ExerciseType


class ExerciseTypes(ViewSet):
    """Level up exercise types"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single exercise type

        Returns:
            Response -- JSON serialized exercise type
        """
        try:
            exercise_type = ExerciseType.objects.get(pk=pk)
            serializer = ExerciseTypeSerializer(exercise_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all exercise types

        Returns:
            Response -- JSON serialized list of exercise types
        """
        exercise_types = ExerciseType.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = ExerciseTypeSerializer(
            exercise_types, many=True, context={'request': request})
        return Response(serializer.data)
    
class ExerciseTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for exercise types

    Arguments:
        serializers
    """
    class Meta:
        model = ExerciseType
        fields = ('id', 'name')
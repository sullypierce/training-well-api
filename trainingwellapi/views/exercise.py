"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from trainingwellapi.models import Exercise, ExerciseType
from django.db.models import Count


class Exercises(ViewSet):
  

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized exercise instance
        """


        # Create a new Python instance of the exercise class
        # and set its properties from what was sent in the
        # body of the request from the client.
        exercise = Exercise()
        exercise.name = request.data["name"]
        exercise.description = request.data["description"]
        exercise.url = request.data["url"]

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `exerciseTypeId` in the body of the request.
        exercisetype = ExerciseType.objects.get(pk=request.data["exercise_type_id"])
        exercise.exercise_type = exercisetype

        # Try to save the new exercise to the database, then
        # serialize the exercise instance as JSON, and send the
        # JSON as a response to the client request
        try:
            exercise.save()
            serializer = ExerciseSerializer(exercise, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single exercise

        Returns:
            Response -- JSON serialized exercise instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/exercises/2
            #
            # The `2` at the end of the route becomes `pk`
            exercise = Exercise.objects.get(pk=pk)
            serializer = ExerciseSerializer(exercise, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a exercise

        Returns:
            Response -- Empty body with 204 status code
        """

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of exercise, get the exercise record
        # from the database whose primary key is `pk`
        exercise = Exercise.objects.get(pk=pk)
        exercise.name = request.data["name"]
        exercise.description = request.data["description"]
        exercise.url = request.data["url"]

        
        exercisetype = ExerciseType.objects.get(pk=request.data["exercise_type_id"])
        exercise.exercise_type = exercisetype
        exercise.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single exercise

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            exercise = Exercise.objects.get(pk=pk)
            exercise.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except exercise.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to exercises resource

        Returns:
            Response -- JSON serialized list of exercises
        """
        
        #get all exercises but add an event_count field
        exercises = Exercise.objects.all().order_by('name')

        

        serializer = ExerciseSerializer(
            exercises, many=True, context={'request': request})
        return Response(serializer.data)
    
class ExerciseSerializer(serializers.ModelSerializer):
    """JSON serializer for exercises

    Arguments:
        serializer type
    """
    class Meta:
        model = Exercise
        fields = ('id', 'description', 'name', 'exercise_type', 'url')
        depth = 1
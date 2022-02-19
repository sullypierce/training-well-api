"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from trainingwellapi.models import LoggedExercise, Exercise, Session
from django.db.models import Count



class LoggedExercises(ViewSet):
  

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized logged_exercise instance
        """

        # Create a new Python instance of the logged_exercise class
        # and set its properties from what was sent in the
        # body of the request from the client.
        logged_exercise = LoggedExercise()
        exercise = Exercise.objects.get(id=request.data['exercise_id'])
        session = Session.objects.get(id=request.data['session_id'])
        
        #find the order of the last exercise for this session and put the new exercise last in order
        exercises = LoggedExercise.objects.filter(session = session).order_by('order')
        try:
            last_exercise = exercises[len(exercises)-1]
            logged_exercise.order = last_exercise.order+1
        except ValueError:
            logged_exercise.order = 1 
        
        logged_exercise.notes = request.data["notes"]
        logged_exercise.completed = request.data["completed"]
        logged_exercise.reps = request.data["reps"]
        logged_exercise.sets = request.data["sets"]
        logged_exercise.weight_used = request.data["weight_used"]
        logged_exercise.exercise = exercise
        logged_exercise.session = session
        
        
        
        # Try to save the new logged_exercise to the database, then
        # serialize the logged_exercise instance as JSON, and send the
        # JSON as a response to the client request
        try:
            logged_exercise.save()
            serializer = LoggedExerciseSerializer(logged_exercise, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single logged_exercise

        Returns:
            Response -- JSON serialized logged_exercise instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/logged_exercises/2
            #
            # The `2` at the end of the route becomes `pk`
            logged_exercise = LoggedExercise.objects.get(pk=pk)
            serializer = LoggedExerciseSerializer(logged_exercise, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a logged_exercise

        Returns:
            Response -- Empty body with 204 status code
        """
        logged_exercise = LoggedExercise.objects.get(pk=pk)
        
        move_spot = request.query_params.get('move')
        if move_spot:
            LoggedExercise.objects.move(logged_exercise, move_spot)
        # Do mostly the same thing as POST, but instead of
        # creating a new instance of logged_exercise, get the logged_exercise record
        # from the database whose primary key is `pk`
        # Create a new Python instance of the logged_exercise class
        # and set its properties from what was sent in the
        # body of the request from the client.
        else:
            logged_exercise.notes = request.data["notes"]
            logged_exercise.completed = request.data["completed"]
            logged_exercise.reps = request.data["reps"]
            logged_exercise.sets = request.data["sets"]
            logged_exercise.weight_used = request.data["weight_used"]
            logged_exercise.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single logged_exercise

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            logged_exercise = LoggedExercise.objects.get(pk=pk)
            logged_exercise.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except logged_exercise.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to logged_exercises resource

        Returns:
            Response -- JSON serialized list of logged_exercises
        """
        #if frontend sends session id query send back only matching exercises: 
        # this will be used for getting the logged_exercises for a particular session
        session_id = request.query_params.get('session_id')
        if session_id:
            logged_exercises = LoggedExercise.objects.filter(session_id=session_id).order_by('order')
            serializer = LoggedExerciseSerializer(
            logged_exercises, many=True, context={'request': request})
            return Response(serializer.data)
        else:
        #get all logged_exercises if it is 
            logged_exercises = LoggedExercise.objects.all()
            serializer = LoggedExerciseSerializer(
                logged_exercises, many=True, context={'request': request})
            return Response(serializer.data)
    
class LoggedExerciseSerializer(serializers.ModelSerializer):
    """JSON serializer for logged_exercises

    Arguments:
        serializer type
    """
    class Meta:
        model = LoggedExercise
        fields = ('id', 'exercise', 'completed', 'reps', 'sets', 'session', 'notes', 'weight_used', 'order')
        depth = 1
        
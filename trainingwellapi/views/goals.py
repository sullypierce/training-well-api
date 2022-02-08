"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from trainingwellapi.models import Account, Goal
from django.db.models import Count


class Goals(ViewSet):
  

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized goal instance
        """

        # Create a new Python instance of the goal class
        # and set its properties from what was sent in the
        # body of the request from the client.
        goal = Goal()
        account = Account.objects.get(user=request.auth.user) 
        goal.account = account
        goal.description = request.data["description"]
        goal.goal_achieved = request.data["goal_achieved"]
        
        
        # Try to save the new goal to the database, then
        # serialize the goal instance as JSON, and send the
        # JSON as a response to the client request
        try:
            goal.save()
            serializer = GoalSerializer(goal, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single goal

        Returns:
            Response -- JSON serialized goal instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/goals/2
            #
            # The `2` at the end of the route becomes `pk`
            goal = Goal.objects.get(pk=pk)
            serializer = GoalSerializer(goal, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a goal

        Returns:
            Response -- Empty body with 204 status code
        """

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of goal, get the goal record
        # from the database whose primary key is `pk`
        goal = Goal.objects.get(pk=pk)
        # Create a new Python instance of the goal class
        # and set its properties from what was sent in the
        # body of the request from the client.
        
        goal.description = request.data["description"]
        goal.goal_achieved = request.data["goal_achieved"]
        goal.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single goal

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            goal = Goal.objects.get(pk=pk)
            goal.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except goal.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to goals resource

        Returns:
            Response -- JSON serialized list of goals
        """
        
        #get all goals but add an event_count field
        goals = Goal.objects.all()

        

        serializer = GoalSerializer(
            goals, many=True, context={'request': request})
        return Response(serializer.data)
    
class GoalSerializer(serializers.ModelSerializer):
    """JSON serializer for goals

    Arguments:
        serializer type
    """
    class Meta:
        model = Goal
        fields = ('id', 'description', 'goal_achieved', 'training_plan')
        depth = 1
        
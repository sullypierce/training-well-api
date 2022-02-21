"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from trainingwellapi.models import Account
from django.db.models import Count


class Coachs(ViewSet):
  

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized goal instance
        """

        # Create a new Python instance of the goal class
        # and set its properties from what was sent in the
        # body of the request from the client.
        
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
            coach = Account.objects.get(pk=pk)
            serializer = AccountSerializer(coach, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def list(self, request):
        """Handle GET requests to goals resource

        Returns:
            Response -- JSON serialized list of goals
        """
        
        #get all goals but add an event_count field
        goals = Account.objects.filter(is_coach=True)

        

        serializer = AccountSerializer(
            goals, many=True, context={'request': request})
        return Response(serializer.data)
    
class AccountSerializer(serializers.ModelSerializer):
    """JSON serializer for Accounts

    Arguments:
        serializer type
    """
    class Meta:
        model = Account
        fields = ('id', 'user')
        depth = 1
        
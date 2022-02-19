"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from trainingwellapi.models import Account, CoachConnection


class CoachConnections(ViewSet):
  

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized benchmark instance
        """
        account = Account.objects.get(user=request.auth.user)

        # Create a new Python instance of the benchmark class
        # and set its properties from what was sent in the
        # body of the request from the client.
        coach_connection = CoachConnection()
        coach = Account.objects.get(pk=request.data["coach_id"])
        coach_connection.coach = coach
        coach_connection.trainee = account
        
        try:
            coach_connection.save()
            serializer = CoachConnectionSerializer(coach_connection, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single benchmark

        Returns:
            Response -- JSON serialized benchmark instance
        """
        try:
            coach_connection = CoachConnection.objects.get(pk=pk)
            serializer = CoachConnectionSerializer(coach_connection, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single benchmark

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            coach_connection = CoachConnection.objects.get(pk=pk)
            coach_connection.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except coach_connection.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to benchmarks resource

        Returns:
            Response -- JSON serialized list of benchmarks
        """
        
        #if the user is a coach send back all the connections where they are a coach
        account = Account.objects.get(user=request.auth.user)
        if account.is_coach:
            
            coach_connections = CoachConnection.objects.filter(coach=account)
            serializer = CoachConnectionSerializer(
            coach_connections, many=True, context={'request': request})
            return Response(serializer.data)
        #if the user is not a coach, there should only be one connection where the user is a trainee, so just send back that one
        else:
            coach_connection = CoachConnection.objects.get(trainee=account)
        
            serializer = CoachConnectionSerializer(
                coach_connection, many=False, context={'request': request})
            return Response(serializer.data)
    
    

          
    
class CoachConnectionSerializer(serializers.ModelSerializer):
    """JSON serializer for CoachConnections

    Arguments:
        serializer type
    """
    class Meta:
        model = CoachConnection
        fields = ("trainee", "coach")
        depth = 2
        
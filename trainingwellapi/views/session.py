"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from trainingwellapi.models import Session, Account, training_plan
from django.db.models import Count
from datetime import date


class Sessions(ViewSet):
  

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized session instance
        """

        
        # Create a new Python instance of the session class
        # and set its properties from what was sent in the
        # body of the request from the client.
        session = Session()
        account = Account.objects.get(user=request.auth.user) 
        session.account = account
        session.assigned_date = request.data["assigned_date"]
        session.time_completed = request.data["time_completed"]
        session.notes = request.data["notes"]
        session.sleep_hours = request.data["sleep_hours"]
        session.energy_level = request.data["energy_level"]
        session.quality = request.data["quality"]
        
        
        
        # Try to save the new session to the database, then
        # serialize the session instance as JSON, and send the
        # JSON as a response to the client request
        try:
            session.save()
            serializer = SessionSerializer(session, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single session

        Returns:
            Response -- JSON serialized session instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/sessions/2
            #
            # The `2` at the end of the route becomes `pk`
            session = Session.objects.get(pk=pk)
            serializer = SessionSerializer(session, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a session

        Returns:
            Response -- Empty body with 204 status code
        """

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of session, get the session record
        # from the database whose primary key is `pk`
        session = Session.objects.get(pk=pk)
        # Create a new Python instance of the session class
        # and set its properties from what was sent in the
        # body of the request from the client.
        
        session.assigned_date = request.data["assigned_date"]
        session.time_completed = request.data["time_completed"]
        session.notes = request.data["notes"]
        session.sleep_hours = request.data["sleep_hours"]
        session.energy_level = request.data["energy_level"]
        session.quality = request.data["quality"]
        session.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single session

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            session = Session.objects.get(pk=pk)
            session.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except session.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to sessions resource

        Returns:
            Response -- JSON serialized list of sessions
        """
        account_id = request.query_params.get('account_id')
        if account_id:
            sessions = Session.objects.filter(account_id = account_id).order_by('assigned_date')
            
            serializer = SessionSerializer(
                sessions, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            account = Account.objects.get(user = request.auth.user)
            sessions = Session.objects.filter(account =account).order_by('assigned_date')
            date_today = date.today()
            
            next_session_found = 0
            def find_next_session(session):
                nonlocal next_session_found
                if date_today <= session.assigned_date and next_session_found == 0:
                    session.next_scheduled = True
                    next_session_found = 1
                    print(session.next_scheduled)
                else:
                    session.next_scheduled = False
                return session
            session_list = map(find_next_session, sessions)
            
            serializer = SessionSerializer(
                session_list, many=True, context={'request': request})
            return Response(serializer.data)
    
class SessionSerializer(serializers.ModelSerializer):
    """JSON serializer for sessions

    Arguments:
        serializer type
    """
    class Meta:
        model = Session
        fields = ('id', 'assigned_date', 'time_completed', 'notes', 'sleep_hours', 'energy_level', 'quality', "account", 'next_scheduled')
        
"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from trainingwellapi.models import TrainingPlan, Account
from django.db.models import Count


class TrainingPlans(ViewSet):
  

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized training_plan instance
        """

        account = Account.objects.get(user=request.auth.user) 
        # Create a new Python instance of the training_plan class
        # and set its properties from what was sent in the
        # body of the request from the client.
        training_plan = TrainingPlan()
        training_plan.start_date = request.data["start_date"]
        training_plan.end_date = request.data["end_date"]
        training_plan.account = account
        
        
        # Try to save the new training_plan to the database, then
        # serialize the training_plan instance as JSON, and send the
        # JSON as a response to the client request
        try:
            training_plan.save()
            serializer = TrainingPlanSerializer(training_plan, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single training_plan

        Returns:
            Response -- JSON serialized training_plan instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/training_plans/2
            #
            # The `2` at the end of the route becomes `pk`
            training_plan = TrainingPlan.objects.get(pk=pk)
            serializer = TrainingPlanSerializer(training_plan, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a training_plan

        Returns:
            Response -- Empty body with 204 status code
        """

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of training_plan, get the training_plan record
        # from the database whose primary key is `pk`
        training_plan = TrainingPlan.objects.get(pk=pk)
        # Create a new Python instance of the training_plan class
        # and set its properties from what was sent in the
        # body of the request from the client.
        
        training_plan.start_date = request.data["start_date"]
        training_plan.end_date = request.data["end_date"]
        training_plan.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single training_plan

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            training_plan = TrainingPlan.objects.get(pk=pk)
            training_plan.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except training_plan.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to training_plans resource

        Returns:
            Response -- JSON serialized list of training_plans
        """
        
        #get all training_plans but add an event_count field
        training_plans = TrainingPlan.objects.all()

        

        serializer = TrainingPlanSerializer(
            training_plans, many=True, context={'request': request})
        return Response(serializer.data)
    
class TrainingPlanSerializer(serializers.ModelSerializer):
    """JSON serializer for training_plans

    Arguments:
        serializer type
    """
    class Meta:
        model = TrainingPlan
        fields = ('id', 'start_date', 'end_date')
        
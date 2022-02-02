"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from trainingwellapi.models import Account, Benchmark, Exercise, ExerciseType
from django.db.models import Count


class Benchmarks(ViewSet):
  

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized benchmark instance
        """
        account = Account.objects.get(user=request.auth.user)

        # Create a new Python instance of the benchmark class
        # and set its properties from what was sent in the
        # body of the request from the client.
        benchmark = Benchmark()
        benchmark.notes = request.data["notes"]
        benchmark.reps = request.data["reps"]
        benchmark.weight = request.data["weight"]
        benchmark.date = request.data["date"]
        
        exercise = Exercise.objects.get(pk=request.data['exercise_id'])
        benchmark.exercise = exercise
        benchmark.account = account
        

        # Try to save the new benchmark to the database, then
        # serialize the benchmark instance as JSON, and send the
        # JSON as a response to the client request
        try:
            benchmark.save()
            serializer = BenchmarkSerializer(benchmark, context={'request': request})
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
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/benchmarks/2
            #
            # The `2` at the end of the route becomes `pk`
            benchmark = Benchmark.objects.get(pk=pk)
            serializer = BenchmarkSerializer(benchmark, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a benchmark

        Returns:
            Response -- Empty body with 204 status code
        """

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of benchmark, get the benchmark record
        # from the database whose primary key is `pk`
        benchmark = Benchmark.objects.get(pk=pk)

        # Create a new Python instance of the benchmark class
        # and set its properties from what was sent in the
        # body of the request from the client.
        benchmark = Benchmark()
        benchmark.notes = request.data["notes"]
        benchmark.reps = request.data["reps"]
        benchmark.weight = request.data["weight"]
        benchmark.date = request.data["date"]
        
        exercise = Exercise.objects.get(pk=request.data['exercise_id'])
        benchmark.exercise = exercise
        benchmark.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single benchmark

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            benchmark = Benchmark.objects.get(pk=pk)
            benchmark.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except benchmark.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to benchmarks resource

        Returns:
            Response -- JSON serialized list of benchmarks
        """
        
        #get all benchmarks but add an event_count field
        benchmarks = Benchmark.objects.all()

        

        serializer = BenchmarkSerializer(
            benchmarks, many=True, context={'request': request})
        return Response(serializer.data)
    
    

          
    
class BenchmarkSerializer(serializers.ModelSerializer):
    """JSON serializer for benchmarks

    Arguments:
        serializer type
    """
    class Meta:
        model = Benchmark
        fields = ('id', 'notes', 'exercise', 'reps', 'weight', 'date')
        depth = 2
        
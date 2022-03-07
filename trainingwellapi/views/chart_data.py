"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from trainingwellapi.models import Benchmark, Account
from django.db.models import Count


class ChartData(ViewSet):



    def retrieve(self, request, pk=None):
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

    

    def list(self, request):
        account = Account.objects.get(user=request.auth.user) 
        data_type = request.query_params.get('datatype')
        if data_type == 'benchmarks':
        #get all exercises but add an event_count field
            benckmarks = Benchmark.objects.filter(account = account).order_by('date')
            benchmark_data = {}
            for benchmark in benckmarks:
                if benchmark.exercise.name in benchmark_data:
                    benchmark_data[benchmark.exercise.name].append({"x": benchmark.weight, "y": benchmark.date})
                else:
                    benchmark_data[benchmark.exercise.name] = [{"x": benchmark.weight, "y": benchmark.date}]
            print(benchmark_data)

        
        return Response(benchmark_data)
    
# class ExerciseSerializer(serializers.ModelSerializer):
#     """JSON serializer for exercises

#     Arguments:
#         serializer type
#     """
#     class Meta:
#         model = Exercise
#         fields = ('id', 'description', 'name', 'exercise_type', 'url')
#         depth = 1
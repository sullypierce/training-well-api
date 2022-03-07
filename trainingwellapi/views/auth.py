from inspect import Traceback
import json
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from trainingwellapi.models import Account, TrainingPlan


@csrf_exempt
def login_user(request):
    '''Handles the authentication of a gamer

    Method arguments:
      request -- The full HTTP request object
    '''

    req_body = json.loads(request.body.decode())

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Use the built-in authenticate method to verify
        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)


        # If authentication was successful, respond with their token
        if authenticated_user is not None:
            account = Account.objects.get(user=authenticated_user)
            training_plan = {}
            token = Token.objects.get(user=authenticated_user)
            try:
                training_plan = TrainingPlan.objects.get(account = account)
                data = json.dumps({"valid": True, "token": token.key, "training_plan_id": training_plan.id, 'is_coach': account.is_coach, "account_name": f'{account.user.first_name} {account.user.last_name}'})
                return HttpResponse(data, content_type='application/json')
            except Exception as ex:
                training_plan = {"id": 0}
                data = json.dumps({"valid": True, "token": token.key, "training_plan_id": training_plan["id"], 'is_coach': account.is_coach, "account_name": f'{account.user.first_name} {account.user.last_name}'})
                return HttpResponse(data, content_type='application/json')

        else:
            # Bad login details were provided. So we can't log the user in.
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')


@csrf_exempt
def register_user(request):
    '''Handles the creation of a new account for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Load the JSON string of the request body into a dict
    req_body = json.loads(request.body.decode())

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    new_user = User.objects.create_user(
        username=req_body['username'],
        email=req_body['email'],
        password=req_body['password'],
        first_name=req_body['first_name'],
        last_name=req_body['last_name']
    )
    coach_bool = False
    if req_body['is_coach'] == 'true':
        coach_bool = True
    # Now save the extra info in the trainingwellapi_account table
    account = Account.objects.create(
        is_coach=coach_bool,
        user=new_user
    )

    # Commit the user to the database by saving it
    account.save()

    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=new_user)
    new_account = Account.objects.get(user=new_user)
    # Return the token to the client
    data = json.dumps({"token": token.key, "is_coach": new_account.is_coach, "account_name": f'{new_account.user.first_name} {new_account.user.last_name}'})
    return HttpResponse(data, content_type='application/json')
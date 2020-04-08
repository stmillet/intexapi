from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """
    
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

class UserInfoList(APIView):
    
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        user = User.objects.get(username=request.data['username'])
        print('test:', user.first_name)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PredictList(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        
        import urllib
        import json 

        body = json.loads(request.body)

        title = body['title']
        description = body['description']
        auto_fb_post_mode = body['auto_fb_post_mode']
        currencycode = body['currencycode']
        has_beneficiary = body['has_beneficiary']
        is_charity = body['is_charity']
        charity_valid = body['charity_valid']

        # formatting the data into a data object for the API call
        data =  {
                    "Inputs": {
                        "input1":
                        {
                            "ColumnNames": ["title", "description", "auto_fb_post_mode", "currencycode", "has_beneficiary", "is_charity", "charity_valid"],
                            "Values": [[ title, description, auto_fb_post_mode, currencycode, has_beneficiary, is_charity, charity_valid ],]
                        }, # in the values array above it may seem weird to put a value for the response var, but azure needs something
                    },
                    "GlobalParameters": {
                    }
                }

        
        body = str.encode(json.dumps(data))

        #API Call for the Total Amount of Donations Received
        url_amount = 'https://ussouthcentral.services.azureml.net/workspaces/1cd50493736146cab3ac55b235e0f510/services/947db55143f84ecd9e56a3fc63d21f56/execute?api-version=2.0&details=true'
        api_key_amount = 'aakk1woKsSfCqpT3J3IWbe8IN/MPHv95QbfUy6s0mGGmYSRsmwp5c8kBCtDV0kcoQxrrO/iL5gJTcfzl1X/zkA=='
        
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key_amount)}

        req = urllib.request.Request(url_amount, body, headers) 

        response = urllib.request.urlopen(req)

        result_amount = response.read()
        result_amount = json.loads(result_amount)
        result_amount = result_amount["Results"]["output1"]["value"]["Values"][0]

        
        #API Call for the Number of Donors
        url_donor = 'https://ussouthcentral.services.azureml.net/workspaces/c6cd80c3a6a645f8b5e5bd3774cb0c50/services/7cbe4f364c4d4283b42bed8361bcbd10/execute?api-version=2.0&details=true'
        api_key_donor = 'krLzOimi0hlUSgVNlTrBxUflIxzK6TN+lrQhib6eVfP5BO9L9yBw+NidP9nyX3CoVPXaca0/aEgg4A4JTHscvA=='

        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key_donor)}
        
        req = urllib.request.Request(url_donor, body, headers)

        response = urllib.request.urlopen(req)

        result_donor = response.read()
        result_donor = json.loads(result_donor)
        result_donor = result_donor['Results']['output1']['value']['Values'][0]

        theResults = {
            'amount': result_amount,
            'donor': result_donor
        }
        
        
        
        return Response(theResults) # this path assumes that this file is in the root directory in a folder named templates
        # the third parameter sends the result (the response variable value) to the template to be rendered
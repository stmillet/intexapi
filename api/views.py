from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken, CampaignSerializer
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from api.models import Campaign

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

class CampaignSearchList(APIView):

    permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        print(request.query_params)
        camps = Campaign.objects.filter(title__icontains=request.query_params['title'])
        serializer = CampaignSerializer(camps, many=True)
        return Response(serializer.data)



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
        url_amount = 'https://ussouthcentral.services.azureml.net/workspaces/c6cd80c3a6a645f8b5e5bd3774cb0c50/services/07fc7eb0789a417c982530e44dda3582/execute?api-version=2.0&details=true'
        api_key_amount = 'sBKCqFuxOLZAS9z8dxDW31s9fFMe3wE+mhjW2DuU1IMI7bhHu2U7NMvfuCxZHX33kHFQo7AgZOVii/ToSaqhsQ=='
        
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key_amount)}

        req = urllib.request.Request(url_amount, body, headers) 

        response = urllib.request.urlopen(req)

        result_amount = response.read()
        result_amount = json.loads(result_amount)
        result_amount = result_amount["Results"]["output1"]["value"]["Values"][0][0]
        result_amount = round(float(result_amount), 2)
        if result_amount < 0:
            result_amount = 0

        
        #API Call for the Number of Donors
        url_donor = 'https://ussouthcentral.services.azureml.net/workspaces/c6cd80c3a6a645f8b5e5bd3774cb0c50/services/2641276d668847e9bf55c746e4cbff00/execute?api-version=2.0&details=true'
        api_key_donor = 'f6yUVfKBYfpDzCoxjAy4m9JX3xDMgce2Df11FtJDDtINXO128xsU0LUK1IFEFMp714hTbgfNzhIiu3P3jdyPaw=='

        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key_donor)}
        
        req = urllib.request.Request(url_donor, body, headers)

        response = urllib.request.urlopen(req)

        result_donor = response.read()
        result_donor = json.loads(result_donor)
        result_donor = result_donor['Results']['output1']['value']['Values'][0][0]
        result_donor = int(float(result_donor))
        if result_donor < 0:
            result_donor = 0

        theResults = {
            'amount': result_amount,
            'donor': result_donor,
            'avg_donor': round(result_amount/result_donor, 2)
        }
        
        
        
        return Response(theResults) # this path assumes that this file is in the root directory in a folder named templates
        # the third parameter sends the result (the response variable value) to the template to be rendered


class CampaignList(APIView):
    '''Get all products or create a product'''
    permission_classes = (permissions.AllowAny,)
    @csrf_exempt
    def get(self, request, format=None):
        camps = Campaign.objects.all()
        serializer = CampaignSerializer(camps, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request, format=None):
        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        search_fields = ['is_charity']
        filter_backends = (filters.SearchFilter,)
        queryset = Campaign.objects.all()
        serializer = CampaignSerializer(queryset, many=True)

        return Response(serializer.data)



class PredictList(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        
        import urllib
        import json 

        body = json.loads(request.body.decode('utf-8'))

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
            avg_donor = 0
        else:
            avg_donor = round(result_amount/result_donor, 2)

        print(result_donor)
        if result_donor == 0:
            avg_donor = 0
        else:
            avg_donor = round(result_amount/result_donor, 2)

        theResults = {
            'amount': result_amount,
            'donor': result_donor,
            'avg_donor': avg_donor
        }
        
        
        
        return Response(theResults) # this path assumes that this file is in the root directory in a folder named templates
        # the third parameter sends the result (the response variable value) to the template to be rendered


class CampaignList(APIView):
    '''Get all products or create a product'''
    permission_classes = (permissions.AllowAny,)
    @csrf_exempt
    def get(self, request, format=None):
        camps = Campaign.objects.all()
        if request.query_params.get('title'):
            camps = camps.filter(title__icontains=request.query_params.get('title'))
        
        if request.query_params.get('title2'):
            camps = camps.filter(title__icontains=request.query_params.get('title2'))
        
        if request.query_params.get('description'):
            camps = camps.filter(description__icontains=request.query_params.get('description'))
        
        if request.query_params.get('currencycode'):
            camps = camps.filter(currencycode__icontains=request.query_params.get('currencycode'))
        
        if request.query_params.get('current_amount_start') and request.query_params.get('current_amount_end'):
            camps = camps.filter(current_amount__range=(request.query_params.get('current_amount_start'), request.query_params.get('current_amount_end')))
        
        if request.query_params.get('auto_fb_post_mode'):
            camps = camps.filter(auto_fb_post_mode__icontains=request.query_params.get('auto_fb_post_mode'))
        
        if request.query_params.get('goal_start') and request.query_params.get('goal_end'):
            camps = camps.filter(goal__range=(request.query_params.get('goal_start'), request.query_params.get('goal_end')))
        
        if request.query_params.get('donators_start') and request.query_params.get('donators_end'):
            camps = camps.filter(donators__range=(request.query_params.get('donators_start'), request.query_params.get('donators_end')))
        
        if request.query_params.get('days_active_start') and request.query_params('days_active_end'):
            camps = camps.filter(days_active__rang=(request.query_params.get('days_active'), request.query_params('days_active_end')))
        
        if request.query_params.get('has_beneficiary'):
            camps = camps.filter(has_beneficiary__icontains=request.query_params.get('has_beneficiary'))
        
        if request.query_params.get('status'):
            camps = camps.filter(status__icontains=request.query_params.get('status'))
        
        if request.query_params.get('deactivated'):
            camps = camps.filter(deactivated__icontains=request.query_params.get('deactivated'))
        
        if request.query_params.get('campaign_hearts_start') and request.query_params('campaign_hearts_end'):
            camps = camps.filter(campaign_hearts__range=(request.query_params.get('campaign_hearts_start'), request.query_params.get('campaign_hearts_end')))
        
        if request.query_params.get('social_share_total_start') and request.query_params.get('social_share_total_end'):
            camps = camps.filter(social_share_total__range=(request.query_params.get('social_share_total_start'), request.query_params.get('social_share_total_end')))
        
        if request.query_params.get('location_country'):
            camps = camps.filter(location_country__icontains=request.query_params.get('location_country'))
        
        if request.query_params.get('is_charity'):
            camps = camps.filter(is_charity__icontains=request.query_params.get('is_charity'))
        
        if request.query_params.get('charity_valid'):
            camps = camps.filter(charity_valid__icontains=request.query_params.get('charity_valid'))
        
        if request.query_params.get('avg_donation_start') and request.query_params.get('avg_donation_end'):
            camps = camps.filter(avg_donation__range=(request.query_params.get('avg_donation_start'), request.query_params.get('avg_donation_end')))
        
        if request.query_params.get('c_rating'):
            camps = camps.filter(c_rating__icontains=request.query_params.get('c_rating'))

        serializer = CampaignSerializer(camps, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request, format=None):
        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

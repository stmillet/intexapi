from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken

# Create your views here.

@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """
    
    serializer = UserSerializer(request.user)
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

def resultsView(request):
# this view receives parameters from the submit html template and calls the API in azure
# this contains API code for Python and Python3 

    # If you are using Python 3+, import urllib instead of urllib2
    #import urllib2.request
    import urllib
    import json 

    # assign all the parameters to variables which you put in the API like the commented code
    # or just put them in directly like I did farther down
    
    title = str(request.POST['title'])
    description = str(request.POST['description'])
    auto_fb_post_mode = str(request.POST['auto_fb_post_mode'])
    currencycode = str(request.POST['currencycode'])
    has_beneficiary = str(request.POST['has_beneficiary'])
    is_charity = str(request.POST['is_charity'])
    charity_valid = str(request.POST['charity_valid'])
    
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

    # the API call
    body = str.encode(json.dumps(data))
    url = 'https://ussouthcentral.services.azureml.net/workspaces/1cd50493736146cab3ac55b235e0f510/services/947db55143f84ecd9e56a3fc63d21f56/execute?api-version=2.0&details=true'
    api_key = 'aakk1woKsSfCqpT3J3IWbe8IN/MPHv95QbfUy6s0mGGmYSRsmwp5c8kBCtDV0kcoQxrrO/iL5gJTcfzl1X/zkA=='
    # Replace my url and api_key with your own values
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    # If you are using Python 3+, replace urllib2 with urllib.request
    #req = urllib2.Request(url, body, headers)
    req = urllib.request.Request(url, body, headers) 

    # python3 uses urllib while python uses urllib2
    #response = urllib2.request.urlopen(req)
    response = urllib.request.urlopen(req)
    print(response)
    
    # this formats the results 
    result = response.read()
    result = json.loads(result) # turns bits into json object
    result = result["Results"]["output1"]["value"]["Values"][0][7] 
    # azure send the response as a weird result object. It would be wise to postman to find the 
    # path to the response var value

    return render(request, "results.html", {"result": result}) # this path assumes that this file is in the root directory in a folder named templates
    # the third parameter sends the result (the response variable value) to the template to be rendered
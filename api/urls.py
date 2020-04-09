from django.urls import path
from .views import current_user, UserList, UserInfoList, PredictList, CampaignList, CampaignSearchList

urlpatterns = [
    path('current_user/', current_user),
    path('users/', UserList.as_view()),
    path('user/', UserInfoList.as_view()),
    path('predict/', PredictList.as_view()),
    path('campaigns/', CampaignList.as_view()),
    # path('search/', CampaignSearchList.as_view()),
]
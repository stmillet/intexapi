from django.urls import path
from .views import current_user, UserList, UserInfoList

urlpatterns = [
    path('current_user/', current_user),
    path('users/', UserList.as_view()),
    path('user/', UserInfoList.as_view())
]
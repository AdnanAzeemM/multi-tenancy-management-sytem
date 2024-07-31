from django.urls import path
from user.views import UserListAPIView, CreateSubUserAPIView, EmployeeAPIView


urlpatterns = [
    path('user_list', UserListAPIView.as_view(), name="user_list"),
    path('create_sub_user', EmployeeAPIView.as_view(), name="create_sub_user"),
]
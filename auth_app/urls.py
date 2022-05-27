from sys import path_hooks
from venv import create
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from .views import create_student,create_teacher, delete_user, auth_check,MyTokenObtainPairView
urlpatterns = [
    path('',auth_check),
    path('create-token',MyTokenObtainPairView.as_view(),name="create_jwt_token"),
    path('refresh-token',TokenRefreshView.as_view(),name="refresh_jwt_token"),
    path('verify-token/',TokenVerifyView.as_view(),name="verify_jwt_token"),
    path('create-student',create_student,name= "student user creation"),
    path('create-teacher',create_teacher,name= "teacher user creation"),
    path('delete-user',delete_user,name="user deletion"),
]


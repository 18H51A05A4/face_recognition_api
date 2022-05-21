from sys import path_hooks
from venv import create
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from .views import create_user, delete_user, auth_check
urlpatterns = [
    path('',auth_check),
    path('create-token/',TokenObtainPairView.as_view(),name="create_jwt_token"),
    path('refresh-token/',TokenRefreshView.as_view(),name="refresh_jwt_token"),
    path('verify-token/',TokenVerifyView.as_view(),name="verify_jwt_token"),
    path('create-user/',create_user,name= "user creation"),
    path('delete-user/',delete_user,name="user deletion")
]


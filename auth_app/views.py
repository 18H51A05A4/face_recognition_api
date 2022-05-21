from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
# Create your views here.

@api_view(["GET"])
def auth_check(request):
    return Response("auth app running")


@api_view(['POST'])
def create_user(request):
    try:
        user = User.objects.create_user(
            username = request.data['username'],
            password =  request.data['password'],
            email =  request.data['email']
        )
        user.save()
    except Exception as e:
        return Response({
            "details" : str(e)
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return Response({
        "details" : "user registration successful"
    })

@api_view(['post'])
def delete_user(request):
    try:
        user = User.objects.get(username=request.data["username"])
        user.delete()
    except Exception as e:
        return Response({
            "details" : str(e)
        },status=status.HTTP_409_CONFLICT)
    return Response({
            "details " : f'user with username {request.data["username"]} deleted'
        })
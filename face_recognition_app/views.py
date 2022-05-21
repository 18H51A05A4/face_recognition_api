from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from  rest_framework import status
from face_recognition_app.face_recognition_service import base64_to_nparray,get_face_encodings,save_encodings,verify_encodings
# Create your views here.

@api_view(['get'])
def check(request):
    return Response("face recognition api running")

    
@api_view(['post'])
def save_user_encodings(request):
    try:
        var= request.data["username"] and request.data["image"]
    except Exception as e:
        return Response({"details":"request body should contain username and image(base64 url)"})
    try:
        image_array = base64_to_nparray(request.data["image"])
        face_encodings = get_face_encodings(image_array)
        save_encodings(request.data["username"],face_encodings)
    except Exception as e:
        return Response({"details":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"details":"user registration completed"})



@api_view(['post'])
def verify_user_encodings(request):
    try:
        var= request.data["username"] and request.data["image"]
    except Exception as e:
        return Response({"details":"request body should contain username and image(base64 url)"})
    try:
        image_array = base64_to_nparray(request.data["image"])
        face_encodings = get_face_encodings(image_array)
        if(verify_encodings(request.data["username"],face_encodings)):
            return Response({"details":"user verified"})
        else:
            return Response({"details":"user not verified"})
    except Exception as e:
        return Response({"details":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
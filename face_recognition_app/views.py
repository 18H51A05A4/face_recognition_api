from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from  rest_framework import status
from attendance_app.models import FaceVerification
from face_recognition_app.face_recognition_service import base64_to_nparray,get_face_encodings,save_encodings,verify_encodings
from PIL import Image
from attendance_app.models import Attendance
# Create your vxews here.

import face_recognition
import re
from io import BytesIO
import base64
import numpy as np
from utilities import get_base_path

from face_recognition_app.face_recognition_service import save_face_encodings,verify_face_encodings


@api_view(['get'])
def check(request):
    return Response("face recognition api running")

    
@api_view(['post'])
def save_user_encodings(request):
    try:
        var= request.data["username"] and request.data["image"]
    except Exception as e:
        return Response({"details":"request body should contain username and image(base64 url)"})
    # try:
    image_data = re.sub('^data:image/.+;base64,', '', request.data['image'])
    image =  face_recognition.load_image_file(BytesIO(base64.b64decode(image_data)))
    locations = face_recognition.face_locations(image)
    encodings = face_recognition.face_encodings(image,locations)
    np.save(get_base_path()+f'\\face_recognition_app\\asssets\\{request.data["username"]}.npy',encodings)
    
        
        # image_array = base64_to_nparray(request.data["image"])
        # face_encodings = get_face_encodings(image_array)
        # face_encodings = preprocessing(image_array)
        # save_encodings(request.data["username"],face_encodings)
    # except Exception as e:
    #     return Response({"details":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"details":"user registration completed"})



@api_view(['post'])
def verify_user_encodings(request):
    try:
        var= request.data["username"] and request.data["image"]
    except Exception as e:
        return Response({"details":"request body should contain username and image(base64 url)"})
    try:
        image_data = re.sub('^data:image/.+;base64,', '', request.data['image'])
        image =  face_recognition.load_image_file(BytesIO(base64.b64decode(image_data)))
        locations = face_recognition.face_locations(image)
        encodings = face_recognition.face_encodings(image,locations)
        encodings1 = np.load(get_base_path()+f'\\face_recognition_app\\asssets\\{request.data["username"]}.npy')
        print(encodings1,encodings)
        res = face_recognition.face_distance(encodings,encodings1)
        print(res)
        if(res>=0.5):
            return Response({
                "res": "true",
                "detail" :f"user verified with {res}"})
        else:
            return Response({
                "res" : "false",
                "detail" : f"user not verified with {res}"})
    except Exception as e:
        return Response({"details":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



@api_view(['POST'])
def save_user_encodings_using_model(request):
    try:
        var= request.data["username"] and request.data["image"]
    except Exception as e:
        return Response({"details":"request body should contain username and image(base64 url)"})
    try:
        save_face_encodings(request.data["username"],request.data["image"])
        return Response("user registration succesful")
    except Exception as e:
        return Response({"details":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  


@api_view(['POST'])
def verify_user_encodings_using_model(request):
    try:
        var= request.data["username"] and request.data["image"]
    except Exception as e:
        return Response({"details":"request body should contain username and image(base64 url)"})
    try:
        res = verify_face_encodings(request.data["username"],request.data["image"])
        print(round(res,5))  
        print(request.data)
        if(res<=0.5):
            obj = Attendance.objects.get(class_id = int(request.data["class_id"]),student_id = int(request.data["user_id"]))
            if(request.data["is_joining"]== 'true'):
                obj.joining_verification = True
                print("joining attendance")
            else:
                obj.leaving_verification = True
                print("leaving attendance")
            
            if(obj.joining_verification and obj.leaving_verification):
                obj.attended = True

            obj.save()
            return Response({
                "res": "true",
                "detail" :f"user verified with {res}"})
        else:
            return Response({
                "res" : "false",
                "detail" : f"user not verified with {res}"})
    except Exception as e:
        return Response({"details":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
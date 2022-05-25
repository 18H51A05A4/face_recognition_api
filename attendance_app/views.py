
from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from utilities import get_payload_from_token
from attendance_app.models import ClassTable,Attendance
from auth_app.models import User
import json 
from django.db.models import Q 
from datetime import datetime
# Create your views here.


#teacher routes

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_class(request):
    payload = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))
    if(payload["is_teacher"] == False):
        return Response({"details": "user should be faculty in order to access this route"},status=status.HTTP_401_UNAUTHORIZED)
    try:
        var = (request.data["class_name"] and request.data["meet_link"] 
                and request.data["start_time"] and request.data["end_time"]
                and request.data["class_date"] and request.data["students"]
              )
    except KeyError:
        return Response({"details":"body should contain class_name, meet_link, start_time, end_time, class_date"},status=status.HTTP_409_CONFLICT)
    
    try:
        record = ClassTable(
            class_name = request.data["class_name"],
            meet_link = request.data["meet_link"],
            start_time = request.data["start_time"],
            end_time = request.data["end_time"],
            class_date = request.data["class_date"],
            teacher_id =  User.objects.get(id = payload["user_id"])
        )

        record.save()

        for student in request.data["students"]:
            att_record = Attendance(
                class_id = ClassTable.objects.get(class_id = record.class_id),
                student_id = User.objects.get(id = student),
            )
            att_record.save()

    except Exception as e:
        return Response({"details":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response("class created")


@api_view(['get'])
@permission_classes([IsAuthenticated,])
def get_student_list(request):
    try:
        students = User.objects.filter(is_teacher = False)
        resp_obj = []
        for i in students:
            obj = {
                "id" :  i.id,
                "username" : i.username
            }
            resp_obj.append(obj)
        
        return Response(resp_obj)
    except Exception as e:
        return Response({"details":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
     



#student routes


@api_view(['get'])
@permission_classes([IsAuthenticated,])
def get_classes(request):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    all_records = ClassTable.objects.all()
    record = []
    # and datetime.strptime(now.strftime("%H:%M:%S"),"%H:%M:%S") <i.end_time
    for i in all_records:
        if(i.class_date > datetime.now().date()):
            record.append(i)
        elif(i.class_date == datetime.now().date() and datetime.now().time() < i.end_time):
            record.append(i)
    print(len(record))
    return Response("ok")


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def take_attendance(request):
    payload = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))
    if(payload["is_teacher"] == True):
        return Response({"details": "user should be student in order to access this route"},status=status.HTTP_401_UNAUTHORIZED)
    try:
        var = (request.data["class_id"] and request.data['is_joining_attendance']
              )
    except KeyError:
        return Response({"details":"body should contain class_id, is_joining_attendance"},status=status.HTTP_409_CONFLICT)

    try:
        if(request.data["is_joining_attendance"]):
            try:
                obj = Attendance.objects.get(class_id = request.data["class_id"],student_id = payload["user_id"])
            except Attendance.DoesNotExist:
                return Response({"details":"either student is not added to class or class not created"},status=status.HTTP_409_CONFLICT)
            obj.joining_verification = True
            obj.save()
        else:
            try:
                obj = Attendance.objects.get(class_id = request.data["class_id"],student_id = payload["user_id"])
            except Attendance.DoesNotExist:
                return Response({"details":"either student is not added to class or class not created"},status=status.HTTP_409_CONFLICT)
            obj.leaving_verification = True
            if(obj.joining_verification):
                obj.attended = True
            else:
                obj.attended = False
            obj.save()
       
    except Exception as e:
        return Response({"details":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response("attendance recorded")


# @api_view(['GET'])
# @permission_classes((IsAuthenticated,))
# def get_attendance(request):
#     payload = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))
#     try:
#         var = (request.data["date"]   
#               )
#     except KeyError:
#         return Response({"details":"body should contain date"},status=status.HTTP_409_CONFLICT)
    
#     if(payload["is_teacher"]):
#         try:
#             class_records= ClassTable.objects.get(teacher_id = payload["user_id"], class_date = request.data["date"])
#         except ClassTable.DoesNotExist:
#             return Response(f"no classes found on {request.data['date']}")
        
#         for class_record in class_records:
#             attendance_records = Attendance.objects.get(class_id = class_record.class_id)
#             for attendance_record in attendance_records:
            
#     else:
#         pass
#     return Response('get attendance route')








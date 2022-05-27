
from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from utilities import get_payload_from_token
from attendance_app.models import ClassTable,Attendance, FaceVerification
from auth_app.models import User
import json 
from django.db.models import Q 
from datetime import datetime
# Create your views here.

#user 
@api_view(['get'])
@permission_classes((IsAuthenticated,))
def get_user_details(request):
    payload = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))
    record = User.objects.get(id =  payload['user_id'])
    obj = {
        "user_id" : record.id,
        "username" : record.username,
        "email" : record.email,
        "is_teacher" : record.is_teacher
    }
    return Response(obj)


@api_view(['POST'])
def set_is_verified(request):
    record = FaceVerification.objects.get(id=2)
    record.is_verified = request.data["is_verified"]
    record.save() 
    return Response("verification updated")


@api_view(['get'])
def is_verified(request):
    record = FaceVerification.objects.get(id=2)
    obj = {
        "is_verified" : record.is_verified
    }
    return Response(obj)


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



@api_view(['post'])
@permission_classes([IsAuthenticated,])
def get_classes_teacher(request):
    payload = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))
    try:
        classes = ClassTable.objects.filter(teacher_id = payload["user_id"])
        records = []
        # and datetime.strptime(now.strftime("%H:%M:%S"),"%H:%M:%S") <i.end_time
        for i in classes:
            obj = {
                "class_id" : i.class_id,
                "class_name" : i.class_name,
                "start_time" : i.start_time,
                "end_time" : i.end_time,
                "class_date" : i.class_date,
                "meeting_link" : i.meet_link
            }
            if(i.class_date >= datetime.strptime(request.data["date"],"%Y-%m-%d").date()):
                records.append(obj)   
        return Response(records)
    except Exception as e:
        return Response({"detail": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['get'])
# @permission_classes([IsAuthenticated,])
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
def get_classes_student(request):
    payload = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))
    try:
        attendance_allrecords = Attendance.objects.filter(student_id = payload["user_id"])    
        records = []
        # and datetime.strptime(now.strftime("%H:%M:%S"),"%H:%M:%S") <i.end_time
        for j in attendance_allrecords:
            i = ClassTable.objects.get(class_id = j.class_id_id)
            obj = {
                "class_id" : i.class_id,
                "class_name" : i.class_name,
                "start_time" : i.start_time,
                "end_time" : i.end_time,
                "class_date" : i.class_date,
                "meeting_link" : i.meet_link
            }
            print(i.class_date ,datetime.now().date())
            if(i.class_date > datetime.now().date()):
                records.append(obj)   
            elif(i.class_date == datetime.now().date() and datetime.now().time() < i.end_time):
                records.append(obj)
        return Response(records)
    except Exception as e:
        return Response({"detail":str(e)},status= status.HTTP_500_INTERNAL_SERVER_ERROR)



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



@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def get_attendance(request):
    payload = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))
    try:
        var = (request.data["date"]   
              )
    except KeyError:
        return Response({"details":"body should contain date"},status=status.HTTP_409_CONFLICT)
    
    if(payload["is_teacher"]):
        try:
            class_records= ClassTable.objects.filter(teacher_id = payload["user_id"], class_date = datetime.strptime(request.data["date"],"%Y-%m-%d"))
        except ClassTable.DoesNotExist:
            return Response(f"no classes found on {request.data['date']}")
        res = []
        for class_record in class_records:
            res1 =[
                {
                "class_id" : class_record.class_id,
                "class_name" : class_record.class_name,
                "start_time": class_record.start_time,
                "end_time" : class_record.end_time,
                "meet_link":class_record.meet_link

            }
            ]
            students = Attendance.objects.filter(class_id = class_record.class_id)
            for student in students:
                obj={
                    "username" : User.objects.get(id = student.student_id_id).username,
                    "is_attended" : student.attended
                }
                res1.append(obj)
            res.append(res1)
        return Response(res)
    else:
        class_records = ClassTable.objects.filter(class_date = datetime.strptime(request.data["date"],"%Y-%m-%d"))
        student_records = Attendance.objects.filter(student_id_id = payload["user_id"])
        res = []
        for student_record in student_records:
            for class_record in class_records:
                if(student_record.class_id_id == class_record.class_id):
                    obj={
                    "class_name" : class_record.class_name,
                    "username" : User.objects.get(id = student_record.student_id_id).username,
                    "joining_attendance" : student.joining_verification,
                    "leaving_attendance" : student.leaving_verification,
                    "is_attended" : student_record.attended,
                    }
                    res.append(obj)
        return Response(res)
            








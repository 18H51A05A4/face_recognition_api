from django.db import models
from auth_app.models import User
# Create your models here.

class ClassTable(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name =  models.CharField(max_length=255)
    meet_link = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()
    class_date =  models.DateField()
    teacher_id = models.ForeignKey(User,to_field='id',on_delete=models.DO_NOTHING)
    ludt = models.DateTimeField(auto_now_add=True)


class Attendance(models.Model):
    att_id = models.AutoField(primary_key=True)
    class_id = models.ForeignKey(ClassTable,to_field='class_id',on_delete=models.DO_NOTHING)
    student_id = models.ForeignKey(User,to_field='id',on_delete=models.DO_NOTHING)
    joining_verification = models.BooleanField(default=False)
    leaving_verification = models.BooleanField(default=False)
    attended = models.BooleanField(default=False)
    ludt = models.DateTimeField(auto_now_add=True)

class StudentSection(models.Model):
    student_id = models.ForeignKey(User,to_field='id',on_delete=models.DO_NOTHING)
    section = models.CharField(max_length=255)
    ludt = models.DateTimeField(auto_now_add=True)


class FaceVerification(models.Model):
    is_verified = models.BooleanField(default=False)
    ludt =  models.DateTimeField(auto_now_add=True)


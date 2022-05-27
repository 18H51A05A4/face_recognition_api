from django.urls import path 
from .views import (create_class, get_classes_student,get_student_list, get_user_details, is_verified, set_is_verified,take_attendance,
get_classes_teacher,get_attendance,
get_user_details)


urlpatterns = [

    #user 
    path('get-user-details',get_user_details),
    path('is-verified',is_verified),
    path('set-is-verified',set_is_verified),


    #teacher routes
    path('create-class',create_class),
    path('get-classes-teacher',get_classes_teacher),
    path('get-students',get_student_list),

    #student routes
    path('take-attendance',take_attendance),
    path('get-classes-student',get_classes_student),

    #common to both 
    path('get-attendance',get_attendance)
    # path('add-students-in-class/',add_students_in_class)

]
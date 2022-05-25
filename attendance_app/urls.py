from django.urls import path 
from .views import create_class,get_student_list,take_attendance,get_classes,get_attendance
urlpatterns = [

    #teacher routes
    path('create-class/',create_class),
    path('get-students/',get_student_list),

    #student routes
    path('take-attendance/',take_attendance),
    path('get-classes/',get_classes),
    path('get-attendance/',get_attendance)
    # path('add-students-in-class/',add_students_in_class)

]
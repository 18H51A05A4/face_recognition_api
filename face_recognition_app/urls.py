from django.urls import path

from .views import check,save_user_encodings, save_user_encodings_using_model,verify_user_encodings, verify_user_encodings_using_model
urlpatterns = [
    path('',check),
    path('save-user-encodings',save_user_encodings),
    path('verify-user-encodings',verify_user_encodings),

    path('save-user-encodings-using-model',save_user_encodings_using_model),
    path('verify-user-encodings-using-model',verify_user_encodings_using_model),

]
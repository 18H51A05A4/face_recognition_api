from django.urls import path
from .views import check,save_user_encodings
urlpatterns = [
    path('',check),
    path('save-user-encodings',save_user_encodings)
]
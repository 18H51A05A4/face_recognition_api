from django.apps import AppConfig
from utilities import get_base_path
from keras import models as kerasmodels

class FaceRecognitionAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'face_recognition_app'
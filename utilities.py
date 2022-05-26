import base64
from face_recognition_api.settings import BASE_DIR,ROOT_URLCONF,SECRET_KEY
import os
import face_recognition
import jwt 

def get_base_path():
    project_name =  ROOT_URLCONF.split('.')[0]
    return os.path.dirname(BASE_DIR)+f'\{project_name}'

# def preprocessing(image_array):
#     frame = face_recognition.face_locations(image_array)
#     face_encodings=  face_recognition.face_encodings(image_array,frame)[0]
#     return face_encodings
    
# def face_distance(encodings1,encodings2):
#     # dist = face_recognition.face_distance([encodings1],encodings2)
#     res = face_recognition.compare_faces([encodings1],encodings2, tolerance=0.6)
#     return res[0]       

def get_payload_from_token(token):
    token =  token.split(' ')[1]
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload
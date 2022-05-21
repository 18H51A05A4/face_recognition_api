from face_recognition_api.settings import BASE_DIR,ROOT_URLCONF
import os

def get_base_path():
    project_name =  ROOT_URLCONF.split('.')[0]
    return os.path.dirname(BASE_DIR)+f'\{project_name}'

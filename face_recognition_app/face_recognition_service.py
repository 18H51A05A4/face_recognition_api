import numpy as np 
import keras.models as kerasmodels
from PIL import Image
import re
from io import BytesIO
import base64
import pickle
from utilities import get_base_path



class MLModel():

    __instance = None
 
    @staticmethod
    def get_instance():
        if(MLModel.__instance is None):
            MLModel()
        return MLModel.__instance
 
    def __init__(self):
        self.model = kerasmodels.load_model(get_base_path()+'\\face_recognition_app\\asssets\\facenet_keras.h5')
        MLModel.__instance =  self 


facenet = MLModel.get_instance()



def get_face_encodings(face):
    # scale pixel values
    face = face.astype('float32')
    # standardization
    mean, std = face.mean(), face.std()
    face = (face-mean)/std
    # transfer face into one sample (3 dimension to 4 dimension)
    sample = np.expand_dims(face, axis=0)
    # make prediction to get embedding
    yhat = facenet.model.predict(sample)
    return yhat[0]


def base64_to_nparray(image_url):
    '''takes base64 url and returns numpy array with resembels the face image'''
    image_data = re.sub('^data:image/.+;base64,', '', image_url)
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    image = image.convert('RGB')
    image = image.resize((160, 160))
    image = np.asarray(image)
    return image


def findCosineDistance(a, b):
    x = np.dot(np.transpose(a),b)
    y = np.dot(np.transpose(a),a)
    z = np.dot(np.transpose(b),b)
    return (1 - (x / (np.sqrt(y) * np.sqrt(z))))


def save_encodings(username,encodings):
    face_encodings = None
    with open('face_encodings.dat',"rb") as file:
        face_encodings = pickle.load(file)    
    face_encodings[username] =  encodings
    with open("face_encodings.dat","wb") as file:
        pickle.dump(face_encodings,file)


def verify_encodings(username,encodings):
    our_encodings = None
    with open('face_encodings.dat',"rb") as file:
        face_encodings = pickle.load(file)
        our_encodings = face_encodings[username]
    dist = findCosineDistance(our_encodings,encodings)
    if(dist > 0.6):
        return True
    else:
        return False


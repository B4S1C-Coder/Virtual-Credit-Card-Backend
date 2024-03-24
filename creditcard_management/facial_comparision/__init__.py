import cv2
import os
import numpy as np
from numpy.linalg import norm
from typing import Any
from tensorflow.keras.models import load_model
from tensorflow.keras import Model
from tensorflow.keras.applications.inception_resnet_v2 import preprocess_input
from .architecture import InceptionResNetV2

# The pre-trained model has been taken from:
# https://github.com/R4j4n/Face-recognition-Using-Facenet-On-Tensorflow-2.X/tree/master

def InceptionResNetV2_FeatureExtractor_FaceNet() -> Any:
    # Inception ResNet V2 model (FaceNet)
    weights_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            "facenet_keras_weights.h5")
    InceptionResNetV2_Model = InceptionResNetV2()
    InceptionResNetV2_Model.load_weights(weights_path)

    # removing the classification block
    desired_layers = InceptionResNetV2_Model.layers[:-4]
    # FaceNet feature extractor
    InceptionResNetV2_FeatureExtractor = Model(inputs=InceptionResNetV2_Model.input,
                                    outputs=desired_layers[-1].output)
    
    return InceptionResNetV2_FeatureExtractor

def cosine_similiarity(face_array_1: Any, face_array_2: Any) -> Any:
    face_array_1 = np.reshape(face_array_1, -1)
    face_array_2 = np.reshape(face_array_2, -1)
    cosine = np.dot(face_array_1, face_array_2)/(norm(face_array_1)*norm(face_array_2))
    return cosine

def extract_faces(image_path: str) -> Any:
    """ Extracts the face out of a given image and returns it as a numpy array """
    print("image_path: ", image_path)
    image = cv2.imread(image_path)
    print(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    face_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    faces = face_classifier.detectMultiScale(image, scaleFactor=1.1,
                        minNeighbors=5, minSize=(40, 40))

    face_image = []
    for (x, y, w, h) in faces:
        face = image[y:y + h, x:x + w]
        face = cv2.resize(face, (160, 160))
        face_image.append(face)

    return face_image

def verify_faces(image_path_1: str, image_path_2: str, model: Any) -> float:
    face_1, face_2 = extract_faces(image_path_1), extract_faces(image_path_2)
    
    # We can utilize tensorflow's built-in preprocess_input for inception resnet v2
    face_1 = preprocess_input(np.expand_dims(face_1[0], axis=0))
    face_2 = preprocess_input(np.expand_dims(face_2[0], axis=0))

    features_1, features_2 = model.predict(face_1), model.predict(face_2)
    similarity = float(cosine_similiarity(features_1, features_2))

    return similarity
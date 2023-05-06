import cv2
import numpy as np
from mtcnn import MTCNN

# MTCNN parameters for easier tweaking
MIN_FACE_SIZE = 30
SCALE_FACTOR = 0.709
STEPS_THRESHOLD = [0.6, 0.7, 0.7]
CONFIDENCE_THRESHOLD = 0.99

# Initialize gender detection model
gender_proto = "models/deploy.prototxt"
gender_model = "models/gender_net.caffemodel"
gender_list = ['Male', 'Female']
gender_net = cv2.dnn.readNet(gender_model, gender_proto)

def predict_gender(net, face_image):
    blob = cv2.dnn.blobFromImage(face_image, 1.0, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)
    net.setInput(blob)
    gender_preds = net.forward()
    gender = gender_list[gender_preds[0].argmax()]
    return gender

def detect_faces_and_gender(image):
    # Initialize MTCNN with custom parameters
    detector = MTCNN(min_face_size=MIN_FACE_SIZE, 
                     scale_factor=SCALE_FACTOR, 
                     steps_threshold=STEPS_THRESHOLD)
    
    faces = detector.detect_faces(image)

    face_gender_data = []
    for face in faces:
        confidence = face['confidence']
        if confidence >= CONFIDENCE_THRESHOLD:
            bounding_box = face['box']
            keypoints = face['keypoints']

            x, y, w, h = bounding_box
            face_image = image[y:y+h, x:x+w]
            gender = predict_gender(gender_net, face_image)  # Use the predict_gender function to detect gender

            face_data = {
                'bounding_box': bounding_box,
                'keypoints': keypoints,
                'gender': gender,
                'confidence': confidence
            }
            face_gender_data.append(face_data)

    return face_gender_data

import cv2
import numpy as np

# Initialize face detection model
face_proto = "models/res10_300x300_ssd_deploy.prototxt"
face_model = "models/res10_300x300_ssd_iter_140000.caffemodel"
face_net = cv2.dnn.readNet(face_model, face_proto)

# Initialize gender detection model
gender_proto = "models/deploy.prototxt"
gender_model = "models/gender_net.caffemodel"
gender_list = ['Male', 'Female']
gender_net = cv2.dnn.readNet(gender_model, gender_proto)

FACE_CONFIDENCE_THRESHOLD = 0.5
GENDER_CONFIDENCE_THRESHOLD = 0.985

def predict_gender(net, face_image):
    blob = cv2.dnn.blobFromImage(face_image, 1.0, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)
    net.setInput(blob)
    gender_preds = net.forward()
    max_index = gender_preds[0].argmax()
    gender = gender_list[max_index]
    confidence = gender_preds[0][max_index]

    return gender, confidence

def detect_faces_and_gender(image):
    h, w = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0), False, False)
    face_net.setInput(blob)
    detections = face_net.forward()

    face_gender_data = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence >= FACE_CONFIDENCE_THRESHOLD:
            x1 = int(detections[0, 0, i, 3] * w)
            y1 = int(detections[0, 0, i, 4] * h)
            x2 = int(detections[0, 0, i, 5] * w)
            y2 = int(detections[0, 0, i, 6] * h)

            bounding_box = (x1, y1, x2 - x1, y2 - y1)
            face_image = image[y1:y2, x1:x2]
            gender, gender_confidence = predict_gender(gender_net, face_image)

            # Set gender to "Unknown" if gender confidence is below threshold
            if gender_confidence < GENDER_CONFIDENCE_THRESHOLD:
                gender = "Unknown"

            face_data = {
                'bounding_box': bounding_box,
                'gender': gender,
                'confidence': confidence,
                'gender_confidence': gender_confidence
            }
            face_gender_data.append(face_data)

    return face_gender_data
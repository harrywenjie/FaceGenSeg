import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox

def detect_faces_and_gender(image):
    faces, _ = cv.detect_face(image)
    face_gender_data = []

    for face in faces:
        start_x, start_y, end_x, end_y = face
        face_crop = image[start_y:end_y, start_x:end_x]
        
        label, confidence = cv.detect_gender(face_crop)
        idx = confidence.index(max(confidence))
        gender = label[idx]

        face_data = {
            'bounding_box': [start_x, start_y, end_x - start_x, end_y - start_y],
            'gender': gender
        }
        face_gender_data.append(face_data)

    return face_gender_data

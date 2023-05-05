import cv2
from mtcnn import MTCNN

def detect_faces_and_gender(image):
    detector = MTCNN()
    faces = detector.detect_faces(image)

    face_gender_data = []
    for face in faces:
        bounding_box = face['box']
        keypoints = face['keypoints']
        gender = face.get('attributes', {}).get('gender', 'unknown')

        face_data = {
            'bounding_box': bounding_box,
            'keypoints': keypoints,
            'gender': gender
        }
        face_gender_data.append(face_data)

    return face_gender_data
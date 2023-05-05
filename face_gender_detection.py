import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox

def detect_faces_and_gender(image):
    faces, confidences = cv.detect_face(image)
    face_gender_data = []

    padding = 20

    for i, face in enumerate(faces):
        startX, startY, endX, endY = face
        startX, startY = max(0, startX - padding), max(0, startY - padding)
        endX, endY = min(image.shape[1] - 1, endX + padding), min(image.shape[0] - 1, endY + padding)

        face_crop = image[startY:endY, startX:endX]

        label, confidence = cv.detect_gender(face_crop)
        idx = confidence.index(max(confidence))
        gender = label[idx]

        face_data = {
            'bounding_box': [startX, startY, endX - startX, endY - startY],
            'gender': gender
        }
        face_gender_data.append(face_data)

        print(f"Face {i + 1}:")
        print(f"  Bounding box: {face_data['bounding_box']}")
        print(f"  Gender: {face_data['gender']}")

    return face_gender_data

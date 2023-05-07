import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis

# Initialize InsightFace gender-age model
model_pack_name = 'buffalo_l'
app = FaceAnalysis(name=model_pack_name, allowed_modules=['detection', 'genderage'])
app.prepare(ctx_id=-1, det_size=(640, 640))

def detect_faces_and_gender(image):
    faces = app.get(image)

    face_gender_data = []
    for face in faces:
        bbox = face.bbox.astype(int).flatten()
        x1, y1, x2, y2 = bbox
        bounding_box = (x1, y1, x2 - x1, y2 - y1)
        
        print(f"face.sex: {face.sex}")  # Print the actual value of face.sex

        gender = "Male" if face.sex == "M" else "Female"

        face_data = {
            'bounding_box': bounding_box,
            'gender': gender,
            'confidence': face.det_score,
        }
        face_gender_data.append(face_data)

    return face_gender_data

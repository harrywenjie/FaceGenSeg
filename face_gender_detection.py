import cv2
from mtcnn import MTCNN

# MTCNN parameters for easier tweaking
MIN_FACE_SIZE = 20
SCALE_FACTOR = 0.709
STEPS_THRESHOLD = [0.6, 0.7, 0.7]
CONFIDENCE_THRESHOLD = 0.99

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
            gender = face.get('attributes', {}).get('gender', 'unknown')

            face_data = {
                'bounding_box': bounding_box,
                'keypoints': keypoints,
                'gender': gender,
                'confidence': confidence  # Add this line to include the confidence in face_data
            }
            face_gender_data.append(face_data)

    return face_gender_data

import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from insightface.utils import get_model_dir

# Import required classes and functions from mask_renderer.py
from insightface.app import MaskRenderer, cv2, ins_get_image

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

        gender = "Male" if face.sex == "M" else "Female"

        face_data = {
            'bounding_box': bounding_box,
            'gender': gender,
            'confidence': face.det_score,
        }
        face_gender_data.append(face_data)

    return face_gender_data

def create_face_mask(image):
    # Initialize MaskRenderer
    mask_renderer = MaskRenderer(name=model_pack_name, insfa=app)
    mask_renderer.prepare(det_size=(640, 640))

    # Build mask parameters
    mask_params = mask_renderer.build_params(image)
    if mask_params is None:
        return None

    # Render white mask on face
    mask_output = mask_renderer.render_mask(image, 'mask_white', mask_params)

    # Create black background for mask
    height, width, _ = image.shape
    mask_background = np.zeros((height, width), dtype=np.uint8)

    # Convert white mask to grayscale and threshold it
    gray_mask = cv2.cvtColor(mask_output, cv2.COLOR_BGR2GRAY)
    _, binary_mask = cv2.threshold(gray_mask, 0, 255, cv2.THRESH_BINARY)

    # Combine mask and black background
    face_segmentation_mask = cv2.bitwise_or(mask_background, binary_mask)

    return face_segmentation_mask

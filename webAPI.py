from fastapi import FastAPI, File, UploadFile
from face_gender_detection import detect_faces_and_gender
from face_segmentation import setup_bisenet, segment_face
import cv2
import numpy as np

app = FastAPI()

# Set up BiSeNet for face segmentation
bisenet_model = setup_bisenet()

@app.post("/process_image/")
async def process_image(image: UploadFile = File(...)):
    image_data = await image.read()
    nparr = np.frombuffer(image_data, np.uint8)
    input_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Detect faces and gender
    face_gender_data = detect_faces_and_gender(input_image)

    results = []

    for i, face_data in enumerate(face_gender_data):
        bounding_box = face_data['bounding_box']
        x, y, w, h = bounding_box
        face_image = input_image[y:y+h, x:x+w]

        # Segment face using BiSeNet
        face_mask = segment_face(bisenet_model, face_image)

        # Save face mask
        mask_filename = f"face_mask_{i}.png"
        cv2.imwrite(mask_filename, face_mask)

        # Print face and gender information
        face_info = {
            "face_id": i + 1,
            "bounding_box": bounding_box,
            "gender": face_data['gender'],
            "mask_filename": mask_filename
        }

        results.append(face_info)

    return {"results": results}
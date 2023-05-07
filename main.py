import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
import cv2
import argparse
from face_gender_detection import detect_faces_and_gender
from face_segmentation import setup_bisenet, segment_face

def main(input_path):
    image = cv2.imread(input_path)

    # Extract original file name without extension
    original_name = os.path.splitext(os.path.basename(input_path))[0]

    # Detect faces and gender
    face_gender_data = detect_faces_and_gender(image)

    # Set up BiSeNet for face segmentation
    bisenet_model = setup_bisenet()

    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)

    for i, face_data in enumerate(face_gender_data):
        bounding_box = face_data['bounding_box']
        x, y, w, h = bounding_box

        # Increase the size of the bounding box by a small factor
        scale_factor = 1.8
        new_w = int(w * scale_factor)
        new_h = int(h * scale_factor)
        new_x = max(0, x - (new_w - w) // 2)
        new_y = max(0, y - (new_h - h) // 2)

        new_bounding_box = (new_x, new_y, new_w, new_h)

        face_image = image[new_y:new_y+new_h, new_x:new_x+new_w]

        # Segment face using BiSeNet
        face_mask = segment_face(bisenet_model, image, face_image, new_bounding_box)

        # Save face mask with the specified format
        gender_letter = 'f' if face_data['gender'] == 'Female' else ('m' if face_data['gender'] == 'Male' else 'u')
        mask_filename = os.path.join(output_dir, f"{original_name}_mask_{gender_letter}_{i + 1}.png")
        cv2.imwrite(mask_filename, face_mask)

        # Print face and gender information
        print(f"Face {i + 1}:")
        print(f"  Bounding box: {bounding_box}")
        print(f"  Gender: {face_data['gender']}")
        # print(f"  Gender Confidence: {face_data['gender_confidence']}")  # Uncomment this line if you have gender confidence
        print(f"  Confidence: {face_data['confidence']}")
        print(f"  Mask saved as: {mask_filename}")

    print("Processing complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FaceGenSeg - Face detection, gender detection, and face segmentation")
    parser.add_argument("input_path", help="Path to the input image")

    args = parser.parse_args()

    print("Welcome to FaceGenSeg!")
    print("This program performs face detection, gender detection, and face segmentation.")
    main(args.input_path)

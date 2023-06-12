##main.py

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
import cv2
import argparse
import numpy as np
from face_gender_detection import detect_faces_and_gender
from face_segmentation import setup_bisenet, segment_face_with_check

filetype = 'jpg'  #use jpg or png

def main(input_path, dilation_pixels, feather_amount, face_classes, exclude_classes, add_original_mask):
    image = cv2.imread(input_path)

    # Extract original file name without extension
    original_name = os.path.splitext(os.path.basename(input_path))[0]

    # Detect faces and gender
    face_gender_data = detect_faces_and_gender(image)

    # Sort face_gender_data by confidence value in descending order
    face_gender_data.sort(key=lambda x: x['confidence'], reverse=True)

    # Set up BiSeNet for face segmentation
    bisenet_model = setup_bisenet()

    output_dir = 'static'
    os.makedirs(output_dir, exist_ok=True)

    for i, face_data in enumerate(face_gender_data):
        bounding_box = face_data['bounding_box']
        x, y, w, h = bounding_box

        # Increase the size of the bounding box by different factors for width and height
        scale_factor_w = 1.4  # Scale factor for width
        scale_factor_h = 1.5  # Scale factor for height
        new_w = int(w * scale_factor_w)
        new_h = int(h * scale_factor_h)
        new_x = max(0, x - (new_w - w) // 2)
        new_y = max(0, y - (new_h - h) // 2)

        new_bounding_box = (new_x, new_y, new_w, new_h)

        face_image = image[new_y:new_y+new_h, new_x:new_x+new_w]

        # Segment face using BiSeNet
        face_mask, segmentation_success = segment_face_with_check(bisenet_model, image, face_image, new_bounding_box, dilation_pixels, feather_amount, face_classes, exclude_classes, add_original_mask)

        # Save face mask with the specified format
        gender_letter = 'f' if face_data['gender'] == 'Female' else ('m' if face_data['gender'] == 'Male' else 'u')
        mask_status = "mask" if segmentation_success else "failed"
        mask_filename = os.path.join(output_dir, f"{original_name}_{mask_status}_{gender_letter}_{i + 1}.{filetype}")  # Use filetype variable
        cv2.imwrite(mask_filename, face_mask)


        # Add mask_filename and bbox_mask_filename to face_data
        face_data['mask_fileurl'] = f"{original_name}_{mask_status}_{gender_letter}_{i + 1}.{filetype}"  # Use filetype variable

        # Print face and gender information
        print(f"Face {i + 1}:")
        print(f"  Bounding box: {bounding_box}")
        print(f"  Gender: {face_data['gender']}")
        print(f"  Confidence: {face_data['confidence']}")
        print(f"  Mask saved as: {mask_filename}")

    print("Processing complete!")
    return face_gender_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FaceGenSeg - Face detection, gender detection, and face segmentation")
    parser.add_argument("input_path", help="Path to the input image")

    args = parser.parse_args()

    print("Welcome to FaceGenSeg!")
    print("This program performs face detection, gender detection, and face segmentation.")
    main(args.input_path)
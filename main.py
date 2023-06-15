##main.py

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
import cv2
import argparse
import numpy as np
from face_gender_detection import detect_faces_and_gender
from face_segmentation import setup_bisenet, segment_face

filetype = 'jpg'  #use jpg or png

def main(
        input_path, dilation_pixels, feather_amount, face_classes, exclude_classes, add_original_mask, threshold,
        dilation_pixels_B, feather_amount_B, add_original_mask_B, iterationsA, iterationsB, scale_factor_w = 1.4, scale_factor_h = 1.5
    ):
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
        new_w = int(w * scale_factor_w)
        new_h = int(h * scale_factor_h)
        new_x = max(0, x - (new_w - w) // 2)
        new_y = max(0, y - (new_h - h) // 2)

        new_bounding_box = (new_x, new_y, new_w, new_h)

        face_image = image[new_y:new_y+new_h, new_x:new_x+new_w]

        # Segment face using BiSeNet
        face_mask, segmentation_success, nonzero_pixels, box_pixels, image_pixels, percentage , box_width , box_height = segment_face(
            bisenet_model, image, face_image, new_bounding_box, dilation_pixels, feather_amount, face_classes, exclude_classes, add_original_mask, threshold,
            dilation_pixels_B, feather_amount_B, add_original_mask_B, iterationsA, iterationsB
        )

        # Convert numpy data types to native Python data types
        nonzero_pixels = int(nonzero_pixels)
        box_pixels = int(box_pixels)
        image_pixels = int(image_pixels)
        percentage = float(percentage)
        box_width = int(box_width)
        box_height = int(box_height)

        padding = int(box_width/1.3)

        # Save face mask with the specified format
        gender_letter = 'f' if face_data['gender'] == 'Female' else ('m' if face_data['gender'] == 'Male' else 'u')
        mask_status = "mask" if segmentation_success else "failed"
        filename = f"{original_name}_{mask_status}_{gender_letter}_{i + 1}.{filetype}"
        localpath = os.path.join(output_dir, filename)  
        cv2.imwrite(localpath, face_mask)


        # Add mask_filename, bbox_mask_filename, and pixel data to face_data
        face_data['mask_filename'] = filename  
        face_data['segmentation_success'] = segmentation_success
        face_data['nonzero_pixels'] = nonzero_pixels
        face_data['box_pixels'] = box_pixels
        face_data['image_pixels'] = image_pixels
        face_data['percentage'] = percentage
        face_data['box_width'] = box_width
        face_data['box_height'] = box_height
        face_data['padding'] = padding
        # Convert numpy.int64 in bounding_box to int
        face_data['bounding_box'] = tuple(int(x) for x in face_data['bounding_box'])        
        # Convert numpy.float32 to float
        face_data['confidence'] = float(face_data['confidence'])

        # Print face and gender information
        print(f"Face {i + 1}:")
        print(f"  Bounding box: {bounding_box}")
        print(f"  Gender: {face_data['gender']}")
        print(f"  Confidence: {face_data['confidence']}")
        print(f"  Mask saved as: {localpath}")

    print("Processing complete!")

    for face_data in face_gender_data:
        for key, value in face_data.items():
            print(f"{key}: {type(value)}")

    return face_gender_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FaceGenSeg - Face detection, gender detection, and face segmentation")
    parser.add_argument("input_path", help="Path to the input image")

    args = parser.parse_args()

    print("Welcome to FaceGenSeg!")
    print("This program performs face detection, gender detection, and face segmentation.")
    main(args.input_path)
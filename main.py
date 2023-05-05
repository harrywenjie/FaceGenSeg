import cv2
import argparse
from face_gender_detection import detect_faces_and_gender
from face_segmentation import setup_bisenet, segment_face

def main(input_path):
    image = cv2.imread(input_path)

    # Detect faces and gender
    face_gender_data = detect_faces_and_gender(image)

    # Set up BiSeNet for face segmentation
    bisenet_model = setup_bisenet()

    for i, face_data in enumerate(face_gender_data):
        bounding_box = face_data['bounding_box']
        x, y, w, h = bounding_box
        face_image = image[y:y+h, x:x+w]

        # Segment face using BiSeNet
        face_mask = segment_face(bisenet_model, face_image)

        # Save face mask
        mask_filename = f"face_mask_{i}.png"
        cv2.imwrite(mask_filename, face_mask)

        # Print face and gender information
        print(f"Face {i + 1}:")
        print(f"  Bounding box: {bounding_box}")
        print(f"  Gender: {face_data['gender']}")
        print(f"  Mask saved as: {mask_filename}")

    print("Processing complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FaceGenSeg - Face detection, gender detection, and face segmentation")
    parser.add_argument("input_path", help="Path to the input image")

    args = parser.parse_args()

    print("Welcome to FaceGenSeg!")
    print("This program performs face detection, gender detection, and face segmentation.")
    main(args.input_path)
##face_segmentation.py

import cv2
import torch
import numpy as np
import math
from PIL import Image
from torchvision import transforms
from face_parsing_PyTorch.model import BiSeNet
import matplotlib.pyplot as plt

def setup_bisenet(pretrained_model_path='face_parsing_PyTorch/res/cp/79999_iter.pth'):
    net = BiSeNet(n_classes=19)
    net.load_state_dict(torch.load(pretrained_model_path, map_location=torch.device('cpu')))
    net.eval()

    return net

#Add dilation pixels here,currently at 5, this is a pixel matrix
# 1-Face, 2-Left Eye Brow, 3-Right Eye Brow, 4-Left Eye, 5-Right Eye, 6-Glass, 7-l ear, 8-r ear, 9-ear ring, 10-nose, 11-teeth, 12-upper lip, 13-lower lip, 14-neck, 15-necklace, 16-Cloth, 17-Hair, 18-Hat
def segment_face(net, input_image, face_image, bounding_box, dilation_pixels=5, feather_amount=5, face_classes=[1,2,3,4,5,6,10,11,12,13], exclude_classes=[7,8,9,17], add_original_mask=True):
    to_tensor = transforms.Compose([
        transforms.Resize((512, 512), Image.BILINEAR),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    with torch.no_grad():
        img = Image.fromarray(cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB))
        img_tensor = to_tensor(img).unsqueeze(0)
        out = net(img_tensor)[0]

    parsing = out.squeeze(0).cpu().numpy().argmax(0)
    resized_parsing = cv2.resize(parsing, (face_image.shape[1], face_image.shape[0]), interpolation=cv2.INTER_NEAREST)

    # Create a binary mask with only face area (excluding hair)
    binary_mask = np.zeros_like(resized_parsing)    

    # Create a separate mask for the ear and hair
    exclude_mask = np.zeros_like(resized_parsing)

    # exclude classes
    for exclude_class in exclude_classes:
        exclude_mask[resized_parsing == exclude_class] = 255
    # Face classes 
    for face_class in face_classes:
        binary_mask[resized_parsing == face_class] = 255

    binary_mask = binary_mask.astype(np.uint8)  # Ensure binary_mask is uint8
    exclude_mask = exclude_mask.astype(np.uint8)  # Ensure ear_hair_mask is uint8

    # Save the original mask before dilation
    original_mask = binary_mask.copy()

    # Dilate the binary mask if dilation_pixels > 0
    if dilation_pixels > 0:
        kernel = np.ones((dilation_pixels, dilation_pixels), np.uint8)
        binary_mask = cv2.dilate(binary_mask, kernel, iterations=1)


    # Multiply feather_amount and round up to the nearest odd number
    feather_amount = int(math.ceil((feather_amount * 10) / 2.) * 2 - 1)

    # Apply a blur to the binary mask to create a feathering effect
    binary_mask = cv2.GaussianBlur(binary_mask, (feather_amount, feather_amount), 0)

    # Add the original mask back to the blurred mask
    if add_original_mask:
        binary_mask = cv2.bitwise_or(binary_mask, original_mask)

    # Subtract the exclude mask from the binary mask
    binary_mask = cv2.bitwise_and(binary_mask, cv2.bitwise_not(exclude_mask))

    # Create an empty mask with the same size as the input image
    full_mask = np.zeros((input_image.shape[0], input_image.shape[1]), dtype=np.uint8)

    # Place the binary mask on the full mask using the bounding box coordinates
    x, y, w, h = bounding_box
    y1, y2 = y, y + h
    x1, x2 = x, x + w
    y1_binary, y2_binary = 0, h
    x1_binary, x2_binary = 0, w

    full_mask[y1:y2, x1:x2] = binary_mask[y1_binary:y2_binary, x1_binary:x2_binary]

    return full_mask

def mask_percentage(full_mask, bounding_box):
    x, y, w, h = bounding_box
    cropped_mask = full_mask[y:y + h, x:x + w]
    nonzero_pixels = np.count_nonzero(cropped_mask)
    total_pixels = w * h
    return (nonzero_pixels / total_pixels) * 100

#Set threshold for segmentation success or fail here, remember we have a boundingbox scale factor currently at 1.4W 1.5H in main.py
def segment_face_with_check(net, input_image, face_image, bounding_box, dilation_pixels, feather_amount, face_classes, exclude_classes, add_original_mask, threshold=10):
    full_mask = segment_face(net, input_image, face_image, bounding_box, dilation_pixels, feather_amount, face_classes, exclude_classes, add_original_mask)
    percentage = mask_percentage(full_mask, bounding_box)
    if percentage >= threshold:
        success = True
    else:
        success = False

    return full_mask, success

import cv2
import torch
import numpy as np
from PIL import Image
from torchvision import transforms
from face_parsing_PyTorch.model import BiSeNet
import matplotlib.pyplot as plt

def setup_bisenet(pretrained_model_path='face_parsing_PyTorch/res/cp/79999_iter.pth'):
    net = BiSeNet(n_classes=19)
    net.load_state_dict(torch.load(pretrained_model_path, map_location=torch.device('cpu')))
    net.eval()

    return net

def segment_face(net, input_image, face_image, bounding_box):
    to_tensor = transforms.Compose([
        transforms.Resize((512, 512)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
    ])

    with torch.no_grad():
        img = Image.fromarray(cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB))
        img_tensor = to_tensor(img).unsqueeze(0)
        out = net(img_tensor)[0]

    parsing = out.squeeze(0).cpu().numpy().argmax(0)
    resized_parsing = cv2.resize(parsing, (face_image.shape[1], face_image.shape[0]), interpolation=cv2.INTER_NEAREST)

    # Create a binary mask with only face area (excluding hair)
    binary_mask = np.zeros_like(resized_parsing)
    face_classes = [1,2,3,4,5,6,7,8,9,10,11,12,13]  # Face-related classes

    # 1-Face, 2-Left Eye Brow, 3-Right Eye Brow, 4-Left Eye, 5-Right Eye, 6-Glass, 7-l ear, 8-r ear, 9-ear ring, 10-nose, 11-teeth, 12-upper lip, 13-lower lip, 14-neck, 15-necklace, 16-Cloth, 17-Hair, 18-Hat

    for face_class in face_classes:
        binary_mask[resized_parsing == face_class] = 255

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

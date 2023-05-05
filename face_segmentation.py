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

def segment_face(net, face_image):
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

    plt.imshow(resized_parsing)
    plt.show()
    return resized_parsing

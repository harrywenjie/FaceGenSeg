# FaceGenSeg

FaceGenSeg is a powerful tool that performs face detection, gender detection, and face segmentation on images. The program utilizes OpenCV, BiSeNet, and a pre-trained model for gender detection. FaceGenSeg comes in two versions: an API version (main.py) and a GUI version (main_GUI.py).

## Installation

1. Install python 3.10.6


2. Make sure venv pacakge is installed
```bash
sudo apt install python3.10-venv
```

2. Clone this repository:

3. Change to the project directory:

```bash
cd FaceGenSeg
```

3. Create a Python virtual environment:

```bash
python3 -m venv venv
```

4. Activate the virtual environment:

```bash
source venv/bin/activate
```

5. Install the required packages:

```bash
pip install -r requirements.txt
```

6. Install the `tkinter` package for your system's Python installation (required for the GUI version):

```bash
sudo apt-get install python3.10-tk
```
## Usage

### API Version

1. Run the main script by passing the image path as an argument:

python main.py --input_path /path/to/your/image.jpg


2. The script will detect faces, determine their gender, and perform face segmentation. The segmented face masks will be saved as `face_mask_X.png` in the current directory, where `X` is the face number.

### GUI Version

1. Run the main_GUI.py script:

2. A graphical interface will open. Click the "Browse" button to select an image from your computer.

3. After selecting an image, click the "Process" button to start processing the image. The script will detect faces, determine their gender, and perform face segmentation.

4. The segmented face masks will be saved as `face_mask_X.png` in the current directory, where `X` is the face number.

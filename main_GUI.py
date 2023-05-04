import tkinter as tk
from tkinter import filedialog
from main_API import main

def open_image():
    file_path = filedialog.askopenfilename(title="Select an image",
                                           filetypes=(("PNG files", "*.png"),
                                                      ("JPEG files", "*.jpg;*.jpeg"),
                                                      ("All files", "*.*")))
    if file_path:
        main(file_path)

root = tk.Tk()
root.title("FaceGenSeg - Face detection, gender detection, and face segmentation")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)

welcome_label = tk.Label(frame, text="Welcome to FaceGenSeg!")
welcome_label.pack(pady=(0, 20))

instructions_label = tk.Label(frame, text="Click the button below to select an image for processing.")
instructions_label.pack(pady=(0, 20))

open_image_button = tk.Button(frame, text="Open Image", command=open_image)
open_image_button.pack()

root.mainloop()

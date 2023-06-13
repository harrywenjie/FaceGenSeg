##webGUI.py

from flask import Flask, render_template, request, redirect, send_from_directory
import os
from main import main as process_image

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["OUTPUT_FOLDER"] = "output"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["OUTPUT_FOLDER"], exist_ok=True)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, ''),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        # Get data from the form
        dilation_pixels = int(request.form.get('dilation_pixels', 5)) 
        dilation_pixels_B = int(request.form.get('dilation_pixels_B', 5)) 
        dilation_pixels_C = int(request.form.get('dilation_pixels_C', 5)) 
        feather_amount = int(request.form.get('feather_amount', 5))
        feather_amount_B = int(request.form.get('feather_amount_B', 5))
        feather_amount_C = int(request.form.get('feather_amount_C', 5))
        face_classes = request.form.getlist('face_classes')
        exclude_classes = request.form.getlist('exclude_classes')
        include_classes = request.form.getlist('include_classes')
        add_original_mask = 'add_original_mask' in request.form
        add_original_mask_B = 'add_original_mask_B' in request.form
        add_original_mask_C = 'add_original_mask_C' in request.form
        threshold = float(request.form.get('threshold', 10))

        # Convert to integers
        face_classes = [int(face_class) for face_class in face_classes]
        exclude_classes = [int(exclude_class) for exclude_class in exclude_classes]
        include_classes = [int(include_class) for include_class in include_classes]

        if file.filename == "":
            return redirect(request.url)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)
        result_data = process_image(
            file_path, dilation_pixels, feather_amount, face_classes, exclude_classes, include_classes, add_original_mask, threshold, 
            dilation_pixels_B, dilation_pixels_C, feather_amount_B, feather_amount_C, add_original_mask_B, add_original_mask_C
        )  # Pass feather_amount to process_image
        os.remove(file_path)
        return render_template("index.html", result_data=result_data)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5500, debug=False)
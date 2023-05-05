from flask import Flask, render_template, request, send_from_directory
import os
import main_API

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"

        file = request.files["file"]
        if file.filename == "":
            return "No selected file"

        file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
        input_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        main_API.main(input_path)
        return send_from_directory(app.config["UPLOAD_FOLDER"], "face_mask_0.png", as_attachment=True)

    return """
    <!doctype html>
    <title>FaceGenSeg</title>
    <h1>FaceGenSeg - Face detection, gender detection, and face segmentation</h1>
    <p>Welcome to FaceGenSeg! Please upload an image to process.</p>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

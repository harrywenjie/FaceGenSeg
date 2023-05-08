from flask import Flask, render_template, request, redirect, url_for
import os
from main import main as process_image

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["OUTPUT_FOLDER"] = "output"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["OUTPUT_FOLDER"], exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        result_data = process_image(file_path)

        os.remove(file_path)

        return render_template("index.html", result_data=result_data)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5500, debug=False)

##webAPI.py

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import os
#import uuid
from main import main as process_image

app = FastAPI()

@app.post("/process/")
async def process_image_endpoint(file: UploadFile = File(...)):
    try:
        # Save the uploaded file to a temporary directory
        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)
        # unique_filename = f"{uuid.uuid4()}_{file.filename}"
        # temp_file_path = os.path.join(temp_dir, unique_filename)

        #uuid should be handled by up stream data
        temp_file_path = os.path.join(temp_dir, file.filename)

        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process the image
        process_image(temp_file_path)

        # Remove the temporary file after processing
        os.remove(temp_file_path)

        return JSONResponse(content={"status": "success", "message": "Image processed successfully."})

    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8800)

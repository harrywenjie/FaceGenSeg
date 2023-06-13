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

        # API版本直接在这里改参数，省事
        dilation_pixels = 5
        feather_amount = 5
        face_classes = [1,2,3,4,5,6,10,11,12,13]
        exclude_classes = [7,8,9,17]
        add_original_mask = True
        threshold = 10
        dilation_pixels_B = 5
        feather_amount_B = 5
        add_original_mask_B = True

        # Process the image
        process_image(
            temp_file_path, dilation_pixels, feather_amount, face_classes, exclude_classes, add_original_mask, threshold,
            dilation_pixels_B, feather_amount_B, add_original_mask_B
        )

        # Remove the temporary file after processing
        os.remove(temp_file_path)

        return JSONResponse(content={"status": "success", "message": "Image processed successfully."})

    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8800)

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
        #特征类对应表
        # 1-Face, 2-Left Eye Brow, 3-Right Eye Brow, 
        # 4-Left Eye, 5-Right Eye, 6-Glass, 7-l ear, 8-r ear, 9-ear ring, 
        # 10-nose, 11-teeth, 12-upper lip, 13-lower lip, 14-neck, 
        # 15-necklace, 16-Cloth, 17-Hair, 18-Hat


        # 第一层像素扩张矩阵大小
        dilation_pixels = 5
        # 第一层羽化
        feather_amount = 5
        # 第一层添加的特征类
        face_classes = [1,2,3,4,5,6,10,11,12,13]
        # 第二层减去的特征类
        exclude_classes = [7,8,9,17]
        # 第一层羽化保留遮罩
        add_original_mask = True
        # 临界值
        threshold = 10
        # 第二层像素扩张矩阵大小
        dilation_pixels_B = 5
        # 第二层羽化
        feather_amount_B = 5
        # 第二层羽化保留遮罩
        add_original_mask_B = True
        # 第一层扩张遍历次数
        iterationsA=1 
        # 第二层扩张遍历次数
        iterationsB=1
        # 识别框宽系数
        scale_factor_w = 1.4
        # 识别框高系数
        scale_factor_h = 1.5
        # 方框遮罩切换开关
        box = True


        # Process the image
        face_gender_data = process_image(
            temp_file_path, dilation_pixels, feather_amount, face_classes, exclude_classes, add_original_mask, threshold,
            dilation_pixels_B, feather_amount_B, add_original_mask_B, iterationsA, iterationsB, scale_factor_w, scale_factor_h,
            box
        )  

        # Remove the temporary file after processing
        os.remove(temp_file_path)
        
        return JSONResponse(content={"status": "success", "message": "Image processed successfully.", "data": face_gender_data})

    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)
    


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8800)

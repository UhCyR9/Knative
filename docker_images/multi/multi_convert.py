from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import StreamingResponse
from PIL import Image, ImageOps
import io
import zipfile
import asyncio

app = FastAPI()

def convert_sepia(input_image):
    sepia_image = ImageOps.colorize(ImageOps.grayscale(input_image), '#704214', '#C0A080')
    return sepia_image

@app.post("/convert/")
async def convert_image(file: UploadFile = File(...), wait: int = Query(default=None)):
    if wait:
        await asyncio.sleep(wait)

    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    gray_image = ImageOps.grayscale(image)
    sepia_image = convert_sepia(image)

    img_byte_arr = io.BytesIO()
    with zipfile.ZipFile(img_byte_arr, mode='w') as zipf:
        for img, name in zip([image, gray_image, sepia_image], ["original.jpg", "black_and_white.jpg", "sepia.jpg"]):
            img_byte_io = io.BytesIO()
            img.save(img_byte_io, format='JPEG')
            img_byte_io.seek(0)
            zipf.writestr(name, img_byte_io.read())

    img_byte_arr.seek(0)
    return StreamingResponse(img_byte_arr, media_type="application/zip", headers={"Content-Disposition": "attachment; filename=result.zip"})

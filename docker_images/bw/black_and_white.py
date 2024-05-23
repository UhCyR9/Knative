from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import StreamingResponse
from PIL import Image, ImageOps
import io
import asyncio

app = FastAPI()


@app.post("/convert/")
async def convert(file: UploadFile = File(...), wait: int = Query(default=None)):
    if wait:
        await asyncio.sleep(wait)

    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    gray_image = ImageOps.grayscale(image)
    img_byte_array = io.BytesIO()
    gray_image.save(img_byte_array, format="PNG")
    img_byte_array.seek(0)
    return StreamingResponse(img_byte_array, media_type="image/jpeg")
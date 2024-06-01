from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import StreamingResponse, HTMLResponse
from PIL import Image, ImageOps
import io
import asyncio
import requests
import base64

app = FastAPI()

def send_event(email, image_data):
    event = {
        "type": "dev.knative.email.imageprocessed",
        "source": "email/image-processor",
        "data": {
            "user_email": email,
            "image_data": image_data
        }
    }
    headers = {
        "Content-Type": "application/json",
        "Ce-Id": "image-processed",
        "Ce-Specversion": "1.0",
        "Ce-Type": "dev.knative.email.imageprocessed",
        "Ce-Source": "email/image-processor"
    }
    response = requests.post('http://broker-ingress.knative-eventing.svc.cluster.local/default/default', json=event, headers=headers)
    if response.status_code != 200:
        print(f"Failed to send event: {response.status_code}, {response.text}")

def convert_to_sepia(image: Image.Image) -> Image.Image:
    sepia_image = ImageOps.colorize(ImageOps.grayscale(image), '#704214', '#C0C080')
    return sepia_image

@app.post("/convert/")
async def convert(file: UploadFile = File(...), wait: int = Query(default=None), email: str = Query(...)):
    if wait:
        await asyncio.sleep(wait)

    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    sepia_image = convert_to_sepia(image)
    img_byte_array = io.BytesIO()
    sepia_image.save(img_byte_array, format="PNG")
    img_byte_array.seek(0)

    image_data = base64.b64encode(img_byte_array.read()).decode('utf-8')

    send_event(email, image_data)

    img_byte_array.seek(0)

    return StreamingResponse(img_byte_array, media_type="image/jpeg")


@app.get("/", response_class=HTMLResponse)
async def main():
    content = """
    <html>
        <head>
            <title>Image Converter</title>
            <script>
                async function submitForm(event) {
                    event.preventDefault();
                    const form = document.getElementById('uploadForm');
                    const formData = new FormData(form);
                    const waitValue = document.getElementById('wait').value;
                    const emailValue = document.getElementById('email').value;
                    
                    const queryChar = form.action.includes('?') ? '&' : '?';
                    const action = form.action + queryChar + 'wait=' + waitValue + '&email=' + encodeURIComponent(emailValue);
                    
                    try {
                        const response = await fetch(action, {
                            method: 'POST',
                            body: formData
                        });

                        if (response.ok) {
                            alert('POST request sent successfully!');
                        } else {
                            alert('Failed to send POST request');
                        }
                    } catch (error) {
                        console.error('Error:', error);
                        alert('An error occurred while sending POST request');
                    }
                }
            </script>
        </head>
        <body>
            <h1>Upload an Image (sepia)</h1>
            <form id="uploadForm" action="/convert" method="post" enctype="multipart/form-data" onsubmit="submitForm(event)">
                <input type="file" name="file">
                <br><br>
                <label for="wait">Wait time (seconds):</label>
                <input type="number" id="wait" name="wait">
                <br><br>
                <label for="email">Email:</label>
                <input type="email" id="email" name="email">
                <br><br>
                <input type="submit" value="Upload">
            </form>
        </body>
    </html>
    """
    return content

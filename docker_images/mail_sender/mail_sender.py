import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from fastapi import FastAPI, Request
from pydantic import BaseModel
from starlette.responses import JSONResponse
import base64

app = FastAPI()

class ImageProcessedEvent(BaseModel):
    user_email: str
    image_data: str

@app.post("/")
async def handle_event(request: Request):
    print("Received event")
    event = await request.json()
    data = ImageProcessedEvent(**event['data'])

    image_data = base64.b64decode(data.image_data)
    
    send_email(data.user_email, image_data)
    return JSONResponse(status_code=200, content={"status": "success"})

def send_email(user_email, image_data):
    msg = MIMEMultipart()
    msg['From'] = 'wojpiotr9@interia.pl'
    msg['To'] = user_email
    msg['Subject'] = 'Your Image is Ready'
    
    body = "Your processed image is ready. Please find the attachment."
    msg.attach(MIMEText(body, 'plain'))
    
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(image_data)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="processed_image.png"')
    
    msg.attach(part)
    
    server = smtplib.SMTP('mail.smtp2go.com', 2525)
    server.starttls()
    server.login('suuproject', 'SuuProject1!')
    text = msg.as_string()
    server.sendmail(msg['From'], msg['To'], text)
    server.quit()

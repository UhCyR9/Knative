FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir fastapi[all] uvicorn[standard] pillow asyncio requests

EXPOSE 8000

ENV NAME MultiConvert

CMD uvicorn multi_convert:app --host 0.0.0.0 --port 8000
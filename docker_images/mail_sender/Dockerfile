FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir fastapi[all] uvicorn[standard] pydantic requests
EXPOSE 8080
ENV NAME MailSender
CMD uvicorn mail_sender:app --host 0.0.0.0 --port 8080

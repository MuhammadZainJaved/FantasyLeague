# Dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
COPY initial_data.json /app/
RUN pip install -r requirements.txt

COPY . /app/

CMD ["./entrypoint.sh"]

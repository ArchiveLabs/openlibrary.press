FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set non-sensitive environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose ports (FastAPI, PostgreSQL, MinIO API, MinIO Console)
EXPOSE 8080 5432 9000 9001

COPY ./olp/ /app/olp/
RUN chmod +x /app/olp/app.py

RUN apt-get update && apt-get install -y nginx
RUN adduser --disabled-password --gecos "" nginx

COPY ./docker/nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./docker/nginx/conf.d/olp.conf /etc/nginx/conf.d/olp.conf

# Run FastAPI app and Nginx
CMD ["sh", "-c", "python -m uvicorn olp.app:app --host 0.0.0.0 --port 1337 --workers=${OLP_WORKERS:-1} --log-level=${OLP_LOG_LEVEL:-info} & exec nginx"]

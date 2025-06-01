FROM python:3.11
WORKDIR /app

ARG APT_MIRROR=
ARG PIP_INDEX_URL=https://pypi.org/simple

COPY requirements.txt .
RUN pip install --index-url "$PIP_INDEX_URL" --no-cache-dir -r requirements.txt;

# Set non-sensitive environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV DEBIAN_FRONTEND=noninteractive

EXPOSE 8080

COPY ./olp/ /app/olp/
RUN chmod +x /app/olp/app.py
RUN unset HTTP_PROXY HTTPS_PROXY
RUN if [ -n "$APT_MIRROR" ]; then \
        echo "deb $APT_MIRROR/debian bookworm main contrib non-free" > /etc/apt/sources.list && \
        echo "deb $APT_MIRROR/debian bookworm-updates main contrib non-free" >> /etc/apt/sources.list && \
        echo "deb $APT_MIRROR/debian-security bookworm-security main contrib non-free" >> /etc/apt/sources.list && \
        echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99no-check-valid-until && \
        apt update -o Dir::Etc::sourcelist="sources.list" -o Dir::Etc::sourceparts="-" -o APT::Get::List-Cleanup="0"; \
    else \
        apt update; \
    fi && apt install -y nginx

RUN adduser --disabled-password --gecos "" nginx

COPY ./docker/nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./docker/nginx/conf.d/olp.conf /etc/nginx/conf.d/olp.conf

# Run FastAPI app and Nginx
CMD ["sh", "-c", "python -m uvicorn olp.app:app --host 0.0.0.0 --port ${OLP_PORT} --workers=${OLP_WORKERS:-1} --log-level=${OLP_LOG_LEVEL:-info} & exec nginx"]

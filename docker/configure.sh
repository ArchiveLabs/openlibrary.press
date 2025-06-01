#!/bin/bash

ENV_FILE="olp.env"

# Exit if the file already exists
if [ -f "$ENV_FILE" ]; then
  echo "$ENV_FILE already exists. No changes made."
  exit 0
fi

# Use environment variables if they are set, otherwise provide defaults or generate secure values
HTTP_PROXY="${HTTP_PROXY:-}"
HTTPS_PROXY="${HTTPS_PROXY:-}"
NO_PROXY="${NO_PROXY:-archive.org,.archive.org}"
PIP_INDEX_URL="${PIP_INDEX_URL:-https://pypi.org/simple}"
APT_MIRROR="${APT_MIRROR:-}"
OLP_PORT="${OLP_PORT:-1337}"
OLP_DOMAIN="${APP_DOMAIN:-http://127.0.0.1:$OLP_PORT}"
OLP_HOST="${OLP_HOST:-0.0.0.0}"
OLP_WORKERS="${OLP_WORKERS:-1}"
OLP_LOG_LEVEL="${OLP_LOG_LEVEL:-\"debug\"}"
OLP_RELOAD="${OLP_RELOAD:-1}"
OLP_SSL_CRT="${OLP_SSL_CRT:-}"
OLP_SSL_KEY="${OLP_SSL_KEY:-}"

# Write to lenny.env
cat <<EOF > "$ENV_FILE"
# System Env
HTTP_PROXY=$HTTP_PROXY
HTTPS_PROXY=$HTTPS_PROXY
NO_PROXY=$NO_PROXY
PIP_INDEX_URL=$PIP_INDEX_URL
APT_MIRROR=$APT_MIRROR

# API App (FastAPI)
OLP_DOMAIN=$OLP_DOMAIN
OLP_HOST=$OLP_HOST
OLP_PORT=$OLP_PORT
OLP_WORKERS=$OLP_WORKERS
OLP_LOG_LEVEL=$OLP_LOG_LEVEL
OLP_RELOAD=$OLP_RELOAD
OLP_SSL_CRT=$OLP_SSL_CRT
OLP_SSL_KEY=$OLP_SSL_KEY

# Stripe
STRIPE_SECRET_KEY=

# IA S3 Keys
IA_ACCESS_KEY=
IA_SECRET_KEY=
EOF

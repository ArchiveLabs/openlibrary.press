#!/bin/bash

ENV_FILE="olp.env"

# Exit if the file already exists
if [ -f "$ENV_FILE" ]; then
  echo "$ENV_FILE already exists. No changes made."
  exit 0
fi

# Use environment variables if they are set, otherwise provide defaults or generate secure values
OLP_DOMAIN="${OLP_DOMAIN:-localhost}"
OLP_HOST="${OLP_HOST:-0.0.0.0}"
OLP_PORT="${OLP_PORT:-8080}"
OLP_WORKERS="${OLP_WORKERS:-1}"
OLP_LOG_LEVEL="${OLP_LOG_LEVEL:-\"debug\"}"
OLP_RELOAD="${OLP_RELOAD:-1}"
OLP_SSL_CRT="${OLP_SSL_CRT:-}"
OLP_SSL_KEY="${OLP_SSL_KEY:-}"

# Write to lenny.env
cat <<EOF > "$ENV_FILE"
# API App (FastAPI)
OLP_DOMAIN=$OLP_DOMAIN
OLP_HOST=$OLP_HOST
OLP_PORT=$OLP_PORT
OLP_WORKERS=$OLP_WORKERS
OLP_LOG_LEVEL=$OLP_LOG_LEVEL
OLP_RELOAD=$OLP_RELOAD
OLP_SSL_CRT=$OLP_SSL_CRT
OLP_SSL_KEY=$OLP_SSL_KEY
EOF

#!/usr/bin/env python

"""
    Configurations for Open Library Press

    :copyright: (c) 2015 by AUTHORS
    :license: see LICENSE for more details
"""

import os
import dotenv
from pathlib import Path
import stripe
from dotenv import load_dotenv

project_root = Path(__file__).resolve().parents[2]  # two levels up from __init__.py
env_path = project_root / 'olp.env'
load_dotenv(dotenv_path=env_path)

# Determine environment
TESTING = os.getenv("TESTING", "false").lower() == "true"

# API server configuration
HOST = os.environ.get('OLP_HOST', '0.0.0.0')
PORT = int(os.environ.get('OLP_PORT', 8080))
DOMAIN = os.environ.get('OLP_DOMAIN', f'http://127.0.0.1:{PORT}')
WORKERS = int(os.environ.get('OLP_WORKERS', 1))
DEBUG = bool(int(os.environ.get('OLP_DEBUG', 0)))

LOG_LEVEL = os.environ.get('OLP_LOG_LEVEL', 'info')
SSL_CRT = os.environ.get('OLP_SSL_CRT')
SSL_KEY = os.environ.get('OLP_SSL_KEY')

OPTIONS = {
    'host': HOST,
    'port': PORT,
    'log_level': LOG_LEVEL,
    'reload': DEBUG,
    'workers': WORKERS,
}
if SSL_CRT and SSL_KEY:
    OPTIONS['ssl_keyfile'] = SSL_KEY
    OPTIONS['ssl_certfile'] = SSL_CRT

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

IA_S3_KEYS = {
    "access": os.getenv('IA_ACCESS_KEY'),
    "secret": os.getenv('IA_SECRET_KEY')
}

__all__ = ['DOMAIN', 'HOST', 'PORT', 'DEBUG', 'OPTIONS', 'TESTING']

#!/usr/bin/env python

"""
    Configurations for Open Library Press

    :copyright: (c) 2015 by AUTHORS
    :license: see LICENSE for more details
"""

import os


# Determine environment
TESTING = os.getenv("TESTING", "false").lower() == "true"

# API server configuration
DOMAIN = os.environ.get('OLP_DOMAIN', '127.0.0.1')
HOST = os.environ.get('OLP_HOST', '0.0.0.0')
PORT = int(os.environ.get('OLP_PORT', 8080))
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


__all__ = ['DOMAIN', 'HOST', 'PORT', 'DEBUG', 'OPTIONS', 'TESTING']

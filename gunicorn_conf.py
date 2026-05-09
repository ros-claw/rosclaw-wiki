"""Gunicorn configuration for ROSClaw Wiki production deployment."""

import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
keepalive = 5
timeout = 120
graceful_timeout = 30
max_requests = 10000
max_requests_jitter = 1000
accesslog = "-"
errorlog = "-"
loglevel = "info"
preload_app = True

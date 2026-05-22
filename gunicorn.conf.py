import os


bind = f"{os.getenv('PAPER_HOST', '0.0.0.0')}:{os.getenv('PAPER_PORT', '8000')}"
workers = int(os.getenv("PAPER_GUNICORN_WORKERS", "2"))
worker_class = "uvicorn.workers.UvicornWorker"
timeout = int(os.getenv("PAPER_GUNICORN_TIMEOUT", "180"))
graceful_timeout = 30
keepalive = 10
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("PAPER_LOG_LEVEL", "info")

@'
bind = "0.0.0.0:5000"
workers = 3
worker_class = "gthread"
threads = 4
timeout = 120
preload_app = True
accesslog = "-"
errorlog = "-"
'@ | Set-Content -Encoding utf8 gunicorn.conf.py

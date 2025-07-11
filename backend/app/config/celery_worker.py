# app/config/celery_worker.py
from app.config.celery_app import celery_app

print("Registered tasks:", celery_app.tasks)  # Для отладки
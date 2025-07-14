# app/config/celery_app.py
from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_routes={"app.tasks.*": {"queue": "default"}},
)

# Автоматически загружаем задачи из модуля app.tasks
celery_app.autodiscover_tasks(['app.tasks'])
celery_app.conf.task_routes = {
    "app.tasks.generate_response_task": {"queue": "default"},
    "app.tasks.generate_response_api_task": {"queue": "api"},
}


# Явно импортируем задачи
import app.tasks
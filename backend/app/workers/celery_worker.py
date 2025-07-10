from celery import Celery
from services.ml import generate_response as call_model
import os

celery_app = Celery(
    "worker",
    broker=os.getenv("REDIS_BROKER", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_BACKEND", "redis://localhost:6379/0"),
)

@celery_app.task(name="process_llm_message")
def process_llm_message(chat_id: str, user_message: str):
    messages = [
        {"role": "user", "content": user_message}
    ]
    response = call_model(messages)
    return {"chat_id": chat_id, "response": response}

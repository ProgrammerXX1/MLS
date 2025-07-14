from app.config.celery_app import celery_app
from app.db.session import SessionLocal
from app.db.models import ChatLog
from datetime import datetime
import time
from app.services.ml import generate_response

@celery_app.task(name="app.tasks.generate_response_task")
def generate_response_task(payload: dict):
    print("Task started")
    db = SessionLocal()

    start_time = time.time()
    try:
        # Заглушка генерации ответа — здесь должна быть твоя модель
        response_text = generate_response(
        messages=payload["messages"],
        model=payload.get("model"),
        temperature=payload.get("temperature", 1.0),
        max_tokens=payload.get("max_tokens", 1024),
        stream=False,
        response_format=payload.get("response_format", "text"),
        moderation=payload.get("moderation", False),
        top_p=payload.get("top_p", 0.75),
        seed=payload.get("seed"),
        stop=payload.get("stop"),
        )
        output_tokens = len(response_text.split())  # 🔧 пример оценки
        input_tokens = sum(len(msg['content'].split()) for msg in payload["messages"])

        latency = round((time.time() - start_time) * 1000, 2)

        log = ChatLog(
            user_id=payload["user_id"],
            api_key=payload.get("api_key"),
            model_name=payload.get("model"),
            code=200,
            latency_ms=latency,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            error="-",  # нет ошибки
        )
        db.add(log)
        db.commit()

        print("Task completed")
        return {
            "response": response_text,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "latency_ms": latency
        }

    except Exception as e:
        db.rollback()
        log = ChatLog(
            user_id=payload["user_id"],
            api_key=payload.get("api_key"),
            model_name=payload.get("model"),
            code=500,
            latency_ms=0.0,
            input_tokens=0,
            output_tokens=0,
            error=str(e),
        )
        db.add(log)
        db.commit()
        raise

    finally:
        db.close()

@celery_app.task(name="app.tasks.generate_response_api_task", queue="api")
def generate_response_api_task(payload: dict):
    print("API Task started")
    db = SessionLocal()
    start_time = time.time()

    try:
        response_text = generate_response(
            messages=payload["messages"],
            model=payload.get("model"),
            temperature=payload.get("temperature", 1.0),
            max_tokens=payload.get("max_tokens", 1024),
            stream=False,
            response_format=payload.get("response_format", "text"),
            moderation=payload.get("moderation", False),
            top_p=payload.get("top_p", 0.75),
            seed=payload.get("seed"),
            stop=payload.get("stop"),
        )

        output_tokens = len(response_text.split())
        input_tokens = sum(len(m['content'].split()) for m in payload["messages"])
        latency = round((time.time() - start_time) * 1000, 2)

        log = ChatLog(
            user_id=payload["user_id"],
            api_key=payload.get("api_key"),
            model_name=payload.get("model"),
            code=200,
            latency_ms=latency,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            error="-",
        )
        db.add(log)
        db.commit()

        return {
            "response": response_text,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "latency_ms": latency
        }

    except Exception as e:
        db.rollback()
        log = ChatLog(
            user_id=payload["user_id"],
            api_key=payload.get("api_key"),
            model_name=payload.get("model"),
            code=500,
            latency_ms=0.0,
            input_tokens=0,
            output_tokens=0,
            error=str(e),
        )
        db.add(log)
        db.commit()
        raise

    finally:
        db.close()


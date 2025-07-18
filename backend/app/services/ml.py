import requests
import logging
import os
from typing import List, Dict, Optional

# Логгирование
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# ✅ Получение переменных окружения с явным требованием
try:
    OLLAMA_HOST = os.environ["PORT_SERVER"].replace("http://", "").replace("https://", "")
    OLLAMA_PORT = os.environ["OLLAMA_PORT"]
    OLLAMA_MODEL = os.environ["OLLAMA_MODEL"]
except KeyError as e:
    raise RuntimeError(f"❌ Не найдена переменная окружения: {e}")

OLLAMA_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/chat"
logger.info(f"📡 URL модели Ollama: {OLLAMA_URL}")


def generate_response(
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    temperature: Optional[float] = 1.0,
    max_tokens: Optional[int] = 1024,
    stream: Optional[bool] = False,
    response_format: Optional[str] = "text",
    moderation: Optional[bool] = False,
    top_p: Optional[float] = 0.75,
    seed: Optional[str] = None,
    stop: Optional[str] = None,
) -> str:
    """
    Отправляет список сообщений с параметрами в Ollama /api/chat
    """
    logger.info("📨 Подготовка запроса к модели...")

    for m in messages:
        logger.info(f" - {m['role']}: {m['content'][:100]}")

    payload = {
        "model": model or OLLAMA_MODEL,
        "messages": messages,
        "stream": stream,
        "options": {
            "temperature": temperature,
            "top_p": top_p,
            "num_predict": max_tokens,
        }
    }

    if seed:
        payload["options"]["seed"] = seed
    if stop:
        payload["options"]["stop"] = [stop]

    logger.info(f"🧪 Payload подготовлен:\n{payload}")

    try:
        logger.info("🚀 Выполняем запрос к модели...")
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        logger.info("✅ Запрос отправлен, получен ответ")

        logger.info(f"📥 Status code: {response.status_code}")
        logger.info(f"📥 Raw response: {response.text[:500]}")

        if response.status_code != 200:
            logger.warning(f"⚠️ Ошибка от модели: {response.status_code}, {response.text}")
            return "⚠️ Ошибка генерации ответа от модели."

        data = response.json()
        content = data.get("message", {}).get("content", "")

        if not content.strip():
            logger.warning("⚠️ Модель не вернула осмысленный ответ")
            return "⚠️ Модель не дала ответ. Попробуйте переформулировать запрос."

        logger.info(f"📤 Ответ от модели: {content[:200]}...")
        return content

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Ошибка соединения с моделью: {e}")
        return f"⚠️ Ошибка подключения к модели. Убедитесь, что сервис работает.\n\n{str(e)}"

    except Exception as e:
        logger.error(f"❌ Неизвестная ошибка генерации ответа: {e}")
        return f"⚠️ Внутренняя ошибка. Попробуйте позже.\n\n{str(e)}"

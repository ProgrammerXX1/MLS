import requests
import logging
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional

# Загрузка переменных окружения
load_dotenv()

# Настройка подключения к Ollama
OLLAMA_HOST = os.getenv("PORT_SERVER", "http://localhost").replace("http://", "").replace("https://", "")
OLLAMA_PORT = os.getenv("OLLAMA_PORT", "11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3:latest")
OLLAMA_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/chat"

# Логгирование
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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
    logger.info("📨 Отправка сообщений модели:")
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
        payload["options"]["stop"] = [stop]  # Ollama ожидает список

    logger.info(f"🧪 Payload к модели: {payload}")

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)

        if response.status_code != 200:
            logger.warning(f"⚠️ Неверный ответ от сервера: {response.status_code}, {response.text}")
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

import requests
import logging
import os
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

PORT_SERVER = os.getenv("PORT_SERVER", "http://localhost")
OLLAMA_PORT = os.getenv("OLLAMA_PORT", "11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3:latest")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def generate_response(messages: List[Dict[str, str]]) -> str:
    """
    Отправляет список сообщений с ролями (system, user, assistant) в Ollama /api/chat
    """
    logger.info("📨 Отправка сообщений модели:")
    for m in messages:
        logger.info(f" - {m['role']}: {m['content'][:100]}")

    try:
        response = requests.post(
            f"{PORT_SERVER}:{OLLAMA_PORT}/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": messages,
                "stream": False
            },
            timeout=60
        )

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

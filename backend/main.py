from fastapi import FastAPI
from app import auth
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
import subprocess
from app.routes import api_keys, chat
from db.session import engine
from alembic.config import Config
from alembic import command
import os
import logging

from dotenv import load_dotenv
load_dotenv()
PORT_SERVER = os.getenv("PORT_SERVER", "http://localhost")

app = FastAPI()
# Миграции Alembic
def run_migrations():
    try:
        logging.info("📦 Применение Alembic миграций...")
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        logging.info("✅ Alembic миграции успешно применены.")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Ошибка Alembic миграции: {e}")

# Вызов миграций до запуска приложения
run_migrations()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:3000"
],
    # allow_origins=[
    #         PORT_SERVER,
    #         f"{PORT_SERVER}:3000",
    #         f"{PORT_SERVER}:8000"
    # ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роуты
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(chat.router, tags=["Chat"])
app.include_router(api_keys.router, tags=["API Keys"])

# @app.on_event("startup")
# def list_routes():
#     print("📍 Список маршрутов:")
#     for route in app.routes:
#         print(f"➡️ {route.path}")


# OpenAPI с BearerAuth
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="ML API",
        version="1.0.1",
        description="Custom API with Bearer Auth only",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Запуск в Docker
if __name__ == "__main__":
    import uvicorn
    import os
    from dotenv import load_dotenv
    load_dotenv()  # Загрузка .env
    host = os.getenv("BACKEND_HOST", "localhost")
    port = int(os.getenv("BACKEND_PORT", 8000))
    uvicorn.run("main:app", host=host, port=port, reload=False)

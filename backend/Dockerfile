FROM nvidia/cuda:12.3.2-runtime-ubuntu22.04

# Установим системные зависимости и Python 3.11.9
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    wget \
    curl \
    software-properties-common \
    zlib1g-dev \
    libssl-dev \
    libffi-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libncursesw5-dev \
    libgdbm-dev \
    liblzma-dev \
    uuid-dev && \
    wget https://www.python.org/ftp/python/3.11.9/Python-3.11.9.tgz && \
    tar -xvf Python-3.11.9.tgz && cd Python-3.11.9 && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make install && \
    cd .. && rm -rf Python-3.11.9 Python-3.11.9.tgz && \
    rm -rf /var/lib/apt/lists/*

# Обновим альтернативы и pip
RUN update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.11 1 && \
    ln -s /usr/local/bin/pip3.11 /usr/local/bin/pip && \
    pip install --upgrade pip

# Установим рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Установим torch отдельно для кеширования слоя
RUN pip install torch==2.7.1

# Установим остальные зависимости
RUN pip install \
    fastapi \
    uvicorn[standard] \
    sqlalchemy \
    psycopg2-binary \
    python-dotenv \
    passlib[bcrypt] \
    python-jose[cryptography] \
    alembic \
    requests \
    pydantic \
    python-multipart \
    psutil \
    pynvml \
    celery \
    redis

# Копируем остальной код
COPY . .

# Открываем порт для приложения
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

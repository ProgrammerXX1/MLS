FROM node:20-alpine

# Установка зависимостей
WORKDIR /app
COPY . .

# Устанавливаем только необходимые пакеты
RUN npm install

# Сборка Nuxt в прод-режиме
RUN npm run build

# Nuxt слушал все адреса
ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=3000

EXPOSE 3000

# Запускаем прод-сервер
CMD ["node", ".output/server/index.mjs", "--hostname", "0.0.0.0", "--port", "3000"]